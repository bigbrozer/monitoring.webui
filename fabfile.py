# -*- coding: UTF-8 -*-
#===============================================================================
# Filename      : fabfile
# Author        : Vincent BESANCON <besancon.vincent@gmail.com>
# Description   : fabfile that may be used with fabric to launch some admin
#                 tasks related to optools.
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

# Fabric API
from fabric.api import env, task, roles, run, cd, puts

# Servers list and roles
from monitoring.fabric import servers

@task
@roles('central')
def optools_update():
    """
    Update IT Operations Tools on remote central server.
    
    Do this after a push to the optools repository to apply the update
    """
    env.user = 'django'
    puts('Connecting as user \'%(user)s\'.' % env)
    with cd('optools'):
        run('git pull')
        run('./manage.py collectstatic')

