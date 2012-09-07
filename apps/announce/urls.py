from django.conf.urls import *

urlpatterns = patterns('apps.announce.views',
    url(r'^show/$',
        view='show',
        name='announce'),
)

