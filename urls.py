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
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    (r'^downtime/schedule/$', 'app_downtime.views.schedule'),
)

# Server static content locally (DEBUG mode only)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/django/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
    )
