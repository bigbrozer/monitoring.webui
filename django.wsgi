import os
import sys

# Adding optools project to sys.path
pwd = os.path.abspath(os.path.dirname(__file__))
optools_dir = os.path.split(pwd)[0]
sys.path.append(optools_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

