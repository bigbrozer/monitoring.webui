# Adding models to Admin site for Nagios app

from django.contrib import admin
from optools.Nagios.models import Satellite

class SatelliteAdmin(admin.ModelAdmin):
	list_display = ('name', 'alias', 'fqdn', 'live_port', 'nagios_url')
	fieldsets = (
		(None, {
			'fields': ('name',)
		}),
		('Network settings', {
			'fields': ('ip_address', 'alias', 'fqdn')
		}),
		('Livestatus settings', {
			'classes': ('collapse',),
			'fields': ('live_port', 'nagios_url')
		}),
	)

admin.site.register(Satellite, SatelliteAdmin)

