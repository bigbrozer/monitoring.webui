from django.conf.urls import *

urlpatterns = patterns('apps.kb.views',
    (r'^show/(?P<kb_url>([a-zA-Z0-9]+:*)+)$', 'show_kb'),
)