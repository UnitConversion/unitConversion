from django.conf.urls.defaults import patterns, url

# from physics_django.magnets.views import (magnetdevicesweb, magnets_help, magnets_home, magnets_content_home, magnets_content_search, magnets_content_list, magnets_content_details, magnets_content_results, systemlistweb, conversionweb)
from physics_django.magnets.views import (magnetinventory, magnetinstall, systemlist, conversion)
from physics_django.magnets.views import (magnetsIndexHtml, magnetsHtmls)

urlpatterns = patterns(
    '',
    url(r'^magnets/web/$', magnetsIndexHtml),
    url(r'^magnets/web/(.+)', magnetsHtmls),

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
