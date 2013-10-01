from django.contrib import admin

from apps.production_orders.models import *

admin.site.register(ProductionOrder)
admin.site.register(FillingProOrd)
admin.site.register(QualificationProOrd)
admin.site.register(Filling)
admin.site.register(Qualifications)