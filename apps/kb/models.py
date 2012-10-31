"""
:mod:`kb.models` -- Models for app kb.
"""

# Django imports
from django.db import models


class Procedure(models.Model):
    """
    Procedure Model.

    Store informations about KB in Dokuwiki.

    - Namespace
    - Rating (grade from -2 to 1)
    - Comment
    """
    class Meta:
        permissions = (
            ("rate_procedure", "Can rate a procedure"),
        )

    RATING_CHOICES = (
        (-2, 'Bad'),
        (-1, 'Average'),
        ( 0, 'Good'),
        ( 1, 'Excellent'),
    )

    namespace = models.CharField(max_length=255, help_text='Namespace for this procedure.')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(help_text='Comment on the grade you given.', blank=True, null=True)
