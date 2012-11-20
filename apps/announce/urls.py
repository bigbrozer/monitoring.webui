from django.conf.urls import *

urlpatterns = patterns('apps.announce.views',
    url(r'^show/$',
        view='show',
        name='announce_show'),
    url(r'^show/(?P<announce_id>\d+)$',
        view='show',
        name='announce_show_id'),
)

