from django.conf.urls import patterns, url


users =patterns('apps.process_admin.views',
    url(r'^lista-de-usuarios$', 'admin_users', name="read_users"),
    url(r'^crear-usuario$', 'admin_users', name="create_user"),
    url(r'^editar-usuario$', 'admin_users', name="update_user"),
    url(r'^eliminar-usuario$', 'admin_users', name="delete_user"),
    url(r'^ver-usuario$', 'admin_users', name="read_user"),
    # url(r'^', , name=""),
    # url(r'^password/reset/done/$', 'password_reset_done2', name="password_reset_done2"),
    # url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm2', name="password_reset_confirm2"),
    # url(r'^password/done/$', 'password_reset_complete2', name="password_reset_complete2"),
    # url(r'^activate/(?P<activation_key>[-\w]+)/invited(?P<is_invited>.*)', 'confirm_account', name="confirm_account"),
    # url(r'^activate/(?P<activation_key>[-\w]+)', 'activate_account', name="activate_account"),
)

activities = patterns('apps.process_admin.views',
    url(r'^agregar_actividad$', 'create_activity', name="create_activity"),
    url(r'^editar_actividad/(?P<id_activity>[0-9]*)', 'update_activity', name="update_activity"),
)
process_admin_urls = users + activities
