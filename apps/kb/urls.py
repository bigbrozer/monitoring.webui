from django.conf.urls import *

urlpatterns = patterns('apps.kb.views',
    (r'^show/(?P<kb_namespace>.*)$', 'show_kb'),
)