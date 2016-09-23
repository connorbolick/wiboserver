from django.conf.urls import patterns, include, url

urlpatterns = patterns('invoice.views',
        url(r'^$', 'index', name='invoiceindexurl'),
        url(r'^(?P<inv_number>\d+)/$', 'detail', name='invoicedetailurl'),
        url(r'^(?P<inv_number>\d+)/payment/new/$', 'new_payment', name='newpaymenturl'),
        url(r'^(?P<inv_number>\d+)/edit/$', 'edit_invoice', name='editinvoiceurl'),
        url(r'^(?P<inv_number>\d+)/print/$', 'print_invoice', name='printinvoiceurl'),
        url(r'^(?P<inv_number>\d+)/payment/$', 'new_payment', name='invoicepaymenturl'),
        url(r'^new/$', 'new_invoice', name='newinvoiceurl'),
        url(r'^payment/$', 'payment_index', name='paymentindexurl'),
)
