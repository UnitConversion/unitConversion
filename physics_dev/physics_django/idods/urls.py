from django.conf.urls.defaults import patterns, url

from physics_django.idods.views import (retrieveVendorWS, saveVendorWS, updateVendorWS)
from physics_django.idods.views import (retrieveCompntTypePropTypeWS, saveCompntTypePropTypeWS, updateCmpntTypePropTypeWS)
from physics_django.idods.views import (retrieveCompntTypeWS, saveCompntTypeWS, updateCmpntTypeWS)
from physics_django.idods.views import (retrieveInventoryWS, saveInventoryWS, updateInventoryWS)
from physics_django.idods.views import (retrieveInventoryPropTmpltWS, saveInventoryPropTmpltWS, updateInventoryPropTmpltWS)
from physics_django.idods.views import (idodsIndexHtml, idodsHtmls)

urlpatterns = patterns(
    '',

    # Retrieve, save and update vendor
    url(r'^id/device/vendor/$', retrieveVendorWS),
    url(r'^id/device/savevendor/$', saveVendorWS),
    url(r'^id/device/updatevendor/$', updateVendorWS),

    # Retrieve, save and update component type
    url(r'^id/device/cmpnttype/$', retrieveCompntTypeWS),
    url(r'^id/device/savecmpnttype/$', saveCompntTypeWS),
    url(r'^id/device/updatecmpnttype/$', updateCmpntTypeWS),

    # Retrieve, save and update component type property type
    url(r'^id/device/cmpnttypeproptype/$', retrieveCompntTypePropTypeWS),
    url(r'^id/device/savecmpnttypeproptype/$', saveCompntTypePropTypeWS),
    url(r'^id/device/updatecmpnttypeproptype/$', updateCmpntTypePropTypeWS),

    # Retrieve, save and update inventory
    url(r'^id/device/inventory/$', retrieveInventoryWS),
    url(r'^id/device/saveinventory/$', saveInventoryWS),
    url(r'^id/device/updateinventory/$', updateInventoryWS),

    # Retrieve, save and update inventory property template
    url(r'^id/device/inventoryproptmplt/$', retrieveInventoryPropTmpltWS),
    url(r'^id/device/saveinventoryproptmplt/$', saveInventoryPropTmpltWS),
    url(r'^id/device/updateinventoryproptmplt/$', updateInventoryPropTmpltWS),
    
    url(r'^id/web/$', idodsIndexHtml),
    url(r'^id/web/.+', idodsHtmls),
)
