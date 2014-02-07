from django.conf.urls.defaults import patterns, url

from physics_django.lattice.views import (vendor)

urlpatterns = patterns(
    '',

    # Retrieve, save and update vendor
    url(r'^id/device/vendor/$', vendor),
)
