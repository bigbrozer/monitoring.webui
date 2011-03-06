# Adding models to Admin site for Highlights app

from django.contrib import admin
from optools.apps.highlights.models import Project, Highlight

class ProjectAdmin(admin.ModelAdmin):
	list_display = ('name',)

class HighlightAdmin(admin.ModelAdmin):
	list_display = ('date', 'title', 'project')
	list_filter = ('date',)
	search_fields = ('title', 'description')
	date_hierarchy = 'date'
	ordering = ('-date',)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Highlight, HighlightAdmin)
