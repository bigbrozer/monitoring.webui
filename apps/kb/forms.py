"""Forms for the app kb."""

# Django imports
from django import forms

# Models imports
from apps.kb.models import Procedure


SEP_RATING_CHOICES = (
    ('', 'Please select rating'),
    ('', '--------------------'),
)

RATING_CHOICES = SEP_RATING_CHOICES + Procedure.RATING_CHOICES

# Comment form
class ProcedureCommentForm(forms.Form):
    rating = forms.ChoiceField(choices=RATING_CHOICES, label='Select rating to apply')
    comment = forms.CharField(widget=forms.Textarea(), label='Enter a comment about your choice')
