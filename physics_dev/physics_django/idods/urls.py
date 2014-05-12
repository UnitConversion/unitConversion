from django.conf.urls.defaults import patterns, url

from physics_django.idods.views import (retrieveVendorWS, saveVendorWS, updateVendorWS)
from physics_django.idods.views import (retrieveCompntTypePropTypeWS, saveCompntTypePropTypeWS, updateCmpntTypePropTypeWS)
from physics_django.idods.views import (retrieveCompntTypeWS, saveCompntTypeWS, updateCmpntTypeWS)
from physics_django.idods.views import (retrieveInventoryWS, saveInventoryWS, updateInventoryWS)
from physics_django.idods.views import (retrieveInventoryPropTmpltWS, saveInventoryPropTmpltWS, updateInventoryPropTmpltWS)
from physics_django.idods.views import (retrieveInstallWS, saveInstallWS, updateInstallWS)
from physics_django.idods.views import (retrieveInstallRelWS, saveInstallRelWS, updateInstallRelWS, deleteInstallRelWS)
from physics_django.idods.views import (retrieveInstallRelPropTypeWS, saveInstallRelPropTypeWS, updateInstallRelPropTypeWS)
from physics_django.idods.views import (retrieveInventoryToInstallWS, saveInventoryToInstallWS, updateInventoryToInstallWS, deleteInventoryToInstallWS)
from physics_django.idods.views import (retrieveDataMethodWS, saveDataMethodWS, updateDataMethodWS)
from physics_django.idods.views import (retrieveRawDataWS, saveRawDataWS)
from physics_django.idods.views import (retrieveOfflineDataWS, retrieveOfflineDataInstallWS, saveOfflineDataWS, updateOfflineDataWS, deleteOfflineDataWS)
from physics_django.idods.views import (uploadFileWS)
from physics_django.idods.views import (retrieveOnlineDataWS, saveOnlineDataWS, updateOnlineDataWS, deleteOnlineDataWS)
from physics_django.idods.views import (testAuth, saveIdWs)
from physics_django.idods.views import (idodsInstallWS)
from physics_django.idods.views import (retrieveTreesWS)
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

    # Retrieve, save and update install
    url(r'^id/device/install/$', retrieveInstallWS),
    url(r'^id/device/saveinstall/$', saveInstallWS),
    url(r'^id/device/updateinstall/$', updateInstallWS),

    # Retrieve, save, update and delete install rel
    url(r'^id/device/installrel/$', retrieveInstallRelWS),
    url(r'^id/device/saveinstallrel/$', saveInstallRelWS),
    url(r'^id/device/updateinstallrel/$', updateInstallRelWS),
    url(r'^id/device/deleteinstallrel/$', deleteInstallRelWS),

    # Retrieve, save and update install rel property type
    url(r'^id/device/installrelproptype/$', retrieveInstallRelPropTypeWS),
    url(r'^id/device/saveinstallrelproptype/$', saveInstallRelPropTypeWS),
    url(r'^id/device/updateinstallrelproptype/$', updateInstallRelPropTypeWS),
    
    # Retrieve, save and update inventory to install
    url(r'^id/device/inventorytoinstall/$', retrieveInventoryToInstallWS),
    url(r'^id/device/saveinventorytoinstall/$', saveInventoryToInstallWS),
    url(r'^id/device/updateinventorytoinstall/$', updateInventoryToInstallWS),
    url(r'^id/device/deleteinventorytoinstall/$', deleteInventoryToInstallWS),
    
    # Retrieve, save and update data method
    url(r'^id/device/datamethod/$', retrieveDataMethodWS),
    url(r'^id/device/savedatamethod/$', saveDataMethodWS),
    url(r'^id/device/updatedatamethod/$', updateDataMethodWS),
    
    # Retrieve, save raw data
    url(r'^id/device/rawdata/$', retrieveRawDataWS),
    url(r'^id/device/saverawdata/$', saveRawDataWS),
    
    # Retrieve, save and update offline data
    url(r'^id/device/offlinedata/$', retrieveOfflineDataWS),
    url(r'^id/device/offlinedatainstall/$', retrieveOfflineDataInstallWS),
    url(r'^id/device/saveofflinedata/$', saveOfflineDataWS),
    url(r'^id/device/updateofflinedata/$', updateOfflineDataWS),
    url(r'^id/device/deleteofflinedata/$', deleteOfflineDataWS),
    
    # Retrieve, save big file
    url(r'^id/device/file/$', uploadFileWS),
    
    # Retrieve, save and update online data
    url(r'^id/device/onlinedata/$', retrieveOnlineDataWS),
    url(r'^id/device/saveonlinedata/$', saveOnlineDataWS),
    url(r'^id/device/updateonlinedata/$', updateOnlineDataWS),
    url(r'^id/device/deleteonlinedata/$', deleteOnlineDataWS),
    
    # Idods install
    url(r'^id/device/idods_install/$', idodsInstallWS),
    
    # Make tree
    url(r'^id/device/trees/$', retrieveTreesWS),
    
    # Test authentication
    url(r'^id/device/test/$', testAuth),
    
    # Save Insertion device
    url(r'^id/device/saveid/$', saveIdWs),
    
    url(r'^id/web/device/$', idodsIndexHtml),
    url(r'^id/web/device/(.+)', idodsHtmls),
)
