#encoding:utf-8
from django.conf.urls import patterns, include, url

from apps.account.urls import account_urls
from apps.process_admin.urls import process_admin_urls
from apps.actions_log.urls import actions_log_urls
from apps.production_orders.urls import production_orders_urls
from apps.payroll.urls import payroll_urls
from apps.pdfmodule.urls import pdfmodule_urls
from apps.inventory.urls import inventory_urls
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apps.website.views.home', name='home'),
    url(r'^conozca-destaju$', 'apps.website.views.description', name='description'),
    url(r'^cuenta/', include(account_urls)),
    url(r'^administracion/', include(process_admin_urls)),
    url(r'^historial/', include(actions_log_urls)),
    url(r'^ordenes-de-produccion/', include(production_orders_urls)),
    url(r'^nomina/', include(payroll_urls)),
    url(r'^pdf/', include(pdfmodule_urls)),
    url(r'^almacen/', include(inventory_urls)),
    url(r'^ajax/editinline$', 'apps.website.views.ajax_edit_in_line', name="edit_in_line"),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

# try:
#     from django.conf.urls.defaults import handler500
# except:
#     from django.conf.urls import handler500
# handler500 = "apps.website.views.server_error"