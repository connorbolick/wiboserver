from cards.models import JobCard, ProductCard, CardQuantity, DesignCard
from django.contrib import admin

def make_archived(modeladmin, request, queryset):
    for obj in queryset:
        obj.archive()
make_archived.short_description = "Archive Jobs"

def make_unarchived(modeladmin, request, queryset):
    for obj in queryset:
        obj.unarchive()
make_unarchived.short_description = "Unarchive Jobs"

class QuantityInline(admin.TabularInline):
    model = CardQuantity
    extra = 1

class DesignCardInline(admin.TabularInline):
    model = DesignCard
    extra = 1

class ProductCardAdmin(admin.ModelAdmin):
    inlines = (QuantityInline,)
    list_display = ('__unicode__', 'job_list', 'status', 'prod_notes', 'client_notes', 'contact', 'assigneduser', 'updated_user', 'updated_date',)
    list_filter = ('status', 'due_date', 'assigneduser', 'jobcard__contact__company', 'jobcard__contact__department',)
    search_fields = ('id', 'product_name', 'jobcard__job_number', 'jobcard__job_name', 'jobcard__contact__first_name', 'jobcard__contact__last_name',)
admin.site.register(ProductCard, ProductCardAdmin)

class JobCardAdmin(admin.ModelAdmin):
    inlines = (QuantityInline,)
    list_display = ('__unicode__', 'status', 'archived', 'prod_notes', 'client_notes', 'contact', 'assigneduser', 'admin_approved_user', 'admin_approved_date', 'updated_user', 'updated_date',)
    list_filter = ('status', 'due_date', 'assigneduser', 'admin_approved_user', 'contact__company', 'contact__department',)
    search_fields = ('job_name', 'job_number', 'contact__first_name', 'contact__last_name',)
    actions = [make_archived, make_unarchived]
admin.site.register(JobCard, JobCardAdmin)
