from django.contrib import admin

from apps.emailmodule.models import *


class emailAdmin(admin.ModelAdmin):
    list_display = ('name', 'email_type', 'description', 'admin_type')


class emailAdminTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class emailGlobalPermissionsAdmin(admin.ModelAdmin):
    list_display = ('id_email_type', 'id_user', 'is_active')


admin.site.register(email, emailAdmin)
admin.site.register(email_admin_type, emailAdminTypeAdmin)
admin.site.register(email_global_permissions, emailGlobalPermissionsAdmin)
