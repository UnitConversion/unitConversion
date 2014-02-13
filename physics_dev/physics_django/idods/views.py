from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.http import require_http_methods
import traceback
import sys
from django.db import connection, transaction
from django.db.transaction import TransactionManagementError

try:
    from django.utils import simplejson as json
except ImportError:
    import json

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
def saveVendorWS(request):
    return _saveData(request, idodsi.saveVendor, ['name', 'description'])

'''
Update vendor
'''
@require_http_methods(["POST"])
def updateVendorWS(request):
    return _updateData(request, idodsi.updateVendor, ['old_name', 'name', 'description'], {'vendor_id': None})

'''
Retrieve component type
'''
@require_http_methods(["GET"])
def retrieveCompntTypeWS(request):
    return _retrieveData(request, idodsi.retrieveComponentType, ['name', 'description'])

'''
Save component type
'''
@require_http_methods(["POST"])
def saveCompntTypeWS(request):
    return _saveData(request, idodsi.saveComponentType, ['name', 'description', 'props'])

'''
Update component type
'''
@require_http_methods(["POST"])
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
def saveCompntTypePropTypeWS(request):
    return _saveData(request, idodsi.saveComponentTypePropertyType, ['name', 'description'])

'''
Update component type property type
'''
@require_http_methods(["POST"])
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
def saveInventoryWS(request):
    return _saveData(request, idodsi.saveInventory, ['cmpnt_type', 'name', 'alias', 'serialno', 'vendor', 'props'])

'''
Update inventory
'''
@require_http_methods(["POST"])
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
def saveInventoryPropTmpltWS(request):
    return _saveData(request, idodsi.saveInventoryPropertyTemplate, ['cmpnt_type', 'name', 'description', 'default', 'unit'])

'''
Update inventory property template
'''
@require_http_methods(["POST"])
def updateInventoryPropTmpltWS(request):
    return _updateData(request, idodsi.updateInventoryPropertyTemplate, ['tmplt_id', 'cmpnt_type', 'name', 'description', 'default', 'unit'])

'''
Retrieve install
'''
@require_http_methods(["GET"])
def retrieveInstallWS(request):
    return _retrieveData(request, idodsi.retrieveInstall, ['name', 'description', 'cmpnt_type', 'coordinatecenter'])

'''
Save install
'''
@require_http_methods(["POST"])
def saveInstallWS(request):
    return _saveData(request, idodsi.saveInstall, ['name', 'description', 'cmpnt_type', 'coordinatecenter'])

'''
Update install
'''
@require_http_methods(["POST"])
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
def saveInstallRelWS(request):
    return _saveData(request, idodsi.saveInstallRel, ['parent_install', 'child_install', 'description', 'order', 'props'])

'''
Update install rel
'''
@require_http_methods(["POST"])
def updateInstallRelWS(request):
    return _updateData(request, idodsi.updateInstallRel, ['parent_install', 'child_install', 'description', 'order', 'props'])

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
def saveInstallRelPropTypeWS(request):
    return _saveData(request, idodsi.saveInstallRelPropertyType, ['name', 'description', 'unit'])

'''
Update install rel property type
'''
@require_http_methods(["POST"])
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
def saveInventoryToInstallWS(request):
    return _saveData(request, idodsi.saveInventoryToInstall, ['install_name', 'inv_name'])

'''
Update inventory to install
'''
@require_http_methods(["POST"])
def updateInventoryToInstallWS(request):
    return _updateData(request, idodsi.updateInventoryToInstall, ['inventory_to_install_id', 'install_name', 'inv_name'])

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
def saveDataMethodWS(request):
    return _saveData(request, idodsi.saveDataMethod, ['name', 'description'])

'''
Update data method
'''
@require_http_methods(["POST"])
def updateDataMethodWS(request):
    return _updateData(request, idodsi.updateDataMethod, ['old_name', 'name', 'description'], {'datamethod_id': None})

'''
Retrieve offline data
'''
@require_http_methods(["GET"])
def retrieveOfflineDataWS(request):
    return _retrieveData(request, idodsi.retrieveOfflineData, ['offlineid', 'description', 'gap', 'phase1', 'phase2', 'phase3', 'phase4', 'phasemode', 'polarmode', 'status', 'method_name', 'inventory_name'])

'''
Save offline data
'''
@require_http_methods(["POST"])
def saveDataOfflineDataWS(request):
    return _saveData(request, idodsi.saveOfflineData, ['inventory_name', 'username', 'description', 'gap', 'phase1', 'phase2', 'phase3', 'phase4', 'phasemode', 'polarmode', 'status', 'data_file_name', 'data_file_ts', 'data', 'script_name', 'script', 'method_name'])

'''
Update offline data
'''
@require_http_methods(["POST"])
def updateOfflineDataWS(request):
    return _updateData(request, idodsi.updateOfflineData, ['offline_data_id', 'inventory_name', 'username', 'description', 'gap', 'phase1', 'phase2', 'phase3', 'phase4', 'phasemode', 'polarmode', 'status', 'data_file_name', 'data_file_ts', 'data', 'script_name', 'script', 'method_name'])

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
def saveDataOnlineDataWS(request):
    return _saveData(request, idodsi.saveOnlineData, ['install_name', 'username', 'description', 'url', 'status'])

'''
Update online data
'''
@require_http_methods(["POST"])
def updateOnlineDataWS(request):
    return _updateData(request, idodsi.updateOnlineData, ['online_data_id', 'install_name', 'username', 'description', 'url', 'status'])

'''
Load index html file
'''
def idodsIndexHtml(request):
    return render_to_response("idods/index.html")

'''
Load html files
'''
def idodsHtmls(request):
    path_parts = request.path.split("/")
    file_name = path_parts[len(path_parts)-1]
    return render_to_response("idods/" + file_name)