from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, loader
from django.forms.models import inlineformset_factory
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from contacts.models import Contact, Address, Telephone, ContactForm, AddressForm
from cards.models import JobCard

@login_required(login_url='/account/login/')
def index(request):
    contact_list = Contact.objects.all().order_by('last_name')
    return render_to_response('contacts/index.html', {'contact_list': contact_list},
            RequestContext(request))

@login_required(login_url='/account/login/')
def detail(request, contact_id):
    c = get_object_or_404(Contact, pk=contact_id)
    opened_list = JobCard.objects.filter(contact=c).filter(billed=False)
    completed_list = JobCard.objects.filter(contact=c).filter(billed=True)

    if not request.POST:
        return render_to_response('contacts/detail.html',{
            'contact':c,
            'opened_list':opened_list,
            'completed_list':completed_list,
            },RequestContext(request))

@login_required(login_url='/account/login/')
def new_contact(request):
    print "new_contact"

    AddressInlineFormSet = inlineformset_factory(Contact, Address, form=AddressForm, extra=1)
    TelephoneInlineFormSet = inlineformset_factory(Contact, Telephone, extra=1)

    if request.method == "POST":
        form = ContactForm(request.POST)
        address_formset = AddressInlineFormSet(request.POST, request.FILES)
        telephone_formset = TelephoneInlineFormSet(request.POST, request.FILES)

        if form.is_valid() and address_formset.is_valid() and telephone_formset.is_valid():
            contact = form.save()
            addresses = address_formset.save(commit=False)
            for a in addresses:
                a.contact_id = contact.pk
                a.save()
            phones = telephone_formset.save(commit=False)
            for p in phones:
                p.contact_id = contact.pk
                p.save()
            address_formset.save_m2m()
            telephone_formset.save_m2m()

            return HttpResponseRedirect(reverse('contacts.views.detail', args=(contact.pk,)))
    else:
        form = ContactForm()
        address_formset = AddressInlineFormSet()
        telephone_formset = TelephoneInlineFormSet()

    return render_to_response("contacts/form.html",{
        "form":form,
        "address_formset":address_formset,
        "telephone_formset":telephone_formset,
        },RequestContext(request))

@login_required(login_url='/account/login/')
def edit_contact(request, contact_id):
    contact = Contact.objects.get(pk=contact_id)

    AddressInlineFormSet = inlineformset_factory(Contact, Address, form=AddressForm, extra=1)
    TelephoneInlineFormSet = inlineformset_factory(Contact, Telephone, extra=1)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        address_formset = AddressInlineFormSet(request.POST, request.FILES, instance=contact)
        telephone_formset = TelephoneInlineFormSet(request.POST, request.FILES, instance=contact)
        if form.is_valid() and address_formset.is_valid() and telephone_formset.is_valid():
            form.save()
            address_formset.save()
            telephone_formset.save()
            return HttpResponseRedirect(reverse('contacts.views.detail', args=(contact.pk,)))
    else:
        form = ContactForm(instance=contact)
        address_formset = AddressInlineFormSet(instance=contact)
        telephone_formset = TelephoneInlineFormSet(instance=contact)
    return render_to_response("contacts/form.html", {
        "form": form,
        "address_formset": address_formset,
        "telephone_formset": telephone_formset,
        },RequestContext(request))
