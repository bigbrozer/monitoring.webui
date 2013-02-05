#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#===============================================================================
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Setuptools install script.
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

import os
from setuptools import setup, find_packages
import monitoring.webui

# Package dependencies
dependencies = [
    'django>=1.4,<1.5',
]

# Init distribute
setup(name = 'monitoring.webui',
    version = monitoring.webui.__version__,
    description = 'Monitoring WebUI for Django',
    author = 'Vincent BESANCON',
    author_email = 'besancon.vincent@gmail.com',
    license = 'GPL',
    namespace_packages = ['monitoring'],
    packages = find_packages(),
    install_requires = dependencies,
)
