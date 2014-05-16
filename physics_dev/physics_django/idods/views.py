from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.http import require_http_methods
import traceback
import sys
from django.db import connection, transaction
from django.db.transaction import TransactionManagementError
from django.template import RequestContext
from utils.timer import Timer

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from authentication import has_perm_or_basicauth
from pyidods.idods import (idods)

# Init idods
idodsi = idods(connection, transaction)

from _mysql_exceptions import MySQLError

from pyidods.logger import _setup_idods_logger
idods_log = _setup_idods_logger('idods')

from utils.utils import _checkkeys, _retrievecmddict

'''
Private template for the retrieve functions
'''
def _retrieveData(request, fun, propList, customDict = {}):
    params = _retrievecmddict(request.GET.copy())
    res = {}
    
    try:
        _checkkeys(params.keys(), propList)
        res = fun(**dict(customDict, **params))
    
    except TypeError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except ValueError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except MySQLError as e:
        idods_log.exception(e)
        return HttpResponseServerError(HttpResponse(content=e))
    
    except Exception as e:
        idods_log.exception(e)
        raise e
    
    return HttpResponse(json.dumps(res), mimetype="application/json")

'''
Private template for save function
'''
def _saveData(request, fun, propList):
    params = _retrievecmddict(request.POST.copy())
    res = {}
    
    try:
        _checkkeys(params.keys(), propList)
        res = fun(**params)
        transaction.commit_unless_managed()
    
    except TypeError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except ValueError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except MySQLError as e:
        idods_log.exception(e)
        return HttpResponseServerError(HttpResponse(content=e))
    
    except TransactionManagementError as e:
        idods_log.exception(e)
        transaction.rollback_unless_managed()
        return HttpResponseServerError(HttpResponse(content=e))
    
    except Exception as e:
        idods_log.exception(e)
        raise e
    
    return HttpResponse(json.dumps(res), mimetype="application/json")

'''
Private template for update function
'''
def _updateData(request, fun, propList, customDict = {}):
    params = _retrievecmddict(request.POST.copy())
    res = {}
    
    try:
        _checkkeys(params.keys(), propList)
        res = fun(**dict(customDict, **params))
        transaction.commit_unless_managed()
    
    except TypeError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except ValueError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except MySQLError as e:
        idods_log.exception(e)
        return HttpResponseServerError(HttpResponse(content=e))
    
    except TransactionManagementError as e:
        idods_log.exception(e)
        transaction.rollback_unless_managed()
        return HttpResponseServerError(HttpResponse(content=e))
    
    except Exception as e:
        idods_log.exception(e)
        raise e
    
    return HttpResponse(json.dumps(res), mimetype="application/json")

'''
Retrieve vendor information
'''
@require_http_methods(["GET"])
def retrieveVendorWS(request):
    return _retrieveData(request, idodsi.retrieveVendor, ['name', 'description'])

'''
Save new vendor
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveVendorWS(request):
    return _saveData(request, idodsi.saveVendor, ['name', 'description'])

'''
Update vendor
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateVendorWS(request):
    return _updateData(request, idodsi.updateVendor, ['old_name', 'name', 'description'], {'vendor_id': None})

'''
Retrieve component type
'''
@require_http_methods(["GET"])
def retrieveCompntTypeWS(request):
    return _retrieveData(request, idodsi.retrieveComponentType, ['name', 'description', 'all_cmpnt_types'])

'''
Save component type
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveCompntTypeWS(request):
    return _saveData(request, idodsi.saveComponentType, ['name', 'description', 'props'])

'''
Update component type
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateCmpntTypeWS(request):
    return _updateData(request, idodsi.updateComponentType, ['old_name', 'name', 'description', 'props'], {'component_type_id': None})

'''
Retrieve component type property type
'''
@require_http_methods(["GET"])
def retrieveCompntTypePropTypeWS(request):
    return _retrieveData(request, idodsi.retrieveComponentTypePropertyType, ['name'])

'''
Save component type property type
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveCompntTypePropTypeWS(request):
    return _saveData(request, idodsi.saveComponentTypePropertyType, ['name', 'description'])

'''
Update component type property type
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateCmpntTypePropTypeWS(request):
    return _updateData(request, idodsi.updateComponentTypePropertyType, ['old_name', 'name', 'description'], {'property_type_id': None})

'''
Retrieve inventory
'''
@require_http_methods(["GET"])
def retrieveInventoryWS(request):
    return _retrieveData(request, idodsi.retrieveInventory, ['name'])

'''
Save inventory
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInventoryWS(request):
    return _saveData(request, idodsi.saveInventory, ['cmpnt_type', 'name', 'alias', 'serialno', 'vendor', 'props'])

'''
Update inventory
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInventoryWS(request):
    return _updateData(request, idodsi.updateInventory, ['old_name', 'cmpnt_type', 'name', 'alias', 'serialno', 'vendor', 'props'], {'inventory_id': None})

'''
Retrieve inventory property template
'''
@require_http_methods(["GET"])
def retrieveInventoryPropTmpltWS(request):
    return _retrieveData(request, idodsi.retrieveInventoryPropertyTemplate, ['name'])

'''
Save inventory property template
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInventoryPropTmpltWS(request):
    return _saveData(request, idodsi.saveInventoryPropertyTemplate, ['cmpnt_type', 'name', 'description', 'default', 'unit'])

'''
Update inventory property template
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInventoryPropTmpltWS(request):
    return _updateData(request, idodsi.updateInventoryPropertyTemplate, ['tmplt_id', 'cmpnt_type', 'name', 'description', 'default', 'unit'])

'''
Retrieve install
'''
@require_http_methods(["GET"])
def retrieveInstallWS(request):
    return _retrieveData(request, idodsi.retrieveInstall, ['name', 'description', 'cmpnt_type', 'coordinatecenter', 'all_install'])

'''
Save install
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInstallWS(request):
    return _saveData(request, idodsi.saveInstall, ['name', 'description', 'cmpnt_type', 'coordinatecenter'])

'''
Update install
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInstallWS(request):
    return _updateData(request, idodsi.updateInstall, ['old_name', 'name', 'description', 'cmpnt_type', 'coordinatecenter'], {'install_id': None})

'''
Retrieve install rel
'''
@require_http_methods(["GET"])
def retrieveInstallRelWS(request):
    return _retrieveData(request, idodsi.retrieveInstallRel, ['parent_install', 'child_install', 'description', 'order', 'date', 'expected_property'], {'install_rel_id': None})

'''
Save install rel
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInstallRelWS(request):
    return _saveData(request, idodsi.saveInstallRel, ['parent_install', 'child_install', 'description', 'order', 'props'])

'''
Update install rel
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInstallRelWS(request):
    return _updateData(request, idodsi.updateInstallRel, ['parent_install', 'child_install', 'description', 'order', 'props'])

'''
Delete install rel
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def deleteInstallRelWS(request):
    return _updateData(request, idodsi.deleteInstallRel, ['parent_install', 'child_install'])

'''
Retrieve install rel property type
'''
@require_http_methods(["GET"])
def retrieveInstallRelPropTypeWS(request):
    return _retrieveData(request, idodsi.retrieveInstallRelPropertyType, ['name'])

'''
Save install rel property type
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInstallRelPropTypeWS(request):
    return _saveData(request, idodsi.saveInstallRelPropertyType, ['name', 'description', 'unit'])

'''
Update install rel property type
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInstallRelPropTypeWS(request):
    return _updateData(request, idodsi.updateInstallRelPropertyType, ['old_name', 'name', 'description', 'unit'], {'type_id': None})

'''
Retrieve inventory to install
'''
@require_http_methods(["GET"])
def retrieveInventoryToInstallWS(request):
    return _retrieveData(request, idodsi.retrieveInventoryToInstall, ['inventory_to_install_id', 'install_name', 'inv_name'], {'inventory_to_install_id': None})

'''
Save inventory to install
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInventoryToInstallWS(request):
    return _saveData(request, idodsi.saveInventoryToInstall, ['install_name', 'inv_name'])

'''
Update inventory to install
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInventoryToInstallWS(request):
    return _updateData(request, idodsi.updateInventoryToInstall, ['inventory_to_install_id', 'install_name', 'inv_name'])

'''
Delete inventory to install
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def deleteInventoryToInstallWS(request):
    return _updateData(request, idodsi.deleteInventoryToInstall, ['inventory_to_install_id'])

'''
Retrieve data method
'''
@require_http_methods(["GET"])
def retrieveDataMethodWS(request):
    return _retrieveData(request, idodsi.retrieveDataMethod, ['name', 'description'])

'''
Save data method
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveDataMethodWS(request):
    return _saveData(request, idodsi.saveDataMethod, ['name', 'description'])

'''
Update data method
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateDataMethodWS(request):
    return _updateData(request, idodsi.updateDataMethod, ['old_name', 'name', 'description'], {'datamethod_id': None})

'''
Retrieve raw data
'''
@require_http_methods(["GET"])
def retrieveRawDataWS(request):
    return _retrieveData(request, idodsi.retrieveRawData, ['raw_data_id'])

'''
Save raw data
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveRawDataWS(request):
    rawFile = request.FILES.getlist('file')[0]
    
    res = {}
    
    try:
        res = idodsi.saveRawData(rawFile.read())
        
        transaction.commit_unless_managed()
    
    except TypeError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except ValueError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except MySQLError as e:
        idods_log.exception(e)
        return HttpResponseServerError(HttpResponse(content=e))
    
    except TransactionManagementError as e:
        idods_log.exception(e)
        transaction.rollback_unless_managed()
        return HttpResponseServerError(HttpResponse(content=e))
    
    except Exception as e:
        idods_log.exception(e)
        raise e
    
    return HttpResponse(json.dumps(res), mimetype="application/json")

'''
Retrieve offline data
'''
@require_http_methods(["GET"])
def retrieveOfflineDataWS(request):
    return _retrieveData(request, idodsi.retrieveOfflineData, ['offlineid', 'description', 'date', 'gap', 'phase1', 'phase2', 'phase3', 'phase4', 'phasemode', 'polarmode', 'status', 'method_name', 'inventory_name'])

'''
Retrieve offline data (via install)
'''
@require_http_methods(["GET"])
def retrieveOfflineDataInstallWS(request):
    return _retrieveData(request, idodsi.retrieveInstallOfflineData, ['install_name', 'description', 'date', 'gap', 'phase1', 'phase2', 'phase3', 'phase4', 'phasemode', 'polarmode', 'status', 'method_name'])

'''
Save offline data
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveOfflineDataWS(request):
    request.POST = request.POST.copy()
    request.POST['username'] = request.user.username
    return _saveData(request, idodsi.saveOfflineData, ['inventory_name', 'username', 'description', 'gap', 'phase1', 'phase2', 'phase3', 'phase4', 'phasemode', 'polarmode', 'status', 'data_file_name', 'data_file_ts', 'data_id', 'script_name', 'script', 'method_name'])

'''
Save data method and offline data
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveDataMethodOfflineDataWS(request):
    
    with Timer() as t:
        request.POST = request.POST.copy()
        request.POST['username'] = request.user.username
        result = _saveData(request, idodsi.saveMethodAndOfflineData, ['inventory_name', 'username', 'method', 'method_desc', 'data_desc', 'data_file_name', 'data_id', 'status', 'gap', 'phase1', 'phase2', 'phase3', 'phase4', 'phase_mode', 'polar_mode'])
    print "=> elasped _saveData, idodsi.saveMethodAndOfflineData: %s s" % t.secs

    return result

'''
Update offline data
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateOfflineDataWS(request):
    request.POST = request.POST.copy()
    request.POST['username'] = request.user.username
    return _updateData(request, idodsi.updateOfflineData, ['offline_data_id', 'inventory_name', 'username', 'description', 'gap', 'phase1', 'phase2', 'phase3', 'phase4', 'phasemode', 'polarmode', 'status', 'data_file_name', 'data_file_ts', 'data_id', 'script_name', 'script', 'method_name'])

'''
Delete offline data
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def deleteOfflineDataWS(request):
    return _updateData(request, idodsi.deleteOfflineData, ['offline_data_id'])

'''
Upload a file
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def uploadFileWS(request):
    rawFile = request.FILES.getlist('file')[0]
    params = _retrievecmddict(request.POST.copy())
    
    data = ""
    
    # Go through all the chunks and assemble the file
    if(rawFile.multiple_chunks()):
        
        for chunk in rawFile.chunks():
            data += chunk
    
    else:
        data = rawFile.read()
    
    # Try saving the file
    try:
        filePath = idodsi.saveFile(params['file_name'], data)
    
        res = {
            'path': filePath['path']
        }
        return HttpResponse(json.dumps(res), mimetype="application/json")
        
    except Exception as e:
        idods_log.exception(e)
        return HttpResponseServerError(HttpResponse(content=e))

'''
Retrieve online data
'''
@require_http_methods(["GET"])
def retrieveOnlineDataWS(request):
    return _retrieveData(request, idodsi.retrieveOnlineData, ['onlineid', 'install_name', 'username', 'description', 'url', 'status'])

'''
Save online data
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveOnlineDataWS(request):
    request.POST = request.POST.copy()
    request.POST['username'] = request.user.username
    return _saveData(request, idodsi.saveOnlineData, ['install_name', 'username', 'description', 'url', 'status'])

'''
Update online data
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateOnlineDataWS(request):
    request.POST = request.POST.copy()
    request.POST['username'] = request.user.username
    return _updateData(request, idodsi.updateOnlineData, ['online_data_id', 'install_name', 'username', 'description', 'url', 'status'])

'''
Delete online data
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def deleteOnlineDataWS(request):
    return _updateData(request, idodsi.deleteOnlineData, ['online_data_id'])

'''
Install idods
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def idodsInstallWS(request):
    return _updateData(request, idodsi.idodsInstall, [])

'''
Retrieve trees
'''
@require_http_methods(["GET"])
def retrieveTreesWS(request):
    return _retrieveData(request, idodsi.retrieveTrees, ['install_name'])

'''
Test authentication
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def testAuth(request):
    return HttpResponse(json.dumps({'result': True}), mimetype="application/json")

'''
Import devices
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def importDeviceWS(request):
    return _updateData(request, idodsi.importDevice, ['line'])

'''
Save insertion device
'''
@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInsertionDeviceWS(request):
    
    with Timer() as t:
        result = _saveData(request, idodsi.saveInsertionDevice, ['install_name', 'coordinate_center', 'project', 'beamline', 'beamline_desc', 'install_desc', 'inventory_name', 'down_corrector', 'up_corrector', 'length', 'gap_max', 'gap_min', 'gap_tolerance', 'phase1_max', 'phase1_min', 'phase2_max', 'phase2_min', 'phase3_max', 'phase3_min', 'phase4_max', 'phase4_min', 'phase_tolerance', 'k_max_circular', 'k_max_linear', 'phase_mode_a1', 'phase_mode_a2', 'phase_mode_p', 'type_name', 'type_desc'])
    print "=> elasped _saveData, idodsi.saveInsertionDevice: %s s" % t.secs

    return result

'''
Load index html file
'''
def idodsIndexHtml(request):
    return render_to_response("idods/index.html", context_instance = RequestContext(request))

'''
Load html files
'''
def idodsHtmls(request, url):
    return render_to_response("idods/" + url, context_instance = RequestContext(request))