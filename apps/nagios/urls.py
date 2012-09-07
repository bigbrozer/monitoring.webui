from django.conf.urls import *

urlpatterns = patterns('apps.nagios.views',
    (r'^satellites/export/$', 'get_satellite_list'),
    (r'^satellites/export/(?P<format>\w+)$', 'get_satellite_list'),
    (r'^kb/(?P<kb_url>([a-zA-Z0-9]+:*)+)$', 'show_kb'),
)