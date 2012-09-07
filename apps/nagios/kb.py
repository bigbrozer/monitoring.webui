"""
:mod:`nagios.kb` to handle Alert procedures (KB)
"""

# TODO: validate the wiki url against a Regexp.

# Std lib imports
import os


def find_procedure(kb, directory='/var/www/kb/data/pages'):
    """
    Return the first procedure page based on a Wiki link or None. Check refs #1493.

    :param kb: the full dokuwiki URL of the form ``xxx:xxx:xxx``...
    :returns: a tuple (kb_file, kb_url).
    """

    # Init logging for debugging
    import logging
    logger = logging.getLogger('nagios.kb.find_procedure')

    # Clean wiki url and transform to a path
    kb_root = directory
    kb_path = kb.strip(':').replace(':', '/')
    kb_file = os.path.join(kb_root, "{0}.txt".format(kb_path))

    logger.debug("Root: %s, KB Path: %s, File: %s", kb_root, kb_path, kb_file)

    # Try to find the procedure until a file ending with *.txt is found inside the procedure root directory.
    while not os.path.isfile(kb_file):
        kb_path = os.path.dirname(kb_path)
        if not kb_path:
            # Go away, procedure is not written
            return None

        kb_file = os.path.join(kb_root, "{0}.txt".format(kb_path))
        logger.debug("No procedure. Go one level below: %s. KB: %s", kb_file, kb_path)

    return kb_file, kb_path.replace('/', ':')


# Module testing
if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(asctime)s | %(module)s <%(funcName)s>: %" \
                                                    "(message)s")
    logger = logging.getLogger('nagios.kb')

    procedure = find_procedure('app:metis:prod:oss:tata:', directory='/tmp/pages')
    logger.debug("Procedure: %s", procedure)
