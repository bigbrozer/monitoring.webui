# Adding models to Admin site for reporting app

from django.contrib import admin
from optools.apps.reporting.models import AckStat, ProcedureStat

class AckStatAdmin(admin.ModelAdmin):
	list_display = ('date', 'active_ack_warn', 'active_ack_crit')

class ProcedureStatAdmin(admin.ModelAdmin):
	list_display = ('date', 'num_no_procedure', 'num_with_procedure')

admin.site.register(AckStat, AckStatAdmin)
admin.site.register(ProcedureStat, ProcedureStatAdmin)
