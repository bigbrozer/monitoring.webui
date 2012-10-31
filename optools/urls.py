from django.conf.urls import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

handler500 = 'apps.common.views.server_error'

urlpatterns = patterns('',
    # Admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    
    # Applications
    # ============
    #
    # Portal
    url(r'^$', 'apps.portal.views.portal_home', name='portal_home'),

    # Common
    (r'', include('apps.common.urls')),

    # Reporting
    (r'', include('apps.kpi.urls')),

    # Announce
    (r'^announce/', include('apps.announce.urls')),

    # Nagios
    (r'^nagios/', include('apps.nagios.urls')),

    # KB
    (r'^kb/', include('apps.kb.urls')),
)

