from django.contrib import admin
from kpi.models import KpiNagios, KpiRedmine
from kpi.models import NagiosNotifications
from datetime import timedelta

class kpiNagiosAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_host', 'total_services', 'linux', 'windows', 'aix','alerts_hard_warning', 'alerts_hard_critical', 'alerts_acknowledged_warning', 'alerts_acknowledged_critical',)
    date_hierarchy = 'date'
    ordering = ['-date']
    
class kpiRedmineAdmin(admin.ModelAdmin):
    list_display = ('date', 'requests_opened', 'requests_closed', 'requests_remained', 'lifetime')
    date_hierarchy = 'date'
    ordering = ['-date']

    def lifetime(self, obj):
        # sec = obj.requests_lifetime
        # t = timedelta(seconds=sec)
        # return str(t)
        return "%s" % timedelta(seconds = obj.requests_lifetime)

class NagiosAdmin(admin.ModelAdmin):
    list_display = ('date', 'host', 'service', 'state', 'acknowledged')
    date_hierarchy = 'date'
    ordering = ['-date']
    list_filter = ('acknowledged', 'state')

admin.site.register(KpiNagios, kpiNagiosAdmin)
admin.site.register(KpiRedmine, kpiRedmineAdmin)
admin.site.register(NagiosNotifications, NagiosAdmin)
