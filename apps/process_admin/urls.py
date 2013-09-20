from django.conf.urls import patterns, url

process_admin_urls = patterns('apps.process_admin.views',
    url(r'^administrar_usuarios$', 'admin_users', name="admin_users"),
    url(r'^agregar_actividad$', 'create_activity', name="create_activity")
    # url(r'^', , name=""),
    # url(r'^password/reset/done/$', 'password_reset_done2', name="password_reset_done2"),
    # url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm2', name="password_reset_confirm2"),
    # url(r'^password/done/$', 'password_reset_complete2', name="password_reset_complete2"),
    # url(r'^activate/(?P<activation_key>[-\w]+)/invited(?P<is_invited>.*)', 'confirm_account', name="confirm_account"),
    # url(r'^activate/(?P<activation_key>[-\w]+)', 'activate_account', name="activate_account"),
)
