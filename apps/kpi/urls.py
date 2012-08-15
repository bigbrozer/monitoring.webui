from django.conf.urls.defaults import *

urlpatterns = patterns('apps.kpi.indicateurs',
    url(r'^reporting/$',
        view='indicateurs',
        name='reporting_home'),
)

