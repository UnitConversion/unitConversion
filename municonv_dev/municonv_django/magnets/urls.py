from django.conf.urls.defaults import patterns, url

from municonv_django.magnets.views import (magnetdevicesweb, magnets_help, systemlistweb, conversionweb) 
from municonv_django.magnets.views import (magnetdevices, systemlist, conversion) 

urlpatterns = patterns(
    '',
    url(r'^magnets/web/devices/$',
        magnetdevicesweb,
        name='magnetdevicesweb'),
    url(r'^magnets/web/system/$',
        systemlistweb,
        name='system'),
    url(r'^magnets/web/magnets_help.html',
        magnets_help,
        name='magnets_help'),
    url(r'^magnets/web/conversion/$',
        conversionweb,
        name='conversionweb'),

    # return raw data not thru html ui
    url(r'^magnets/devices/$',
        magnetdevices,
        name='magnetdevices'),
    url(r'^magnets/system/$',
        systemlist,
        name='system'),
    url(r'^magnets/conversion/$',
        conversion,
        name='conversion'),
)
