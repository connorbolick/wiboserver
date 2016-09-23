from django.db import models
from django.forms import ModelForm
from django import forms
from roi.models import ClientROI

# Create your models here.
class Contact(models.Model):
    """
    Stores information about the client.
    Serves and foreign key for:
        Address
        Telephone
    """
    # Default Price Level Choices
    INTERNAL = "INT"
    EXTERNAL = "EXT"
    PRICE_LEVEL_CHOICES = (
            (INTERNAL, 'internal'),
            (EXTERNAL, 'external')
            )
        
    first_name      = models.CharField(max_length=30)
    last_name       = models.CharField(max_length=30)
    company         = models.CharField('Company or organization',
                                max_length=255)
    department      = models.CharField('Department or major',
                                max_length=255)
    #title           = models.CharField('Position title',
    #                            max_length=255)
    default_price_level = models.CharField(max_length=3,
                                choices=PRICE_LEVEL_CHOICES)
    email           = models.EmailField(max_length=254)
    student_id      = models.CharField('XID number',max_length=10, 
                                null=True, blank=True)
    roi             = models.ForeignKey(ClientROI, null=True, blank=True)
    notes           = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"%s %s (%s, %s)" % (self.first_name, self.last_name, 
                self.department,self.company)

class Address(models.Model):
    """
    Stores addresses associated with a client.
    Each address must belong to a client.

    The max_length for these was borrowed from 
    django-shop and django-postal to allow for
    easier use of international address support
    """
    contact         = models.ForeignKey(Contact)
    street_address  = models.CharField('address',
                                max_length=255)
    city            = models.CharField(max_length=20)
    state           = models.CharField(max_length=255)
    postal_code     = models.CharField('zip code',
                                max_length=20)
    country         = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u"%s %s %s %s" % (self.street_address, \
                self.city, self.postal_code, self.state)

class Telephone(models.Model):
    """
    Stores telephone numbers associated with a client.
    Each phone number must belong to a client.
    """
    contact        = models.ForeignKey(Contact)
    
    # Phone Type choices
    CAMPUS  = "CAMP"
    WORK    = "WORK"
    CELL    = "CELL"
    HOME    = "HOME"

    PHONE_TYPE_CHOICES = (
            (CAMPUS, 'campus'),
            (WORK, 'work'),
            (CELL, 'cell'),
            (HOME, 'home')
            )

    phone_type      = models.CharField(max_length=4,
                            choices=PHONE_TYPE_CHOICES)
    phone_number    = models.CharField(max_length=24)

    def __unicode__(self):
        return u"%s (%s)" % (self.phone_number, self.phone_type)

class ContactForm(ModelForm):
    """
    Creates a form based on the model indicated.
    Lets django do all the heavy lifting on.
    """
    class Meta:
        model = Contact
	fields = '__all__'

class AddressForm(ModelForm):
    """
    Creates a form based on the Address model.
    Not strickly needed with the inlineformset_factory
    over in the view, but needed to exclude the country field.
    """
    state = forms.CharField( widget =
            forms.TextInput(attrs={'class':'span1'}) )
    postal_code = forms.CharField( widget =
            forms.TextInput(attrs={'class':'span2'}) )
    class Meta:
        model = Address
	fields = '__all__'
        exclude = ('country',)
