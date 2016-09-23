from django.db import models

class ROI(models.Model):
    """
    Defines a client Return on Investment
    """
    name    = models.CharField(max_length=30)
    cost    = models.DecimalField(max_digits=9, decimal_places=3)
    notes   = models.TextField(blank=True, null=True)
    active  = models.BooleanField(default=True)
    start   = models.DateField(null=True,blank=True)
    end     = models.DateField(null=True,blank=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        abstract=True

class ClientROI(ROI):
    pass

class JobROI(ROI):
    pass
