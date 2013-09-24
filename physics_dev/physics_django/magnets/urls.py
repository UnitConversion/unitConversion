from django.conf.urls.defaults import patterns, url

#from physics_django.magnets.views import (magnetdevicesweb, magnets_help, magnets_home, magnets_content_home, magnets_content_search, magnets_content_list, magnets_content_details, magnets_content_results, systemlistweb, conversionweb) 
from physics_django.magnets.views import (magnets_help, magnets_home, magnets_content_home, magnets_content_search, magnets_content_list, magnets_content_details, magnets_content_results, magnets_measurement_data)
from physics_django.magnets.views import (magnetinventory, magnetinstall, systemlist, conversion) 

urlpatterns = patterns(
    '',
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
	url(r'^magnets/web/results.html$',
        magnets_content_results,
        name='magnets_content_results'),
    url(r'^magnets/web/magnets_help.html',
        magnets_help,
        name='magnets_help'),
	url(r'^magnets/web/measurement_data.html',
        magnets_measurement_data,
        name='magnets_measurement_data'),

    # return raw data not thru html ui
    url(r'^magnets/inventory/$',
        magnetinventory,
        name='magnetinventory'),
    url(r'^magnets/install/$',
        magnetinstall,
        name='magnetinstall'),
    url(r'^magnets/system/$',
        systemlist,
        name='system'),
    url(r'^magnets/conversion/$',
        conversion,
        name='conversion'),
)
