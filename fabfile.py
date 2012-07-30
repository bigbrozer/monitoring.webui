# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : fabfile
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : Fabric tasks for the project.
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

"""
Fabric tasks available for project IT Operations Tools.
"""

from fabric.api import *
from fabric.colors import *
from contextlib import nested
from monitoring.fabric import servers

@task
@hosts('monitoring-dc.app.corp')
def static():
    """Run collectstatic for the project."""
    env.user = 'django'
    with nested(prefix('workon optools'), cd('optools')):
        puts(green('Updating static files...'))
        run('python ./manage.py collectstatic --noinput -c')

@task
@hosts('monitoring-dc.app.corp')
def update():
    """Update project source."""
    env.user = 'django'
    run('cd optools && git pull')

@task
@hosts('monitoring-dc.app.corp')
def setup():
    """Setup the project in production."""
    env.user = 'django'

    # Clone / update the repository
    with settings(warn_only=True):
        if run('test -d optools').failed:
            with cd('$HOME'):
                puts(green('Clone git repository...'))
                run('git clone /git/repositories/admin/optools.git')
                run('mkdir -p /var/www/static/optools')
        else:
            update()
    
    # Create the virtualenv for the project
    puts(green('Creating Python virtual environment...'))
    run('mkvirtualenv optools')

    with cd('optools'):
        puts(green('Installing project dependencies...'))
        run('~/Envs/optools/bin/pip install -r requirements.txt')

    # Setup Apache config
    with nested(cd('~django/optools'), settings(user='root')):
        puts(green('Set the Apache configuration...'))
        run('ln -sf ~django/optools/apache/django_optools /etc/apache2/conf.d/django_optools')
        run('service apache2 force-reload')

    # Collect static files
    static()

