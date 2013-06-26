# -*- coding: utf-8 -*-
# Copyright (C) Faurecia <http://www.faurecia.com/>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

    # Misc
    url(r'^support/browser/$',
        view='browser_out_of_date',
        name='browser_out_of_date'),

    (r'^maintenance/$',
     TemplateView.as_view(template_name='maintenance.html')),

    (r'^error/404/$', TemplateView.as_view(template_name='404.html')),
    (r'^error/500/$', TemplateView.as_view(template_name='500.html')),
)
