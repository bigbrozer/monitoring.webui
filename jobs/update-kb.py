#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#===============================================================================
# Filename      : update-kb
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Keep up-to-date Procedure model with dokuwiki.
#-------------------------------------------------------------------------------
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

# Std imports
import logging
import sys
import os

# Locate optools settings
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'

# Apps imports
from apps.kb.wiki import Wiki
from apps.kb.models import Procedure

# Django imports
from django.db import transaction

# Logging
logger = logging.getLogger('optools.debug.jobs.update_kb')
logger.info('Starting job: %s.', os.path.basename(__file__))

# Wiki instance
dokuwiki = Wiki()

# Run on first import (database is empty)
def bulk_import():
    logger.info('Start Bulk import.')
    logger.info('Importing %d entries in the database.', len(dokuwiki))

    with transaction.commit_on_success():
        for kb in dokuwiki:
            logger.debug("Inserting kb \"%s\"...", kb)
            new_kb = Procedure(namespace=kb.namespace)
            new_kb.is_written = kb.is_written
            new_kb.last_modified = kb.META.get('last_modified')
            new_kb.author = kb.META.get('author')
            new_kb.save()

    logger.info('Bulk import is done.')

if not Procedure.objects.all():
    # First import, table is empty
    bulk_import()
else:
    pass
