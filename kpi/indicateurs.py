from kpi.models import KpiNagios, KpiRedmine
from kpi.models import  CountNotifications, RecurrentAlerts, OldestAlerts
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import redirect
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'reporting.settings'

def indicateurs(request):
    """
    View showing the charts for the differents kpi requested
    param: http request
    """
    kpi_redmine = KpiRedmine.objects.all().order_by("date")

    chart_data_request = "[\n"

    for index, kpi in enumerate(kpi_redmine):
        lifetime = kpi.requests_lifetime/3600/24
        lifetime_normal = kpi.requests_lifetime_normal/3600/24
        lifetime_high = kpi.requests_lifetime_high/3600/24
        lifetime_urgent = kpi.requests_lifetime_urgent/3600/24

        chart_data_request += '{date: new Date("%s"), remained: %d, '\
            'opened: %d, closed: %d, global: %d, '\
            'normal: %d, high: %d, urgent: %d}' % (kpi.date.isoformat(),
                                                   kpi.requests_remained, kpi.requests_opened, kpi.requests_closed,
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
        'linux: %d, windows: %d, aix: %d}' % (kpi.date.isoformat(),
                                              kpi.total_host, kpi.total_services, kpi.written_procedures,
                                              kpi.missing_procedures, kpi.linux, kpi.windows, kpi.aix)

        if index != len(kpi_nagios)-1:
            chart_data_nagios += ",\n"

    chart_data_nagios += "\n]"

    result = CountNotifications.objects.all().order_by("date")

    chart_data_alerts = "[\n"

    for alert in result:
        chart_data_alerts += '{date: new Date("%s"), warning: %d, '\
            'warning_acknowledged: %d, critical: %d, '\
            'critical_acknowledged: %d}' % (alert.date.isoformat(),
                                            alert.warning,
                                            alert.warning_acknowledged,
                                            alert.critical,
                                            alert.critical_acknowledged)
        chart_data_alerts += ",\n"

    chart_data_alerts += "\n]"

    chart_data_recurrents_alerts = "[\n"

    recurrents_alerts = RecurrentAlerts.objects.all().order_by("-frequency")[:15]
    others = RecurrentAlerts.objects.all()
    number_others = 0

    for alert in recurrents_alerts:
        chart_data_recurrents_alerts += '{name: "%s@%s", repetitions: %d, '\
        'url: "http://monitoring-dc.app.corp/thruk/cgi-bin/status.cgi?host=%s"}' % (alert.service,
                                                                              alert.host,
                                                                              alert.frequency,
                                                                              alert.host)
        chart_data_recurrents_alerts += ",\n"
    for alert in others:
        number_others += alert.frequency
#    chart_data_recurrents_alerts += '{name: "others", repetitions: %d, '\
#        'url: "http://monitoring-dc.app.corp/thruk/cgi-bin/status.cgi"}' % number_others
    chart_data_recurrents_alerts += "\n]"

    chart_data_oldests_alerts = "[\n"
    oldest_alerts = OldestAlerts.objects.all().order_by("date_error")[:25]
    for alert in oldest_alerts:
        days = alert.date - alert.date_error
        date_error = "%s-%s-%s" % (alert.date_error.year, alert.date_error.month, alert.date_error.day)
        days = days.total_seconds()/60/60/24
        chart_data_oldests_alerts += '{name: "%s@%s", days: %d, date_error: "%s"}' % (alert.service,
                                                                    alert.host, days, date_error)
        chart_data_oldests_alerts += ",\n"

    chart_data_oldests_alerts += "\n]"

    return render_to_response(
        'main.html', locals(), context_instance = RequestContext(request))

def redirect_to_indic(request):
    """ redirect the users to indicateurs"""
    return redirect("/indicateurs/")
