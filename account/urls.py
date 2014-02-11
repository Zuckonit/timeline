from django.conf.urls import patterns, url
from views import _login, _logout, _register, _update_profile, show_user_profile


urlpatterns = patterns('',
    # Examples:
    url(r'^login/$', _login),
    url(r'^logout/$', _logout),
    url(r'^register/$', _register),
    url(r'^update_profile/$', _update_profile),
    url(r'^profile/$', show_user_profile),
)
