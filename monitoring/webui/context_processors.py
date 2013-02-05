# -*- coding: utf-8 -*-
#===============================================================================
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Context processors for Optools
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

import logging


logger = logging.getLogger(__name__)

def browser(request):
    """
    Adds browser-related context variables to the context.

    This adds in context a ``browser`` key wich is a dict:

    - name: name of the browser.
    - version: full version of the browser.
    - outdated: specify if browser is outdated so unsupported.
    - major_version: the browser major version (None if not available).
    """
    import httpagentparser

    if request.META.get('HTTP_USER_AGENT'):
        br =  httpagentparser.detect(request.META['HTTP_USER_AGENT'])['browser']

        if isinstance(br, dict):
            br['major_version'] = None
            br['outdated'] = False
            try:
                # Try to get the major version (does not work all the time ;-) )
                br['major_version'] = int(br['version'].split('.')[0])
            except:
                # Forget the major browser version
                pass

            # Mark outdated browsers
            if "internet explorer" in br['name'].lower() \
            and br['major_version'] \
            and br['major_version'] < 9:
                br['outdated'] = True

            return {'browser': br}
        else:
            return {'browser': None}

def project(request):
    """
    Add project related context variables to the context.

    Context
        PROJECT_VERSION: the version of optools (last git tag). Show NA if not available.
        PROJECT_DEBUG_MODE: are we in DEBUG mode ?
        PROJECT_DB_HOST: the host running the database.
    """
    from django.conf import settings
    import subprocess

    try:
        version = subprocess.check_output(['git', '--git-dir={}/.git'.format(settings.PROJECT_PATH),
                               'describe','--tags'])
    except:
        version = 'NA'

    return {
        'PROJECT_VERSION': version.strip('\n'),
        'PROJECT_DEBUG_MODE': settings.DEBUG,
        'PROJECT_DB_HOST': settings.DATABASES['default']['HOST'],
    }
