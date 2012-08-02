from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic import TemplateView

from apps.common.views import UserEdit

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Portal
    (r'^$', TemplateView.as_view(template_name="portal/portal.html")),

    # Login / Logout
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/profile/$', UserEdit.as_view(), name='user_profile'),

    # Applications
    # ============
    #
    # Nagios
    (r'^nagios/satellites/export/$', 'apps.nagios.views.get_satellite_list'),
    (r'^nagios/satellites/export/(?P<format>\w+)$', 'apps.nagios.views.get_satellite_list'),

    # Reporting
    url(r'^reporting/', 'apps.kpi.indicateurs.indicateurs'),
)

