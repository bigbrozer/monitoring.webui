from kpi.models import KpiNagios, KpiRedmine
from kpi.models import NagiosNotifications
from jobs.insert import insert
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime

def indicateurs(request):
    """
    vue qui affiche les indicateurs
    """
    kpi_redmine = KpiRedmine.objects.all().order_by("date")

    json_data = "["
    for index, kpi in enumerate(kpi_redmine):
        json_data += '{date: new Date(%d, %d, %d), remained: %d}'\
            % (kpi.date.year, (kpi.date.month - 1),
            (kpi.date.day - 1), kpi.requests_remained)
        if index != len(kpi_redmine):
            json_data += ", "
        #json_data.append({'date': date, 'remained': })
    json_data += "]"

    chart_data = json_data

    return render_to_response(
        'main.html', locals(), context_instance = RequestContext(request))
