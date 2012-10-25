from django.conf.urls import *

from apps.nagios.views import SatelliteListView

urlpatterns = patterns('apps.nagios.views',
    url(r'^satellites/$',
        SatelliteListView.as_view(),
        name='systems_list'),
    url(r'^satellites/export/$',
        view='get_satellite_list'),
    url(r'^satellites/export/(?P<format>\w+)$',
        view='get_satellite_list',
        name='satellites_export'),
    (r'^passive/$', 'send_passive'),
)