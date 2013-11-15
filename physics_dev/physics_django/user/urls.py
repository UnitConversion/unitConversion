from django.conf.urls.defaults import patterns, url

from physics_django.user.views import (userLogin, userLogout)

# Url paterns for logging in and logging out
urlpatterns = patterns(
    '',
    url(r'^user/login/$',
        userLogin,
        name='login'),
    url(r'^user/logout/$',
        userLogout,
        name='logout'),
)
