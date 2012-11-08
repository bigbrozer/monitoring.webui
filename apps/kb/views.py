"""
Django views for application kb.
"""

# Std imports
import logging

# Django imports
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse

# Models imports
from apps.kb.models import Procedure

# Local app imports
from apps.kb import wiki


def show_kb(request, kb_namespace):
    """
    Handle the way KB is shown.

    Try to find the first procedure found in ``kb_namespace``. Redirect to first found if
    the requested procedure is not found and user is not a KB Manager.

    For peoples member of group **kb_manager**, propose to create the procedure
    if missing (all namespaces).

    For others, it says that the procedure is missing and the alert should be
    part of a Stratos ticket to the relevant group.

    :param kb_namespace: the dokuwiki procedure page of the form ``xxx:xxx:xxx...``.

    Template:
        kb/manage_procedure.html

    Context:
        locals
    """
    # Internals
    _dokuwiki = wiki.Wiki()
    _kb_found = None

    # Context
    user_is_helpdesk = request.user.groups.filter(name='helpdesk')
    kb_requested = _dokuwiki[kb_namespace]
    title = "Showing KB %s" % kb_requested.namespace
    section = {'kb': 'active'}

    # Checking for first written procedure in the parents
    for parent in kb_requested.parents:
        if parent.is_written:
            _kb_found = parent

    # Redirect to the procedure if the requested is created
    if kb_requested.is_written:
        return redirect(kb_requested.META['read_url'])
    # Redirect to the first procedure found if user is not helpdesk
    if user_is_helpdesk and _kb_found:
        return redirect(_kb_found.META['read_url'])
    # No procedure exist or user is not helpdesk
    else:
        return render_to_response(
            "kb/manage_procedure.html",
            locals(),
            context_instance=RequestContext(request)
        )

@permission_required('kb.rate_procedure')
def rate_kb(request):
    """
    Show page to rate quality of procedures in dokuwiki.
    If an Ajax request is send to this page, it will update Procedure model if user is authorized to do so.

    Permissions required:
        kb.rate_procedure

    Template:
        kb/rate_procedure.html

    Context:
        locals
    """
    logger = logging.getLogger('optools.debug.kb.rating')

    if not request.is_ajax():
        title = 'KB'
        section = {'kb': 'active'}
        procedures = Procedure.objects.all()

        return render_to_response(
            "kb/rate_procedure.html",
            locals(),
            context_instance=RequestContext(request)
        )
    elif request.is_ajax():
        kb_list = request.GET.getlist('kb[]')

        # Update status
        for kb in kb_list:
            procedure, created = Procedure.objects.get_or_create(namespace=kb, defaults={'rating': -1, 'comment': None})

            if request.GET.has_key('rating'):
                rating = request.GET['rating']
                procedure.rating = int(rating)

            if request.GET.has_key('comment'):
                comment = request.GET['comment']
                procedure.comment = comment

            procedure.validated = True
            procedure.save()

        return HttpResponse()
