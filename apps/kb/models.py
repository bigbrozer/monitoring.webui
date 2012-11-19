"""
:mod:`apps.kb.models` -- Models for app kb.
"""

# Std imports
import os
import logging
import re
from datetime import datetime
from pprint import pformat

# Django imports
from django.utils.encoding import smart_str
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import utc
from django.conf import settings


#===============================================================================
#   ____ _
#  / ___| | __ _ ___ ___  ___  ___
# | |   | |/ _` / __/ __|/ _ \/ __|
# | |___| | (_| \__ \__ \  __/\__ \
#  \____|_|\__,_|___/___/\___||___/
#
#===============================================================================

class Procedure(models.Model):
    """
    Procedure Model.
    Store informations about KB from Dokuwiki to a database.
    """
    logger = logging.getLogger('optools.apps.kb.models.Procedure')
    console = logging.getLogger('debug.kb.models.Procedure')

    namespace_regexp = r'^([a-zA-Z0-9_-]+:*)+$'

    class MetaError(Exception):
        """Raised if error is encountered during meta file parsing."""
        pass

    # Possible rating choices
    RATING_CHOICES = (
        (-2, 'Bad'),
        (-1, 'Average'),
        ( 0, 'Good'),
        ( 1, 'Excellent'),
    )

    # Table columns
    namespace = models.CharField(max_length=255, unique=True, help_text='Namespace for this procedure.', editable=False)
    is_written = models.BooleanField(help_text='Is the procedure has been written ?', default=False, editable=False)
    validated = models.BooleanField(help_text='Is the procedure is validated ?', default=False, editable=False)
    author = models.CharField(max_length=128, help_text='Last modification author.', blank=True, null=True, editable=False)
    parents = models.ManyToManyField('Procedure', help_text='These are the parent procedures.', null=True, editable=False)
    rating = models.IntegerField(choices=RATING_CHOICES, help_text='Rating for this procedure.', default=-1)
    comment = models.TextField(help_text='Comment on the grade you given.', blank=True, null=True)
    last_modified = models.DateTimeField(help_text='Time of the last modification.', blank=True, null=True, editable=False)

    # KB constructor: register a new KB in the database with all details (without performing DB stuff)
    @classmethod
    def register(cls, namespace):
        procedure = cls(namespace=namespace)

        procedure._strip_namespace()
        procedure.update_meta()

        return procedure

    # Saving
    def save(self, *args, **kwargs):
        """Customize saving model method."""
        try:
            # Call validation manually
            self.full_clean()
        except ValidationError as e:
            self.logger.critical('Errors found about Procedure model validation ! Please fix them.')
            for error in e.message_dict['__all__']:
                self.logger.critical('%s', error)
            raise # Forward exception

        self.update_meta()

        # Un-validate the procedure if it has been modified
        try:
            if self.last_modified != Procedure.objects.get(pk=self.id).last_modified:
                self.console.debug('Kb \"%s\" has changed. Un-validate.', self)
                self.validated = False
        except Procedure.DoesNotExist:
            pass

        super(Procedure, self).save(*args, **kwargs)

    # Special KB methods
    def update_meta(self):
        """Update META information about the procedure."""
        # Check if file exist for the procedure
        if os.path.isfile(self.get_filename()):
            self.is_written = True
        else:
            self.is_written = False

        # Update META informations
        self._populate_meta()

    def get_name(self):
        """Get the name for this procedure."""
        return self.namespace.split(':')[-1]

    def get_filename(self):
        """Get the filename for this procedure."""
        return os.path.join(settings.DOKUWIKI_PAGES_DIR, "{}.txt".format(self.namespace.replace(':', '/')))

    def get_changes_filename(self):
        """Get the filename containing changes for this procedure."""
        return os.path.join(settings.DOKUWIKI_META_DIR, "{}.changes".format(self.namespace.replace(':', '/')))

    def get_read_url(self):
        """Get the URL to read the procedure online."""
        return '{}/{}'.format(settings.DOKUWIKI_BASE_URL, self.namespace)

    def get_edit_url(self):
        """Get the URL to edit the procedure online."""
        return '{}/{}?do=edit'.format(settings.DOKUWIKI_BASE_URL, self.namespace)

    def _populate_meta(self):
        """Populate META information about the Kb."""
        try:
            with open(self.get_changes_filename(), 'r') as meta_file:
                last_change = meta_file.readlines()[-1].split('\t')
                self.console.debug("Parsing line:\n%s", pformat(last_change))
                self.last_modified = datetime.fromtimestamp(long(last_change[0]), tz=utc)
                self.author = last_change[4]
        except IOError:
            # Do nothing. No meta information available, procedure may not exist
            self.console.debug('No META information for \"%s\".', self)
            pass
        except ValueError:
            # Can occur if timestamp cannot be converted to datetime or if it is not found
            raise Procedure.MetaError('Error during meta file \"%s\" parsing !' % self.get_changes_filename())

    def _strip_namespace(self):
        """
        Clean and validate namespace.
        """
        if not re.match(Procedure.namespace_regexp, self.namespace):
            raise ValidationError('KB namespace should be of the form %s !' % Procedure.namespace_regexp)

        self.namespace = self.namespace.lower().strip(':')

    def get_parents(self):
        """
        Build the list of parent namespaces for the procedure.

        :return: parent list for procedure ``['app:toto', 'app:toto:tata', '...']``.
        """
        parents_to_build = []
        parents = self.namespace.split(':')[:-1]

        for index, parent in enumerate(parents):
            index += 1
            parents_to_build.append(":".join(parents[:index]))

        return parents_to_build

    def _linkify_parents(self):
        """Make parents relations."""
        for parent_name in self.get_parents():
            try:
                parent_model = Procedure.objects.get(namespace=parent_name)
            except Procedure.DoesNotExist:
                parent_model = Procedure.register(namespace=parent_name)

            self.parents.add(parent_model)

    # Comparaison operators
    def __eq__(self, other):
        if isinstance(other, (str, unicode)):
            return other == self.namespace
        elif isinstance(other, Procedure):
            return self.namespace == other.namespace

        super(Procedure, self).__eq__(other)

    # Misc
    def __str__(self):
        return smart_str(self.namespace)

    def __unicode__(self):
        return self.namespace

    def __hash__(self):
        return hash(self.namespace)
