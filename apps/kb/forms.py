"""Forms for the app kb."""

# Django imports
from django import forms

# Models imports
from apps.kb.models import Procedure


# Comment form
class ProcedureCommentForm(forms.Form):
    rating = forms.ChoiceField(choices=Procedure.RATING_CHOICES, label='Select rating to apply')
    comment = forms.CharField(widget=forms.Textarea(), label='Enter a comment about your choice')
