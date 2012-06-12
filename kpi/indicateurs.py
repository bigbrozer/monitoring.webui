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

    chart_data_lifetime = "[\n"
    chart_data_request = "[\n"
    for index, kpi in enumerate(kpi_redmine):

        chart_data_request += '{date: new Date("%s"), remained: %d, '\
            'opened: %d, closed: %d}' % (kpi.date.isoformat(),\
            kpi.requests_remained, kpi.requests_opened, kpi.requests_closed)

        lifetime = round(kpi.requests_lifetime/3600)
        lifetime_normal = round(kpi.requests_lifetime_normal/3600)
        lifetime_high = round(kpi.requests_lifetime_high/3600)
        lifetime_urgent = round(kpi.requests_lifetime_urgent/3600)

        chart_data_lifetime += '{date: new Date("%s"), global: %d, '\
            'normal: %d, high: %d, urgent: %d}' %  (kpi.date.isoformat(),\
            lifetime, lifetime_normal, lifetime_high, lifetime_urgent)

        if index != len(kpi_redmine)-1:
            chart_data_request += ",\n"
            chart_data_lifetime += ",\n"

    chart_data_request += "\n]"
    chart_data_lifetime += "\n]"

    return render_to_response(
        'main.html', locals(), context_instance = RequestContext(request))

def redirect_to_indic(request):
    """ redirect the users to indicateurs"""
    return redirect("/indicateurs")
