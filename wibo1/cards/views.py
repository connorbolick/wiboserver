from datetime import datetime
from decimal import Decimal

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.forms.models import inlineformset_factory, formset_factory
from django.template import Context, loader, RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from cards.models import *
from invoice.models import *
from employee.models import Employee

@login_required(login_url="/account/login/")
def item_index(request):
    '''displays all the items'''
    exclude_list = ['finished','cancelled',]

    product_cards = ProductCard.objects.exclude(status__in = exclude_list)
    service_cards = ServiceCard.objects.exclude(status__in = exclude_list)
    adjustment_cards = AdjustmentCard.objects.exlude(status__in = exclude_list)

    return render_to_response('cards/items_index.html',{
        'product_cards':product_cards,
        'service_cards':service_cards,
        'adjustment_cards':adjustment_cards,
        },RequestContext(request))

@login_required(login_url='/account/login/')
def product_index(request):
    """
    Fetches the ProductCards with statuses that are
    in production, designing, or quoted
    """
    production_list = ProductCard.objects.filter(production_status__in= \
            [ProductCard.PRINT, ProductCard.OUT_SOURCED,]).order_by('due_date','status')
    design_list = ProductCard.objects.filter(production_status__in= \
            [ProductCard.DESIGN,]).order_by('due_date','status')
    quote_list = ProductCard.objects.filter(production_status__in = \
            [ProductCard.QUOTED,]).order_by('due_date','status')
    return render_to_response('cards/product_index.html',{
        "production_list": production_list,
        "design_list": design_list,
        "quote_list": quote_list,
        },RequestContext(request))

@login_required(login_url='/account/login/')
def new_product(request):
    """
    Creates a form for a new ProductCard.
    Saves it if everything validates
    """

    MaterialInlineFormSet = inlineformset_factory(ProductCard, CardQuantity, \
            form=MaterialCardQuantityForm, extra=6)
    DesignFormSet = inlineformset_factory(ProductCard, DesignCard, max_num=1, \
            extra=1, form=DesignForm)

    if request.method == "POST":
        form = ProductForm(request.POST, request.POST)
        material_formset = MaterialInlineFormSet(request.POST, request.FILES)

        if form.is_valid() and material_formset.is_valid():
            product = form.save(commit=False)
            product.created_user = request.user
            product.updated_uset = request.user
            product.save()
            materials = material_formset.save(commit=False)
            for m in materials:
                m.product = product
                m.save()
            material_formset.save_m2m()

            job = form.cleaned_data['job']
            q = CardQuantity.objects.create(
                    qtype = CardQuantity.PRODUCT,
                    product = product,
                    job_card = job,
                    units = 1)
            q.save()

            return HttpResponseRedirect(reverse('cards.views.product_detail',args=(product.pk,) ))

    else:
        form = ProductForm()
        if request.GET.get('job'):
            form.initial['job'] = request.GET.get('job')
        material_formset = MaterialInlineFormSet()

    return render_to_response("cards/product_form.html",{
        "form": form,
        "material_formset": material_formset,
        }, RequestContext(request))

@login_required(login_url='/account/login/')
def product_detail(request,product_id):
    if not request.POST:
        p = get_object_or_404(ProductCard, pk=product_id)
        j = CardQuantity.objects.filter(product=p).filter(qtype='product')
        items = CardQuantity.objects.filter(product=p).exclude(qtype="product")
        return render_to_response('cards/product_detail.html',{
            'product':p,
            'jobs':j,
            'items':items,
            },RequestContext(request))

@login_required(login_url='/account/login/')
def edit_product(request, product_id):
    """
    Pulls the product (and material information from the database
    and passes it to the template
    """
    product = get_object_or_404(ProductCard, pk=product_id)
    materials = CardQuantity.objects.filter(product=product).\
            filter(qtype='material')
    services = CardQuantity.objects.filter(product=product).\
            filter(qtype='service')
    adjustments = CardQuantity.objects.filter(product=product).\
            filter(qtype='adjustments')

    MaterialInlineFormSet = inlineformset_factory(ProductCard, CardQuantity, \
            form = MaterialCardQuantityForm, extra=5)
    ServiceInlineFormset = inlineformset_factory(ProductCard, CardQuantity, \
            form = MaterialCardQuantityForm, extra=3)
    AdjustmentInlineFormset = inlineformset_factory(ProductCard, CardQuantity, \
            form = MaterialCardQuantityForm, extra=3)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        material_formset = MaterialInlineFormSet(request.POST, request.FILES, instance=product, queryset=materials)
        
        if form.is_valid() and material_formset.is_valid():
            product = form.save(commit=False)
            product.updated_user = request.user
            product.save()
            fs = material_formset.save()
            #for i in fs:
            #    print i.qtype
            job = form.cleaned_data['job']
            if not CardQuantity.objects.filter(job_card=job).filter(product=product):
                q = CardQuantity.objects.create(
                        qtype = CardQuantity.PRODUCT,
                        product = product,
                        job_card = job,
                        units = 1)
                q.save()
            product.save()
            if job:
                return HttpResponseRedirect(reverse('cards.views.job_detail', args=(job.pk,)))
            else:
                return HttpResponseRedirect(reverse('cards.views.product_detail', args=(product_id,)))

    else:
        form = ProductForm(instance=product)
        if CardQuantity.objects.filter(product=product).filter(qtype='product'):
            form.initial['job'] = CardQuantity.objects.filter(product=product).filter(qtype='product')[0].job_card
        material_formset = MaterialInlineFormSet(instance=product, queryset=materials)

    return render_to_response("cards/product_form.html",{
        "form": form,
        "material_formset": material_formset,
        }, RequestContext(request))

@login_required(login_url='/account/login/')
def copy_product(request, product_id):
    """
    Copies the attributes from one ProductCard to a new one
    """
    old_product = get_object_or_404(ProductCard, pk=product_id)
    items = CardQuantity.objects.filter(product=old_product)\
            .exclude(qtype=CardQuantity.PRODUCT)
    
    initial_product = {'name':old_product.name,
            'status':Card.QUOTE}

    if request.method == "POST":
        form = ProductForm(request.POST,request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.assigneduser = Employee.objects.get(pk=product.assigneduser.pk)
            product.name = old_product.name
            product.created_user = request.user
            product.updated_user = request.user
            product.save()
            job = form.cleaned_data['job']
            q = CardQuantity.objects.create(
                    qtype = CardQuantity.PRODUCT,
                    product = product,
                    job_card = job,
                    units = 1)
            q.save()
            
            for i in items:
                q = CardQuantity.objects.create(
                        qtype = i.qtype,
                        material = i.material,
                        product = product,
                        service = i.service,
                        adjustment = i.adjustment,
                        units = i.units,
                        width = i.width,
                        height = i.height
                        )
                q.save()
            product.save()
            return HttpResponseRedirect(reverse('cards.views.edit_product',args=(product.pk,) ))
    
    else:
        form = ProductForm(initial=initial_product)
        if request.GET.get('job'):
            form.initial['job'] = request.GET.get('job')

    return render_to_response("cards/product_form.html",{
        "form": form,
        }, RequestContext(request))

@login_required(login_url='/account/login/')
def job_index(request):
    """
    Grabs the jobs from the database.
    """
    view = 'In Progress'
    jobslist = None
    jobsbyuser = None
    excludelist = [Card.FINISHED,Card.CANCELLED,Card.HOLD]
    users = None

    if request.GET.get('sort'):
        if request.GET.get('sort') == 'date':
            jobslist = JobCard.objects.exclude(status__in=excludelist)\
                    .order_by('due_date','assigneduser','status')
        
        elif request.GET.get('sort') == 'user':
            jobsbyuser = dict()
            users = Employee.objects.filter(active=True)
            for u in users:
                query = JobCard.objects.filter(assigneduser=u)\
                        .exclude(status__in=excludelist)\
                        .order_by('due_date','status')
                if query:
                    jobsbyuser.update({u:query})

        else:
            jobslist = JobCard.objects.exclude(status__in=excludelist)\
                    .order_by('assigneduser','due_date','status')
    else:
        jobslist = JobCard.objects.exclude(status__in=excludelist)\
                .order_by('assigneduser','due_date','status')


    if request.GET.get('status'):
        status = request.GET.get('status')
        view = status.title()
        jobslist = JobCard.objects.filter(status=status).order_by('due_date')

    if request.method == "POST":
        
        if 'job_checkbox' in request.POST:
            request.session['new_inv_jobs'] = \
                    request.POST.getlist('job_checkbox')

            return HttpResponseRedirect(reverse('invoice.views.new_invoice'))

    return render_to_response('cards/job_index.html',{
        "jobslist":jobslist,
        'view':view,
        'jobsbyuser':jobsbyuser,
        'users':users,
        }, RequestContext(request))

@login_required(login_url='/account/login/')
def job_detail(request,job_number):
    """
    displays the details about a job
    """
    if request.method == "POST":
        request.session['new_inv_jobs'] = [job_number]
        return HttpResponseRedirect(reverse('invoice.views.new_invoice'))

    if not request.POST:
        invoice = None
        card = get_object_or_404(JobCard, pk=job_number)
        if card.billed:
            invoice = InvQuantity.objects.filter(job_card=card)
            if invoice:
                invoice = invoice[0].invoice

        items = CardQuantity.objects.filter(job_card=card)

        return render_to_response('cards/job_detail.html',{
            'card':card,
            'items':items,
            'invoice':invoice,
            },RequestContext(request))

@login_required(login_url='/account/login/')
def edit_job(request,job_number):
    """
    pulls the job (job card) from the database, along with
    the associated product cards.
    """
    job = get_object_or_404(JobCard, pk=job_number)
    products = CardQuantity.objects.filter(job_card=job).filter(material=None)

    ProductInlineFormset = inlineformset_factory(JobCard, CardQuantity, \
            form = ProductCardQuantityForm, extra=0)

    if request.method == "POST":
        form = JobForm(request.POST, request.FILES, instance=job)
        product_formset = ProductInlineFormset(request.POST, request.FILES, \
                instance=job, queryset=products)
        if form.is_valid() and product_formset.is_valid():
            print request
            product_formset.save()
            job = form.save(commit=False)
            if 'thumbnail' in form.cleaned_data:
                job.thumbnail = form.cleaned_data['thumbnail']
            job.updated_user = request.user
            
            job.save()
            return HttpResponseRedirect(reverse('cards.views.job_detail', 
                args=(job_number,)))

    else:
        form = JobForm(instance=job)
        product_formset = ProductInlineFormset(instance=job, queryset=products)

    return render_to_response("cards/job_form.html",{
        "form": form,
        "product_formset": product_formset,
        }, RequestContext(request))


@login_required(login_url='/account/login/')
def new_job(request):
    """
    Creates a new job
    """
    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            if 'thumbnail' in form.cleaned_data:
                job.thumbnail = form.cleaned_data['thumbnail']
            job.created_user = request.user
            job.updated_user = request.user
            job.save()
            return HttpResponseRedirect(reverse('cards.views.job_detail',args=(job.pk,) ))

    else:
        form = JobForm()

    return render_to_response("cards/job_form.html",{
        "form":form,
        }, RequestContext(request))

@login_required(login_url='/account/login/')
def quote(request,job_number):
    """
    displays the standard invoice that can be printed
    """
    
    job = get_object_or_404(JobCard,pk = job_number)
    items = CardQuantity.objects.filter(job_card=job)
    if job.payment_type != PaymentEvent.IDO:
        tax = job.price * settings.TAX_RATE
    else:
        tax = 0.0
    total = job.price + Decimal(tax)

    return render_to_response("cards/quote_detail.html",{
        "job":job,
        "items":items,
        "tax":tax,
        "total":total,
        },RequestContext(request))

def quote_print(request,job_number):
    """
    displays the standard invoice that can be printed
    """
    
    job = get_object_or_404(JobCard,pk = job_number)
    items = CardQuantity.objects.filter(job_card=job)
    if job.payment_type != PaymentEvent.IDO:
        tax = job.price * settings.TAX_RATE
    else:
        tax = 0.0
    total = job.price + Decimal(tax)

    return render_to_response("cards/quote_print.html",{
        "job":job,
        "items":items,
        "tax":tax,
        "total":total,
        },RequestContext(request))

@login_required(login_url='/account/login/')
def product_rush(request,product_id):
    """
    displays a form for the type of rush fee,
    then calculated and adds the rush fee
    """
    prod = get_object_or_404(ProductCard, pk=product_id)
    RushFeeInlineFormset = inlineformset_factory(ProductCard, CardQuantity,\
            form=HistoryLockForm, extra=1)

    rush_fee_type = None
    rush_fee_formset = None
    if request.method == "POST":
        if request.GET.get('type'):
            rush_fee_formset = RushFeeInlineFormset(request.POST, request.FILES)

            if rush_fee_formset.is_valid():
                fees = rush_fee_formset.save(commit=False)

                for each in fees:
                    print each
                    each.material = Material.objects.filter(product_name='Rush Fee')[0]
                    each.product = prod
                    each.history_lock = True
                    each.width = 0.0
                    each.height = 0.0
                    each.save()
                rush_fee_formset.save_m2m()

                return HttpResponseRedirect(reverse('cards.views.product_detail',
                    args=(prod.pk,)))

        else:
            return HttpResponseRedirect('?type='+str(request.POST.get('rush_fee_type')))

    else:
        if request.GET.get('type'):
            fee_type = request.GET.get('type')
            
            if fee_type == RushFeeForm.R12:
                int_fee = settings.R12_PER * prod.price_int
                if int_fee < settings.R12_MIN:
                    int_fee = settings.R12_MIN
                ext_fee = settings.R12_PER * prod.price_ext
                if ext_fee < settings.R12_MIN:
                    ext_fee = settings.R12_MIN
                
                int_fee = "%.2f" % int_fee
                ext_fee = "%.2f" % ext_fee

                initial=[{'units':1,'locked_price_int':int_fee,'locked_price_ext':ext_fee}]
                rush_fee_formset = RushFeeInlineFormset(initial=initial)
            if fee_type == RushFeeForm.R24:
                int_fee = settings.R24_PER * prod.price_int
                if int_fee < settings.R24_MIN:
                    int_fee = settings.R24_MIN
                ext_fee = settings.R24_PER * prod.price_ext
                if ext_fee < settings.R24_MIN:
                    ext_fee = settings.R24_MIN
            
                int_fee = "%.2f" % int_fee
                ext_fee = "%.2f" % ext_fee
                
                initial=[{'units':1,'locked_price_int':int_fee,'locked_price_ext':ext_fee}]
                rush_fee_formset = RushFeeInlineFormset(initial=initial)
            if fee_type == RushFeeForm.R48:
                int_fee = settings.R48_PER * prod.price_int
                if int_fee < settings.R48_MIN:
                    int_fee = settings.R48_MIN
                ext_fee = settings.R48_PER * prod.price_ext
                if ext_fee < settings.R48_MIN:
                    ext_fee = settings.R48_MIN
            
                int_fee = "%.2f" % int_fee
                ext_fee = "%.2f" % ext_fee

                initial=[{'units':1,'locked_price_int':int_fee,'locked_price_ext':ext_fee}]
                rush_fee_formset = RushFeeInlineFormset(initial=initial)
        else:
            rush_fee_type = RushFeeForm()

    return render_to_response("cards/rush.html", {
        "rush_fee_type":rush_fee_type,
        "rush_fee_formset":rush_fee_formset,
        }, RequestContext(request))

@login_required(login_url='/account/login')
def pickup_index(request):
    """
    Displays the products that are "Ready for Pickup"
    """
    status = Card.READY_FOR_PICKUP

    if request.GET.get('status'):
        status = request.GET.get('status')

    view = status.title()

    pickup_list = ProductCard.objects.filter(status = status)

    if request.method == "POST":
        if 'product_checkbox' in request.POST:
            products = ProductCard.objects.filter(
                    pk__in = request.POST.getlist('product_checkbox'))

            for p in products:
                p.status = Card.FINISHED
                p.save()

    else:
        pass

    return render_to_response("cards/pickup_index.html",{
        "view":view,
        "pickup_list":pickup_list,
        },RequestContext(request))

@login_required(login_url='/account/login/')
def template_index(request):
    """
    Displays the products with production_status of template
    """
    product_list = ProductCard.objects.filter( \
            status = Card.TEMPLATE)
    job = None
    if request.GET.get('job'):
        job = request.GET.get('job')

    if request.method == "POST":
        if 'product_checkbox' in request.POST:
            pass
    else:
        pass
    return render_to_response("cards/template_index.html",{
        "product_list":product_list,
        },RequestContext(request))

@login_required(login_url='/account/login/')
@user_passes_test(lambda u: u.groups.filter(name='admin').count(), login_url='/')
def admin_approve_quote(request,job_number):
    '''
    sets the approved flag of a job to True so the quote link can be clicked
    '''
    job = get_object_or_404(JobCard, pk=job_number)

    job.admin_approved = True
    job.admin_approved_user = request.user
    job.admin_approved_date = datetime.datetime.now()
    job.save()

    return HttpResponseRedirect(reverse('cards.views.job_detail',
        args=(job_number,)))
