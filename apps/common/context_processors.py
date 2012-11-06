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

import httpagentparser


def browser(request):
    """
    Adds browser-related context variables to the context.

    This adds in context a ``browser`` key wich is a dict:

    - name: name of the browser.
    - version: full version of the browser.
    - outdated: specify if browser is outdated so unsupported.
    - major_version: the browser major version (None if not available).
    """
    if request.META.get('HTTP_USER_AGENT'):
        br =  httpagentparser.detect(request.META['HTTP_USER_AGENT'])['browser']
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