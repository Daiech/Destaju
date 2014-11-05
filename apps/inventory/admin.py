from django.contrib import admin

from .models import *

admin.site.register(Inventory)
admin.site.register(ProviderOrder)
admin.site.register(QuantityProviderTool)
admin.site.register(EmployedOrder)
admin.site.register(QuantityEmployedTool)
