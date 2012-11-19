from django.conf.urls import *

urlpatterns = patterns('apps.kb.views',
    url(r'^show/(?P<kb_namespace>.*)$', 'show_kb', name='show_kb'),
)