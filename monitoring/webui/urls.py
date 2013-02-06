from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from monitoring.webui.views import UserEdit

urlpatterns = patterns('monitoring.webui.views',
    # Login / Logout
    url(r'^accounts/login/$',
        view='http_login',
        name='login'),
    url(r'^accounts/profile/$',
        view=login_required(UserEdit.as_view()),
        name='user_profile'),

    # Announce
    url(r'^announce/$',
        view='show_announcement',
        name='announce_show'),
    url(r'^announce/(?P<announce_id>\d+)$',
        view='show_announcement',
        name='announce_show_id'),

    # Misc
    url(r'^support/browser/$',
        view='browser_out_of_date',
        name='browser_out_of_date'),

    (r'^maintenance/$',
     TemplateView.as_view(template_name='maintenance.html')),

    (r'^error/404/$', TemplateView.as_view(template_name='404.html')),
    (r'^error/500/$', TemplateView.as_view(template_name='500.html')),
)
