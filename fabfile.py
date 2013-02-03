# -*- coding: UTF-8 -*-
#===============================================================================
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
Fabric tasks available for project Central Operations Tools.
"""

from fabric.api import *
from fabric.colors import *
from monitoring.fabric import servers


def static():
    """Run collectstatic for the project."""
    env.user = 'django'
    with prefix('workon optools'), cd('optools'):
        puts(green('Updating static files...'))
        run('python ./manage.py collectstatic --noinput -c')


@task
@hosts('monitoring-dc.app.corp')
def update():
    """Apply latest updates on project in production."""
    env.user = 'django'

    puts(green('Updating project\'s branch master.', bold=True))

    puts(cyan('- Pushing branch master and tags to remote central...'))
    local('git push central master && git push central --tags')

    puts(cyan('- Applying update...'))
    run('cd optools && git pull')

    # Collect static files
    static()


@task
@hosts('monitoring-dc.app.corp')
def install():
    """Install the project in production."""
    env.user = 'django'

    # Clone / update the repository
    with settings(warn_only=True):
        if run('test -d optools').failed:
            with cd('$HOME'):
                puts(green('Clone git repository...'))
                run('git clone /git/repositories/admin/optools.git')
                run('mkdir -p /var/www/static/optools')
                run('mkdir -p ~/public_html/reporting')
        else:
            update()

    # Create the virtualenv for the project
    puts(green('Creating Python virtual environment...'))
    with cd('optools'):
        run('mkvirtualenv optools -r requirements.txt')

    # Setup Apache config
    with cd('~django/optools'), settings(user='root'):
        puts(green('Install Apache\'s configuration...'))
        run('ln -sf ~django/optools/apache/django_optools /etc/apache2/conf.d/django_optools')
        run('service apache2 force-reload')

    # Collect static files
    static()


@task
@hosts('monitoring-dc.app.corp')
def update_kpi():
    """Launch the script that update the KPI."""
    env.user = "django"
    run('/home/django/optools/cron/update.sh')


@task
@hosts('monitoring-dc.app.corp')
def clean_cache():
    """Clean the Django cache."""
    sudo('rm -rf /var/tmp/django_cache/optools')


@task
@hosts('monitoring-dc.app.corp')
def show_log():
    """Show the optools log."""
    import tempfile

    env.tmpdir = tempfile.mkdtemp(prefix="optools-")
    get("/home/django/optools/log/optools.log", "%(tmpdir)s" % env)
    local("gvim -f %(tmpdir)s/optools.log && rm -rf %(tmpdir)s" % env)