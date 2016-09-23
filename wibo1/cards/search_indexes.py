from haystack import indexes
from haystack import site
from cards.models import ProductCard, JobCard

class ProductCardIndex(indexes.SearchIndex):
    """
    Defines what Haystack should place in the search index
    """
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    due_date = indexes.CharField(model_attr='due_date')
    user = indexes.CharField(model_attr='assigneduser')

    def get_model(self):
        return ProductCard

class JobCardIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    user = indexes.CharField(model_attr='assigneduser')
    contact = indexes.CharField(model_attr='contact')
    billing_contact = indexes.CharField(model_attr='billing_contact')

    def get_model(self):
        return JobCard

site.register(ProductCard,ProductCardIndex)
site.register(JobCard,JobCardIndex)
