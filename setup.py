#!/usr/bin/env python2.7
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

from setuptools import setup, find_packages

# Way to obtain the project version if project is already installed somewhere
# in the Python path.
project_namespace = {}
with open("monitoring/webui/version.py") as version_file:
    exec(version_file.read(), project_namespace)

# Package dependencies
dependencies = [
    'django==1.5.1',
    'httpagentparser==1.2.2',
    'pytz==2013b',
]

setup(name='monitoring.webui',
      version=project_namespace["__version__"],
      description='Monitoring WebUI for Django',
      author='Vincent BESANCON',
      author_email='besancon.vincent@gmail.com',
      license='GPL',
      namespace_packages=['monitoring'],
      packages=find_packages(),
      install_requires=dependencies,
      include_package_data=True)
