from django.conf.urls.defaults import patterns, url

from physics_django.activeinterlock.views import (activeinterlock) 

urlpatterns = patterns(
    '',
    url(r'^activeinterlock/$',
        activeinterlock,
        name='activeinterlock'),
)
