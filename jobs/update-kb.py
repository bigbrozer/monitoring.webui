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

__all__ = ['update', 'delete_removed']

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
logger = logging.getLogger('optools.jobs.update_kb')
logger.info('Starting job: %s.', os.path.basename(__file__))

# Wiki instance
dokuwiki = Wiki()

#===============================================================================
#  _____                 _   _
# |  ___|   _ _ __   ___| |_(_) ___  _ __  ___
# | |_ | | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# |  _|| |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/
#
#===============================================================================

def update_fields(kb, model):
    """Update fields in the database. Associate attributes to DB fields."""
    logger.debug('Updating fields of KB \"%s\" in database.', kb)

    # Direct to a db field
    for field in kb.db_fields:
        setattr(model, field, getattr(kb, field))
    # Get META informations and insert in db field
    for meta in kb.db_meta_fields:
        setattr(model, meta, getattr(kb, 'META').get(meta))

def update():
    """Update or create KB in the database, keep in sync with dokuwiki."""
    have_kb_in_db = Procedure.objects.count()

    if have_kb_in_db:
        logger.info("Entering update mode.")
    else:
        logger.info("Entering create mode.")

    with transaction.commit_on_success():
        logger.info("Populating database...")
        for kb in dokuwiki:
            model, created = Procedure.objects.get_or_create(namespace=kb.namespace)
            if created:
                logger.debug('Kb \"%s\" is new in database.', kb)
            # Update fields
            update_fields(kb, model)

            # Process all parents
            for parent in kb.parents:
                parent_model, created = Procedure.objects.get_or_create(namespace=parent.namespace)
                if created:
                    logger.debug('Parent \"%s\" for kb \"\" is new in database.', parent, kb)
                model.parents.add(parent_model)

            # Save KB in database
            model.save()

    logger.info('Done. Database now have %d procedures.', Procedure.objects.count())

def delete_removed():
    """Find all KB that no longer exist in dokuwiki and delete them from the database."""
    logger.info("Checking to replicate deletions of KB from wiki to database.")
    kb_in_dokuwiki = set(dokuwiki)
    kb_in_db = set(Procedure.objects.all())
    deleted_kb = kb_in_db - kb_in_dokuwiki

    for procedure in deleted_kb:
        logger.debug('Kb \"%s\" has been removed from wiki. Deletes database entry.', procedure.namespace)
        procedure.delete()

    logger.info("Done. Deleted %s procedures from database.", len(deleted_kb))

#===============================================================================
#  __  __       _
# |  \/  | __ _(_)_ __
# | |\/| |/ _` | | '_ \
# | |  | | (_| | | | | |
# |_|  |_|\__,_|_|_| |_|
#
#===============================================================================

def main():
    """Main job procedure."""
    update()
    delete_removed()

if __name__ == '__main__':
    main()
