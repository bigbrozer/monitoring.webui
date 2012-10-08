"""
:mod:`kb.wiki` to handle Alert procedures (KB)
"""

# Std lib imports
import os
import re

# Django imports
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'
from django.conf import settings


# Import *
__all__ = ['KbError', 'KbUrlMalformed', 'get_procedure_details']

# Dokuwiki config
DOKUWIKI_BASE_URL = '/kb' if not settings.DEBUG else 'http://monitoring-dc.app.corp/kb'
DOKUWIKI_DIR = '/var/www/kb/data/pages' if not settings.DEBUG else '/tmp/pages'


# Exceptions
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
        self.message = 'KB URL \"%s\" is malformed. Must be \"%s\" !' % (kb, regexp)
        super(KbUrlMalformed, self).__init__(self.message)


# Procedures
def get_procedure_details(namespace):
    """
    Return details about all KB of the specified ``namespace``. Check request #1493.

    It returns a list of dict containing all info about a namespace, use the following keys:

    * **created**: is the procedure is written ?
    * **edit_url**: link to edit procedure in dokuwiki
    * **file**: local file storing the procedure content
    * **namespace**: dokuwiki URL for the procedure (xxx:xxx:xxx...)
    * **page**: name of the procedure page

    :param namespace: the dokuwiki's namespace of the form ``xxx:xxx:xxx[...]``.
    :rtype: list
    """

    # Test KB URL before proceeding
    kb_url_regexp = r'^([a-zA-Z0-9]+:*)+$'
    if not re.match(kb_url_regexp, namespace):
        raise KbUrlMalformed(namespace, kb_url_regexp)

    kb_namespaces = namespace.strip(':').split(':')
    kb_details = []

    # Browse all namespaces levels and get info on each namespaces
    for pos, nsp in enumerate(kb_namespaces):
        pos += 1
        kb_info = {}

        kb_info['page'] = nsp
        kb_info['namespace'] = ':'.join(kb_namespaces[:pos])
        kb_info['file'] = os.path.join(DOKUWIKI_DIR, "{0}.txt".format('/'.join(kb_namespaces[:pos])))
        kb_info['edit_url'] = '{0}/{1}?do=edit'.format(DOKUWIKI_BASE_URL, kb_info['namespace'])

        if os.path.isfile(kb_info['file']):
            kb_info['created'] = True
        else:
            kb_info['created'] = False

        kb_details.append(kb_info)

    return kb_details

# Module testing
if __name__ == '__main__':
    import logging
    from pprint import pprint

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s (<%(funcName)s>)")
    logger = logging.getLogger('kb.wiki')

    page = 'app:metis:prod:oss:tata'

    pprint(get_procedure_details(page))
