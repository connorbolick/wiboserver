from haystack import indexes, site
from invoice.models import Invoice, PaymentEvent

class InvoiceIndex(indexes.SearchIndex):
    """
    Defines what Haystack should place in the search index
    """
    text = indexes.CharField(document=True, use_template=True)
    payment_type = indexes.CharField(model_attr="payment_type")
    client = indexes.CharField(model_attr='billing_contact')
    invoice_date = indexes.CharField(model_attr='invoice_date')
    
    def get_model(self):
        return Invoice

site.register(Invoice, InvoiceIndex)
