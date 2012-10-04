from django.conf.urls import *

urlpatterns = patterns('apps.kpi.indicateurs',
    url(r'^reporting/$',
        view='indicateurs',
        name='reporting_home'),
)

