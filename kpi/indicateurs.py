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
    one_day = timedelta(days = 1)
    json_data = "[\n"
    for index, kpi in enumerate(kpi_redmine):
        if kpi.date.month != (kpi.date + one_day).month:
            month = kpi.date.month
            day = 0
            year = kpi.date.year
            if kpi.date.month == 12:
                month = 0
                day = 0
                year = kpi.date.year + 1
        else:
            month = kpi.date.month-1
            day = kpi.date.day
            year = kpi.date.year


        json_data += '{date: new Date(%d, %d, %d), remained: %d, opened: %d,' \
            ' closed: %d}'\
            % (year, month, day,
            kpi.requests_remained, kpi.requests_opened,
            kpi.requests_closed)
        if index != len(kpi_redmine)-1:
            json_data += ",\n"
    json_data += "\n]"

    chart_data = json_data

    return render_to_response(
        'main.html', locals(), context_instance = RequestContext(request))
