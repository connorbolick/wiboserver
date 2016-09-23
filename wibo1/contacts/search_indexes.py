import datetime
from haystack import indexes
from haystack import site
from contacts.models import Contact, Address, Telephone

class ContactIndex(indexes.SearchIndex):
    """
    Defines what Haystack should place in the search index
    """
    text = indexes.CharField(document=True, use_template=True)
    company = indexes.CharField(model_attr='company')
    email = indexes.CharField(model_attr='email')
    student_id = indexes.CharField(model_attr='student_id')

    def get_model(self):
        return Contact

site.register(Contact, ContactIndex)
