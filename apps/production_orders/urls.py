from django.conf.urls import patterns, url


generation_of_production_order = patterns('apps.production_orders.views',
    url(r'^ordenes-de-produccion$', 'create_production_order', name="create_production_order"),
    url(r'^editar-orden-de-produccion/(?P<id_production_order>[0-9]+)', 'update_production_order', name="update_production_order"),
    url(r'^eliminar-orden-de-produccion/(?P<id_production_order>[0-9]+)', 'delete_production_order', name="delete_production_order")
)

filling = patterns('apps.production_orders.views',
    url(r'^llenado_de_op$', 'filling_pro_ord', name="filling_pro_ord"),
    url(r'^llenar/(?P<id_production_order>[0-9]+)$', 'filling', name="filling"),
)
 

production_orders_urls = generation_of_production_order + filling