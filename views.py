from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import authenticate, login

import httpagentparser

from apps.common.forms import UserEditForm

def http_login(request):
    """
    Called after successfull basic HTTP authentication and check if user filled
    his profile.
    """
    redirection = ""
    user = None

    # Should we redirect after login ?
    if request.GET.has_key('next'):
        redirection = request.GET['next']

    # Find user
    if settings.DEBUG:
        user = User.objects.get(username='test')
        userauth = authenticate(username=user.username, password='test')
        login(request, userauth)
    else:
        user = User.objects.get(username=request.META['REMOTE_USER'])

    # Test if user filled his profile
    if user.first_name and user.last_name and user.email:
        if redirection:
            return redirect(redirection)
        else:
            return redirect('portal_home')
    else:
        if redirection:
            return redirect('%s?redirect=%s' % (reverse('user_profile'), redirection))
        else:
            return redirect('user_profile')

class UserEdit(UpdateView):
    """
    Class based view to show the User profile editing form.
    """
    form_class = UserEditForm
    model = User

    def get_object(self, queryset=None):
        obj = User.objects.get(username=self.request.user)
        return obj

    def get_success_url(self):
        try:
            return self.request.GET['redirect']
        except KeyError:
            return reverse("portal_home")

def browser_out_of_date(request):
    """
    Warn user that the browser is not well supported.
    """
    title = "Browser out of date"

    browser = httpagentparser.detect(request.META['HTTP_USER_AGENT'])['browser']
    if "internet explorer" in browser['name'].lower() and int(browser['version'].split('.')[0]) < 9:
        return render_to_response("common/browser_not_supported.html", locals(), context_instance = RequestContext(request))
    else:
        return redirect('portal_home')

