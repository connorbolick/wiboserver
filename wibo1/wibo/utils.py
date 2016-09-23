 
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.http import HttpRequest
from django.utils.importlib import import_module

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test

from cards.models import *
from invoice.models import *
 
from datetime import datetime
 
def cards_migration_extras_0009_1():
    quantcards = CardQuantity.objects.all()
    for q in quantcards:
        if q.material != None and q.product != None and q.job_card == None:
            q.qtype = CardQuantity.MATERIAL
        elif q.product != None and q.job_card != None and q.material == None:
            q.qtype = CardQuantity.PRODUCT

        print q
        q.save()

def cards_migration_extras_0009_2():
    prodcards = ProductCard.objects.all()
    for p in prodcards:
        p.name = p.product_name
        p.assigneduser = User.objects.get(pk=p.designer.pk)
        print p
        p.save()

def cards_migration_extras_0009_3():
    jobcards = JobCard.objects.all()
    for j in jobcards:
        j.name = j.job_name
        j.prod_notes = j.job_notes
        j.payment_type = str(j.payment_type).upper()
        if j.billed:
            j.status = Card.FINISHED

        print j
        j.save()

def set_invoice_date(products=True,jobs=True,invoices=True):
    if products:
        for p in ProductCard.objects.all():
            try:
                p.update()
                p.save()
            except Exception as e:
                print 'error',p,e
            print p

    if jobs:
        for j in JobCard.objects.filter(billed=False):
            j.update()
            j.save()
            print j
   
    if invoices:
        invoices = Invoice.objects.all()
        for i in invoices:
            i.payment_type = str(i.payment_type).upper()
            i.save()
            print i

            jobs = i.job_cards.all()

            for j in jobs:
                print j
                j.invoice_date = i.invoice_date
                j.save()

def update_employees():
    for e in Employee.objects.all():
        e.save()
        print e

def update_products():
    jobs = JobCard.objects.all()

    for j in jobs:
        if j.billed == True:
            quant = CardQuantity.objects.filter(job_card=j)
            for q in quant:
                if q.qtype == CardQuantity.PRODUCT:
                    q.product.status = Card.FINISHED
                    q.product.save()
                    print q.product
        if j.status == Card.CANCELLED:
            quant = CardQuantity.objects.filter(job_card=j)
            for q in quant:
                if q.qtype == CardQuantity.PRODUCT:
                    q.product.status = Card.CANCELLED
                    q.product.save()
                    print q.product
        if j.status == Card.HOLD:
            quant = CardQuantity.objects.filter(job_card=j)
            for q in quant:
                if q.qtype == CardQuantity.PRODUCT:
                    q.product.status = Card.HOLD
                    q.product.save()
                    print q.product

def waste_audit(start="2013-1-1", end=datetime.today()):
    ignore = ['Rush Fee','Additional Labor','Discount','Design','Design Not Printed']

    if start:
        start = datetime.strptime(start,"%Y-%m-%d").date()
    if type(end) != datetime:
        end = datetime.strptime(end,"%Y-%m-%d").date()
    query = JobCard.objects.filter(billed=True,invoice_date__gte=start, invoice_date__lte=end)


    no_notes = []

    for j in query:
        quant = CardQuantity.objects.filter(job_card = j)
        for q in quant:
            if q.waste_notes == None and q.qtype == 'product':
                p = q.product
                if p.name not in ignore:
                    pq = CardQuantity.objects.filter(product=p).exclude(qtype='product')
                    for i in pq:
                        if (i.waste_notes==None or i.waste_notes==""):
                            no_notes.append(j)
    no_notes = list(set(no_notes))
    no_notes.sort()

    for each in no_notes:
        print each.job_number, each, each.assigneduser


def jobs_with_design(start="2013-1-1", end=datetime.today()):
    if start:
        start = datetime.strptime(start,"%Y-%m-%d").date()
    if type(end) != datetime:
        end = datetime.strptime(end,"%Y-%m-%d").date()
    query = JobCard.objects.filter(billed=True,invoice_date__gte=start, invoice_date__lte=end)

    design_jobs = []
    for j in query:
        quant = CardQuantity.objects.filter(job_card= j,qtype='product')
        for q in quant:
            p = q.product
            pq = CardQuantity.objects.filter(product=p).filter(qtype='material')
            for i in pq:
                if "Design" in i.material.product_name:
                    design_jobs.append(j)
                if "Design" in i.material.description:
                    design_jobs.append(j)
    design_jobs = list(set(design_jobs))
    
    for each in design_jobs:
        print each.job_number, each


def thumb_audit(start="2013-1-1", end=datetime.today()):
    ignore = ['Rush Fee','Discount','Envelopes','Additional Labor','Design','Other Item']

    if start:
        start = datetime.strptime(start,"%Y-%m-%d").date()
    if type(end) != datetime:
        end = datetime.strptime(end,"%Y-%m-%d").date()
    query = JobCard.objects.filter(billed=True,invoice_date__gte=start, invoice_date__lte=end)

    no_thumb = []

    for j in query:
        quant = CardQuantity.objects.filter(job_card = j)
        for q in quant:
            if q.qtype != 'material' and q.item.name not in ignore:
                if q.item.thumbnail == "":
                    no_thumb.append(j)
    no_thumb = list(set(no_thumb))
    no_thumb.sort()

    for each in no_thumb:
        print each.job_number, each, each.assigneduser

def job_roi(start="2013-1-1", end=datetime.today()):
    if start:
        start = datetime.strptime(start,"%Y-%m-%d").date()
    if type(end) != datetime:
        end = datetime.strptime(end,"%Y-%m-%d").date()
    query = JobCard.objects.filter(billed=True,invoice_date__gte=start, invoice_date__lte=end)

    investments = dict()

    if query:
        total_jobs = float(len(query))

        for job in query:
            roi = 'None'
            if job.job_roi:
                roi = job.job_roi.name
            if roi in investments:
                investments[roi]['count'] += 1
                investments[roi]['rev']   += job.price
                investments[roi]['percent']= \
                        investments[roi]['count'] / total_jobs
            else:
                investments.update({
                    roi:{
                        'count'     :1,
                        'rev'       :job.price,
                        'percent'   :1/total_jobs,
                        },
                    })

    print investments

def payment_events_in_process(start="2013-1-1", end=datetime.today(),recieved=False):
    if start:
        start = datetime.strptime(start,"%Y-%m-%d").date()
    if type(end) != datetime:
        end = datetime.strptime(end,"%Y-%m-%d").date()
    query = PaymentEvent.objects.filter(payment_received=False, payment_date__gte=start,
        payment_date__lte=end)

    total = 0.0

    if query:
        for p in query:
            total += float(p.payment_amount)
            print 'payment:',p.pk,'inv:',p.invoice,'data',p.payment_date,"proc:", p.payment_processed,"rec:",p.payment_received,'amt:',p.payment_amount, "notes:",p.payment_notes 
    print total

def list_jobs_with(qtype=CardQuantity.MATERIAL,pk=1):
    '''lists all the jobs that have a material in one of their products'''

    if qtype == CardQuantity.MATERIAL:
        query = CardQuantity.objects.filter(qtype=CardQuantity.MATERIAL, material=pk)
    if qtype == CardQuantity.PRODUCT:
        query = CardQuantity.objects.filter(qtype=CardQuantity.PRODUCT, material=pk)
    if qtype == CardQuantity.SERVICE:
        query = CardQuantity.objects.filter(qtype=CardQuantity.SERVICE, material=pk)
    if qtype == CardQuantity.ADJUSTMENT:
        query = CardQuantity.objects.filter(qtype=CardQuantity.ADJUSTMENT, material=pk)

    jobs = []
    
    for q in query:
        if qtype == CardQuantity.PRODUCT:
            pq = q
        else:
            prod = q.product
            pq   = CardQuantity.objects.filter(qtype=CardQuantity.PRODUCT, product=prod)

        for p in pq:
            jobs.append(p.job_card)

    jobs = list(set(jobs))
    return jobs

def print_jobs_with(qtype=CardQuantity.MATERIAL,pk=1):
    jobs = list_jobs_with(qtype,pk)

    for j in jobs:
        print j.pk, j.name
