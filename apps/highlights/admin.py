# Adding models to Admin site for Highlights app

from django.contrib import admin
from optools.apps.highlights.models import Project, Highlight
from optools.apps.highlights.actions import export_as_csv_action

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name',)

class HighlightAdmin(admin.ModelAdmin):
	list_display = ('date', 'title', 'project')
	list_filter = ('date',)
	search_fields = ('title', 'description')
	date_hierarchy = 'date'
	ordering = ('-date',)
	actions = [
		export_as_csv_action("Export selected highlights as Excel file", fields=[
			'date',
			'title',
			'project',
			'description',
		], header=True),
	]

admin.site.register(Project, ProjectAdmin)
admin.site.register(Highlight, HighlightAdmin)
