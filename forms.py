from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class UserEditForm(forms.ModelForm):
    """
    CLass based view to show the User profile editing form.
    """
    success_url = "/optools/accounts/profile"

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

