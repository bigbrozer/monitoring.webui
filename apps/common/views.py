from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.generic import UpdateView

import httpagentparser

from apps.common.forms import UserEditForm

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

