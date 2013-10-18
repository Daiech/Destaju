from django.conf.urls import patterns, url


discounts = patterns('apps.payroll.views',
    url(r'^listar-descuentos-aplicados/$', 'list_discounts_applied', name="list_discounts_applied"),
    url(r'^ver-descuentos-aplicados/(?P<id_user>[0-9]+)', 'read_discounts_applied', name="read_discounts_applied"),
    url(r'^aplicar-descuento/(?P<id_user>[0-9]+)', 'create_discount_applied', name="create_discount_applied"),
    url(r'^editar-descuento-aplicado/(?P<id_discount_applied>[0-9]+)', 'update_discount_applied', name="update_discount_applied"),
    url(r'^eliminar-descuento-aplicado/(?P<id_discount_applied>[0-9]+)', 'delete_discount_applied', name="delete_discount_applied")
)

payroll = patterns('apps.payroll.views',
    url(r'^listar-nomina/$', 'list_payroll', name="list_payroll"),
)

payroll_urls = discounts + payroll