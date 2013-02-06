from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from monitoring.webui.models import Announcement


# Customize the Announcement model
class AnnouncementAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Hero Unit', {
            'fields': ('hero_unit_title', 'hero_unit_desc')
        }),
        ('Announcement', {
            'fields': ('title', 'content', ('is_enabled', 'show_hero_unit'))
        }),
        )
    list_display = ('title', 'is_enabled', 'created_on')
    list_display_links = ('created_on', 'title')
    ordering = ['-created_on']
    list_filter = ('is_enabled',)
    search_fields = ['title']


# Customize the User model admin
UserAdmin.list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'date_joined')
UserAdmin.list_editable = ('is_active', 'is_staff')
UserAdmin.ordering = ['-date_joined']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Announcement, AnnouncementAdmin)