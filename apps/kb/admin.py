# Adding models to Admin site for kb app

# Django imports
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.contrib import admin

# Models imports
from apps.kb.models import Procedure

# Forms imports
from apps.kb.forms import ProcedureCommentForm

class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('namespace', 'rating', 'comment', 'validated', 'is_written', 'author', 'last_modified')
    list_filter = ('rating', 'validated', 'is_written')
    list_editable = ('rating',)
    search_fields = ['^namespace']
    list_per_page = 15
    ordering = ['-last_modified', 'is_written']

    actions = ['rate_and_comment', 'unvalidate']

    # Disable delete_selected action
    def get_actions(self, request):
        actions = super(ProcedureAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    # Rating Actions
    def rate_and_comment(self, request, queryset):
        comment_form = None
        ids = []

        if 'comment' in request.POST:
            comment_form = ProcedureCommentForm(request.POST)
            if comment_form.is_valid():
                num = queryset.count()
                comment = comment_form.cleaned_data['comment']
                rating = comment_form.cleaned_data['rating']
                rating_key = dict(comment_form.fields['rating'].choices)[int(rating)]

                queryset.update(comment=comment, rating=rating)

                if num == 1:
                    message_bit = "1 procedure was"
                else:
                    message_bit = "%s procedures were" % num
                self.message_user(request, '%s rated as %s.' % (message_bit, rating_key))

                return HttpResponseRedirect(request.get_full_path())

        if '_selected_action' in request.POST:
            ids = request.POST.getlist('_selected_action')

        if not comment_form:
            comment_form = ProcedureCommentForm()

        context = {
            'title': 'Rate selected procedures',
            'section': {'kb': 'active'},
            'procedures': queryset,
            'comment_form': comment_form,
            'ids': ids,
        }

        return render_to_response(
            "kb/rate.html",
            context,
            context_instance=RequestContext(request)
        )
    rate_and_comment.short_description = 'Rate selected procedures'

    def unvalidate(self, request, queryset):
        """Admin action to unvalidate selected procedures."""
        num = queryset.count()
        queryset.update(validated=False)

        if num == 1:
            message_bit = "1 procedure was"
        else:
            message_bit = "%s procedures were" % num
        self.message_user(request, '%s unvalidated successfully.' % message_bit)
    unvalidate.short_description = 'Unvalidate selected procedures'

# Register in admin site
admin.site.register(Procedure, ProcedureAdmin)

