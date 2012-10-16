"""
Django views for application kb.
"""

# Django imports
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

# Local app imports
import wiki


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
    section = {'kb': 'active'}

    # Who is
    user = request.user
    user_is_helpdesk = user.groups.filter(name='helpdesk')

    kb_found = None

    # Info
    kb_details = wiki.get_procedure_details(kb_namespace)
    kb_requested = kb_details[-1]

    # Checking if a procedure is found in the namespaces, get the last one
    for kb in kb_details:
        if kb['created']:
            kb_found = kb

    # Redirect to the procedure if the requested is created
    if kb_requested['created']:
        return redirect("{}/{}".format(wiki.DOKUWIKI_BASE_URL, kb_requested['namespace']))
    # Redirect to the first procedure found if user is not helpdesk
    if user_is_helpdesk and kb_found:
        return redirect("{}/{}".format(wiki.DOKUWIKI_BASE_URL, kb_found['namespace']))
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

    Permissions required:
        kb.rate_procedure

    Template:
        kb/rate_procedure.html

    Context:
        locals
    """
    section = {'kb': 'active'}
    DOKUWIKI_BASE_URL = wiki.DOKUWIKI_BASE_URL
    all_kb_namespaces = wiki.iterpages()

    return render_to_response(
        "kb/rate_procedure.html",
        locals(),
        context_instance=RequestContext(request)
    )
