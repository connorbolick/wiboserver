import locale
from decimal import Decimal
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from contacts.models import Contact
from inventory.models import Material
from invoice.models import Invoice, PaymentEvent
from django.conf import settings
from django import forms
from django.core.urlresolvers import reverse

from employee.models import Employee
from roi.models import JobROI

# adding for signaling because circular reference issue
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

CHARTFIELD_LEN = 23

# Create your models here.
class Card(models.Model):
    """
    Abstract base class for card models
    """
    # Status Choices
    HOLD = 'on hold'
    NEEDS_APPROVAL = 'needs approval'
    IN_PRODUCTION = 'in production'
    FINISHED = 'finished'
    CANCELLED = 'cancelled'
    APPROVED = 'approved'
    NEEDS_DESIGNER = 'needs designer'

    DESIGNING = 'designing'
    READY_FOR_PICKUP = 'ready for pickup'
    QUOTE = 'quote'
    OUTSOURCED = 'outsourced'
    TEMPLATE = 'template'

    NEEDS_REVISIONS = 'needs revisions'
    PROVIDED = 'provided'
    COPY_REVIEW = 'Copy Review'
    CONCEPTING = 'Concepting'
    DESIGNING = 'Designing'
    DESIGN_REVIEW = 'Design Review'
    DESIGN_REVISIONS = 'Design Revisions'
    NEEDS_DESIGNER = 'Needs Designer'
    NEED_INFO = 'Need Info'
    NEED_QUOTE = 'Need Quote'
    NEED_QUOTE_APPROVAL = 'Need Quote Approval'
    NEED_DESIGN_APPROVAL = 'Need Design Approval'
    NEEDS_THUMBNAIL = 'Needs Thumbnail'
    RESEARCHING = 'Researching'
    REVIEW_CLIENT = 'Review - Client'
    NON_PRINT_PRODUCTION = 'Non-Print Production'
    PRINT_PRODUCTION = 'Print Production'
    COMPLETED = 'Completed / Delivered'

    STATUS_CHOICES = (
            (HOLD, 'on hold'),
            (NEEDS_APPROVAL, 'needs approval'),
            (APPROVED, 'approved'),
            (IN_PRODUCTION, 'in production'),
            (FINISHED, 'finished'),
            (READY_FOR_PICKUP, 'ready for pickup'),
            (CANCELLED, 'cancelled'),
            (COPY_REVIEW, 'Copy Review'),
            (CONCEPTING, 'Concepting'),
            (DESIGNING, 'Designing'),
            (DESIGN_REVIEW, 'Design Review'),
            (DESIGN_REVISIONS, 'Design Revisions'),
            (NEEDS_DESIGNER, 'Needs Designer'),
            (NEED_INFO, 'Need Info'),
            (NEED_QUOTE, 'Need Quote'),
            (NEED_QUOTE_APPROVAL, 'Need Quote Approval'),
            (NEED_DESIGN_APPROVAL, 'Need Design Approval'),
            (NEEDS_THUMBNAIL, 'Needs Thumbnail'),
            (RESEARCHING, 'Researching'),
            (REVIEW_CLIENT, 'Review - Client'),
            (NON_PRINT_PRODUCTION, 'Non-Print Production'),
            (PRINT_PRODUCTION, 'Print Production'),
            (COMPLETED, 'Completed / Delivered')
            )

    # a descriptive name like "scrim banner" or "Spring Formal Materials"
    name = models.CharField(max_length=255)
    # SAPUBs FileMaker # or online marketplace order #
    order_number = models.CharField(max_length=20, blank=True, null=True)
    # date the card is due
    due_date = models.DateField(null=True)
    # designer or employee assigned to the card
    assigneduser = models.ForeignKey(Employee)
    # the total cost to produce the card, recalculated on save()
    cost = models.DecimalField(max_digits=9, decimal_places=3,null=True)
    # notes for users and staff for this card
    prod_notes = models.TextField(blank=False, null=False, default=False)
    # notes for clients (this shows up on quotes and invoices)
    client_notes = models.TextField(blank=True, null=True)
    # the client's rep who approved the quote/artwork
    approved_by = models.CharField(max_length=255, blank=True, null=True)
    # when approval was given
    approved_on = models.DateField(blank=True,null=True)
    # the calculated cost of waste for the job, recalculated on save()
    waste_cost = models.DecimalField(max_digits=9, decimal_places=3,
                                      blank=True, null=True)
    # an image representing the card (final printed file, etc)
    thumbnail = models.ImageField(upload_to='thumbs/%Y/%m/%d/',blank=True,
                                    default="")
    # flags the card as needing manager attention
    attention = models.BooleanField(default=False)
    # if the price of this card is included on invoices/quotes
    billable = models.BooleanField(default=True)
    # if the job is finished and no furthat WIBO action is needed
    archived = models.BooleanField(default=False)
    # who created the card
    created_user = models.ForeignKey(
                    User, related_name="%(app_label)s_%(class)s_created_set")
    # when the card was created (date and time)
    created_date = models.DateTimeField(auto_now_add=True)
    # who last updated the card
    updated_user = models.ForeignKey(
                    User, related_name="%(app_label)s_%(class)s_updated_set")
    # when the last update was made
    updated_date = models.DateTimeField(auto_now=True)
    # if a manager has approved the card (quote or design)
    admin_approved = models.BooleanField(default=False)
    # who the approving manager was
    admin_approved_user = models.ForeignKey(
                    User, null=True, blank=True,
                    related_name="%(app_label)s_%(class)s_admin_set")
    # when manager approval was given
    admin_approved_date = models.DateTimeField(null=True, blank=True)

    def update(self):
        '''updates the stored price, cost and waste cost fields'''
        raise NotImplementedError, "update() not implemented"

    def archive_validate(self):
        '''verifies all information is present and the card can be archived'''
        if self.approved_on == None:
            return False, "Approval needed"
        return True

    def archive(self):
        '''sets the archive flag (so the card shouldn't change)'''
        self.archived=True
        self.save()

    def unarchive(self):
        '''unarchives the card'''
        self.archived=False
        self.save()

    def get_absolute_url(self):
        '''defines the absolute url to the instance'''
        raise NotImplementedError, "get_absolute_url() not implemented"

    def _get_waste(self):
        '''saves the waste cost'''
        waste = 0
        q = None
        if isinstance(self,ProductCard):
            q = CardQuantity.objects.filter(product=self)\
                    .exclude(qtype=CardQuantity.PRODUCT)
        if isinstance(self,ServiceCard):
            q = CardQuantity.objects.filter(service=self)\
                    .exclude(qtype=CardQuantity.SERVICE)
        if isinstance(self,AdjustmentCard):
            q = CardQuantity.objects.filter(adjustment=self)\
                    .exclude(qtype=CardQuantity.ADJUSTMENT)

        if q == None:
            raise NotImplementedError

        for each in q:
            waste += float(each.waste_cost)

        return waste

    def _past_due(self):
        """ true if past due, false if not """
        if self.status not in [self.FINISHED, self.CANCELLED,
                self.READY_FOR_PICKUP, self.TEMPLATE]:
            if self.due_date - datetime.date.today() < \
                    datetime.timedelta(0):
                return "past"
            elif self.due_date - datetime.date.today() < \
                    datetime.timedelta(1):
                return "today"
            elif self.due_date - datetime.date.today() < \
                    datetime.timedelta(3):
                return "close"

        return "good"

    past_due = property(_past_due)

    def __unicode__(self):
        if self.order_number:
            return "%s PO#%s (%s)" % (self.name, self.order_number, self.pk)
        return "%s (%s)" % (self.name, self.pk)

    class Meta:
	#fields = '__all__'
        abstract=True

class AdjustmentCard(Card):
    '''A card for adding an arbitrary value to a quote/invoice'''
    # current status of the card
    status = models.CharField(max_length=100,choices=Card.STATUS_CHOICES)
    # materials used on the card (using a through model)
    materials = models.ManyToManyField(Material, through='CardQuantity')
    # the calculated internal price of the card, updated by save()
    price_int = models.DecimalField(max_digits=9, decimal_places=3)
    # the calculated external price of the card, updated by save()
    price_ext = models.DecimalField(max_digits=9, decimal_places=3)
    # amount of adjustment for internal clients
    internal_amt = models.DecimalField(max_digits=9, decimal_places=3)
    # amount of adjustment for external clients
    external_amt = models.DecimalField(max_digits=9, decimal_places=3)
    # the cost of the card
    cost_amt = models.DecimalField(max_digits=9, decimal_places=3)

    def _get_price_int(self):
        """calculates the price of the product"""
        price = 0

        price += self.internal_amt

        q = CardQuantity.objects.filter(adjustment = self).\
                filter(job = None)

        for each in q:
            price += each.price_int

        return price

    def _get_price_ext(self):
        """calculates the price of the product"""
        price = 0

        price += self.external_amt

        q = CardQuantity.objects.filter(adjustment = self).\
                filter(job = None)

        for each in q:
            price += each.price_ext

        return price

    def _get_cost(self):
        """
        calculates the cost of producing the product
        (not including labor)
        """
        cost = 0

        cost += self.cost_amt

        q = CardQuantity.objects.filter(adjustment = self) \
                .filter(job=None)

        for each in q:
            cost += each.cost

        return cost

    def update(self):
        '''updates the cached info'''
        self.price_int  = self._get_price_int()
        self.price_ext  = self._get_price_ext()
        self.cost       = self._get_cost()
        self.waste_cost = self._get_waste()

    def save(self, *args, **kwargs):
        '''saves the object'''
        self.update()
        super(ServiceCard,self).save(*args, **kwargs)

        q = CardQuantity.objects.filter(adjustment=self)\
                .exclude(qtype=CardQuantity.ADJUSTMENT)

        for each in q:
            each.save()

    def get_absolute_url(self):
        return '#'


class ServiceCard(Card):
    '''A service card, for services'''
    # the current status of the card
    status = models.CharField(max_length=100,choices=Card.STATUS_CHOICES)
    # adjustments added to the card
    adjustments = models.ManyToManyField(AdjustmentCard,
                                         through='CardQuantity')
    price_int = models.DecimalField(max_digits=9, decimal_places=3)
    # the internal price of the card, updated by save()
    price_ext = models.DecimalField(max_digits=9, decimal_places=3)
    # the external price of the card, updated by save()
    internal_rate = models.DecimalField(max_digits=9, decimal_places=3)
    # the internal (per hour) rate of the card
    external_rate = models.DecimalField(max_digits=9, decimal_places=3)
    # the external (per hour) rate of the card
    cost_rate = models.DecimalField(max_digits=9, decimal_places=3)

    def _get_price_int(self):
        """calculates the price of the product"""
        price = 0

        price += self.internal_rate

        q = CardQuantity.objects.filter(service = self).\
                filter(job = None)

        for each in q:
            price += each.price_int

        return price

    def _get_price_ext(self):
        """calculates the price of the product"""
        price = 0

        price += self.external_rate

        q = CardQuantity.objects.filter(service = self).\
                filter(job = None)

        for each in q:
            price += each.price_ext

        return price

    def _get_cost(self):
        """
        calculates the cost of producing the product
        (not including labor)
        """
        cost = 0

        cost += self.cost_rate

        q = CardQuantity.objects.filter(service = self) \
                .filter(job=None)

        for each in q:
            cost += each.cost

        return cost

    def update(self):
        '''updates the cached info'''
        self.price_int = self._get_price_int()
        self.price_ext = self._get_price_ext()
        self.cost = self._get_cost()
        self.waste_cost = self._get_waste()

    def save(self, *args, **kwargs):
        '''saves the object'''
        self.update()
        super(ServiceCard,self).save(*args, **kwargs)

        q = CardQuantity.objects.filter(service=self)\
                .exclude(qtype=CardQuantity.SERVICE)

        for each in q:
            each.save()

    def get_absolute_url(self):
        return '#'


class ProductCard(Card):
    """Defines a card that contains the product information.
    """
    # Production Status Choices
    STATUS_CHOICES = Card.STATUS_CHOICES + (
            (Card.QUOTE, Card.QUOTE),
            (Card.DESIGNING, Card.DESIGNING),
            (Card.OUTSOURCED, Card.OUTSOURCED),
            (Card.READY_FOR_PICKUP, Card.READY_FOR_PICKUP),# note the ,
            )
    # name of the product (depreciated: replaced by Card.name)
    product_name = models.CharField(max_length=255,default="", blank=True,
                                    null=True)
    # current status of the card
    status = models.CharField(max_length=100,choices=STATUS_CHOICES)
    # materials added to the card
    materials = models.ManyToManyField(Material, through='CardQuantity')
    # service cards added to the card
    services = models.ManyToManyField(ServiceCard, through='CardQuantity')
    # adjustment cards added to the card
    adjustments = models.ManyToManyField(AdjustmentCard,
                    through='CardQuantity')
    # the internal price of the card
    price_int = models.DecimalField(max_digits=9, decimal_places=3)
    # the external price of the card
    price_ext = models.DecimalField(max_digits=9, decimal_places=3)

    def _get_price_int(self):
        """calculates the price of the product"""
        price = 0

        q = CardQuantity.objects.filter(product = self).\
                filter(job_card = None)

        for each in q:
            price += float(each.price_int)

        return price

    def _get_price_ext(self):
        """calculates the price of the product"""
        price = 0

        q = CardQuantity.objects.filter(product = self).\
                filter(job_card = None)

        for each in q:
            price += float(each.price_ext)

        return price

    def _get_cost(self):
        """
        calculates the cost of producing the product
        (not including labor)
        """
        cost = 0

        q = CardQuantity.objects.filter(product = self) \
                .filter(job_card=None)

        for each in q:
            cost += float(each.cost)

        return cost

    def update(self):
        '''updates the cached info'''
        self.price_int = self._get_price_int()
        self.price_ext = self._get_price_ext()
        self.cost = self._get_cost()
        self.waste_cost = self._get_waste()

    def save(self, *args, **kwargs):
        '''saves the object'''
        self.update()
        super(ProductCard,self).save(*args, **kwargs)

        q = CardQuantity.objects.filter(product=self)\
                .filter(qtype=CardQuantity.PRODUCT)

        for each in q:
            try:
                each.job_card.save()
            except Exception as e:
                print "ProductCard.save() for each job: %s" % e

    def __unicode__(self):
        return super(ProductCard,self).__unicode__()

    def get_absolute_url(self):
        return reverse('cards.views.product_detail',args=[str(self.id)])

    def job_list(self):
        q = CardQuantity.objects.filter(product=self).filter(qtype=CardQuantity.PRODUCT)
        jstring = ''
        for each in q:
            jstring = jstring + "<a href='/admin/cards/jobcard/%s'>%s</a><br/>" % (each.job_card.job_number, each.job_card)
        return jstring
    job_list.allow_tags = True

    def contact(self):
        q = CardQuantity.objects.filter(product=self).filter(qtype=CardQuantity.PRODUCT)
        jstring = ''
        for each in q:
            jstring = jstring + "%s<br/>" % (each.job_card.contact)
        return jstring
    contact.allow_tags = True

class JobCard(Card):
    """Defines a card that contains the billing information for an order.
    """
    # Status Choices
    STATUS_CHOICES = Card.STATUS_CHOICES + (
            (Card.QUOTE, 'quote'), # note the ,
            )
    # current status of the card
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    # name of the job (depreciated: replaced with Card.name)
    job_name = models.CharField(max_length=255,null=True,blank=True)
    # how the client indicates they will be paying
    payment_type = models.CharField(max_length=100,
                                    choices=PaymentEvent.PAYMENT_EVENT_TYPE)
    # primary key for the JobCard table
    job_number = models.AutoField(primary_key=True)
    # the primary contact for the job
    contact = models.ForeignKey(Contact, related_name='job')
    # where the job originated from (marketing effort, etc)
    job_roi = models.ForeignKey(JobROI,related_name='job',blank=True,null=True)
    # when the client was last contacted
    client_last_contacted = models.DateField(blank=True, null=True)
    # the pricing level the job is billed at
    price_level = models.CharField(max_length=3,
                                   choices = Contact.PRICE_LEVEL_CHOICES)
    # the price of the job, recalculated by save()
    price = models.DecimalField(max_digits=9,decimal_places=3)
    # override the price listed for this job overall. Default False!
    price_override = models.BooleanField(default=False)
    # if an invoice has been created for the job
    billed = models.BooleanField(default=False)
    # when an invoice was created for the job
    invoice_date = models.DateTimeField(blank=True, null=True)
    # who will be paying for the job
    billing_contact = models.ForeignKey(Contact, related_name='billing')
    # the account number to be charged for IDO payments
    dept_chartstring = models.CharField(max_length=50, blank=True, null=True)

    # cards added to the job
    products = models.ManyToManyField(ProductCard,
                                      through='CardQuantity')
    services = models.ManyToManyField(ServiceCard,
                                      through='CardQuantity')
    adjustments = models.ManyToManyField(AdjustmentCard,
                                         through='CardQuantity')

    # notes for the job (depreciated: use Card.prod_notes or Card.client_notes)
    job_notes = models.TextField(blank=True,null=True)

    def _get_time_in_scope(self):
        '''returns the datetime invoiced - datetime created'''
        return self.invoice_date - self.created_date

    time_in_scope = property(_get_time_in_scope)


    def lock_price(self):
        """ Enables the history lock to preserve the price on each CardQuantity
        """
        q = CardQuantity.objects.filter(job_card=self)
        for each in q:
            each.lock_price()

    def _get_price_int(self):
        """Calculates the internal price of a job"""
        price = 0
        q = CardQuantity.objects.filter(job_card=self)

        for each in q:
            price += float(each.price_int)

        return price

    def _get_price_ext(self):
        """Calculates the internal price of a job"""
        price = 0
        q = CardQuantity.objects.filter(job_card=self)

        for each in q:
            price += float(each.price_ext)

        return price

    def _get_waste(self):
        """calculated the cost of production """
        waste = 0
        q = CardQuantity.objects.filter(job_card=self)

        for each in q:
            waste += float(each.waste_cost) + \
                    float(each.item.waste_cost)

        return waste

    def _get_cost(self):
        """calculated the cost of production """
        cost = 0
        q = CardQuantity.objects.filter(job_card=self)
        for each in q:
            cost += float(each.cost)
        return cost + self._get_waste()

    def _get_next_duedate(self):
        '''Gets the next due date from the associated products
        depreciated: use manual entry instead
        '''
        date = self.due_date

        if self.pk and self.products.count() > 0:
            for each in self.products.all():
                if not date:
                    date = each.due_date
                else:
                    if each.due_date < date:
                        date = each.due_date

        return date

    def update(self):
        '''updates the stored price, cost and waste cost fields'''
        # Price
        if not self.price_override:
            if self.price_level == Contact.INTERNAL:
                self.price = self._get_price_int()
            elif self.price_level == Contact.EXTERNAL:
                self.price = self._get_price_ext()
            else:
                raise NotImplementedError, 'price level not defined'

        # Waste
        self.waste_cost = self._get_waste()

        # Cost
        if self.billable:
            self.cost = self._get_cost()
        else:
            self.cost = 0.0

        # Due Date
        #self.due_date = self._get_next_duedate()

    def archive_validate(self):
        '''verifies the card has the required fields to be archived'''
        valid = True
        messages = []

        if self.payment_type == PaymentEvent.IDO:
            if len(self.dept_chartstring) < CHARTSTRING_LEN:
                valid = False
                messages.append("Missing Chartfield String")
            if self.dept_chartstring.find('xxx') < 0:
                valid = False
                messages.append("Spending Category not found (XXXX -> 7015)")

        return valid, messages

    def archive(self):
        '''archived the card'''
        # Lock the price on the associated items
        q = CardQuantity.objects.filter(job_card=self)

        for each in q:
            each.lock_price()

        super(JobCard, self).archive()

    def unarchive(self):
        '''unarchive the card'''
        q = CardQuantity.objects.filter(job_card=self)
        for each in q:
            each.unlock_price()

        super(JobCard, self).unarchive()

    def clean(self, *args, **kwargs):
        '''define custom validation'''
        from django.core.exceptions import ValidationError

        if self.status == Card.FINISHED and self.billed == False:
            raise ValidationError(
                'Job cannot be marked "finished" until it has been invoiced.')
        if self.status == Card.FINISHED:
            qnts = CardQuantity.objects.filter(job_card=self)
            for q in qnts:
                if q.item.thumbnail == "":
                    message = 'Job cannot be marked "%s" ' % Card.FINISHED + \
                              'until all items have thumbnails. Fix: %s'%q.item
                    raise ValidationError(message)
                if q.qtype == CardQuantity.MATERIAL and \
                        (q.waste_notes == "" or q.waste_notes == None):
                    raise ValidationError(
                        'Job cannot be marked "%s" ' % Card.FINISHED +\
                        'until all items have waste entered. Fix: %s %s' % (q.item, q))

        super(JobCard, self).clean(*args,**kwargs)

    @receiver(pre_save, sender=Material)
    def lock_prices(sender, **kwargs):
        # this should trigger a history lock in cards_cardquantity
        # when a Material updates its price. should find
        # existing jobs/products with materials
        products = CardQuantity.objects.filter(material=kwargs['instance'],qtype=CardQuantity.MATERIAL).exclude(history_lock=1)

        for p in products:
            jobs = CardQuantity.objects.filter(product=p.product,qtype=CardQuantity.PRODUCT,\
                    job_card__status__in=[Card.READY_FOR_PICKUP,Card.FINISHED,Card.CANCELLED])

            for j in jobs:
                jprods = CardQuantity.objects.filter(job_card=j.job_card,qtype=CardQuantity.PRODUCT)

                for jp in jprods:
                    materials = CardQuantity.objects.filter(product=jp.product,qtype=CardQuantity.MATERIAL)
                    for m in materials:
                        mtemp = CardQuantity(id=m.id, history_lock=1, locked_price_int=m.price_int, locked_price_ext=m.price_ext, locked_cost=m.cost,\
                                material_id=m.material_id, product_id=m.product_id, job_card_id=m.job_card_id,\
                                width=m.width, height=m.height, waste_units=m.waste_units, waste_notes=m.waste_notes,\
                                qtype=m.qtype, service_id=m.service_id, adjustment_id=m.adjustment_id, units=m.units)

                        mtemp.save()

                    temp = CardQuantity(id=jp.id, history_lock=1, locked_price_int=jp.price_int,\
                            locked_price_ext=jp.price_ext, locked_cost=jp.cost, units=jp.units,\
                            material_id=jp.material_id, product_id=jp.product_id, job_card_id=jp.job_card_id,\
                            width=jp.width, height=jp.height, waste_units=jp.waste_units, waste_notes=jp.waste_notes,\
                            qtype=jp.qtype, service_id=jp.service_id, adjustment_id=jp.adjustment_id)
                    temp.save()

    @receiver(post_save, sender=Material)
    def propagate_prices(sender, **kwargs):
        # this should be triggered when a change happens to a Material
        # it should find jobs associated and limited by the job's status
        # and then the products associated to that job
        products = CardQuantity.objects.filter(material=kwargs['instance'],qtype=CardQuantity.MATERIAL)

        for p in products:
            jobs = CardQuantity.objects.filter(product=p.product,qtype=CardQuantity.PRODUCT,\
                    job_card__archived=False).exclude(job_card__status__in=[Card.READY_FOR_PICKUP,Card.FINISHED,Card.CANCELLED])

            for j in jobs:
                #print j.job_card
                jprods = CardQuantity.objects.filter(job_card=j.job_card,qtype=CardQuantity.PRODUCT)

                for jp in jprods:
                    #print jp.product
                    jp.product.save()

                j.job_card.update()
                j.job_card.save()

    def __unicode__(self):
        if self.order_number:
            return "%s PO#%s (#%s)" % (self.name, self.order_number,
                    self.job_number)
        return "%s (#%s)" % (self.name, self.job_number)

    @property
    def sorted_product_date_set(self):
        '''returns the products sorted by due date'''
        return self.products.all().order_by('due_date')

    def save(self, *args, **kwargs):
        '''saves the object (and stores the next due date)'''
        self.update()

        super(JobCard, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cards.views.job_details',self.job_number)


class DesignCard(Card):
    """defines a design card to track design/copy labor
    depreciated: use service card instead
    """
    # Design Status Choices
    DESIGN      = 'design'
    REVISION    = 'revision'
    APPROVED    = 'approved'
    PROVIDED    = 'provided'
    DESIGN_STATUS_CHOICES = (
            (DESIGN,    'designing'),
            (REVISION,  'revising'),
            (APPROVED,  'approved'),
            (PROVIDED,  'provided')
            )

    product         = models.ForeignKey(ProductCard)
    #thumbnail       = models.ImageField(upload_to='design', blank=True)
    design_status   = models.CharField(max_length=10,
                            choices=DESIGN_STATUS_CHOICES)
    super_approval  = models.ForeignKey(Employee, related_name='+', \
                            null=True, blank=True)
    super_date      = models.DateField(blank=True, null=True)
    client_approval = models.CharField(max_length=255, \
                            null=True, blank=True)
    client_date     = models.DateField(blank=True, null=True)
    writer_approval = models.ForeignKey(Employee, related_name='+', \
                            null=True, blank=True)
    writer_date     = models.DateField(blank=True, null=True)
    design_notes    = models.TextField(blank=True, null=True)

# =THROUGH models

class CardQuantity(models.Model):
    """
    Defines an intermediary model that connects each material
    used in a product to a quantity.

    Requires:
        ProductCards
        Material
    """
    MATERIAL = 'material'
    PRODUCT = 'product'
    SERVICE = 'service'
    ADJUSTMENT = 'adjustment'
    TYPE_CHOICES = (
            (MATERIAL, 'material'),
            (PRODUCT, 'product'),
            (SERVICE, 'service'),
            (ADJUSTMENT, 'adjustment')
            )

    # the type of card this described the quantity of
    qtype       = models.CharField(max_length=50, choices=TYPE_CHOICES,
                                   null=True)
    # the cards attached to this quantity object
    # their should be exactly two (of different types) while this is in use
    material = models.ForeignKey(Material, null=True, blank=True)
    product = models.ForeignKey(ProductCard, null=True, blank=True)
    service = models.ForeignKey(ServiceCard, null=True, blank=True)
    adjustment = models.ForeignKey(AdjustmentCard, null=True, blank=True)
    job_card = models.ForeignKey(JobCard, null=True, blank=True)

    # quantity of the described object
    units = models.DecimalField(max_digits=9, decimal_places=3)
    # width (used for sqft calculations if applicable)
    width = models.DecimalField(max_digits=9, decimal_places=3,blank=True,
                                default=0)
    # height (used for sqft calculations if applicable)
    height = models.DecimalField(max_digits=9, decimal_places=3, blank=True,
                                 default=0)
    # number of units of waste for this quantity
    waste_units = models.DecimalField(max_digits=9,decimal_places=3,blank=True,
                                       null=True)
    # an explanation of why/how there was waste
    waste_notes = models.TextField(blank=True, null=True)
    # if the cached cost and price values should be used
    history_lock = models.BooleanField(default=False)
    # cache of the current internal price value for archiving
    locked_price_int = models.DecimalField(max_digits=9, decimal_places=3,
                                           default=0)
    # cache of the current external price value for archiving
    locked_price_ext = models.DecimalField(max_digits=9, decimal_places=3,
                                           default=0)
    # cache of the current cost value for archiving
    locked_cost = models.DecimalField(max_digits=9, decimal_places=3,
                                      default=0)


    def _get_square_ft(self):
        """
        calculates the square footage, if applicable
        """
        if self.material.unit == Material.SQFT:
            return (self.width/settings.IN_PER_FT) * \
                    (self.height/settings.IN_PER_FT)
        else:
            return 1

    sqft = property(_get_square_ft)

    def _get_price_int(self):
        """
        does the heavy lifting for price calculations.
        calculates the # of units and multiplies it by the
        unit price.

        Contains duplicate code from _get_price_ext(self).
        """
        price_int = 0.0
        if not self.history_lock:
            if self.qtype == self.MATERIAL and self.material:
                price_int = self.sqft * self.material.unit_price_int * \
                        self.units

            elif self.qtype == self.PRODUCT and self.product:
                price_int = self.product.price_int * self.units

            elif self.qtype == self.SERVICE and self.service:
                price_int = self.service.price_int * self.units

            elif self.qtype == self.ADJUSTMENT and self.adjustment:
                price_int = self.adjustment.price_int * self.units
        else:
            price_int = self.locked_price_int

        return price_int

    def _get_price_ext(self):
        """
        does the heavy lifting for price calculations.
        calculates the # of units and multiplies it by the
        unit price.

        Contains duplicate code from _get_price_ext(self).
        """
        price_ext = 0.0
        if not self.history_lock:
            if self.qtype == self.MATERIAL and self.material:
                price_ext = self.sqft * self.material.unit_price_ext * \
                        self.units

            elif self.qtype == self.PRODUCT and self.product:
                price_ext = self.product.price_ext * self.units

            elif self.qtype == self.SERVICE and self.service:
                price_ext = self.service.price_ext * self.units

            elif self.qtype == self.ADJUSTMENT and self.adjustment:
                price_ext = self.adjustment.price_ext * self.units
        else:
            price_ext = self.locked_price_ext

        return price_ext

    price_int = property(_get_price_int)
    price_ext = property(_get_price_ext)

    def _get_basic_cost(self,num_units):
        """
        Calculates the base cost, based on the units passed in
        """
        cost = 0.0
        if not self.history_lock:
            if self.qtype == self.MATERIAL and self.material:
                cost = self.sqft * self.material.unit_cost * num_units
                if self.material.category == Material.ROLAND_MATERIALS:
                    cost += self.sqft * num_units * settings.ROLAND_INK

                elif self.material.category == Material.HP_MATERIALS:
                    cost += self.sqft * num_units * settings.HP_INK

                elif self.material.category == Material.DIGITAL_MATERIALS:
                    cost += num_units * settings.DIGITAL_INK

            elif self.qtype == self.PRODUCT and self.product:
                try:
                    cost = Decimal(self.product.cost) * num_units
                except TypeError:
                    pass

            elif self.qtype == self.SERVICE and self.service:
                cost = self.service.cost * num_units

            elif self.qtype == self.ADJUSTMENT and self.adjustment:
                cost = self.adjustment.cost * num_units
        else:
            cost = self.locked_cost

        return cost

    def _get_waste(self):
        """
        Calculates the waste
        """
        units = self.waste_units
        if units == None:
            units = 0

        waste = self._get_basic_cost(num_units=units)

        return waste

    waste_cost = property(_get_waste)

    def _get_cost(self):
        """
        Calculates the cost of production (not including labor)
        Includes waste.
        """
        cost = 0
        if not self.history_lock:
            cost = self._get_basic_cost(num_units = self.units)
        else:
            cost = self.locked_cost

        return cost

    cost = property(_get_cost)

    def lock_price(self):
        """
        Saves the price and cost to the locked fields.
        """
        self.history_lock = True

        self.price_lock_int = self._get_price_int()

        self.price_lock_ext = self._get_price_ext()

        self.locked_cost = self._get_cost()

    def _get_item(self):
        if self.qtype == self.MATERIAL:
            return self.material
        elif self.qtype == self.PRODUCT:
            return self.product
        elif self.qtype == self.SERVICE:
            return self.service
        elif self.qtype == self.ADJUSTMENT:
            return self.adjustment
        else:
            return self

    item = property(_get_item)

    def _name(self):
        if self.qtype == self.MATERIAL:
            string = "%s (%s)" % (self.material.product_name,
                    self.material.description)
            return string
        elif self.qtype == self.PRODUCT:
            return self.product.name
        elif self.qtype == self.SERVICE:
            return self.service.name
        elif self.qtype == self.ADJUSTMENT:
            return self.adjustment.name
        else:
            return self

    name = property(_name)


    def __unicode__(self):
        if self.material and self.material.unit == Material.SQFT:
            return "Material: %s at (%s\" x %s\")" % (self.material,
                    self.width, self.height)
        if self.material:
            return "Material: %s" % (self.material)
        if self.product:
            return "Product %s" % (self.product.product_name)
        return "CardQuantity: %s" % (self.pk)


# =MODEL_FORMS
"""
Model forms define user interactive elements that
Django's form factories can use to generate the
HTML and server side back end for forms.

The following definitions get used in cards.views
"""

class CardForm(ModelForm):
    '''Creates the base form for cards'''
    due_date = forms.DateField(widget = \
            forms.TextInput(attrs={'class':'datepicker'}) )
    prod_notes = forms.CharField(widget =\
            forms.Textarea(attrs={'rows':'2'}), required=False)
    approved_on = forms.DateField(widget = \
            forms.TextInput(attrs={'class':'datepicker'}), required=False)
    assigneduser= forms.ModelChoiceField(
            Employee.objects.filter(active=True).order_by('last_name','first_name'))
    class Meta:
        exclude = ('cost', 'waste_cost', 'billable', 'archived','created_user',
                   'updated_user','admin_approved','admin_approved_user',
                   'admin_approved_date',)

class ProductForm(CardForm):
    """
    Creates a form based on the model indicated.
    Lets django do all the work
    """
    excludejobs = ['finished','cancelled','on hold']
    job = forms.ModelChoiceField(
            JobCard.objects.filter(billed=False).exclude(status=excludejobs).order_by('-job_number'),
            required=False)

    class Meta:
        model = ProductCard
        exclude= CardForm.Meta().exclude + \
                ('materials','services','adjustments','price_int',
                 'price_ext','name',#)
                 'product_name','designer','name',)

class ServiceForm(CardForm):
    """
    Creates a form based on the model indicated.
    Lets django do all the work
    """
    job = forms.ModelChoiceField(JobCard.objects.filter(billed=False))
    class Meta:
        model = ProductCard
        exclude= CardForm.Meta().exclude + \
                ('materials','services','adjustments','price_int',
                 'price_ext','name',#)
                 'product_name','designer',)

class AdjustmentForm(CardForm):
    """
    Creates a form based on the model indicated.
    Lets django do all the work
    """
    job = forms.ModelChoiceField(JobCard.objects.filter(billed=False))
    class Meta:
        model = ProductCard
        exclude= CardForm.Meta().exclude + \
                ('materials','services','adjustments','price_int',
                 'price_ext','name',#)
                 'product_name','designer',)

class MaterialCardQuantityForm(ModelForm):
    """
    Creates a form based on the model.
    Excludes JobCard on CardQuantity model.
    Used on New and Edit Product pages.
    """
    def __init__(self, *args, **kwargs):
        super(MaterialCardQuantityForm, self).__init__(*args, **kwargs)
        self.fields['material'].required=True
        #self.fields['qtype'].initial='material'

    material = forms.ModelChoiceField(Material.objects\
            .order_by('product_name'))
    units = forms.DecimalField( widget =\
            forms.TextInput(attrs={'class':'span1'}) )
    width = forms.DecimalField( widget =\
            forms.TextInput(attrs={'class':'span1'}), required=False,
            initial="0")
    height= forms.DecimalField( widget =\
            forms.TextInput(attrs={'class':'span1'}), required=False,
            initial="0")
    waste_units = forms.DecimalField( widget =\
            forms.TextInput(attrs={'class':'span1'}), required=False)
    waste_notes = forms.CharField( widget = \
            forms.Textarea(attrs={'rows':'2'}), required=False)

    qtype   = forms.CharField(widget=forms.HiddenInput(),
                initial = CardQuantity.MATERIAL)

    class Meta:
        model = CardQuantity
        exclude = ('job_card','history_lock',\
                   'locked_price_int','locked_price_ext',\
                   'locked_cost','service','adjustment')

class JobForm(CardForm):
    """
    Creates a form based on the indicated model.
    """
    contact = forms.ModelChoiceField(Contact.objects.order_by('first_name'))
    billing_contact = forms.ModelChoiceField(Contact.objects.\
            order_by('first_name'))
    client_notes = forms.CharField(widget = \
            forms.Textarea(attrs={'rows':'2'}),required=False)
    due_date = forms.DateField( widget = \
            forms.TextInput(attrs={'class':'datepicker'}),required=False)
    client_last_contacted = forms.DateField( widget = \
            forms.TextInput(attrs={'class':'datepicker'}),required=False)
    job_roi  = forms.ModelChoiceField(JobROI.objects.filter(active=True))
    class Meta:
        model = JobCard
        exclude = CardForm.Meta().exclude + \
                ('products','billed','invoice_date','services','adjustments',#)
                 'job_notes','price','job_name','approved_date','qtype',
                 'material','product','service','adjustment')
        fields =  ('name','order_number','status','due_date','assigneduser',
                   'attention','prod_notes','client_notes','contact',
                   'client_last_contacted','billing_contact','payment_type',
                   'price_level','approved_by','approved_on','dept_chartstring',
                   'job_roi')


class ProductCardQuantityForm(ModelForm):
    """
    Creates a form based on the indicated model.
    removed the "Materials" column when editing
    the JobCard.
    """
    product=forms.ModelChoiceField(ProductCard.objects.all(),
            widget=\
            forms.Select(attrs={'readonly':'readonly'}))
    units = forms.DecimalField( widget =\
            forms.TextInput(attrs={'class':'span1'}) )
    width = forms.DecimalField( widget =\
            forms.TextInput(attrs={'class':'span1'}), required=False )
    height= forms.DecimalField( widget =\
            forms.TextInput(attrs={'class':'span1'}), required=False )
    class Meta:
        model = CardQuantity
        exclude = ('material','waste_units', 'waste_notes','history_lock',
                   'locked_price_int','locked_price_ext','locked_cost', 'qtype',
                   'material','service','adjustment')

class DesignForm(ModelForm):
    """
    Creates a form based on the DesignCard model
    """
    super_date = forms.DateField( widget = \
            forms.TextInput(attrs={'class':'datepicker'}),
            required=False)
    client_date = forms.DateField( widget = \
            forms.TextInput(attrs={'class':'datepicker'}),
            required=False)
    writer_date = forms.DateField( widget = \
            forms.TextInput(attrs={'class':'datepicker'}),
            required=False)
    design_notes = forms.CharField( widget = \
            forms.Textarea(attrs={'rows':'2'}),
            required=False)

    class Meta:
        model = DesignCard
	fields = '__all__'

class HistoryLockForm(ModelForm):
    """
    Defines a form for editing history lock info on a
    CardQuantity object.
    """
    class Meta:
        model = CardQuantity
        exclude = ('product','material','job_card',
                   'width','height','history_lock','locked_cost',
                   'waste_units','waste_notes',)

# =FORMS
class JobActionForm(forms.Form):
    """
    creates the form for action stuff on multiple records
    """
    # ACTION CHOICES
    NEW_INV = 'New Invoice'
    CLOSE   = 'Close'

    ACTION_CHOICES = (
            (NEW_INV, 'new invoice'),
            (CLOSE, 'close jobs'),
            )
    action = forms.ChoiceField(choices=ACTION_CHOICES)

class RushFeeForm(forms.Form):
    """
    Creates a form for adding rush fees
    """
    # Fee Choices
    R12 = 'r12'
    R24 = 'r24'
    R48 = 'r48'

    RUSH_FEE_CHOICES = (
            (R12, 'same day'),
            (R24, 'next day'),
            (R48, 'two days'),
            )
    rush_fee_type = forms.ChoiceField(choices=RUSH_FEE_CHOICES)

