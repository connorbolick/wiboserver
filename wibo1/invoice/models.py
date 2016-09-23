import datetime

from django import forms
from django.db import models
from django.conf import settings
#from cards.models import JobCard
from django.forms import ModelForm
from contacts.models import Contact
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

class Invoice(models.Model):
    """
    Defines an invoice.
    Relates JobCard objects with payment events
    """
    CASH            = 'CASH'
    CHECK           = 'CHECK'
    IDO             = 'IDO'
    WEB_INV         = 'WEB'
    GIFT_CARD       = 'GIFT'
    MARKETPLACE     = 'MARKET'
    PAYMENT_EVENT_TYPE = (
            (CASH, 'Cash'),
            (CHECK, 'Check'),
            (IDO, 'Interdepartmental Order'),
            (WEB_INV, 'Web Invoice'),
            (GIFT_CARD, 'Gift Certificate'),
            (MARKETPLACE, 'Marketplace'),
            )
    invoice_number  = models.AutoField(primary_key=True)
    payment_type    = models.CharField(max_length=10, \
                            choices=PAYMENT_EVENT_TYPE)
    invoice_date    = models.DateField(auto_now_add=True)
    billing_contact = models.ForeignKey(Contact, related_name='invoice')
    job_cards       = models.ManyToManyField('cards.JobCard', through='InvQuantity')
    invoice_notes   = models.TextField(blank=True, null=True)
    billed          = models.BooleanField(default=False)
    taxable         = models.BooleanField(default=True)
    paid            = models.BooleanField(default=False)
    created_user    = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_created_set")
    created_date    = models.DateTimeField(auto_now_add=True)
    updated_user    = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_updated_set")
    updated_date    = models.DateTimeField(auto_now=True)
    notes           = models.TextField(blank=True, null=True)
    

    def get_invoice_number(self):
        """
        Gets the formated invoice number
        """
        return "%s%05d" % (self.invoice_date.year, self.invoice_number)
    invoice_number_display = property(get_invoice_number)
    # total price
    def _get_price(self):
        """
        grabs the price from all the associated 
        job cards (through InvQuantity objects)
        """
        price = 0
        q = InvQuantity.objects.filter(invoice=self)

        for each in q:
            price += each.units * each.price

        return price

    price = property(_get_price)
    # tax
    def _get_tax(self):
        if self.taxable:
            tax = self.price * settings.TAX_RATE
        else:
            tax = 0

        return tax

    tax = property(_get_tax)
    # total paid
    def _get_total_paid(self):
        """
        add all the payment event amounts together
        """
        paid = 0

        payment_events = PaymentEvent.objects.filter(invoice=self)

        
        if payment_events:
            for each in payment_events:
                paid += each.payment_amount

        return paid

    paid_amount = property(_get_total_paid)

    def _get_grand_total(self):
        """
        calculates the grand total for the invoice
        """
        return self.price + self.tax

    grand_total = property(_get_grand_total)
    # remaining balance
    def _get_balance(self):
        """
        calcuates the balance on the invoice
        price + tax - payments
        """
        return self.grand_total - self.paid_amount

    balance = property(_get_balance)

    def __unicode__(self):
        return "Invoice: %s" % self.invoice_number_display
    
    def get_absolute_url(self):
        return reverse('invoice.views.detail',args=[self.invoice_number])

    def job_list(self):
        string = ''
        for each in self.job_cards.all():
            string = string +  "<a href='/admin/cards/jobcard/%s'>%s</a><br/>" % (each.job_number, each)
        return string
    job_list.allow_tags = True

class PaymentEvent(models.Model):
    """
    Base class for payment events

    **Should not be instantiated by itself...ever**
    """
    CASH            = 'CASH'
    CHECK           = 'CHECK'
    IDO             = 'IDO'
    WEB_INV         = 'WEB'
    GIFT_CARD       = 'GIFT'
    MARKETPLACE     = 'MARKET'
    PAYMENT_EVENT_TYPE = (
            (CASH, 'Cash'),
            (CHECK, 'Check'),
            (IDO, 'Interdepartmental Order'),
            (WEB_INV, 'Web Invoice'),
            (GIFT_CARD, 'Gift Certificate'),
            (MARKETPLACE, 'Marketplace'),
            )

    invoice         = models.ForeignKey(Invoice)
    payment_user    = models.ForeignKey(User, related_name='+')
    payment_date    = models.DateTimeField(auto_now_add=True)
    payment_amount  = models.DecimalField(max_digits=9, decimal_places=3)
    # processed payments have been:
    #   put in the safe (Cash/Check),
    #   sent to SABO (IDO),
    #   forwarded on to WebInvoice,
    #   ect.
    payment_processed = models.BooleanField(default=False)
    # received payments have shown up on our
    # activity report / account statments
    payment_received= models.BooleanField(default=False)
    payment_notes   = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "Payment: %s, $%s" % (self.pk, self.payment_amount)

    def invoice_detail(self):
        return "<a href='/admin/invoice/invoice/%s'>%s</a><br/>" % (self.invoice.invoice_number, self.invoice)
    invoice_detail.allow_tags = True

    def job_detail(self):
        return self.invoice.job_list()
    job_detail.allow_tags = True

    def billing_contact(self):
        return self.invoice.billing_contact

class PaymentEvent_In_House(PaymentEvent):
    """
    Abstract base class that defines an in-house payment
    contains elements included for all in-house payments
    (i.e. a cash or check payment delievered directly to CB+D)
    """
    receipt_number  = models.CharField(max_length=20)

    class Meta:
        """make the class abstract"""
        abstract=True

class PaymentEventCash(PaymentEvent_In_House):
    """
    Defines a cash payment
    """
    payment_type = models.CharField(max_length=5, default=PaymentEvent.CASH, \
            editable=False)

    def __unicode__(self):
        return "%s - Cash" % super(PaymentEventCash,self).__unicode__()

class PaymentEventCheck(PaymentEvent_In_House):
    """
    Defines a check payment
    """
    payment_type = models.CharField(max_length=5, default=PaymentEvent.CHECK, \
            editable=False)
    check_number    = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s - Check %s" % (super(PaymentEventCheck,self).__unicode__(), \
                self.check_number)

class PaymentEventGiftCard(PaymentEvent_In_House):
    """
    Defines a gift card
    """
    payment_type = models.CharField(max_length=5, default=PaymentEvent.GIFT_CARD, \
            editable=False)
    gift_card_number    = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s - Gift Card %s" % (super(PaymentEventGiftCard,self).__unicode__(), \
                self.gift_card_number)


class PaymentEventIDO(PaymentEvent):
    """
    defines an IDO payment
    """
    payment_type = models.CharField(max_length=5, default=PaymentEvent.IDO, \
            editable=False)
    dept_chartstring= models.CharField(max_length=50)
    approved_by     = models.CharField(max_length=30)
    approved_date   = models.DateField()

    def __unicode__(self):
        return "%s - IDO %s" % (super(PaymentEventIDO,self).__unicode__(), \
                self.dept_chartstring)

class PaymentEventWebInvoice(PaymentEvent):
    """
    defines a record of sending an invoice on 
    to the web invoice system for the University
    """
    payment_type = models.CharField(max_length=5, default=PaymentEvent.WEB_INV, \
            editable=False)
    web_invoice_number  = models.CharField(max_length=20,blank=True,null=True)
    sent_to_client  = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s - Web %s" % (super(PaymentEventWebInvoice,self).__unicode__(), \
                self.web_invoice_number)

class PaymentEventMarketplace(PaymentEvent):
    '''
    defines a payment recieved through Clemson University's web Marketplace
    '''
    payment_type = models.CharField(max_length=10, default=PaymentEvent.MARKETPLACE,\
            editable=False)
    order_number = models.CharField(max_length=20)

    def __unicode__(self):
        return "%s - Marketplace %s" % \
                (super(PaymentEventMarketplace,self).__unicode__(),
                 self.order_number)



# =THROUGH models

class InvQuantity(models.Model):
    """
    defines an intermediary model to relate job cards
    to invoices
    """
    invoice         = models.ForeignKey(Invoice)
    job_card        = models.ForeignKey('cards.JobCard')
    units           = models.DecimalField(max_digits=9, \
            decimal_places=3, default=1)
    def _get_price(self):
        """
        grabs the price from the job cards
        """
        return self.job_card.price

    price = property(_get_price)

    def _get_extended_price(self):
        """
        grabs the extended price (price * units)
        """
        return self.price * self.units

    extended_price = property(_get_extended_price)

    def _get_percentage_invoiced(self):
        """
        adds all the quantity objects associated with
        a job together
        """
        q_objs = InvQuantity.objects.filter(job_card=self.job_card)
        
        percent = 0

        for each in q_objs:
            percent += each.units

        return percent

    percentage_invoiced = property(_get_percentage_invoiced)

    def __unicode__(self):
        return "InvQuantity: invoice %s, job %s, units %s" % \
                (self.invoice, self.job_card, self.units)
# =FORMS

class InvoiceForm(ModelForm):
    """
    Creates a forms based on the invoice model
    """
    class Meta:
        model = Invoice
        exclude = ('job_cards','billed','taxable','paid','created_user','updated_user')

class PaymentTypeForm(forms.Form):
    """
    Creates a form for selecting the payment type
    """
    payment_type = forms.ChoiceField(choices=PaymentEvent.PAYMENT_EVENT_TYPE)

class PaymentForm(ModelForm):
    """
    Creates a form based on the PaymentEvent model
    """
    payment_amount = forms.DecimalField( widget = \
            forms.TextInput(attrs={'class':'span1'}) )
    #payment_date = forms.CharField( widget = \
    #        forms.TextInput(attrs={'class':'span2 datepicker'}) )
    payment_notes = forms.CharField( widget = \
            forms.Textarea(attrs={'rows':'2'}), required=False)
    class Meta:
        model = PaymentEvent
        exclude = ('invoice', 'payment_processed', 'payment_received', 'payment_user',
                'payment_date')

class PaymentActionForm(forms.Form):
    """
    creates the form to allow batch actions on payments
    """
    # ACTION CHOICES
    PROCESS = 'process'
    RECEIVE = 'receive'

    ACTION_CHOICES = (
            (PROCESS, 'process'),
            (RECEIVE, 'receive'),
            )

    action = forms.ChoiceField(choices=ACTION_CHOICES)
