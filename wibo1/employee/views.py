from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.forms.models import inlineformset_factory, formset_factory
from django.template import Context, loader, RequestContext
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.timezone import utc
import datetime

from employee.models import *
from cards.models import *
from timetask.models import *

@login_required(login_url='/account/login/')
def index(request):
    """
    Shows all active employees
    """

    employees       = Employee.objects.filter(active=True)

    designer_list   = employees.filter(title=Employee.DESIGNER)
    writers_list    = employees.filter(title=Employee.WRITER)
    managers_list   = employees.filter(
            title__in=[Employee.PRODUCTION_MANAGER,Employee.ART_DIRECTOR])
    sales_list      = employees.filter(title=Employee.SALES)
    hr_list         = employees.filter(title=Employee.HR)
    marketing_list  = employees.filter(title=Employee.MARKETING)
    supply_list     = employees.filter(title=Employee.SUPPLY)
    photographers_list = employees.filter(title=Employee.PHOTOGRAPHER)
    studentadmins_list = employees.filter(title=Employee.STUDENT_ADMIN)
    web_list        = employees.filter(title=Employee.WEB)
    sapubs_list     = employees.filter(
            title__in=[Employee.SAPUB_ADMIN,Employee.SAPUB_STAFF])

    employees_emails=""
    for e in employees:
        employees_emails += "," + e.email

    designer_emails=""
    for e in designer_list:
        designer_emails += "," + e.email

    writers_emails=""
    for e in writers_list:
        writers_emails += "," + e.email

    managers_emails=""
    for e in managers_list:
        managers_emails += "," + e.email

    sales_emails=""
    for e in sales_list:
        sales_emails += "," + e.email

    hr_emails=""
    for e in hr_list:
        hr_emails += "," + e.email

    marketing_emails=""
    for e in marketing_list:
        marketing_emails += "," + e.email

    supply_emails=""
    for e in supply_list:
        supply_emails += "," + e.email

    photographers_emails=""
    for e in photographers_list:
        photographers_emails += "," + e.email

    studentadmins_emails=""
    for e in studentadmins_list:
        studentadmins_emails += "," + e.email

    web_emails=""
    for e in web_list:
        web_emails += "," + e.email

    sapubs_emails=""
    for e in sapubs_list:
        sapubs_emails += "," + e.email

    

    return render_to_response('employee/index.html', {
        'all_emails'        : employees_emails,
        'designer_list'     : designer_list,
        'designer_emails'   : designer_emails,
        'writers_list'      : writers_list,
        'writers_emails'   : writers_emails,
        'managers_list'     : managers_list,
        'managers_emails'   : managers_emails,
        'sales_list'        : sales_list,
        'sales_emails'   : sales_emails,
        'hr_list'           : hr_list,
        'hr_emails'   : hr_emails,
        'markering_list'    : marketing_list,
        'marketing_emails'   : marketing_emails,
        'photographers_list': photographers_list,
        'photographers_emails'   : photographers_emails,
        'studentadmins_list': studentadmins_list,
        'studentadmins_emails'   : studentadmins_emails,
        'web_list'          : web_list,
        'web_emails'   : web_emails,
        'sapubs_list'       : sapubs_list,
        'sapubs_emails'   : sapubs_emails,
        'supply_list'       : supply_list,
        'supply_emails'   : supply_emails,
        },RequestContext(request))

@login_required(login_url='/account/login/')
@user_passes_test(lambda u: u.groups.filter(name='admin').count(), login_url='/')
def new_employee(request):
    """
    makes a new employee and wibo user
    """

    if request.method=="POST":
        form = EmployeeForm(request.POST,request.FILES)

        if form.is_valid():
            employee = form.save(commit=False)
            # create a wibo user
            wibo_user = User.objects.create_user(
                    employee.user_name,
                    employee.email,
                    settings.DEFAULT_PASSWORD)
            wibo_user.first_name = employee.first_name
            wibo_user.last_name = employee.last_name
            wibo_user.save()
            # add user to permission groups
            for group,titles in PERMISIONS.iteritems():
                if employee.title in titles:
                    g = Group.objects.get(name=group)
                    wibo_user.groups.add(g)
            # add the new user to the employee
            employee.wibo_user = wibo_user
            employee.save()
            return HttpResponseRedirect(reverse('employee.views.index'))

    else: 
        form = EmployeeForm()

    return render_to_response("employee/form.html",{
        "form":form,
        },RequestContext(request))

def detail(request,employee_id,mnum="0"):
    """Displays details about an employee"""

    if request.method == 'POST':
        loginform = LogInBasic(request.POST)
        if loginform.is_valid():
            #print loginform.cleaned_data['job'].job_number
            #print loginform.cleaned_data['type]
            if loginform.cleaned_data['type'] == 'production time':
                corrected = 'prod'
            elif loginform.cleaned_data['type'] == 'rework time':
                corrected = 'rework'

            return HttpResponseRedirect('/employee/logtasktime/'+str(loginform.cleaned_data['job'].job_number)+"/"+corrected)
            #return HttpResponseRedirect(reverse('employee.views.logtasktime'), kwargs={'job_number': loginform.cleaned_data['job'].job_number, 'type': loginform.cleaned_data['type']})
    else:
        loginform = LogInBasic()

    scope = ['on hold', 'needs approval', 'in production','default']
    jobscope = scope + ['quote','outsourced','approved']
    productscope = scope + ['quote','outsourced','designing','ready for pickup','approved']
    loggedin = False
    log_list = None
    log_jobs = None
    msg_lout = ''

    if mnum == '1':
        message = "You're still logged in, please log out first."
    elif mnum == '2':
        message = "You're now clocked in."
    elif mnum == '3':
        message = "You're now clocked out."
    else:
        message = ''

    employee = get_object_or_404(Employee, pk=employee_id)
    job_list    = JobCard.objects.filter(assigneduser=employee.wibo_user)\
            .filter(status__in=jobscope).order_by('due_date','status')
    product_list = ProductCard.objects.filter(assigneduser=employee.wibo_user)\
            .filter(status__in=productscope).order_by('due_date','status')

    if int(request.user.pk) == int(employee_id):
        loggedin = True
        try:
            log_list = Timelog.objects.get(employee=request.user.pk, time_out__isnull=True)
            
            if log_list.job.status not in jobscope and log_list.job.assigneduser.wibo_user_id == request.user.pk:
                msg_lout = "You're currently logged in for job: " + str(log_list.job) + ", "
                msg_lout = msg_lout + "which has status: " + log_list.job.status + ". "
            elif log_list.job.assigneduser.wibo_user_id != request.user.pk:
                msg_lout = "You're currently logged in for job: " + str(log_list.job)
                msg_lout = msg_lout + " (assigned to: " +  str(log_list.job.assigneduser) + "), "
                msg_lout = msg_lout + " which has status: " + log_list.job.status + ". "
            else:
                msg_lout = ''

        except Timelog.DoesNotExist:
            log_list = None
    else:
        loggedin = False


    return render_to_response('employee/detail.html',{
        'e':employee,
        'job_list':job_list,
        'product_list':product_list,
        'log_list':log_list,
        'loggedin':loggedin,
        'message' : message,
        'message2': msg_lout,
        'loginform': loginform,
        },RequestContext(request))

@login_required(login_url='/account/login/')
def logtasktime(request,job_number,type):

    job = JobCard.objects.get(pk=job_number)
    employee = Employee.objects.get(pk=request.user.pk)
    corrected_type = ''
    query = None

    if type == 'prod':
        corrected_type = Timelog.PROD
    elif type == 'rework':
        corrected_type = Timelog.REWORK

    try:
        query = Timelog.objects.get(employee=employee, job=job, type=corrected_type, time_in__isnull=False, time_out__isnull=True)
    except Timelog.DoesNotExist:
        query = None
    except Timelog.MultipleObjectsReturn:
        query = None

    if query != None:
        # log out the user
        form = LogOutForm(instance=query)
        timeout = form.save(commit=False)
        timeout.time_out = datetime.datetime.now().replace(tzinfo=utc)
        timeout.calculated = (timeout.time_out - query.time_in).total_seconds()
        log_meta = timeout.save()

        message = 3

    else:
        # log in the user, but make sure that there's not a missed punch already

        query = Timelog.objects.filter(employee=employee, time_in__isnull=False, time_out__isnull=True)

        if query.count() == 0:
            form = LogInForm({'employee' : employee.pk, 'job' : job.pk, 'type' : corrected_type, 'time_in' : datetime.datetime.now().replace(tzinfo=utc) })

            if form.is_valid():
                log_meta = form.save()

            message = 2
        else:
            message = 1

    return HttpResponseRedirect(reverse('employee.views.detail', kwargs={'employee_id':request.user.pk,'mnum':message}))
