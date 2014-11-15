from django.conf.urls import patterns, url


inventory = patterns('apps.inventory.views',
    url(r'^listar-inventario/$', 'list_inventory', name="list_inventory"),
    url(r'^listar-historial-item/$', 'list_item_history', name="list_item_history"),
    url(r'^listar-ordenes-de-proveedores', 'list_provider_order', name="list_provider_order"),
    url(r'^aprobar-orden-proveedor', 'approve_provider_order', name="approve_provider_order"),
    url(r'^rechazar-orden-proveedor', 'reject_provider_order', name="reject_provider_order"),
    url(r'^listar-ordenes-de-empleados', 'list_employed_order', name="list_employed_order"),
    url(r'^aprobar-orden-empleados', 'approve_employed_order', name="approve_employed_order"),
    url(r'^rechazar-orden-empleados', 'reject_employed_order', name="reject_employed_order"),
)


inventory_urls = inventory
