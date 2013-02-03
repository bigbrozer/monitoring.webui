# Views for app portal

import logging

# Django imports
from django.shortcuts import render


logger = logging.getLogger(__name__)

def portal_home(request):
    """
    The home of the portal.
    """
    return render(request, 'portal/portal.html', {'title': "Home", 'section': {'home': 'active'}})

