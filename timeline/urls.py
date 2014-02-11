from django.conf.urls import patterns, include, url

from views import post_new_timeline, show_user_timeline
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'timeline.views.home', name='home'),
    # url(r'^timeline/', include('timeline.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('account.urls')),
    url(r'^post_new_timeline/$', post_new_timeline), 
    url(r'^blog/', show_user_timeline),
)
