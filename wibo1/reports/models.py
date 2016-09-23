#from django.db import models
from django import forms
from django.db import models

# Create your models here.

# forms
class StartEndDateForm(forms.Form):
    """
    Creates a start and end date form
    """
    start = forms.DateField( widget =\
            forms.TextInput(attrs={'class':'datepicker'}),
            required=False)
    end = forms.DateField( widget = \
            forms.TextInput(attrs={'class':'datepicker'}),
            required=False)

class KeyValueMap(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=300)

    def __unicode__(self):
        return u'%s=>%s' % (self.key, self.value)