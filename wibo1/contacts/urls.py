from django.conf.urls import patterns, include, url

urlpatterns = patterns('contacts.views',
        url(r'^$',                     'index', name='contactsindexurl'),
        url(r'^(?P<contact_id>\d+)/$', 'detail', name='contactdetailsurl'),
        url(r'^new/$',                 'new_contact', name='newcontacturl'),
        url(r'^(?P<contact_id>\d+)/edit/$','edit_contact', name='editcontacturl'),

)
