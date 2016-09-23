from django.contrib import admin
from inventory.models import Material

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'description', 'unit', 'unit_price_int', 'unit_price_ext', 'unit_cost', 'category',)
    #list_editable = ('product_name', 'description', 'unit', 'unit_price_int', 'unit_price_ext', 'unit_cost', 'category',)
    list_display_links = ()
    list_filter = ('category',)
    search_fields = ('product_name',)
admin.site.register(Material,MaterialAdmin)
