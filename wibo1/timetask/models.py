from django.db import models
from decimal import Decimal
import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.conf import settings
from django import forms
from django.core.urlresolvers import reverse
from decimal import Decimal

from employee.models import Employee
from cards.models import JobCard

# Create your models here.
class Timelog(models.Model):
    PROD = "production time"
    REWORK = "rework time"

    # because i don't know where else to store the hourly rate
    # meant as a way to help figure out cost
    PERHOUR = 5.00
    MULTRATE = Decimal(PERHOUR / 3600.00)

    TYPE_CHOICES = (
            (PROD, 'production time'),
            (REWORK, 'rework time')
            )
    employee = models.ForeignKey(Employee)
    job = models.ForeignKey(JobCard)
    type = models.CharField('type', max_length=20, choices=TYPE_CHOICES)
    time_in = models.DateTimeField(blank=True, null=True, editable=True)
    time_out = models.DateTimeField(blank=True, null=True, editable=True)
    calculated = models.DecimalField(max_digits=19, decimal_places=10, editable=False, blank=True, null=True)

    def __unicode__(self):
        return "%s, Job: %s (In: %s, Out: %s, Type: %s)" % (self.employee, self.job, self.time_in, self.time_out, self.type)

    def save(self):
        super(Timelog, self).save()
        if self.time_out != None:
            self.calculated = (self.time_out - self.time_in).total_seconds()
            super(Timelog, self).save()

class LogInBasic(ModelForm):
    def __init__(self, *args, **kwargs):
        super(LogInBasic, self).__init__(*args, **kwargs)
        self.fields['job'] = forms.ModelChoiceField(queryset=JobCard.objects.order_by('-job_number'))
        self.fields['job'].required = True
        self.fields['type'].required = True
    class Meta:
        model = Timelog
        exclude = ('employee', 'time_in', 'calculated', 'time_out')

class LogInForm(ModelForm):
    '''Creates the base form for cards'''
    class Meta:
        model = Timelog
        exclude = ('calculated','time_out',)

class LogOutForm(ModelForm):
    class Meta:
        model = Timelog
        exclude = ('employee', 'job', 'type', 'time_in',)
