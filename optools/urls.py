from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin
    (r'^admin/', include(admin.site.urls)),
    
    # Applications
    # ============
    #
    # Common
    (r'', include('apps.common.urls')),

    # Reporting
    (r'', include('apps.kpi.urls')),

    # Portal
    url(r'^$', 'apps.portal.views.portal_home', name='portal_home'),

    # Announce
    (r'^announce/', include('apps.announce.urls')),

    # Nagios
    (r'^nagios/satellites/export/$', 'apps.nagios.views.get_satellite_list'),
    (r'^nagios/satellites/export/(?P<format>\w+)$', 'apps.nagios.views.get_satellite_list'),
)

