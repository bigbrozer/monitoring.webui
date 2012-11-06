"""
WSGI config for optools project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import site

# Get the project root directory
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Add virtualenv's site-packages to Python Path
site.addsitedir('/home/django/Envs/optools/lib/python2.7/site-packages')
project_env_lib = sys.path.pop()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "optools.settings")

# Add project directory to Python Path
sys.path.insert(0, project_env_lib)
sys.path.insert(0, project_dir)

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
