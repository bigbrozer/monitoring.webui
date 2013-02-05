from django.conf.urls import *
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from views import UserEdit

urlpatterns = patterns('apps.common.views',
    # Login / Logout
    url(r'^accounts/login/$', 'http_login', name='login'),
    url(r'^accounts/profile/$', login_required(UserEdit.as_view()), name='user_profile'),

    # Misc
    url(r'^support/browser/$', 'browser_out_of_date', name='browser_out_of_date'),
    (r'^maintenance/$', TemplateView.as_view(template_name='maintenance.html')),
    (r'^error/404/$', TemplateView.as_view(template_name='404.html')),
    (r'^error/500/$', TemplateView.as_view(template_name='500.html')),
)
