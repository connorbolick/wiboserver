from django import forms
from django_select2 import *
from django.db.models import Q
from contacts.models import Contact
from cards.models import JobCard
from employee.models import *

from django.core.exceptions import ValidationError

def validate_fail_always(value):
    raise ValidationError(u'%s not valid. Infact nothing is valid!' % value)

########### Forms ##############]

class GetContactSearchForm(forms.Form):
    clients = ModelSelect2MultipleField(queryset=Contact.objects, required=False)

class GetEmployeeSearchForm(forms.Form):
    employees = ModelSelect2MultipleField(queryset=Employee.objects, required=False)
