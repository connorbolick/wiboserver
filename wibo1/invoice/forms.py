from django import forms
from django_select2 import *
from django.db.models import Q

from cards.models import JobCard
from contacts.models import Contact

from django.core.exceptions import ValidationError

def validate_fail_always(value):
    raise ValidationError(u'%s not valid. Infact nothing is valid!' % value)

########### Forms ##############

class GetJobSearchForm(forms.Form):
    jobs = ModelSelect2MultipleField(queryset=JobCard.objects, required=False, label='By Job')

class GetClientSearchForm(forms.Form):
    clients = ModelSelect2MultipleField(queryset=Contact.objects, required=False, label='By Contact')

class GetInvSearchForm(forms.Form):
    inv = ModelSelect2MultipleField(queryset=Contact.objects, required=False, label='By Inv No')
