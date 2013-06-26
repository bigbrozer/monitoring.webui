# -*- coding: utf-8 -*-
# Copyright (C) Faurecia <http://www.faurecia.com/>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
