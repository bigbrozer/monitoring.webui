"""
Django views for application kb.
"""

# Django imports
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
    """

    # Who is
    user = request.user
    user_is_kb_manager = user.groups.filter(name='kb_manager')

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
    # Redirect to the procedure one has been found and user is not a KB Manager
    if not user_is_kb_manager and kb_found:
        return redirect("{}/{}".format(wiki.DOKUWIKI_BASE_URL, kb_found['namespace']))
    # User is a KB Manager or no procedure exist
    else:
        return render_to_response(
            "kb/manage_procedure.html",
            locals(),
            context_instance=RequestContext(request)
        )
