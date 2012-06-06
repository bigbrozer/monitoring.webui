from kpi.models import KpiNagios, KpiRedmine
from kpi.models import NagiosNotifications
from jobs.insert import insert
from django.shortcuts import render_to_response
from django.template import RequestContext

def indicateurs(request):
    """
    vue qui affiche les indicateurs
    """
    kpi_redmine = KpiRedmine.objects.all().order_by("date")

    json_data = "["
    nbr = 0
    for kpi in kpi_redmine:
        if nbr == 0:
            json_data += '{date: new Date(%d, %d, %d), remained: %d}'\
        % (kpi.date.year, kpi.date.month, kpi.date.day, kpi.requests_remained)
            nbr = 1
        else:
            json_data += ', {date: new Date(%d, %d, %d), remained: %d}'\
        % (kpi.date.year, kpi.date.month, kpi.date.day, kpi.requests_remained)
        #json_data.append({'date': date, 'remained': })
    json_data += "]"

    chart_data = json_data

    return render_to_response(
        'test.html', locals(), context_instance = RequestContext(request))
