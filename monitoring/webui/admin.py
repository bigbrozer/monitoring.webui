from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Customize the User model admin
UserAdmin.list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'last_login', 'date_joined')
UserAdmin.list_editable = ('is_active', 'is_staff')
UserAdmin.ordering = ['-date_joined']

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
