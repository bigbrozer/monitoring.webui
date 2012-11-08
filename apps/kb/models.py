"""
:mod:`apps.kb.models` -- Models for app kb.
"""

# Django imports
from django.db import models


class Procedure(models.Model):
    """
    Procedure Model.
    Store informations about KB from Dokuwiki to a database.
    """
    class Meta:
        permissions = (
            ("rate_procedure", "Can rate a procedure"),
        )

    # Possible rating choices
    RATING_CHOICES = (
        (-2, 'Bad'),
        (-1, 'Average'),
        ( 0, 'Good'),
        ( 1, 'Excellent'),
    )

    # Table columns
    namespace = models.CharField(max_length=255, unique=True, help_text='Namespace for this procedure.')
    is_written = models.BooleanField(help_text='Is the procedure has been written ?', default=False)
    validated = models.BooleanField(help_text='Is the procedure is validated ?', default=False)
    author = models.CharField(max_length=128, help_text='Last modification author.', blank=True, null=True)
    parents = models.ManyToManyField('Procedure', blank=True, null=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=-1)
    comment = models.TextField(help_text='Comment on the grade you given.', blank=True, null=True)
    last_modified = models.DateTimeField(blank=True, null=True)

    # Instance representation as string
    def __unicode__(self):
        return self.namespace

    def __hash__(self):
        return hash(self.namespace)