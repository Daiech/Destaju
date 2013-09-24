from django.conf.urls import patterns, url


users = patterns('apps.process_admin.views',
    url(r'^lista-de-usuarios/$', 'admin_users', name="admin_users"),
    url(r'^editar-usuario/(?P<id_user>[0-9]+)/$', 'update_user', name="update_user"),
    url(r'^eliminar-usuario/(?P<id_user>[0-9]+)/$', 'delete_user', name="delete_user"),
    url(r'^ver-usuario/(?P<id_user>[0-9]+)/$', 'read_user', name="read_user"),
)

activities = patterns('apps.process_admin.views',
    url(r'^agregar-actividad$', 'create_activity', name="create_activity"),
    url(r'^editar-actividad/(?P<id_activity>[0-9]+)', 'update_activity', name="update_activity"),
    url(r'^eliminar-actividad/(?P<id_activity>[0-9]+)', 'delete_activity', name="delete_activity")
)

legal_discounts = patterns('apps.process_admin.views',
    url(r'^descuentos-legales$', 'create_legal_discounts', name="create_legal_discounts"),
    url(r'^editar-descuento-legal/(?P<id_legal_discount>[0-9]+)', 'update_legal_discount', name="update_legal_discount"),
    url(r'^eliminar-descuento-legal/(?P<id_legal_discount>[0-9]+)', 'delete_legal_discount', name="delete_legal_discount")
)

general_discounts = patterns('apps.process_admin.views',
    url(r'^descuentos-generales$', 'create_general_discounts', name="create_general_discounts"),
    url(r'^editar-descuento-general/(?P<id_general_discount>[0-9]+)', 'update_general_discount', name="update_general_discount"),
    url(r'^eliminar-descuento-general/(?P<id_general_discount>[0-9]+)', 'delete_general_discount', name="delete_general_discount")
)

places = patterns('apps.process_admin.views',
    url(r'^lugares$', 'create_places', name="create_places"),
    url(r'^editar-lugar/(?P<id_place>[0-9]+)', 'update_place', name="update_place"),
    url(r'^eliminar-lugar/(?P<id_place>[0-9]+)', 'delete_place', name="delete_place")
)

tools = patterns('apps.process_admin.views',
    url(r'^herramientas$', 'create_tools', name="create_tools"),
    url(r'^editar-herramienta/(?P<id_tool>[0-9]+)', 'update_tool', name="update_tool"),
    url(r'^eliminar-herramienta/(?P<id_tool>[0-9]+)', 'delete_tool', name="delete_tool")
)

process_admin_urls = users + activities + legal_discounts + general_discounts + places + tools
