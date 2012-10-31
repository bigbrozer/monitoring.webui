# -*- coding: utf-8 -*-
#===============================================================================
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Some utilities functions
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

# Django imports
from django.shortcuts import redirect

# Apps imports
from apps.common.context_processors import browser


def check_browser_support(request):
    """
    Check browser support.
    """
    # Get browser data using the context processor, maybe not the best way to do it here...
    br = browser(request)
    if br['browser']['outdated']:
        return redirect("browser_out_of_date")