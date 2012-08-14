from django.contrib import admin

from models import Announcement


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


admin.site.register(Announcement, AnnouncementAdmin)
