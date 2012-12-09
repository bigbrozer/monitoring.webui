================================================================================
Developper documentation
================================================================================

This is the developper documentation (handbook) for this project. This is things
to know.

Get started
===========

First we need to configure your environment.

Setup local settings
--------------------

Create file ``settings_local.py`` in ``optools`` folder relative to the project
root.

Add the following content in it::

 import os
 from optools.settings import LOGGING
 from django.conf import settings

 DEBUG = True
 DEVEL = DEBUG
 TEMPLATE_DEBUG = DEBUG

 INTERNAL_IPS = ('127.0.0.1',)
 
 LOGIN_URL = '/accounts/login/'
 LOGOUT_URL = '/accounts/logout/'
 AUTHENTICATION_BACKENDS = (
     'django.contrib.auth.backends.ModelBackend',
 )
 
 CACHES = {
     'default': {
         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
     }
 }
 
 DOKUWIKI_BASE_URL = 'http://monitoring-dc.app.corp/kb'
 DOKUWIKI_PAGES_DIR = os.path.join(settings.PROJECT_PATH, 'var/pages')
 DOKUWIKI_META_DIR = os.path.join(settings.PROJECT_PATH, 'var/meta')
 
 SECRET_KEY = 'k6k^1fvqhj(-rod&amp;xcray3wr=)p!de_x(u(*d@f_da7036749@'
 LOGGING['loggers']['debug']['level'] = 'INFO'

PyCharm
=======

Team configuration
------------------

The Pycharm's config is shared among us and stored in ``.idea`` folder which is
part of the repository. It includes default run configuration, coding styles,
etc...

Configuring Python interpreter
------------------------------

The Python interpreter should be called ``Python (optools)`` and Python bin set
to ``~/Envs/optools/bin/python``.

Making Changes to a Database Schema
===================================

This is the procedure to apply if you change the database schema for the
project.

- Add the field to your model.

- Run ``manage.py sqlall [yourapp]`` to see the new
CREATE TABLE statement for the model. Note the column definition for the new
field.

- Start your database’s interactive shell (e.g., psql or mysql, or you can
use ``manage.py dbshell``). Execute an ``ALTER TABLE`` statement that adds your
new column.

Cron jobs
=========

Look at the django's user crontab for the list of croned jobs on
monitoring-dc.app.corp::

 $ ssh monitoring-dc.app.corp -l django
 $ crontab -l
