from roi.models import *
from django.contrib import admin

class ClientROIAdmin(admin.ModelAdmin):
    pass
admin.site.register(ClientROI, ClientROIAdmin)

class JobROIAdmin(admin.ModelAdmin):
    pass
admin.site.register(JobROI, JobROIAdmin)
