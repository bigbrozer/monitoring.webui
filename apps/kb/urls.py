from django.conf.urls import *

urlpatterns = patterns('apps.kb.views',
    (r'^show/(?P<kb_namespace>([a-zA-Z0-9]+:*)+)$', 'show_kb'),
)