# Adding models to Admin site for reporting app

from django.contrib import admin
from optools.apps.reporting.models import NagiosKPI

class NagiosKPIAdmin(admin.ModelAdmin):
	list_display = ('date', 'total_hosts', 'total_services', 'alert_warn_total', 'alert_crit_total', 'service_without_kb')

admin.site.register(NagiosKPI, NagiosKPIAdmin)
