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

# Std imports
import logging

# Django imports
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# Project imports
from monitoring.webui.forms import UserEditForm

# 3rd party
import httpagentparser


logger = logging.getLogger(__name__)

def http_login(request):
    """
    Called after successfull basic HTTP authentication and check if user filled
    his profile.
    """
    logger.debug('Request full path: %s', request.get_full_path())
    redirection = ""
    response = None

    # Should we redirect after login ?
    if request.GET.has_key('next'):
        qr = request.GET.copy()
        next = qr.pop('next')[0]
        remains = qr.urlencode()
        redirection = '{0}?{1}'.format(next, remains)
        logger.debug('Should redirect to: %s', redirection)

    # Find user
    if settings.DEBUG:
        user = User.objects.get(username='test@corp')
        userauth = authenticate(username=user.username, password='test')
        login(request, userauth)
    else:
        user = User.objects.get(username=request.META['REMOTE_USER'])

    operating_system, browser = httpagentparser.simple_detect(request.META.get('HTTP_USER_AGENT'))
    logger.info('%s logged in using browser %s on %s.', user.username, browser, operating_system)

    # Validation
    if not user.is_active or user.username.startswith('0') or not user.username.endswith('@corp'):
        # Be sure that the login will not be used anymore
        user.is_active = False
        user.save()
        logger.info('User name %s is mal-formed !', user.username)
        return HttpResponse('Invalid account. Please use your <strong>normal</strong> user account and append <em>@corp</em>.')

    # Auto fill profile (if possible)
    user.first_name = request.META.get('AUTHENTICATE_GIVENNAME', '')
    user.last_name = request.META.get('AUTHENTICATE_SN', '')
    user.email = request.META.get('AUTHENTICATE_MAIL', '')
    user.save()

    if (user.first_name or user.last_name) and user.email:
        if redirection:
            response = redirect(redirection)
        else:
            response = redirect('index')
    else:
        # Profile is not completed
        logger.info('User %s has not filled his profile.', user.username)
        if redirection:
            response = redirect('%s?redirect=%s' % (reverse('user_profile'), redirection))
        else:
            response = redirect('user_profile')

    return response


class UserEdit(UpdateView):
    """
    Class based view to show the User profile editing form.
    """
    form_class = UserEditForm
    model = User

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(UserEdit, self).get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        obj = User.objects.get(username=self.request.user)
        return obj

    def get_success_url(self):
        try:
            return self.request.GET['redirect']
        except KeyError:
            return reverse("index")


def browser_out_of_date(request):
    """
    Warn user that the browser is not well supported.
    """
    return render(request, "common/browser_not_supported.html", {'title': "Browser out of date"})

def server_error(request):
    """
    Handle 500 error codes.
    """
    return render(request, "500.html", {'title': "Severe error !"})
