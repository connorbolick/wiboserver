from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

#from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^$", TemplateView.as_view(template_name = "homepage.html")),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r"^admin/", include(admin.site.urls)),

    url(r"^account/", include("account.urls")),

    # url(r"^search/", include("haystack.urls")),

    # WIBO URLs
    url(r'^cards/', include('cards.urls')),
    url(r'^contacts/', include('contacts.urls')),
    url(r'^invoice/', include('invoice.urls')),
    url(r'^employee/',include('employee.urls')),
    url(r'^sapub/request/$', 'wibo.views.sapub_request', name='jobrequeseturl'),
    url(r'^wibo/logout-all-users/$', 'wibo.views.logout_all_users', name='logoutallurl'),
    url(r'^wibo/cardmigrationextra00091/$', 'wibo.views.cards_migration_extras_0009_1', name='cardsmigrationextra0009url'),
    url(r'^wibo/cardmigrationextra00092/$', 'wibo.views.cards_migration_extras_0009_2', name='cardsmigrationextra0009url'),
    url(r'^wibo/cardmigrationextra00093/$', 'wibo.views.cards_migration_extras_0009_3', name='cardsmigrationextra0009url'),
    url(r"^reports/", include('reports.urls')),
    #url(r"^printsmart/$",direct_to_template,{"template":"printsmart_request.html"}, name="printsmarturl"),
    url(r"^printsmart/$", TemplateView.as_view(template_name="printsmart_request.html")),
    url(r'^select2/', include('django_select2.urls')),
    )

urlpatterns += staticfiles_urlpatterns()
