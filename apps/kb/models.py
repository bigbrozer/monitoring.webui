"""
:mod:`kb.models` -- Models for app kb.
"""

# Std imports
from datetime import datetime

# Django imports
from django.db import models
from django.utils.timezone import utc


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

    namespace = models.CharField(max_length=255, unique=True, help_text='Namespace for this procedure.')
    rating = models.IntegerField(choices=RATING_CHOICES, default=-3)
    comment = models.TextField(help_text='Comment on the grade you given.', default="No comment")
    validated = models.BooleanField(help_text='Is the procedure is validated ?', default=False)
    last_modified = models.DateTimeField(default=datetime.now(tz=utc))

    def __unicode__(self):
        return self.namespace
