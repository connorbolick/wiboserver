from datetime import datetime
#from decimal import Decimal

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
#from django.forms.models import inlineformset_factory, formset_factory
from django.template import Context, loader, RequestContext
from django.core.urlresolvers import reverse
#from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test

from reports.models import *
from cards.models import CardQuantity, JobCard
from inventory.models import Material
from timetask.models import Timelog
from pprint import pprint
from decimal import Decimal

from reports.forms import *
from django.db.models import Q, Sum
from django_select2 import Select2View, NO_ERR_RESP

@login_required(login_url='/account/login/')
def spar_report(request):
    start_date = None
    end_date = None
    if request.GET.get('start'):
        start_date = request.GET.get('start')
        start_data = datetime.strptime(start_date,"%Y-%m-%d").date()
    if request.GET.get('end'):
        end_date = request.GET.get('end')
        end_date = datetime.strptime(end_date,"%Y-%m-%d").date()

    date_form = StartEndDateForm(initial={'start':start_date, 'end':end_date})

    query = None
    
    if start_date or end_date or request.GET.get('list') or request.GET.get('excel'):
        # build the query 
        query = JobCard.objects.filter(billed=True)
        if start_date:
            query = query.filter(invoice_date__gte=start_date)
        if end_date:
            query = query.filter(invoice_date__lte=end_date)

    # Each of these dictionaries holds the relevant info for that "group by" category
    by_department   = dict()    # keyed by company + department string
    by_category     = dict()    # keyed by product name
    with_p_design   = []        # number of jobs with printed designs
    with_nonp_design= []        # number of jobs with non printed designs
    total_prods= 0
    cumulative_prop = 0.0
    total_jobs = 0
    total_prod_jobs = 0         # she needs the total number within the categories
    total_co_jobs = 0           # again...she's saying it's not totaling right...

    # loop through query and populate the dicts
    if query:
        total_jobs = float(len(query))
        for job in query:
            # save the company and department for later
            company = job.contact.company
            department = job.contact.department
            products = job.products.all()

            # if the company is in by_department
            if company in by_department:
                # if the department in already there
                if department in by_department[company]:
                    total_co_jobs += 1
                    by_department[company][department]['count'] += 1
                    by_department[company][department]['percent'] = \
                        by_department[company][department]['count'] / total_jobs
                # if the department is not already there
                else:
                    by_department[company].update({
                        department : {
                            'count' : 1,
                            'percent' : (1 / total_jobs),
                            },
                        })
                    total_co_jobs += 1
            # if the company is not in by_department
            else:
                by_department.update({
                    company : {
                        department : {
                            'count': 1,
                            'percent' : (1 / total_jobs),
                            },
                        },
                    })
                total_co_jobs += 1

            # loop through all the products on this job 
            for p in products:
                total_prods += 1
                quantity = CardQuantity.objects.filter(job_card=job,product=p)
                quantity = quantity[0]
                # if that product name is already in the list...
                if p.name in by_category:
                    #by_category[p.name]['count'] += quantity.units
                    by_category[p.name]['count'] += 1
                    total_prod_jobs += 1
                # otherwise...
                else:
                    #by_category.update({p.name: {'count':quantity.units,}, })
                    by_category.update({p.name: {'count':1,}, })
                    total_prod_jobs += 1

                for m in p.materials.all():
                    if m.pk == settings.MATERIAL_DESIGN_PRINTED:
                        with_p_design.append(job)
                    elif m.pk == settings.MATERIAL_DESIGN_NPRINTED:
                        with_nonp_design.append(job)

        with_p_design = list(set(with_p_design))
        with_nonp_design = list(set(with_nonp_design))

        # Sales Track stuff
        for prod in by_category.keys():
            by_category[prod]['prop'] = \
                by_category[prod]['count']/float(total_prods)

        # sort by prop
        by_category = sorted(by_category.items(), key=lambda t: t[1]['prop'])
        by_category.reverse()

        # get cumulative
        for i in range(0,len(by_category)):
            cumulative_prop += by_category[i][1]['prop']
            by_category[i][1]['cumulative']= cumulative_prop


    # if the Excel button is pushed
    # this returns an html table with the .xls extention
    # Excel can open and read that
    if request.REQUEST.get('excel'):
        response = render_to_response("reports/spar_table.html", {
            'by_department':by_department,
            'total_jobs':total_jobs,
            'by_category':by_category,
            'total_prods':len(by_category),
            'cumulative_prop':cumulative_prop,
            'printed_design_total':len(with_p_design),
            'nonprinted_design_total':len(with_nonp_design),
            'total_prod_jobs':total_prod_jobs,
            'total_co_jobs':total_co_jobs,
            #'query':query, #used for debugging
            })
        response['Content-Disposition'] = 'attachment; filename="spar_report.xls"'
        response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
        return response
    
    #if request.REQUEST.get('list'):
    else:
        return render_to_response("reports/spar.html",{
                'date_form':date_form,
                'by_department':by_department,
                'total_jobs':total_jobs,
                'by_category':by_category,
                'total_prods':len(by_category),
                'cumulative_prop':cumulative_prop,
                'printed_design_total':len(with_p_design),
                'nonprinted_design_total':len(with_nonp_design),
                'total_prod_jobs':total_prod_jobs,
                'total_co_jobs':total_co_jobs,
                #'query':query, #used for debugging
            }, RequestContext(request))

@login_required(login_url='/account/login/')
def waste_report(request):
    """
    Creates a report of waste
    Really ineffienct
    """
    ########################
    start_date = None
    end_date = None
    if request.GET.get('start'):
        start_date = request.GET.get('start')
    if request.GET.get('end'):
        end_date = request.GET.get('end')

    date_form = StartEndDateForm(initial={'start':start_date, 'end':end_date})

    query = None
    
    if start_date or end_date or request.GET.get('list') or request.GET.get('excel'):
        # build the query 
        query = JobCard.objects.filter(billed=True)
        if start_date:
            query = query.filter(invoice_date__gte=start_date)
        if end_date:
            query = query.filter(invoice_date__lte=end_date)
    ###########################

    # This is what gets returned to the stuffs
    total_jobs = 0          # total number of jobs
    total_revenue = 0       # total revenue (job_card.price)
    total_cost = 0          # total cost (job_card.cost)
    total_waste_cost = 0    # waste from each CardQuantity
    total_profit = 0        # total revenue - total cost (not waste)
    adjusted_profit = 0     # total profit + total waste
    total_waste_wt = 0
    total_waste_t = 0
    total_cost_wt = 0
    total_cost_t = 0

    profit_percentage = 0       # total profit / total revenue
    waste_percentage = 0        # total waste / total profit
    adj_profit_percentage = 0   # adjusted_profit / total_revenue
    waste_to_cost_percentage = 0# totat_waste / total_cost

    jobs_with_waste = []

    waste_by_user = dict() # waste organized by user
    waste_by_mat = dict() #
    profit_margin = dict()
    jobs_extrainfo = dict()

    # loop through query and populate the dicts
    if query:
        #### LOGIC GOES HERE ####
        total_jobs = len(query)
        for job in query:
            total_revenue += job.price
            waste_found = False
            # add the waste
            #print job.waste_cost, job.cost, job.price
            wt_cost_sum = Timelog.objects.filter(job=job,time_out__isnull=False).aggregate(Sum('calculated'))
            wt_waste_sum = Timelog.objects.filter(job=job,time_out__isnull=False,type='rework time').aggregate(Sum('calculated'))
            if job.waste_cost != 0.0 or Timelog.objects.filter(job=job,time_out__isnull=False,type='rework time'):
                waste_found = True

            total_waste_cost += job.waste_cost
            total_cost += job.cost + job.waste_cost

            if wt_cost_sum['calculated__sum'] != None and wt_waste_sum['calculated__sum'] != None:
                total_waste_wt += wt_waste_sum['calculated__sum'] * Timelog.MULTRATE + job.waste_cost
                total_cost_wt += wt_cost_sum['calculated__sum'] * Timelog.MULTRATE + job.cost + job.waste_cost

                total_waste_t += wt_waste_sum['calculated__sum'] * Timelog.MULTRATE
                total_cost_t += wt_cost_sum['calculated__sum'] * Timelog.MULTRATE
            else:
                total_waste_wt += job.waste_cost
                total_cost_wt += job.cost + job.waste_cost

            user = job.assigneduser
            if user in waste_by_user:
                waste_by_user[user]['total_jobs'] += 1
            else:
                waste_by_user.update({
                    user: {
                        'count':0,
                        'jobs': {},
                        'cost':0,
                        'total_jobs' : 1,
                        'total_cost' : 0,
                        'ratio' : 0,
                        'tratio' : 0,
                        'wratio' : 0,
                        'total_time' : Decimal(0),
                        'total_rework' : Decimal(0),
                        'total_costwt' : Decimal(0),
                        'total_wastewt' : Decimal(0),
                        'total_costt' : Decimal(0),
                        'total_wastet' : Decimal(0),
                        }
                    })

            if waste_found:
                jobs_with_waste.append(job)
                total_time = Timelog.objects.filter(job=job,time_out__isnull=False).aggregate(Sum('calculated'))
                total_rework = Timelog.objects.filter(job=job,time_out__isnull=False,type='rework time').aggregate(Sum('calculated'))

                if total_time['calculated__sum'] != None and total_rework['calculated__sum'] != None:
                    jobs_extrainfo.update({
                        job.job_number : {
                            'total':total_time['calculated__sum'] * Timelog.MULTRATE + job.cost,
                            'waste':total_rework['calculated__sum'] * Timelog.MULTRATE + job.waste_cost,
                            'time_total':total_time['calculated__sum'] * Timelog.MULTRATE,
                            'time_waste':total_rework['calculated__sum'] * Timelog.MULTRATE,
                            'total_time':total_time['calculated__sum'],
                            'total_rework':total_rework['calculated__sum'],
                        },
                    })
                else:
                    jobs_extrainfo.update({
                        job.job_number : {
                            'total': job.cost,
                            'waste': job.waste_cost,
                            'time_total':Decimal(0),
                            'time_waste':Decimal(0),
                            'total_time':Decimal(0),
                            'total_rework':Decimal(0),
                        },
                    })

                # add the job to the waste_by_user dict
                total_time = Timelog.objects.filter(employee=user,job=job,time_out__isnull=False).aggregate(Sum('calculated'))
                total_rework = Timelog.objects.filter(employee=user,job=job,time_out__isnull=False,type='rework time').aggregate(Sum('calculated'))
                if job in waste_by_user[user]['jobs']:
                    # need to include time waste cost based on time logger
                    if total_time['calculated__sum'] != None and total_rework['calculated__sum'] != None:
                        waste_by_user[user]['jobs'][job]['total_costwt'] += total_time['calculated__sum'] * Timelog.MULTRATE + job.cost
                        waste_by_user[user]['jobs'][job]['total_wastewt'] += total_rework['calculated__sum'] * Timelog.MULTRATE + job.waste_cost
                        waste_by_user[user]['jobs'][job]['total_costt'] += total_time['calculated__sum'] * Timelog.MULTRATE
                        waste_by_user[user]['jobs'][job]['total_wastet'] += total_rework['calculated__sum'] * Timelog.MULTRATE
                        waste_by_user[user]['jobs'][job]['total_time'] += total_time['calculated__sum']
                        waste_by_user[user]['jobs'][job]['total_rework'] += total_rework['calculated__sum']
                else:
                    if total_time['calculated__sum'] != None and total_rework['calculated__sum'] != None:
                        waste_by_user[user]['jobs'].update({
                            job : {
                                'total_costwt' : total_time['calculated__sum'] * Timelog.MULTRATE + job.cost,
                                'total_wastewt' : total_rework['calculated__sum'] * Timelog.MULTRATE + job.waste_cost,
                                'total_costt' : total_time['calculated__sum'] * Timelog.MULTRATE,
                                'total_wastet' : total_rework['calculated__sum'] * Timelog.MULTRATE,
                                'total_time' : total_time['calculated__sum'],
                                'total_rework' : total_rework['calculated__sum'],
                            }
                        })

                        waste_by_user[user]['total_costwt'] += total_time['calculated__sum'] * Timelog.MULTRATE + job.cost
                        waste_by_user[user]['total_wastewt'] += total_rework['calculated__sum'] * Timelog.MULTRATE + job.waste_cost
                        waste_by_user[user]['total_costt'] += total_time['calculated__sum'] * Timelog.MULTRATE
                        waste_by_user[user]['total_wastet'] += total_rework['calculated__sum'] * Timelog.MULTRATE
                        waste_by_user[user]['total_time'] += total_time['calculated__sum']
                        waste_by_user[user]['total_rework'] += total_rework['calculated__sum']

                    else:
                        waste_by_user[user]['jobs'].update({
                            job : {
                                'total_costwt' : job.cost,
                                'total_wastewt' :  job.waste_cost,
                                'total_costt' : Decimal(0),
                                'total_wastet' : Decimal(0),
                                'total_time' : Decimal(0),
                                'total_rework' : Decimal(0),
                            }
                        })

                        waste_by_user[user]['total_costwt'] += job.cost
                        waste_by_user[user]['total_wastewt'] += job.waste_cost


                    waste_by_user[user]['count'] += 1
                    waste_by_user[user]['cost'] += job.waste_cost
                    waste_by_user[user]['total_cost'] += job.cost


                # waste by material
                for p in job.products.all():
                    for mq in CardQuantity.objects.filter(
                            product__pk=p.pk,qtype=CardQuantity.MATERIAL,
                            waste_units__gt=0):
                        if mq.material in waste_by_mat:
                            waste_by_mat[mq.material]['cost'] += mq.waste_cost
                            waste_by_mat[mq.material]['units'] += mq.waste_units
                            if job not in waste_by_mat[mq.material]['jobs']:
                                waste_by_mat[mq.material]['jobs'].append(job)
                        else:
                            waste_by_mat.update({
                                mq.material : {
                                    'cost' : mq.waste_cost,
                                    'units' : mq.waste_units * mq.sqft,
                                    'jobs' : [job],
                                    'unitage' : mq.material.unit,
                                },
                                })

                        for mat in Material.objects.filter(cardquantity__material_id=mq.material_id):
                            if job.job_number in profit_margin:
                                if job.price_level == 'INT':
                                    profit_margin[job.job_number] += (mat.unit_price_int - mat.unit_cost) * mq.units
                                else:
                                    profit_margin[job.job_number] += (mat.unit_price_ext - mat.unit_cost) * mq.units
                            else:
                                if job.price_level == 'INT':
                                    profit_margin.update({job.job_number: (mat.unit_price_int - mat.unit_cost) * mq.units})
                                else:
                                    profit_margin.update({job.job_number: (mat.unit_price_ext - mat.unit_cost) * mq.units})

    # calculate totals
    total_profit = total_revenue - total_cost
    adjusted_profit = total_profit + total_waste_cost
    if total_revenue != 0:
        profit_percentage = total_profit / total_revenue
        waste_percentage = total_waste_cost / adjusted_profit
        adj_profit_percentage = adjusted_profit / total_revenue
        waste_to_cost_percentage = total_waste_cost / total_cost

    #pprint(waste_by_user)
    #pprint(jobs_extrainfo)
    for emp in waste_by_user:
        if waste_by_user[emp]['total_cost'] != 0:
            waste_by_user[emp]['ratio'] = waste_by_user[emp]['cost']/waste_by_user[emp]['total_cost']
        else:
            waste_by_user[emp]['ratio'] = 0

        if waste_by_user[emp]['total_costt'] != 0:
            waste_by_user[emp]['wratio'] = waste_by_user[emp]['total_wastet']/waste_by_user[emp]['total_costt']
        else:
            waste_by_user[emp]['wratio'] = 0

        if waste_by_user[emp]['total_costwt'] != 0:
            waste_by_user[emp]['tratio'] = waste_by_user[emp]['total_wastewt']/waste_by_user[emp]['total_costwt']
        else:
            waste_by_user[emp]['tratio'] = 0


    # compile it into an easy to use dict
    values = {
        'total_jobs':total_jobs,
        'total_with_waste':len(jobs_with_waste),
        'total_revenue':total_revenue,
        'total_cost':total_cost,
        'total_waste_cost':total_waste_cost,
        'total_cost_t':total_cost_t,
        'total_waste_t':total_waste_wt,
        'total_cost_wt':total_cost_t,
        'total_waste_wt':total_waste_wt,
        'total_profit':total_profit,
        'adjusted_profit':adjusted_profit,
        'profit_percentage':profit_percentage,
        'waste_percentage':waste_percentage,
        'adj_profit_percentage':adj_profit_percentage,
        'waste_to_cost_percentage':waste_to_cost_percentage,
        }

    ###########################
    # if the Excel button is pushed
    # this returns an html table with the .xls extention
    # Excel can open and read that
    if request.REQUEST.get('excel'):
        response = render_to_response("reports/waste_table.html", {
            'jobs':jobs_with_waste,
            #'jobs':query, #used for debugging
            'values':values,
            'by_user':waste_by_user,
            'by_mat':waste_by_mat,
            'p_margin':profit_margin,
            'jobs_extrainfo':jobs_extrainfo,
            })
        response['Content-Disposition'] = 'attachment; filename="waste_report.xls"'
        response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
        return response
    
    #if request.REQUEST.get('list'):
    else:
        return render_to_response("reports/waste.html",{
                'date_form':date_form,
                'jobs':jobs_with_waste,
                #'jobs':query, #used for debugging
                'values':values,
                'by_user':waste_by_user,
                'by_mat':waste_by_mat,
                #'query':query, #used for debugging
                'p_margin':profit_margin,
                'jobs_extrainfo':jobs_extrainfo,
            }, RequestContext(request))

@login_required(login_url='/account/login/')
def material_report(request):
    """
    Creates a report of waste
    Really ineffienct
    """
    ########################
    start_date = None
    end_date = None
    if request.GET.get('start'):
        start_date = request.GET.get('start')
    if request.GET.get('end'):
        end_date = request.GET.get('end')

    date_form = StartEndDateForm(initial={'start':start_date, 'end':end_date})

    query = None
    
    if start_date or end_date or request.GET.get('list') or request.GET.get('excel'):
        # build the query 
        query = JobCard.objects.filter(billed=True)
        if start_date:
            query = query.filter(invoice_date__gte=start_date)
        if end_date:
            query = query.filter(invoice_date__lte=end_date)
    ###########################

    # This is what gets returned to the stuffs
    total_jobs = 0
    total = 0

    by_category = dict()

    # loop through query and populate the dicts
    if query:
        #### LOGIC GOES HERE ####
        total_jobs = len(query)
        for job in query:
            prods  = CardQuantity.objects.filter(job_card=job,
                    qtype=CardQuantity.PRODUCT)
            for p in prods:
                #print "pro",p.product, p.units
                mats = CardQuantity.objects.filter(product=p.product,\
                        qtype=CardQuantity.MATERIAL)
                for m in mats:
                    #print "   mat",m.material, m.units, m.sqft
                    total += 1
                    material = m.material
                    cat = material.category
                    mat = material.product_name

                    unitage = m.sqft * m.units * p.units
                    cost = m.cost * unitage
                    waste = m.waste_cost * unitage
                    # price/cost stuff
                    if job.price_level == Contact.INTERNAL:
                        gross = material.unit_price_int * unitage
                    elif job.price_level == Contact.EXTERNAL:
                        gross = material.unit_price_ext * unitage
                    else:
                        raise NotImplementedError, 'price level not defined'
                    net = gross - cost - waste


                    if cat in by_category:
                        if mat in by_category[cat]:
                            by_category[cat][mat]['count']   += 1
                            by_category[cat][mat]['percent']  = \
                                by_category[cat][mat]['count'] / total
                            by_category[cat][mat]['unitage'] += unitage
                            by_category[cat][mat]['cost']    += cost
                            by_category[cat][mat]['waste']   += waste
                            by_category[cat][mat]['gross']   += gross
                            by_category[cat][mat]['net']     += net
                        else:
                            by_category[cat].update({
                                mat : {
                                    'count'   : 1,
                                    'percent' : (1/total),
                                    'unitage' : unitage,
                                    'unit'    : material.unit,
                                    'cost'    : cost,
                                    'waste'   : waste,
                                    'gross'   : gross,
                                    'net'     : net,
                                    },
                                })

                    else:
                        by_category.update({
                            cat : {
                                mat : {
                                    'count'   : 1,
                                    'percent' : (1/total),
                                    'unitage' : unitage,
                                    'unit'    : material.unit,
                                    'cost'    : cost,
                                    'waste'   : waste,
                                    'gross'   : gross,
                                    'net'     : net,
                                    },
                                },
                            })

    # calculate totals

    # compile it into an easy to use dict

    ###########################
    # if the Excel button is pushed
    # this returns an html table with the .xls extention
    # Excel can open and read that
    if request.REQUEST.get('excel'):
        response = render_to_response("reports/material_table.html", {
            'by_category':by_category,
            })
        response['Content-Disposition'] = 'attachment; filename="material_report.xls"'
        response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
        return response
    
    #if request.REQUEST.get('list'):
    else:
        return render_to_response("reports/material.html",{
                'date_form':date_form,
                'by_category':by_category,
                #'query':query, #used for debugging
            }, RequestContext(request))



@login_required(login_url='/account/login/')
def inventory_report(request):
    """
    Creates a report of inventory
    """
    ########################

    inventory = Material.objects.all()
    
    ###########################

    # This is what gets returned to the stuffs
    total_inventory = inventory.count()

    # calculate totals

    # compile it into an easy to use dict

    ###########################
    # if the Excel button is pushed
    # this returns an html table with the .xls extention
    # Excel can open and read that
    if request.REQUEST.get('excel'):
        response = render_to_response("reports/inventory_table.html", {
            'inventory':inventory,
            })
        response['Content-Disposition'] = 'attachment; filename="material_report.xls"'
        response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
        return response
    
    #if request.REQUEST.get('list'):
    else:
        return render_to_response("reports/inventory.html",{
                'inventory':inventory,
                #'query':query, #used for debugging
            }, RequestContext(request))

@login_required(login_url='/account/login/')
def audit_report(request):
    """
    Creates a report of waste
    Really ineffienct
    """
    ########################
    start_date = None
    end_date = None
    if request.GET.get('start'):
        start_date = request.GET.get('start')
    if request.GET.get('end'):
        end_date = request.GET.get('end')

    date_form = StartEndDateForm(initial={'start':start_date, 'end':end_date})

    query = None
    
    if start_date or end_date or request.GET.get('list') or request.GET.get('excel'):
        # build the query 
        query = JobCard.objects.filter(billed=True)
        if start_date:
            query = query.filter(invoice_date__gte=start_date)
        if end_date:
            query = query.filter(invoice_date__lte=end_date)
    ###########################

    # This is what gets returned to the stuffs
    total_jobs = 0          # total number of jobs in query
    waste_total = 0          # total number of jobs that need waste notes
    thumb_total = 0       # total number of jobs that need thumbnails added

    waste_by_user = dict()  # keyed by user
    thumb_by_user = dict()  # keyed by user

    waste_product_name_ignore = ['Rush Fee','Additional Labor','Discount',
                                 'Design','Design Not Printed']
    thumb_product_name_ignore = ['Rush Fee','Discount','Envelopes',
                                 'Additional Labor','Design','Other Item']


    # loop through query and populate the dicts
    if query:
        #### LOGIC GOES HERE ####
        total_jobs = len(query)
        for job in query:
            quant = CardQuantity.objects.filter(job_card=job)
            for q in quant:
                if q.qtype == 'material' and q.item.name and q.item.name not in thumb_product_name_ignore:
                    if q.item.thumbnail == "":
                        if job.assigneduser in thumb_by_user:
                            if job not in thumb_by_user[job.assigneduser]['jobs']:
                                thumb_total += 1
                                thumb_by_user[job.assigneduser]['jobs'].append(job)
                                thumb_by_user[job.assigneduser]['count'] += 1
                                #thumb_by_user[job.assigneduser]['percent'] = \
                                #        thumb_by_user[job.assigneduser]['count'] / total_jobs

                        else:
                            thumb_by_user.update({
                                job.assigneduser : {
                                    'count' : 1,
                                    #'percent' : (1 / total_jobs),
                                    'jobs' : [job],
                                    }
                                })
                if q.qtype == 'product' and q.product.name and q.item.name not in waste_product_name_ignore:
                    p = q.product
                    pq = CardQuantity.objects.filter(product=p).exclude(qtype='product')
                    for i in pq:
                        if (i.waste_notes==None or i.waste_notes==""):
                            if job.assigneduser in waste_by_user:
                                if job not in waste_by_user[job.assigneduser]['jobs']:
                                    waste_by_user[job.assigneduser]['jobs'].append(job)
                                    waste_by_user[job.assigneduser]['count']+= 1
                                    #waste_by_user[job.assigneduser]['percent']=\
                                    #        waste_by_user[job.assigneduser]['count'] \ total_jobs
                            else:
                                waste_by_user.update({
                                    job.assigneduser : {
                                        'count':1,
                                        #'percent' : (1/total_jobs),
                                        'jobs':[job],
                                        }
                                    })

    ###########################
    # if the Excel button is pushed
    # this returns an html table with the .xls extention
    # Excel can open and read that
    if request.REQUEST.get('excel'):
        response = render_to_response("reports/audit_table.html", {
            'thumb_by_user':thumb_by_user,
            'waste_by_user':waste_by_user,
            #'jobs':query, #used for debugging
            })
        response['Content-Disposition'] = 'attachment; filename="waste_report.xls"'
        response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
        return response
    
    #if request.REQUEST.get('list'):
    else:
        return render_to_response("reports/audit.html",{
                'date_form':date_form,
                'thumb_by_user':thumb_by_user,
                'waste_by_user':waste_by_user,
                #'query':query, #used for debugging
            }, RequestContext(request))



@login_required(login_url='/account/login/')
def revenue_report(request):
    """
    GBG - Daniel wanted a report similar to SPAR but about the ROIs
    5/28/2014
    """
    ########################
    start_date = None
    end_date = None
    if request.GET.get('start'):
        start_date = request.GET.get('start')
        start_data = datetime.strptime(start_date,"%Y-%m-%d").date()
    if request.GET.get('end'):
        end_date = request.GET.get('end')
        end_date = datetime.strptime(end_date,"%Y-%m-%d").date()

    date_form = StartEndDateForm(initial={'start':start_date, 'end':end_date})

    query = None

    if start_date or end_date or request.GET.get('list') or request.GET.get('excel'):
        # build the query
        # only get jobs that have an roi listed...
        query = JobCard.objects.filter(billed=True,job_roi_id__isnull=False).order_by('job_roi', 'contact__company', 'contact__department')
        if start_date:
            query = query.filter(invoice_date__gte=start_date).order_by('job_roi', 'contact__company', 'contact__department')
        if end_date:
            query = query.filter(invoice_date__lte=end_date).order_by('job_roi', 'contact__company', 'contact__department')

    # Each of these dictionaries holds the relevant info for that "group by" category
    by_roi   = dict()    # keyed by job's roi
    total_rev = dict()

    # loop through query and populate the dicts
    if query:
        total_jobs = float(len(query))
        for job in query:
            # save the roi name
            roi = job.job_roi.name
            company = job.contact.company
            department = job.contact.department

            # if the roi is in by_roi
            if roi in by_roi:
                # if the company exists in the by_roi[roi] already
                if company in by_roi[roi]:
                    # department exists already
                    if department in by_roi[roi][company]['depts']:
                        by_roi[roi][company]['depts'][department]['revenue'] += job.price
                        by_roi[roi][company]['depts'][department]['job_cnt'] += 1
                        by_roi[roi][company]['depts'][department]['jobs'].append(job)
                        by_roi[roi][company]['c_rev'] += job.price
                        by_roi[roi][company]['c_job_cnt'] += 1

                        total_rev[roi] += job.price

                    else:
                        by_roi[roi][company]['depts'].update({
                            department : {
                                'revenue' : job.price,
                                'job_cnt' : 1,
                                'jobs': [job],
                                },
                        })

                        by_roi[roi][company]['c_rev'] += job.price
                        by_roi[roi][company]['c_job_cnt'] += 1

                        total_rev[roi] += job.price
                else:
                    by_roi[roi].update({
                        company : {
                            'depts' : {
                                department : {
                                    'revenue' : job.price,
                                    'job_cnt' : 1,
                                    'jobs': [job],
                                    },
                                },
                            'c_rev' : job.price,
                            'c_job_cnt' : 1,
                            },
                        })

                    total_rev[roi] += job.price
            else:
                by_roi.update({
                    roi : {
                        company : {
                            'depts' : {
                                department : {
                                    'revenue' : job.price,
                                    'job_cnt' : 1,
                                    'jobs': [job],
                                    },
                                },
                            'c_rev' : job.price,
                            'c_job_cnt' : 1,
                            },
                        },
                    })

                total_rev.update({
                    roi : job .price,
                })

    # if the Excel button is pushed
    # this returns an html table with the .xls extention
    # Excel can open and read that
    if request.REQUEST.get('excel'):
        response = render_to_response("reports/revenue_table.html", {
            'by_roi':by_roi,
            'total_rev':total_rev,
            #'query':query, #used for debugging
            })
        response['Content-Disposition'] = 'attachment; filename="revenue_report.xls"'
        response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
        return response

    #if request.REQUEST.get('list'):
    else:
        return render_to_response("reports/revenue.html",{
                'date_form':date_form,
                'by_roi':by_roi,
                'total_rev':total_rev,
                #'query':query,
            }, RequestContext(request))



@login_required(login_url='/account/login/')
def client_report(request):
    """
    GBG - Daniel wanted a report that allowed seeing revenue based on a client search
    """
    ########################
    start_date = None
    end_date = None

    if request.GET.get('start'):
        start_date = request.GET.get('start')
        start_data = datetime.strptime(start_date,"%Y-%m-%d").date()
    if request.GET.get('end'):
        end_date = request.GET.get('end')
        end_date = datetime.strptime(end_date,"%Y-%m-%d").date()

    query = JobCard.objects.none()
    form = GetContactSearchForm()
    date_form = StartEndDateForm(initial={'start':start_date, 'end':end_date})

    if start_date or end_date or request.GET.get('list') or request.GET.get('excel'):
        # build the query
        # only get jobs that have an roi listed...
        query = JobCard.objects.filter(billed=True)

        if start_date:
            query = query.filter(invoice_date__gte=start_date)
        if end_date:
            query = query.filter(invoice_date__lte=end_date)

        form = GetContactSearchForm(request.GET)

        if form.is_valid() :
            if form.cleaned_data['clients'] != []:
                query = query.filter(contact__in = form.cleaned_data['clients'])

    # Each of these dictionaries holds the relevant info for that "group by" category
    by_co  = dict()    # keyed by job's roi
    total_rev = dict()

    # loop through query and populate the dicts
    if query:
        total_jobs = float(len(query))
        for job in query:
            # save the roi name
            company = job.contact.company
            client = job.contact_id
            dept = job.contact.department

            # if the roi is in by_roi
            if company in by_co:
                # if the company exists in the by_roi[roi] already
                if client in by_co[company]:
                    by_co[company][client]['revenue'] += job.price
                    by_co[company][client]['job_cnt'] += 1
                    by_co[company][client]['jobs'].append(job)

                    total_rev[company] += job.price
                else:
                    by_co[company].update({
                        client : {
                            'name' : job.contact.first_name + ' ' + job.contact.last_name,
                            'dept' : dept,
                            'revenue' : job.price,
                            'job_cnt' : 1,
                            'jobs': [job],
                        },
                    })

                    total_rev[company] += job.price
            else:
                by_co.update({
                    company : {
                        client : {
                            'name' : job.contact.first_name + ' ' + job.contact.last_name,
                            'dept': dept,
                            'revenue' : job.price,
                            'job_cnt' : 1,
                            'jobs': [job],
                        },
                    },
                })

                total_rev.update({
                    company : job.price,
                })

    # if the Excel button is pushed
    # this returns an html table with the .xls extention
    # Excel can open and read that
    if request.REQUEST.get('excel'):
        response = render_to_response("reports/client_table.html", {
            'by_co':by_co,
            'total_rev':total_rev,
            #'query':query, #used for debugging
            })
        response['Content-Disposition'] = 'attachment; filename="revenue_report.xls"'
        response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
        return response

    #if request.REQUEST.get('list'):
    else:
        return render_to_response("reports/client.html",{
                'form':form,
                'date_form':date_form,
                'by_co':by_co,
                'total_rev':total_rev,
            }, RequestContext(request))

@login_required(login_url='/account/login/')
@user_passes_test(lambda u: u.groups.filter(name='admin').count(), login_url='/')
def time_report(request):
    """
    GBG - David wanted a report to see everyone's time...stuff.
    """
    ########################
    start_date = None
    end_date = None

    if request.GET.get('start'):
        start_date = request.GET.get('start')
        start_data = datetime.strptime(start_date,"%Y-%m-%d").date()
    if request.GET.get('end'):
        end_date = request.GET.get('end')
        end_date = datetime.strptime(end_date,"%Y-%m-%d").date()

    query = Timelog.objects.none()
    form = GetEmployeeSearchForm()
    date_form = StartEndDateForm(initial={'start':start_date, 'end':end_date})

    if start_date or end_date or request.GET.get('list') or request.GET.get('excel'):
        # build the query
        # only get jobs that have an roi listed...
        query = Timelog.objects.filter(calculated__isnull=False)

        if start_date:
            query = query.filter(time_in__gte=start_date)
        if end_date:
            query = query.filter(time_in__lte=end_date)

        form = GetEmployeeSearchForm(request.GET)

        if form.is_valid() :
            if form.cleaned_data['employees'] != []:
                query = query.filter(employee__in = form.cleaned_data['employees'])

    # Each of these dictionaries holds the relevant info for that "group by" category
    by_emp  = dict()    # keyed by employee
    totals = {'rework' : Decimal(0.0), 'prod' : Decimal(0.0), 'all' : Decimal(0.0)}

    # loop through query and populate the dicts
    if query:
        for log in query:
            emp = log.employee
            type = log.type
            job_num = log.job.job_number

            if emp in by_emp:
                if job_num in by_emp[emp]['jobs']:
                    if type in by_emp[emp]['jobs'][job_num]['types']:
                        by_emp[emp]['jobs'][job_num]['types'][type]['logs'].append(log)
                        by_emp[emp]['jobs'][job_num]['types'][type]['total'] += log.calculated
                        by_emp[emp]['jobs'][job_num]['total'] += log.calculated
                        by_emp[emp]['totals']['all'] += log.calculated
                        by_emp[emp]['totals'][type] += log.calculated

                    else:
                        by_emp[emp]['jobs'][job_num]['types'].update({
                            type: {
                            'logs' : [log],
                            'total' : log.calculated,
                            },
                        })
                        by_emp[emp]['jobs'][job_num]['total'] += log.calculated
                        by_emp[emp]['totals']['all'] += log.calculated
                        by_emp[emp]['totals'][type] += log.calculated

                else:
                    by_emp[emp]['jobs'].update({
                        job_num :  {
                            'types' : {
                                type : {
                                    'logs' : [log],
                                    'total' : log.calculated,
                                },
                            },
                            'name' : log.job,
                            'total' : log.calculated,
                        },
                    })
                    by_emp[emp]['j_count'] += 1
                    by_emp[emp]['totals']['all'] += log.calculated
                    by_emp[emp]['totals'][type] += log.calculated
            else:
                if type == 'rework time':
                    insert = {'all' : log.calculated, type : log.calculated, 'production time' : Decimal(0.0) }
                else:
                    insert = {'all' : log.calculated, 'rework time' : Decimal(0.0), 'production time' : log.calculated }

                by_emp.update({
                    emp : {
                        'jobs' : {
                            job_num : {
                                'types' : {
                                    type : {
                                        'logs' : [log],
                                        'total' : log.calculated,
                                    },
                                },
                                'name' : log.job,
                                'total' : log.calculated,
                            },
                        },
                        'totals' : insert,
                        'j_count' : 1,
                    },
                })

    for e in by_emp:
        for j in by_emp[e]['jobs']:
            for t in by_emp[e]['jobs'][j]['types']:
                if t == 'rework time':
                    totals['rework'] += by_emp[e]['jobs'][j]['types'][t]['total']
                    by_emp[e]['jobs'][j]['pr'] = by_emp[e]['jobs'][j]['types'][t]['total'] / by_emp[e]['jobs'][j]['total']
                else:
                    totals['prod'] += by_emp[e]['jobs'][j]['types'][t]['total']
                    by_emp[e]['jobs'][j]['pp'] = by_emp[e]['jobs'][j]['types'][t]['total'] / by_emp[e]['jobs'][j]['total']
        totals['all'] += by_emp[e]['totals']['all']
        by_emp[e]['pr'] = by_emp[e]['totals']['rework time'] / by_emp[e]['totals']['all']
        by_emp[e]['pp'] = by_emp[e]['totals']['production time'] / by_emp[e]['totals']['all']

    # if the Excel button is pushed
    # this returns an html table with the .xls extention
    # Excel can open and read that
    if request.REQUEST.get('excel'):
        response = render_to_response("reports/timelog_table.html", {
            'by_emp':by_emp,
            'totals':totals,
            #'query':query, #used for debugging
            })
        response['Content-Disposition'] = 'attachment; filename="revenue_report.xls"'
        response['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
        return response

    #if request.REQUEST.get('list'):
    else:
        return render_to_response("reports/timelog.html",{
                'form':form,
                'date_form':date_form,
                'by_emp':by_emp,
                'totals':totals,
            }, RequestContext(request))
