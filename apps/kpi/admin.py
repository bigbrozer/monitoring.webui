"""
settings from the admin site
"""

from django.contrib import admin
from apps.kpi.models import KpiNagios, KpiRedmine
from apps.kpi.models import NagiosNotifications, CountNotifications, RecurrentAlerts, OldestAlerts
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
        'written_procedures', 'total_written', 'missing_procedures', 'total_missing',
        'linux', 'windows', 'aix', 'comment_host', 'comment_service', 'comment_procedure')
    date_hierarchy = 'date'
    ordering = ['-date']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        ('Host & Services', {'fields': ['total_host', 'comment_host', 'total_services', 'comment_service']}),
        ('Operating Systems', {'fields': ['linux', 'windows', 'aix']}),
        ('Procedures', {'fields': ['written_procedures', 'total_written', 'missing_procedures', 'total_missing', 'comment_procedure']}),
    ]

class KpiRedmineAdmin(admin.ModelAdmin):
    """
    modify default settings for kpi redmine
    """
    list_display = ('date', 'requests_opened', 'requests_closed',
        'requests_remained', 'requests_waiting', 'lifetime', 'lifetime_normal', 'lifetime_high',
        'lifetime_urgent', 'comment_lifetime')
    date_hierarchy = 'date'
    ordering = ['-date']
    actions = ['update']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        ('Requests', {'fields': ['requests_opened', 'requests_closed', 'requests_remained', 'requests_waiting']}),
        ('Lifetime', {'fields': ['requests_lifetime', 'comment_lifetime', 'requests_lifetime_normal', 'requests_lifetime_high', 'requests_lifetime_urgent']}),
    ]

    def update(self, request, queryset):
        """
        update database from selected date
        """
        from jobs.insert import insert_redmine

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
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        (None, {'fields': ['host', 'service', 'state', 'acknowledged']}),
    ]
    def update(self, request, queryset):
        """
        update database from last date
        """
        from jobs.insert import insert_nagios_notifications, get_notifications

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
        'critical_acknowledged', 'comment_notification_warning', 'comment_notification_warning_ack',
        'comment_notification_critical', 'comment_notification_critical_ack')
    date_hierarchy = 'date'
    ordering = ['-date']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        ('Warning', {'fields': ['warning', 'comment_notification_warning', 'warning_acknowledged', 'comment_notification_warning_ack']}),
        ('Critical', {'fields': ['critical', 'comment_notification_critical', 'critical_acknowledged', 'comment_notification_critical_ack']}),
    ]

class RecurrentAlertsAdmin(admin.ModelAdmin):
    """
    modify default settings for count notifications
    """
    list_display = ('date', 'host', 'service', 'frequency')
    ordering = ['-frequency']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        (None, {'fields': ['host', 'service', 'frequency']}),
    ]

class OldestAlertsAdmin(admin.ModelAdmin):
    """
    modify default settings for count notifications
    """
    list_display = ('date', 'host', 'service', 'date_error')
    date_hierarchy = 'date'
    ordering = ['date_error']
    fieldsets = [
        ('Date information',{'fields': ['date'], 'classes': ['collapse']}),
        (None, {'fields': ['host', 'service', 'date_error']}),
    ]

admin.site.register(KpiNagios, KpiNagiosAdmin)
admin.site.register(KpiRedmine, KpiRedmineAdmin)
admin.site.register(NagiosNotifications, NagiosAdmin)
admin.site.register(CountNotifications, CountNotificationsAdmin)
admin.site.register(RecurrentAlerts, RecurrentAlertsAdmin)
admin.site.register(OldestAlerts, OldestAlertsAdmin)
