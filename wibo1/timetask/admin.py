from django.contrib import admin
from timetask.models import Timelog

class TimelogAdmin(admin.ModelAdmin):
    list_display = ('employee', 'job', 'type', 'time_in', 'time_out')
    #list_editable = ('product_name', 'description', 'unit', 'unit_price_int', 'unit_price_ext', 'unit_cost', 'category',)
    list_display_links = ()
    list_filter = ('type',)
    search_fields = ('employee__first_name', 'employee__last_name', 'employee__user_name','job__job_number', 'job__job_name',)

admin.site.register(Timelog,TimelogAdmin)
