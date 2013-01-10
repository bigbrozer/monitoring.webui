# Adding models to Admin site for Nagios app

from django.contrib import admin
from apps.nagios.models import Satellite, SecurityPort

class SatelliteAdmin(admin.ModelAdmin):
    list_display = ('name', 'active', 'alias', 'fqdn', 'ip_address')
    list_filter = ('active',)
    fieldsets = (
        (None, {
            'fields': ('name', 'active')
        }),
        ('Network settings', {
            'fields': ('ip_address', 'alias', 'fqdn')
        }),
        ('Livestatus settings', {
            'classes': ('collapse',),
            'fields': ('live_port', 'nagios_url')
        }),
    )


class SecurityPortAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'protocol', 'begin_port', 'end_port')
    fieldsets = (
        ('Indentity', {
            'fields': ('name', 'description', 'protocol')
        }),
        ('Range', {
            'fields': ('begin_port', 'end_port')
        }),
    )


admin.site.register(Satellite, SatelliteAdmin)
admin.site.register(SecurityPort, SecurityPortAdmin)

