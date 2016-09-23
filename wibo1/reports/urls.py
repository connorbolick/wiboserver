from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

urlpatterns = patterns('reports.views',
        url(r'^$', TemplateView.as_view(template_name="reports/index.html")),
        url(r'^spar/$', 'spar_report', name='sparreporturl'),
        url(r'^waste/$', 'waste_report', name='wastereporturl'),
        url(r'^material/$', 'material_report', name='materialreporturl'),
        url(r'^inventory/$', 'inventory_report', name='inventoryreporturl'),
        url(r'^audit/$', 'audit_report', name='auditreporturl'),
        url(r'^revenue/$', 'revenue_report', name='revenuereporturl'),
        url(r'^client/$', 'client_report', name='clientreporturl'),
        url(r'^timelog/$', 'time_report', name='timereporturl'),
)
