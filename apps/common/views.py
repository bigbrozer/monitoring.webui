from django.contrib.auth.models import User
from django.views.generic import UpdateView

from apps.common.forms import UserEditForm

class UserEdit(UpdateView):
    """
    CLass based view to show the User profile editing form.
    """
    form_class = UserEditForm
    model = User

    def get_object(self, queryset=None):
        obj = User.objects.get(username=self.request.user)
        return obj

    def get_success_url(self):
        return "/optools/accounts/profile/"
