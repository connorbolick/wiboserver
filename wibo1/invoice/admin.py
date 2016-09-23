from invoice.models import *
from django.contrib import admin

class QuantityInline(admin.TabularInline):
    model = InvQuantity
    extra = 1

class PaymentEventInline(admin.TabularInline):
    model = PaymentEvent
    extra = 0

class InvoiceAdmin(admin.ModelAdmin):
    inlines = (QuantityInline,PaymentEventInline, )
    list_display = ('__unicode__', 'job_list', 'invoice_date', 'invoice_notes', 'billing_contact', 'payment_type', 'paid', 'billed', 'taxable', 'created_user', 'created_date', 'updated_user', 'updated_date',)
    list_filter = ('payment_type', 'paid', 'billed', 'taxable', 'invoice_date', 'billing_contact__company', 'billing_contact__department',)
    search_fields = ('invoice_number', 'billing_contact__first_name', 'billing_contact__last_name', 'job_cards__job_number', 'job_cards__job_name',)
admin.site.register(Invoice, InvoiceAdmin)
class CashInline(PaymentEventInline):
    model = PaymentEventCash
class CheckInline(PaymentEventInline):
    model = PaymentEventCheck
class GiftCardInline(PaymentEventInline):
    model = PaymentEventGiftCard
class IDOInline(PaymentEventInline):
    model = PaymentEventIDO
class WebInline(PaymentEventInline):
    model = PaymentEventWebInvoice

class PaymentEventAdmin(admin.ModelAdmin):
    inlines = (CashInline, CheckInline, GiftCardInline, IDOInline, WebInline,)
    list_display = ('__unicode__', 'invoice_detail', 'job_detail', 'payment_notes', 'billing_contact', 'payment_amount', 'payment_received', 'payment_date', 'payment_user', 'payment_processed',)
    list_filter = ('payment_received', 'payment_date', 'payment_processed', 'invoice__billing_contact__company', 'invoice__billing_contact__department',)
    search_fields = ('id', 'invoice__invoice_number', 'invoice__job_cards__job_number', 'invoice__job_cards__job_name', 'invoice__billing_contact__first_name', 'invoice__billing_contact__last_name',)
admin.site.register(PaymentEvent, PaymentEventAdmin)
