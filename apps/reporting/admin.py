# Adding models to Admin site for reporting app

from django.contrib import admin
from optools.apps.reporting.models import AckStat, ProcedureStat, NagiosKPI

class AckStatAdmin(admin.ModelAdmin):
	list_display = ('date', 'active_ack_warn', 'active_ack_crit')

class ProcedureStatAdmin(admin.ModelAdmin):
	list_display = ('date', 'num_no_procedure', 'num_with_procedure')

class NagiosKPIAdmin(admin.ModelAdmin):
	list_display = ('date', 'total_hosts', 'total_services', 'alert_warn_total', 'alert_crit_total', 'service_without_kb')

admin.site.register(AckStat, AckStatAdmin)
admin.site.register(ProcedureStat, ProcedureStatAdmin)
admin.site.register(NagiosKPI, NagiosKPIAdmin)
