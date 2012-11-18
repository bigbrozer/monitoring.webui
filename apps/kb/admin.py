# Adding models to Admin site for kb app

# Django imports
from django.contrib import admin
from django.forms import Textarea
from django.db import models

# Models imports
from apps.kb.models import Procedure


class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('namespace', 'rating', 'comment', 'validated', 'is_written', 'author', 'last_modified')
    list_filter = ('rating', 'validated', 'is_written')
    radio_fields = {"rating": admin.VERTICAL}
    search_fields = ['^namespace']
    list_per_page = 20
    ordering = ['-last_modified', 'is_written']

    actions = [
        'rate_bad',
        'rate_average',
        'rate_good',
        'rate_excellent'
    ]

    # Overrides fields
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':20})},
    }

    # Disable delete_selected action
    def get_actions(self, request):
        actions = super(ProcedureAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # Rating Actions
    def rate_as(self, request, queryset, rating, mark):
        """Base for Admin action to rate selected procedures."""
        rows_updated = queryset.update(rating=rating, validated=True)
        if rows_updated == 1:
            message_bit = "1 procedure was"
        else:
            message_bit = "%s procedures were" % rows_updated
        self.message_user(request, "%s successfully rated as %s." % (message_bit, mark))

    def rate_bad(self, request, queryset):
        """Admin action to rate selected procedures as bad."""
        self.rate_as(request, queryset, -2, 'bad')
    rate_bad.short_description = 'Rate as Bad'

    def rate_average(self, request, queryset):
        """Admin action to rate selected procedures as average."""
        self.rate_as(request, queryset, -1, 'average')
    rate_average.short_description = 'Rate as Average'

    def rate_good(self, request, queryset):
        """Admin action to rate selected procedures as good."""
        self.rate_as(request, queryset, 0, 'good')
    rate_good.short_description = 'Rate as Good'

    def rate_excellent(self, request, queryset):
        """Admin action to rate selected procedures as excellent."""
        self.rate_as(request, queryset, 1, 'excellent')
    rate_excellent.short_description = 'Rate as Excellent'


# Register in admin site
admin.site.register(Procedure, ProcedureAdmin)

