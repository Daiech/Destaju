from django.conf.urls import url, patterns
actions_log_urls = patterns('apps.actions_log.views',
	# url(r'^pdf', 'actions_log.views.getPDF', name='getPDF'),
    url(r'^user/(?P<username>[-\w]+)/order/(?P<field>[-\w]+)$', 'showUserActionsOrder', name='user_actions_order'),
    url(r'^order/(?P<field>[-\w]+)$', 'showOrderActions', name='order_actions'),
    url(r'^action/(?P<id_action>[-\w]+)$', 'showAction', name='order_actions'),
    url(r'^views$', 'showViewsLog', name='views_log'),
    url(r'^viewsstats$', 'showViewsStats', name='views_stats'),
    url(r'^modificaciones$', 'read_modifications', name='read_modifications'),
    url(r'^(?P<username>[-\w]+)', 'showUserActions', name='user_actions'),
    url(r'^$', 'showActions', name='actions'),
)
