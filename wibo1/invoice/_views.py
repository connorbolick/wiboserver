from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from django.forms.models import inlineformset_factory, formset_factory, modelformset_factory
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from cards.models import JobCard, CardQuantity, Card
from invoice.models import *
from invoice.utils import check_payments

from invoice.forms import *
from django.db.models import Q
from django_select2 import Select2View, NO_ERR_RESP

@login_required(login_url='/account/login/')
def index(request):
    unpaid_list = Invoice.objects.filter(paid=False).order_by('invoice_date')
    paid_list   = Invoice.objects.filter(paid=True).order_by('invoice_date')

    view = ''
    unpaid_total=''
    unpaid_subtotal=''
    form_job = GetJobSearchForm()
    form_client = GetClientSearchForm()
    form_inv = GetInvSearchForm()

    if request.GET.get('view') and request.GET.get('view').lower() == 'paid':
        view = 'Paid'
        invoice_list = Invoice.objects.filter(paid=True).order_by('invoice_date')

    elif request.GET.get('view') and request.GET.get('view').lower() == 'unpaid':
        view = 'Unpaid'
        invoice_list = Invoice.objects.filter(paid=False).order_by('invoice_date')
        unpaid_total=0
        unpaid_subtotal=0
        for i in invoice_list:
            unpaid_subtotal += i.grand_total
            unpaid_total += i.balance
    else:
        view = ''
        invoice_list = Invoice.objects.order_by('invoice_date')

    if request.GET.get('pay'):
        invoice_list = invoice_list.filter(
                payment_type = request.GET.get('pay'))

    form_job = GetJobSearchForm(request.GET)
    if form_job.is_valid():
        if form_job.cleaned_data['jobs'] != []:
            invoice_list = invoice_list.filter(job_cards__in = form_job.cleaned_data['jobs'])

    form_client = GetClientSearchForm(request.GET)
    if form_client.is_valid():
        if form_client.cleaned_data['clients'] != []:
            invoice_list = invoice_list.filter(job_cards__billing_contact__in = form_client.cleaned_data['clients'])
     
    for_inv = GetInvSearchForm(request.GET)
    if form_inv.is_valid():
        if form_inv.cleaned_data['invoice'] != []:
            invoice_list = invoice_list.filter(job_cards__in = form_inv.cleaned_data['invoice'])

    paginator = Paginator(invoice_list,50)

    page = request.GET.get('page')
    try:
        invoice_list = paginator.page(page)
    except PageNotAnInteger:
        invoice_list = paginator.page(1)
    except EmptyPage:
        invoice_list = paginator.page(paginator.num_pages)

    print "page",invoice_list

    return render_to_response('invoice/index.html',{
        'form_job':form_job,
        'form_client':form_client,
        'invoice_list':invoice_list,
        'unpaid_total':unpaid_total,
        'unpaid_subtotal':unpaid_subtotal,
        'view':view,
        },RequestContext(request))

@login_required(login_url='/account/login/')
def detail(request, inv_number):
    """
    displays a printable invoice with options
    """
    inv = get_object_or_404(Invoice, pk=inv_number)
    jobs = InvQuantity.objects.filter(invoice=inv)

    return render_to_response('invoice/detail.html',{
        'inv':inv,
        'jobs':jobs,
        },RequestContext(request))

@login_required(login_url='/account/login/')
def print_invoice(request, inv_number):
    """
    displays a printable invoice
    """
    inv = get_object_or_404(Invoice, pk=inv_number)
    jobs = InvQuantity.objects.filter(invoice=inv)

    return render_to_response('invoice/print_invoice.html',{
        'inv':inv,
        'jobs':jobs,
        },RequestContext(request))

@login_required(login_url='/account/login/')
def new_payment(request, inv_number):
    """
    Creates the forms needed to add payment info
    to an invoice.
    """
    inv = get_object_or_404(Invoice, pk=inv_number)

    CashModelFormset = inlineformset_factory(Invoice, PaymentEventCash, \
            extra=1, form=PaymentForm)
    CheckModelFormset = inlineformset_factory(Invoice, PaymentEventCheck, \
            extra=1, form=PaymentForm)
    GiftCardModelFormset = inlineformset_factory(Invoice, PaymentEventGiftCard, \
            extra=1, form=PaymentForm)
    IdoModelFormset = inlineformset_factory(Invoice, PaymentEventIDO, \
            extra=1, form=PaymentForm)
    WebModelFormset = inlineformset_factory(Invoice, PaymentEventWebInvoice, \
            extra=1, form=PaymentForm)
    MarketplaceModelFormset = inlineformset_factory(Invoice, PaymentEventMarketplace,\
            extra=1, form=PaymentForm)

    payment_type = None

    if request.method == "POST":
        if request.GET.get('type'):
            pay_type = request.GET.get('type')
            
            if pay_type == 'cash':
                pay_formset = CashModelFormset(request.POST, request.FILES, instance=inv)
            if pay_type == 'check':
                pay_formset = CheckModelFormset(request.POST, request.FILES, instance=inv)
            if pay_type == 'gift':
                pay_formset = GiftCardModelFormset(request.POST, request.FILES, instance=inv)
            if pay_type == 'ido':
                pay_formset = IdoModelFormset(request.POST, request.FILES, instance=inv)
            if pay_type == 'web':
                pay_formset = WebModelFormset(request.POST, request.FILES, instance=inv)
            if pay_type == 'market':
                pay_formset = MarketplaceModelFormset(request.POST, request.FILES, instance=inv)
        else:
            if request.POST.get('payment_type') == PaymentEvent.CASH:
                return HttpResponseRedirect('?type=cash')
            if request.POST.get('payment_type') == PaymentEvent.CHECK:
                return HttpResponseRedirect('?type=check')
            if request.POST.get('payment_type') == PaymentEvent.GIFT_CARD:
                return HttpResponseRedirect('?type=gift')
            if request.POST.get('payment_type') == PaymentEvent.IDO:
                return HttpResponseRedirect('?type=ido')
            if request.POST.get('payment_type') == PaymentEvent.WEB_INV:
                return HttpResponseRedirect('?type=web')
            if request.POST.get('payment_type') == PaymentEvent.MARKETPLACE:
                return HttpResponseRedirect('?type=market')

        if pay_formset.is_valid():
            payment = pay_formset.save(commit=False)

            for each in payment:
                each.invoice = inv
                each.payment_user = request.user
                each.save()
            
            check_payments(inv)

            return HttpResponseRedirect(reverse('invoice.views.detail',args=(inv_number,) ))

    else:
        if request.GET.get('type'):
            pay_type = request.GET.get('type')
            
            if pay_type == 'cash':
                pay_formset = CashModelFormset()
            if pay_type == 'check':
                pay_formset = CheckModelFormset()
            if pay_type == 'gift':
                pay_formset = GiftCardModelFormset()
            if pay_type == 'ido':
                pay_formset = IdoModelFormset()
            if pay_type == 'web':
                pay_formset = WebModelFormset()
            if pay_type == 'market':
                pay_formset = MarketplaceModelFormset()

        else:
            pay_formset = None
            payment_type = PaymentTypeForm()

    return render_to_response("invoice/payment_form.html",{
            'pay_formset' :pay_formset,
            'payment_type':payment_type,
        }, RequestContext(request))

@login_required(login_url='/account/login/')
def new_invoice(request):
    """
    creates a new invoice from the information
    from the job index page (stored in session as
    'new_inv_jobs'
    """
    
    if request.method=="POST":
        return HttpResponse("POST")
    
    # if there's the session data we need
    elif 'new_inv_jobs' in request.session:
        job_list = request.session['new_inv_jobs']
        jobs = JobCard.objects.filter(pk__in=job_list)
        
        # stop if any materials don't have waste
        #for j in jobs:
        #    products = CardQuantity.objects.filter(job_card=j,\
        #            qtype=Card.PRODUCT)
        #
        #    for p in product:
        #        items = CardQuantity.objects.filter(product=p,\
        #                qtype=Card.MATERIAL)
        #
        #        for i in items:
        #            if i.waste_units == '':
                        


        # gets the payment_type and contact from
        # the first job in the list
        #   A possible upgrade would include
        #   searching the job list and setting
        #   this to the most common value
        #   Or asking the user directly
        job_payment_type = jobs[0].payment_type
        job_billing_contact = jobs[0].billing_contact
        
        # make the invoice object
        inv = Invoice.objects.create(
                payment_type = job_payment_type,
                billing_contact = job_billing_contact,
                created_user = request.user,
                updated_user = request.user
                )
        inv.save()

        if inv.payment_type == PaymentEvent.IDO:
            """
            if the payment type is IDO
            create a payment event from the jobcard info
            but only if it's been marked as delievered
            also add something in the way status updates 
            are processed so it check when you mark a 
            job card as delivered too
            """
            inv.taxable=False
            inv.save()

        # attach the JobCards
        for j in jobs:
            q = InvQuantity.objects.create(
                    invoice = inv,
                    job_card = j,
                    )
            """if q.percentage_invoiced > 1:
                inv.delete()
                raise ValueError("Job_Card already invoiced at 100%")"""
            per_inv = q.percentage_invoiced
            if per_inv < 1:
                q.units = 1 - per_inv
            print q.units,q.percentage_invoiced
            q.save()
            # set the billed option to True
            j.billed = True
            j.lock_price()
            j.invoice_date = datetime.datetime.now()
            j.save()
            if j.payment_type == PaymentEvent.IDO and \
                    j.approved_by and j.approved_on and j.dept_chartstring:
                paymentevent = PaymentEventIDO.objects.create(
                        invoice = inv,
                        payment_user = request.user,
                        payment_amount = j.price,
                        payment_notes = "auto generated from Job # %s" % j.pk,
                        dept_chartstring = j.dept_chartstring,
                        approved_by = j.approved_by,
                        approved_date = j.approved_on)
                paymentevent.save()
            if j.payment_type == PaymentEvent.MARKETPLACE and j.order_number:
                paymentevent = PaymentEventMarketplace.objects.create(
                        invoice = inv,
                        payment_user = request.user,
                        payment_amount = j.price + j.price * float(settings.TAX_RATE),
                        payment_notes = "auto generated from Job # %s" % j.pk,
                        order_number = j.order_number)
                paymentevent.save()
                
        
        # delete the session variable
        try:
            del request.session['new_inv_jobs']
        except KeyError:
            pass
        
        return HttpResponseRedirect(reverse('invoice.views.detail',args=(inv.pk,) ))

@login_required(login_url='/account/login/')
def edit_invoice(request, inv_number):
    """
    Lets users edit invoices
    """
    inv = get_object_or_404(Invoice, pk=inv_number)
    jobs = InvQuantity.objects.filter(invoice=inv)

    JobInlineFormset = inlineformset_factory(Invoice, InvQuantity, \
            extra=0, can_delete=False)

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=inv)
        job_formset = JobInlineFormset(request.POST, request.FILES, \
                instance=inv, queryset=jobs)

        if form.is_valid() and job_formset.is_valid():
            inv = form.save(commit=False)
            inv.updated_user = request.user
            if inv.payment_type == PaymentEvent.IDO:
                inv.taxable=False
            else:
                inv.taxable=True
            inv.save()
            job_formset.save()
            return HttpResponseRedirect(reverse('invoice.views.detail', \
                    args=(inv_number,) ))

    else:
        form = InvoiceForm(instance=inv)
        job_formset = JobInlineFormset(instance=inv, queryset=jobs)

    return render_to_response("invoice/invoice_form.html",{
        "form":form,
        "job_formset":job_formset,
        }, RequestContext(request))

@login_required(login_url='/account/login/')
def payment_index(request):
    """
    displays the recorded payments
    """
    payments = PaymentEvent.objects.filter().order_by("pk").reverse()

    if request.GET.get('processed'):
        status = request.GET.get('processed')
        if status == 'true':
            status = True
        elif status == 'false':
            status = False
        payments = payments.filter(payment_processed=status)

    if request.GET.get('received'):
        status = request.GET.get('received')
        if status == 'true':
            status = True
        elif status == 'false':
            status = False
        payments = payments.filter(payment_received=status)

    paginator = Paginator(payments, 40)

    page = request.GET.get('page')
    try:
        payments = paginator.page(page)
    except PageNotAnInteger:
        payments = paginator.page(1)
    except EmptyPage:
        payments = paginator.page(paginator.num_pages)

    if request.method == "POST":
        action_form = PaymentActionForm(request.POST)

        if action_form.is_valid() and 'payment_checkbox' in request.POST:
            action = action_form.cleaned_data['action']
            payments = []
            
            if 'payment_checkbox' in request.POST:
                payments = request.POST.getlist('payment_checkbox')

            if action == PaymentActionForm.PROCESS:
                for pk in payments:
                    payment = PaymentEvent.objects.get(pk=pk)
                    payment.payment_processed = True
                    payment.save()
            if action == PaymentActionForm.RECEIVE:
                for pk in payments:
                    payment = PaymentEvent.objects.get(pk=pk)
                    payment.payment_received = True
                    payment.save()
                    check_payments(payment.invoice)

            return HttpResponseRedirect(reverse('invoice.views.payment_index'))
    else:
        action_form = PaymentActionForm()

    return render_to_response('invoice/payment_index.html',{
        'action_form':action_form,
        'payments':payments,
        'page_range':paginator.page_range,
        },RequestContext(request))
