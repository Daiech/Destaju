from django.conf.urls import patterns, url


generation_of_production_order = patterns('apps.production_orders.views',
    url(r'^ordenes-de-produccion/$', 'create_production_order', name="create_production_order"),
    url(r'^editar-orden-de-produccion/(?P<id_production_order>[0-9]+)', 'update_production_order', name="update_production_order"),
    url(r'^eliminar-orden-de-produccion/(?P<id_production_order>[0-9]+)', 'delete_production_order', name="delete_production_order"),
    url(r'^generar-pdf/(?P<id_production_order>[0-9]+)', 'generate_pdf', name="generate_pdf")
)

filling = patterns('apps.production_orders.views',
    url(r'^llenado_de_op/$', 'filling_pro_ord', name="filling_pro_ord"),
    url(r'^llenar/(?P<id_production_order>[0-9]+)$', 'filling', name="filling"),
)
 
qualification = patterns('apps.production_orders.views',
    url(r'^calificacion_de_op/$', 'qualification_pro_ord', name="qualification_pro_ord"),
    url(r'^calificar/(?P<id_production_order>[0-9]+)$', 'qualification', name="qualification"),
)

approval = patterns('apps.production_orders.views',
    url(r'^aprobacion_de_op/$', 'approval_pro_ord', name="approval_pro_ord"),
    url(r'^aprobar/(?P<id_production_order>[0-9]+)$', 'approval', name="approval"),
)

list_pro_ord = patterns('apps.production_orders.views',
    url(r'^consultar_op/$', 'list_production_orders', name="list_production_orders"),
    url(r'^ver_op/(?P<id_production_order>[0-9]+)$', 'show_production_order_ajax', name="show_production_order_ajax"),
)



production_orders_urls = generation_of_production_order + filling + qualification + list_pro_ord + approval
