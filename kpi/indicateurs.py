from kpi.models import KpiNagios, KpiRedmine
from kpi.models import NagiosNotifications
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import timedelta
from django.shortcuts import redirect

def indicateurs(request):
    """
    vue qui affiche les indicateurs
    """
    kpi_redmine = KpiRedmine.objects.all().order_by("date")

    chart_data_request = "[\n"

    for index, kpi in enumerate(kpi_redmine):
        lifetime = round(kpi.requests_lifetime/3600/24)
        lifetime_normal = round(kpi.requests_lifetime_normal/3600/24)
        lifetime_high = round(kpi.requests_lifetime_high/3600/24)
        lifetime_urgent = round(kpi.requests_lifetime_urgent/3600/24)

        chart_data_request += '{date: new Date("%s"), remained: %d, '\
            'opened: %d, closed: %d, global: %d, '\
            'normal: %d, high: %d, urgent: %d}' % (kpi.date.isoformat(),\
            kpi.requests_remained, kpi.requests_opened, kpi.requests_closed,\
            lifetime, lifetime_normal, lifetime_high, lifetime_urgent)

        if index != len(kpi_redmine)-1:
            chart_data_request += ",\n"

    chart_data_request += "\n]"

    chart_data_nagios = "[\n"
    kpi_nagios = KpiNagios.objects.all().order_by("date")

    for index, kpi in enumerate(kpi_nagios):
        chart_data_nagios += '{date: new Date("%s"), total_host: %d, '\
        'total_services: %d, written_procedures: %d, missing_procedures: %d, '\
        'linux: %d, windows: %d, aix: %d}' % (kpi.date.isoformat(),\
        kpi.total_host, kpi.total_services, kpi.written_procedures,\
        kpi.missing_procedures, kpi.linux, kpi.windows, kpi.aix)

        if index != len(kpi_nagios)-1:
            chart_data_nagios += ",\n"

    chart_data_nagios += "\n]"


    return render_to_response(
        'main.html', locals(), context_instance = RequestContext(request))

def redirect_to_indic(request):
    """ redirect the users to indicateurs"""
    return redirect("/indicateurs")
