import datetime
 
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
 
 
def init_session(session_key):
    """
    Initialize same session as done for ``SessionMiddleware``.
    """
    engine = import_module(settings.SESSION_ENGINE)
    return engine.SessionStore(session_key)
 

@login_required(login_url='/account/login/')
@user_passes_test(lambda u: u.groups.filter(name='admin').count(), login_url='/')
def logout_all_users(request):
    """
    Read all available users and all available not expired sessions. Then
    logout from each session.
    """
    now = datetime.datetime.now()
    request = HttpRequest()
 
    sessions = Session.objects.filter(expire_date__gt=now)
    users = dict(User.objects.values_list('id', 'username'))
 
    print('Found %d not-expired session(s).' % len(sessions))
 
    for session in sessions:
        username = session.get_decoded().get('_auth_user_id')
        request.session = init_session(session.session_key)
 
        logout(request)
        print('    Successfully logout %r user.' % username)
 
    print('All OK!')
    return HttpResponseRedirect('/')

@login_required(login_url="/account/login/")
def sapub_request(request):
    form = JobForm()

    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save()
            return HttpResponseRedirect(reverse('cards.views.job_detail',args=(job.pk,) ))

    else:
        form = JobForm()

    return render_to_response("sapub_request.html",{
        "form":form,
        },RequestContext(request))


@login_required(login_url='/account/login/')
@user_passes_test(lambda u: u.groups.filter(name='admin').count(), login_url='/')
def cards_migration_extras_0009_1(request):
    quantcards = CardQuantity.objects.all()
    for q in quantcards:
        if q.material != None and q.product != None and q.job_card == None:
            q.qtype = CardQuantity.MATERIAL
        elif q.product != None and q.job_card != None and q.material == None:
            q.qtype = CardQuantity.PRODUCT

        print q
        q.save()
    return HttpResponseRedirect('/')

@login_required(login_url='/account/login/')
@user_passes_test(lambda u: u.groups.filter(name='admin').count(), login_url='/')
def cards_migration_extras_0009_2(request):
    prodcards = ProductCard.objects.all()
    for p in prodcards:
        p.name = p.product_name
        p.assigneduser = User.objects.get(pk=p.designer.pk)
        print p
        p.save()
    return HttpResponseRedirect('/')

@login_required(login_url='/account/login/')
@user_passes_test(lambda u: u.groups.filter(name='admin').count(), login_url='/')
def cards_migration_extras_0009_3(request):
    jobcards = JobCard.objects.all()
    for j in jobcards:
        j.name = j.job_name
        j.prod_notes = j.job_notes

        print j
        j.save()
    return HttpResponseRedirect('/')
