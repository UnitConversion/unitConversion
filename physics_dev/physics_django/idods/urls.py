from django.conf.urls.defaults import patterns, url

from physics_django.idods.views import (retrieveVendorWS, saveVendorWS, updateVendorWS)
from physics_django.idods.views import (idodsIndexHtml, idodsHtmls)

urlpatterns = patterns(
    '',

    # Retrieve, save and update vendor
    url(r'^id/device/vendor/$', retrieveVendorWS),
    url(r'^id/device/savevendor/$', saveVendorWS),
    url(r'^id/device/updatevendor/$', updateVendorWS),
    
    url(r'^id/web/$', idodsIndexHtml),
    url(r'^id/web/.+', idodsHtmls),
)
