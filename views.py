from django.contrib.auth.models import User
from django.views.generic import UpdateView

from apps.common.forms import UserEditForm

class UserEdit(UpdateView):
    form_class = UserEditForm
    model = User
    success_url = "/accounts/profile/"

    #def get(self, request, **kwargs):
    #    self.object = User.objects.get(username=self.request.user)
    #    form_class = self.get_form_class()
    #    form = self.get_form(form_class)
    #    context = self.get_context_data(object=self.object, form=form)
    #    return self.render_to_response(context)

    def get_object(self, queryset=None):
        obj = User.objects.get(username=self.request.user)
        return obj

