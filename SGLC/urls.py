from django.conf.urls import patterns, include, url
from apps.account.urls import account_urls
from apps.process_admin.urls import process_admin_urls
from apps.actions_log.urls import actions_log_urls
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
print actions_log_urls
urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'apps.website.views.home', name='home'),
    url(r'^cuenta/', include(account_urls)),
    url(r'^administracion/', include(process_admin_urls)),
    url(r'^historial/', include(actions_log_urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
