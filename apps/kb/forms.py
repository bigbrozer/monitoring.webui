"""Forms for the app kb."""

# Django imports
from django.forms import ModelForm

# Models imports
from apps.kb.models import Procedure


# Create the form class fro Procedure model
class ProcedureForm(ModelForm):
    class Meta:
        model = Procedure