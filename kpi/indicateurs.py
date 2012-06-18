from kpi.models import KpiNagios, KpiRedmine
from kpi.models import NagiosNotifications
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.db.models import Count
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'reporting.settings'

from jobs import nagios_notifications

def indicateurs(request):
    """
    View showing the charts for the differents kpi requested
    param: http request
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
    alerts = []

    for index, kpi in enumerate(kpi_nagios):
        chart_data_nagios += '{date: new Date("%s"), total_host: %d, '\
        'total_services: %d, written_procedures: %d, missing_procedures: %d, '\
        'linux: %d, windows: %d, aix: %d}' % (kpi.date.isoformat(),\
        kpi.total_host, kpi.total_services, kpi.written_procedures,\
        kpi.missing_procedures, kpi.linux, kpi.windows, kpi.aix)

        if index != len(kpi_nagios)-1:
            chart_data_nagios += ",\n"

    chart_data_nagios += "\n]"

    # notifs = NagiosNotifications.objects.extra({'dateDay' : "date(date)"})\
    # .values("dateDay", "acknowledged", "state").annotate(alerts = Count("id"))\
    # .order_by("dateDay")
    # result = {}
    # tmp = {}
    # chart_data_alerts = ""
    # for values in notifs:
    #     result[str(values['dateDay'])] =
    #     if values['acknowledged']:
    #         if values['state'] == 1:
    #             tmp['warning_ack'] = values['alerts']
    #             result[str(values['dateDay'])].update(tmp)
    #         if values['state'] == 2:
    #             result[str(values['dateDay'])] = {}
    #             result[str(values['dateDay'])]['critical_ack'] += values['alerts']
    #     if not values['acknowledged']:
    #         if values['state'] == 1:
    #             result[str(values['dateDay'])] = {}
    #             result[str(values['dateDay'])]['warning'] += values['alerts']
    #         if values['state'] == 2:
    #             result[str(values['dateDay'])] = {}
    #             result[str(values['dateDay'])]['critical'] += values['alerts']

    # chart_data_alerts = result

# result = NagiosNotifications.objects.all()

#     chart_data_alerts = "[\n"

#     for alerts in result:
#         chart_data_alerts += '{date: new Date("%s"), alerts_hard_warning: %d, '\
#             'alerts_hard_critical: %d, alerts_acknowledged_warning: %d, '\
#             'alerts_acknowledged_critical: %d}' % (first_date,\
#             alerts['alerts_hard_warning'],\
#             alerts['alerts_hard_critical'],\
#             alerts['alerts_acknowledged_warning'],\
#             alerts['alerts_acknowledged_critical'])
#         first_date += one_day
#         chart_data_alerts += ",\n"

#     chart_data_alerts += "\n]"


    return render_to_response(
        'main.html', locals(), context_instance = RequestContext(request))

def redirect_to_indic(request):
    """ redirect the users to indicateurs"""
    return redirect("/indicateurs")
