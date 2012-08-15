from django.conf.urls.defaults import *

urlpatterns = patterns('apps.announce.views',
    url(r'^show/$',
        view='show',
        name='announce'),
)

