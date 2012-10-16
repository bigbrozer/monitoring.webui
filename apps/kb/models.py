"""
:mod:`kb.models` -- Models for app kb.
"""

from django.db import models


class Procedure(models.Model):
    """
    Procedure Model.

    Store informations about KB in Dokuwiki.

    - Namespace
    - Rating
    - Comment
    """
    class Meta:
        permissions = (
            ("rate_procedure", "Can rate a procedure"),
        )
