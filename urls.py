from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^optools/', include('optools.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^optools/admin/', include(admin.site.urls)),
    
    # Applications
    # ============
    #
    # Login / Logout
    (r'^optools/login/$', 'django.contrib.auth.views.login'),
    (r'^optools/logout/$', 'django.contrib.auth.views.logout'),
    
    # Downtime
    (r'^optools/downtime/schedule/$', 'optools.apps.downtime.views.schedule'),
    
    # Reporting
    (r'^optools/reporting/stats/$', 'optools.apps.reporting.views.stats'),
    (r'^optools/reporting/stats/data/procedure$', 'optools.apps.reporting.views.procedure_stat_data'),
    (r'^optools/reporting/stats/data/total$', 'optools.apps.reporting.views.total_stat_data'),
    
    # Nagios
    (r'^optools/nagios/satellites/export/$', 'optools.apps.nagios.views.get_satellite_list'),
    (r'^optools/nagios/satellites/export/(?P<format>\w+)$', 'optools.apps.nagios.views.get_satellite_list'),
	(r'^optools/nagios/hosts/search$', 'optools.apps.nagios.views.search_hosts'),
)

