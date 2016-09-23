from django.db import models

# Create your models here.
class Material(models.Model):
    """
    Class that describe materials
    Key for:
        Quantity
        ProductCard
    """
    # unit choices
    EACH = 'EACH'
    SQFT = 'SQFT'
    LNFT = 'LNFT'
    HOUR = 'HOUR'

    UNIT_CHOICES = (
            (EACH, 'unit'),
            (SQFT, 'square foot'),
            (LNFT, 'linear foot'),
            (HOUR, 'hour')
            )
    # category choices
    ROLAND_MATERIALS    = 'Roland Printer Roll Materials'
    HP_MATERIALS        = 'HP Printer Roll Materials'
    ROLAND_SUPPLIES     = 'Roland Supplies'
    HP_SUPPLIES         = 'HP Supplies'
    DIGITAL_MATERIALS   = 'Digital Print Materials'
    XEROX_SUPPLIES      = 'Xerox WC Supplies'
    RICOH_SUPPLIES      = 'RICOH Supplies'
    BANNER_SUPPLIES     = 'Banner Supplies'
    MOUNTING_SUPPLIES   = 'Mounting Supplies'
    MISC_SUPPLIES       = 'Misc Supplies'
    MISC_MATERIALS      = 'Misc Materials'
    OFFICE_SUPPLIES     = 'Office Supplies'
    CLEANING_SUPPLIES   = 'Cleaning Supplies'
    WIBO_USE            = 'WIBO Use Only'

    CAT_CHOICES = (
        (ROLAND_MATERIALS,     'Roland Printer Roll Materials'),
        (HP_MATERIALS,         'HP Printer Roll Materials'),
        (ROLAND_SUPPLIES,      'Roland Supplies'),
        (HP_SUPPLIES,          'HP Supplies'),
        (DIGITAL_MATERIALS,    'Digital Print Materials'),
        (XEROX_SUPPLIES,       'Xerox WC Supplies'),
        (RICOH_SUPPLIES,       'RICOH Supplies'),
        (BANNER_SUPPLIES,      'Banner Supplies'),
        (MOUNTING_SUPPLIES,    'Mounting Supplies'),
        (MISC_SUPPLIES,        'Misc Supplies'),
        (MISC_MATERIALS,       'Misc Materials'),
        (OFFICE_SUPPLIES,      'Office Supplies'),
        (CLEANING_SUPPLIES,    'Cleaning Supplies'),
        (WIBO_USE,             'WIBO Use Only'),
            )

    product_name    = models.CharField(max_length=255)
    description     = models.CharField(max_length=255)
    unit            = models.CharField(max_length=4,
                            choices=UNIT_CHOICES)
    unit_price_int  = models.DecimalField(max_digits=9, decimal_places=3)
    unit_price_ext  = models.DecimalField(max_digits=9, decimal_places=3)
    unit_cost       = models.DecimalField(max_digits=9, decimal_places=3)
    category        = models.CharField(max_length=50,
                            choices=CAT_CHOICES)

    def __unicode__(self):
        return "%s" % (self.product_name)
''''
    # I actually need to override the save to propagate?
    def save(self, *args, **kwargs):
        super(Material, self).save(*args, **kwargs)

        # pull jobs with associated materials that aren't finished, cancelled, or archived
        products = Material.objects.filter(cardquantity__material=self,cardquantity__qtype='material')

        for p in products:
            jobs = Material.objects.filter(cardquantity__product=p.product,cardquantity__qtype='product',\
                    cardquantity__job_card__archived=False).exclude(cardquantity__job_card__status__in=['cancelled','finished','ready for pickup'])

            for j in jobs:
                j.update()
                j.save()
'''''