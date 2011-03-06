import os
import sys

# Adding optools project to sys.path
optools_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(optools_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'optools.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

