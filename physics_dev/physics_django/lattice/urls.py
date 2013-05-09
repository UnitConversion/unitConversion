from django.conf.urls.defaults import patterns, url

from physics_django.lattice.views import (lattices, models) 

urlpatterns = patterns(
    '',
    # return raw data not thru html ui
    url(r'^lattice/$',
        lattices,
        name='lattices'),
    url(r'^lattice/model/$',
        models,
        name='model'),
)
