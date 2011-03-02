# Adding models to Admin site for reporting app

from django.contrib import admin
from optools.Reporting.models import AckStat

class AckStatAdmin(admin.ModelAdmin):
	list_display = ('date', 'active_ack_warn', 'active_ack_crit')

admin.site.register(AckStat, AckStatAdmin)
