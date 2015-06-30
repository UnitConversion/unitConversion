from django.conf.urls import patterns, url

from user.views import (user_login, user_logout)

# Url paterns for logging in and logging out
urlpatterns = patterns(
    '',
    url(r'^user/login/$',
        user_login,
        name='login'),
    url(r'^user/logout/$',
        user_logout,
        name='logout'),
)
