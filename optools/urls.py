from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Applications
    # ============
    #
    # Nagios
    (r'^nagios/satellites/export/$', 'optools.apps.nagios.views.get_satellite_list'),
    (r'^nagios/satellites/export/(?P<format>\w+)$', 'optools.apps.nagios.views.get_satellite_list'),
    (r'^nagios/hosts/search$', 'optools.apps.nagios.views.search_hosts'),

    # Reporting
    url(r'^reporting/', 'kpi.indicateurs.indicateurs'),
)

