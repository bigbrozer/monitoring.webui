from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.conf import settings

import httpagentparser

from apps.common.forms import UserEditForm

def login(request):
    """
    Called after successfull basic HTTP authentication and check if user filled
    his profile.
    """
    # Find user
    if settings.DEBUG:
        user = User.objects.get(username='besancon@corp')
    else:
        user = User.objects.get(username=request.META['REMOTE_USER'])

    # Test if user filled his profile
    if user.first_name and user.last_name and user.email:
        if request.GET.has_key('next'):
            return redirect(request.GET['next'])
        else:
            return redirect('portal_home')
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

