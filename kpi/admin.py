from django.contrib import admin
from kpi.models import KpiNagios, KpiRedmine
from kpi.models import NagiosNotifications

class kpiNagiosAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_host', 'total_services', 'linux', 'windows', 'aix','alerts_hard_warning', 'alerts_hard_critical', 'alerts_acknowledged_warning', 'alerts_acknowledged_critical',)

class kpiRedmineAdmin(admin.ModelAdmin):
    list_display = ('date', 'requests_opened', 'requests_closed', 'requests_remained', 'requests_lifetime')

class NagiosAdmin(admin.ModelAdmin):
    list_display = ('date', 'host', 'service', 'state', 'acknowledged')
    date_hierarchy = 'date'
    ordering = ['-date']
    list_filter = ('acknowledged', 'state')

admin.site.register(KpiNagios, kpiNagiosAdmin)
admin.site.register(KpiRedmine, kpiRedmineAdmin)
admin.site.register(NagiosNotifications, NagiosAdmin)
