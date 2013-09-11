from django.conf.urls.defaults import patterns, url

from physics_django.magnets.views import (magnetdevicesweb, magnets_help, magnets_home, magnets_content_home, magnets_content_search, magnets_content_list, magnets_content_details, systemlistweb, conversionweb) 
from physics_django.magnets.views import (magnetdevices, systemlist, conversion) 

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
    url(r'^magnets/web/$',
        magnets_home,
        name='magnets_home'),
	url(r'^magnets/web/index.html$',
        magnets_home,
        name='magnets_home'),
	url(r'^magnets/web/content.html$',
        magnets_content_home,
        name='magnets_content_home'),
	url(r'^magnets/web/search.html$',
        magnets_content_search,
        name='magnets_content_search'),
	url(r'^magnets/web/list.html$',
        magnets_content_list,
        name='magnets_content_list'),
	url(r'^magnets/web/details.html$',
        magnets_content_details,
        name='magnets_content_details'),

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
