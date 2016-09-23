from django.conf.urls import patterns, include, url

urlpatterns = patterns('employee.views',
        url(r'^$', 'index', name='employeeindexurl'),
        url(r'^(?P<employee_id>\d+)/$', 'detail', name='employeedetailurl'),
        url(r'^(?P<employee_id>\d+)/(?P<mnum>[0-3]+)/$', 'detail', name='employeedetailurl'),
        url(r'^new/$', 'new_employee', name='newemployeeurl'),
        #url(r'^(?P<employee_id>\d+)/edit/$', 'edit_employee', name='editemployeeurl'),
        url(r'^logtasktime/(?P<job_number>\d+)/(?P<type>\w+)/$', 'logtasktime', name = 'logtasktimeurl'),
)
