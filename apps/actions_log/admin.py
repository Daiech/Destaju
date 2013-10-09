#encoding:utf-8
from django.contrib import admin

from apps.actions_log.models import *

admin.site.register(actions)
admin.site.register(UpdateTables) 

