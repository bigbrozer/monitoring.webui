"""
settings from the admin site
"""

from django.contrib import admin
from kpi.models import KpiNagios, KpiRedmine
from kpi.models import NagiosNotifications, CountNotifications
from jobs.insert import insert_redmine, insert_nagios_notifications
from jobs.insert import get_notifications
from django.utils import timezone
import pytz

class KpiNagiosAdmin(admin.ModelAdmin):
    """
    modify default settings for kpi nagios
    """
    #fields = (('date', 'total_host', 'total_services', 'written_procedures',
    # 'missing_procedures', 'linux', 'windows', 'aix'),('alerts_hard_warning',
    #  'alerts_hard_critical', 'alerts_acknowledged_warning',
    #  'alerts_acknowledged_critical', ))
    list_display = ('date', 'total_host', 'total_services',
        'written_procedures', 'missing_procedures', 'linux', 'windows', 'aix')
    date_hierarchy = 'date'
    ordering = ['-date']

class KpiRedmineAdmin(admin.ModelAdmin):
    """
    modify default settings for kpi redmine
    """
    list_display = ('date', 'requests_opened', 'requests_closed',
        'requests_remained', 'lifetime', 'lifetime_normal', 'lifetime_high',
        'lifetime_urgent')
    date_hierarchy = 'date'
    ordering = ['-date']
    actions = ['update']

    def update(self, request, queryset):
        """
        update database from selected date
        """
        tzname = timezone.get_current_timezone_name()
        tzinfo = pytz.timezone(tzname)
        for query in queryset:
            date = query.date
        date_locale = tzinfo.normalize(date)
        KpiRedmine.objects.filter(date__gte = date).delete()
        rows_updated = insert_redmine()
        self.message_user(
            request,
            "%s entries successfully updated from %s" % (rows_updated,
                                                    date_locale.strftime("%c")))
        # self.message_user(request, "%s" % (queryset))
    update.short_description = "Update database from selected date"

class NagiosAdmin(admin.ModelAdmin):
    """
    modify default settings for nagios notifications
    """
    list_display = ('date', 'host', 'service', 'state', 'acknowledged')
    date_hierarchy = 'date'
    ordering = ['-date']
    list_filter = ('acknowledged', 'state')
    actions = ['update']
    def update(self, request, queryset):
        """
        update database from last date
        """
        tzname = timezone.get_current_timezone_name()
        tzinfo = pytz.timezone(tzname)
        date = NagiosNotifications.objects.order_by('-date')[0].date
        date_locale = tzinfo.normalize(date)
        rows_updated = insert_nagios_notifications(get_notifications())
        self.message_user(
            request,
            "%s new notifications imported from %s" % (rows_updated,
                                                    date_locale.strftime("%c")))
    update.short_description = "Update database"

class CountNotificationsAdmin(admin.ModelAdmin):
    """
    modify default settings for count notifications
    """
    list_display = ('date', 'warning', 'warning_acknowledged', 'critical',
        'critical_acknowledged')
    date_hierarchy = 'date'
    ordering = ['-date']

admin.site.register(KpiNagios, KpiNagiosAdmin)
admin.site.register(KpiRedmine, KpiRedmineAdmin)
admin.site.register(NagiosNotifications, NagiosAdmin)
admin.site.register(CountNotifications, CountNotificationsAdmin)
