from contacts.models import Contact, Address, Telephone
from django.contrib import admin

class AddressInline(admin.TabularInline):
    model = Address
    extra = 1

class TelephoneInline(admin.TabularInline):
    model = Telephone
    extra = 1

class ContactAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,          {'fields':['first_name','last_name']}),
        ('Contact Information', {'fields':['company','email', \
                'default_price_level','student_id','roi'], \
                'classes':['collapse']}),
    ]
    inlines = [AddressInline, TelephoneInline]

admin.site.register(Contact, ContactAdmin)
