from django.contrib import admin

from apps.process_admin.models import *


class EmploymentsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active')


class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_permissions', 'is_active')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "dni", "phone", "cell_phone", "date_born", "city", "user_type", "is_active_worker")


class PermissionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'user_types', 'is_active')


admin.site.register(Employments, EmploymentsAdmin)
admin.site.register(UserType, UserTypeAdmin)
admin.site.register(Permissions, PermissionsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Activities)