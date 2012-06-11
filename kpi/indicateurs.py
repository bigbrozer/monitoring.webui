from kpi.models import KpiNagios, KpiRedmine
from kpi.models import NagiosNotifications
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import timedelta

def indicateurs(request):
    """
    vue qui affiche les indicateurs
    """
    kpi_redmine = KpiRedmine.objects.all().order_by("date")
    json_data = "[\n"
    for index, kpi in enumerate(kpi_redmine):
        json_data += '{date: new Date("%s"), remained: %d, opened: %d,' \
            ' closed: %d}'\
            % (kpi.date.isoformat(),
            kpi.requests_remained, kpi.requests_opened,
            kpi.requests_closed)
        if index != len(kpi_redmine)-1:
            json_data += ",\n"
    json_data += "\n]"

    chart_data = json_data

    return render_to_response(
        'main.html', locals(), context_instance = RequestContext(request))
