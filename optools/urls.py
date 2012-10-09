from django.conf.urls import *

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
    (r'^nagios/', include('apps.nagios.urls')),

    # KB
    (r'^kb/', include('apps.kb.urls')),
)

