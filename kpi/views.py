from django.http import HttpResponse
from kpi.models import KpiNagios, KpiRedmine
from kpi.models import NagiosNotifications

def indicateurs(request):
    result = collecte()
    return HttpResponse(result)
