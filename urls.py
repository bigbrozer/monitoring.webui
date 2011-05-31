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
    (r'^admin/', include(admin.site.urls)),
    
    # Applications
    # ============
    #
    # Login / Logout
    (r'^login/$', 'django.contrib.auth.views.login'),
    (r'^logout/$', 'django.contrib.auth.views.logout'),
    
    # Downtime
    (r'^downtime/schedule/$', 'optools.apps.downtime.views.schedule'),
    
    # Reporting
    (r'^reporting/stats/$', 'optools.apps.reporting.views.stats'),
    (r'^reporting/stats/data/alerts$', 'optools.apps.reporting.views.alerts_stat_data'),
    (r'^reporting/stats/data/procedure$', 'optools.apps.reporting.views.procedure_stat_data'),
    (r'^reporting/stats/data/total$', 'optools.apps.reporting.views.total_stat_data'),
    
    # Nagios
    (r'^nagios/satellites/export/$', 'optools.apps.nagios.views.get_satellite_list'),
    (r'^nagios/satellites/export/(?P<format>\w+)$', 'optools.apps.nagios.views.get_satellite_list'),
	(r'^nagios/hosts/search$', 'optools.apps.nagios.views.search_hosts'),
)

# Server static content locally (from dev alptop only ;-))
if settings.DEVMODE:
    urlpatterns += patterns('',
        (r'^static/django/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

