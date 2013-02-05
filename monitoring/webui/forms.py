from django import forms
from django.contrib.auth.models import User

class UserEditForm(forms.ModelForm):
    """
    Customize the User profile editing form based on User model.
    """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

