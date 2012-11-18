# Adding models to Admin site for kb app

from django.contrib import admin
from apps.kb.models import Procedure


class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('namespace', 'rating', 'comment', 'is_written', 'author', 'last_modified')
    list_editable = ('rating', 'comment')
    list_filter = ('rating', 'is_written')
    search_fields = ['namespace']
    ordering = ['-last_modified']

admin.site.register(Procedure, ProcedureAdmin)

