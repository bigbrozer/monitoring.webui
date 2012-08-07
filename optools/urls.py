from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from apps.common.views import UserEdit

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Portal
    url(r'^$', 'apps.portal.views.portal_home', name='portal_home'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Login / Logout
    url(r'^accounts/login/$', 'apps.common.views.login', name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^accounts/profile/$', login_required(UserEdit.as_view()), name='user_profile'),

    # Misc
    url(r'^support/browser/$', 'apps.common.views.browser_out_of_date', name='browser_out_of_date'),

    # Applications
    # ============
    #
    # Nagios
    (r'^nagios/satellites/export/$', 'apps.nagios.views.get_satellite_list'),
    (r'^nagios/satellites/export/(?P<format>\w+)$', 'apps.nagios.views.get_satellite_list'),

    # Reporting
    url(r'^reporting/$', 'apps.kpi.indicateurs.indicateurs', name='reporting_home'),
)

