from django.conf.urls import patterns, url


users = patterns('apps.process_admin.views',
    url(r'^lista-de-usuarios/$', 'read_users', name="read_users"),
    url(r'^crear-usuario/$', 'create_user', name="create_user"),
    url(r'^editar-usuario/(?P<id_user>[0-9]+)/$', 'update_user', name="update_user"),
    url(r'^eliminar-usuario/(?P<id_user>[0-9]+)/$', 'delete_user', name="delete_user"),
    url(r'^ver-usuario/(?P<id_user>[0-9]+)/$', 'read_user', name="read_user"),
)

activities = patterns('apps.process_admin.views',
    url(r'^agregar_actividad$', 'create_activity', name="create_activity"),
    url(r'^editar-actividad/(?P<id_activity>[0-9]+)', 'update_activity', name="update_activity"),
    url(r'^eliminar-actividad/(?P<id_activity>[0-9]+)', 'delete_activity', name="delete_activity")
)
process_admin_urls = users + activities
