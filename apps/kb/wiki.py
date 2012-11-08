"""
:mod:`apps.kb.wiki` to handle Alert procedures (KB)
"""

# Std lib imports
import os
import re
from datetime import datetime
import logging
from pprint import pformat

# Django imports
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'
from django.conf import settings
from django.utils.timezone import utc

# Models imports
from apps.kb.models import Procedure

# Dokuwiki config
DOKUWIKI_BASE_URL = '/kb' if not settings.DEBUG else 'http://monitoring-dc.app.corp/kb'
DOKUWIKI_PAGES_DIR = '/var/www/kb/data/pages' if not settings.DEBUG else os.path.join(settings.PROJECT_PATH, 'var/pages')
DOKUWIKI_META_DIR = '/var/www/kb/data/meta' if not settings.DEBUG else os.path.join(settings.PROJECT_PATH, 'var/meta')


#===============================================================================
#  _____                    _   _
# | ____|_  _____ ___ _ __ | |_(_) ___  _ __  ___
# |  _| \ \/ / __/ _ \ '_ \| __| |/ _ \| '_ \/ __|
# | |___ >  < (_|  __/ |_) | |_| | (_) | | | \__ \
# |_____/_/\_\___\___| .__/ \__|_|\___/|_| |_|___/
#                    |_|
#===============================================================================
class KbError(Exception):
    """
    Base class for all exceptions related to KB.
    """

    def __init__(self, message, *args, **kwargs):
        self.message = message
        super(KbError, self).__init__(self.message)

    def __str__(self):
        return self.message


class KbUrlMalformed(KbError):
    """
    Raised when given procedure URL does not validate.
    """
    def __init__(self, kb, regexp):
        self.message = 'KB namespace \"%s\" is malformed. Must be \"%s\" !' % (kb, regexp)
        super(KbUrlMalformed, self).__init__(self.message)


#===============================================================================
#   ____ _
#  / ___| | __ _ ___ ___  ___  ___
# | |   | |/ _` / __/ __|/ _ \/ __|
# | |___| | (_| \__ \__ \  __/\__ \
#  \____|_|\__,_|___/___/\___||___/

#===============================================================================
class Kb(object):
    """
    This class init a Kb and store information such as: name, namespace, last modified timestamp, parents kb, etc...
    """
    logger = logging.getLogger('optools.apps.kb.wiki.Kb')

    namespace_valid_regexp = r'^([a-zA-Z0-9_-]+:*)+$'
    db_fields = (
        'namespace',
        'is_written',
    )
    db_meta_fields = (
        'last_modified',
        'author',
    )

    def __init__(self, namespace):
        # Validate namespace before proceeding
        if not re.match(Kb.namespace_valid_regexp, namespace):
            raise KbUrlMalformed(namespace, Kb.namespace_valid_regexp)

        # Attributes
        self.namespace = namespace.lower().strip(':')
        self.name = self.namespace.split(':')[-1]
        self.filename = os.path.join(DOKUWIKI_PAGES_DIR, "{}.txt".format(self.namespace.replace(':', '/')))
        self.changes_filename = os.path.join(DOKUWIKI_META_DIR, "{}.changes".format(self.namespace.replace(':', '/')))
        self.is_written = False
        self.META = {
            'read_url': '{}/{}'.format(DOKUWIKI_BASE_URL, self.namespace),
            'edit_url': '{}/{}?do=edit'.format(DOKUWIKI_BASE_URL, self.namespace),
        }
        self.parents = []

        if os.path.isfile(self.filename):
            self.is_written = True

        # Building parents and META
        self._populate_meta()
        self._build_parents_list()
        self.logger.debug('%s attributes:\n%s', repr(self), pformat(self.__dict__))

    def _build_parents_list(self):
        parents_pages = self.namespace.split(':')[:-1]
        for index, parent in enumerate(parents_pages):
            index += 1
            self.parents.append(":".join(parents_pages[:index]))

    def _populate_meta(self):
        """Populate META information about the Kb."""
        try:
            with open(self.changes_filename, 'r') as meta_file:
                last_change = meta_file.readlines()[-1].split('\t')
                self.logger.debug("Parsing line:\n%s", pformat(last_change))
                self.META['last_modified'] = datetime.fromtimestamp(long(last_change[0]), tz=utc)
                self.META['author'] = last_change[4]
        except IOError:
            # Do nothing. No meta information available, procedure may not exist
            self.logger.debug('No META information for \"%s\".', self)
            pass
        except ValueError as e:
            # Can occur if timestamp cannot be converted to datetime or if it is not found
            raise KbError(e)

    def __str__(self):
        return self.namespace

    def __unicode__(self):
        return unicode(self.namespace)

    def __repr__(self):
        return "{} <{}>".format(self.__class__.__name__, self)

    # Comparaison operators
    def __eq__(self, other):
        if isinstance(other, (str, unicode)):
            return other == self.namespace
        elif isinstance(other, (Kb, Procedure)):
            return self.namespace == other.namespace
        else:
            raise NotImplementedError("Comparing with %s is not implemented !" % type(other))

    def __hash__(self):
        return hash(self.namespace)


class Wiki(object):
    """
    Class that provides access to the content stored in Dokuwiki.
    It is aware of all KB in it, you are able to search a KB, have details on it, etc...
    """
    logger = logging.getLogger('optools.apps.kb.wiki.Wiki')

    def __init__(self):
        self.logger.info("Initializing Wiki.")
        # Atrributes
        self._index = []

        # Build index and parents relations
        self._build_index()
        self._build_parent_relations()

        # Log
        self.logger.debug('%s attributes:\n%s', repr(self), pformat(self.__dict__))
        self.logger.info('Wiki initialized. Indexed %d procedures.', len(self))

    def _build_index(self):
        """Build the index of all KB in dokuwiki (txt files in data/pages folder)."""
        self.logger.info('Building index.')
        self.logger.debug('Pages directory is \"%s\".' % DOKUWIKI_PAGES_DIR)

        # Check all procedure files that exist in Dokuwiki, create Kb objects
        for root, lsdirs, lsfiles in os.walk(DOKUWIKI_PAGES_DIR):
            lsfiles.sort()
            lsdirs.sort()

            root_namespace = os.path.relpath(root, DOKUWIKI_PAGES_DIR).replace('/', ':')
            if root_namespace != "." and not root_namespace in self._index:
                self._index.append(Kb(root_namespace))

            for page in lsfiles:
                name = os.path.splitext(page)[0]
                path = os.path.join(root, name)
                namespace = os.path.relpath(path, DOKUWIKI_PAGES_DIR).replace('/', ':')
                self._index.append(Kb(namespace))

    def _build_parent_relations(self):
        """Build the parents relation-ships for all Kb."""
        self.logger.info('Doing parents relation-ships.')
        for kb in self._index:
            self.logger.debug('Building parents for \"%s\".', kb)
            for pi, parent in enumerate(kb.parents):
                kb_index = self._index.index(parent)
                kb.parents[pi] = self._index[kb_index]

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return "<{}>".format(self)

    def __getitem__(self, key):
        if key in self._index:
            return self._index[self._index.index(key)]

    def __iter__(self):
        return self._index.__iter__()

    def __len__(self):
        return self._index.__len__()
