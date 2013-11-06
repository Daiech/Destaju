from django.conf.urls import patterns, url


discounts = patterns('apps.payroll.views',
    url(r'^listar-descuentos-aplicados/$', 'list_discounts_applied', name="list_discounts_applied"),
    url(r'^ver-descuentos-aplicados/(?P<id_user>[0-9]+)', 'read_discounts_applied', name="read_discounts_applied"),
    url(r'^aplicar-descuento/(?P<id_user>[0-9]+)', 'create_discount_applied', name="create_discount_applied"),
    url(r'^editar-descuento-aplicado/(?P<id_discount_applied>[0-9]+)', 'update_discount_applied', name="update_discount_applied"),
    url(r'^eliminar-descuento-aplicado/(?P<id_discount_applied>[0-9]+)', 'delete_discount_applied', name="delete_discount_applied")
)

payroll = patterns('apps.payroll.views',
    url(r'^nomina-actual/$', 'list_payroll', name="list_payroll"),
    url(r'^listar-pdf/$', 'pdf_payroll_list', name="pdf_payroll_list"),
    url(r'^guardar-nomina/$', 'set_payroll', name="set_payroll"),
    url(r'^listar-nomina/$', 'show_payroll_list', name="show_payroll_list"),
    url(r'^ver-nomina/(?P<payroll_pk>[0-9]+)', 'read_payroll', name="read_payroll"),
    url(r'^generar-pdf-nomina/(?P<payroll_pk>[0-9]+)', 'generate_pdf_payroll', name="generate_pdf_payroll"),
)

increases = patterns('apps.payroll.views',
    url(r'^listar-aumentos-aplicados/$', 'list_increases_applied', name="list_increases_applied"),
    url(r'^ver-aumentos-aplicados/(?P<id_user>[0-9]+)', 'read_increases_applied', name="read_increases_applied"),
    url(r'^aplicar-aumento/(?P<id_user>[0-9]+)', 'create_increase_applied', name="create_increase_applied"),
    url(r'^editar-aumento-aplicado/(?P<id_increase_applied>[0-9]+)', 'update_increase_applied', name="update_increase_applied"),
    url(r'^eliminar-aumento-aplicado/(?P<id_increase_applied>[0-9]+)', 'delete_increase_applied', name="delete_increase_applied")
)

payroll_urls = discounts + payroll + increases