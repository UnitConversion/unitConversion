from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.http import require_http_methods
import traceback
import sys
import time
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


def _retrieveData(request, fun, propList, customDict={}):
    '''
    Private template for the retrieve functions
    '''
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


def _saveData(request, fun, propList):
    '''
    Private template for save function
    '''
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


def _updateData(request, fun, propList, customDict={}):
    '''
    Private template for update function
    '''
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


@require_http_methods(["GET"])
def retrieveVendorWS(request):
    '''
    Retrieve vendor information
    '''
    return _retrieveData(request, idodsi.retrieveVendor, ['name', 'description'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveVendorWS(request):
    '''
    Save new vendor
    '''
    return _saveData(request, idodsi.saveVendor, ['name', 'description'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateVendorWS(request):
    '''
    Update vendor
    '''
    return _updateData(request, idodsi.updateVendor, ['old_name', 'name', 'description'], {'vendor_id': None})


@require_http_methods(["GET"])
def retrieveCompntTypeWS(request):
    '''
    Retrieve component type
    '''
    return _retrieveData(request, idodsi.retrieveComponentType, ['name', 'description'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveCompntTypeWS(request):
    '''
    Save component type
    '''
    return _saveData(request, idodsi.saveComponentType, ['name', 'description', 'props'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateCmpntTypeWS(request):
    '''
    Update component type
    '''
    return _updateData(request, idodsi.updateComponentType, ['old_name', 'name', 'description', 'props'], {'component_type_id': None})


@require_http_methods(["GET"])
def retrieveCompntTypePropTypeWS(request):
    '''
    Retrieve component type property type
    '''
    return _retrieveData(request, idodsi.retrieveComponentTypePropertyType, ['name'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveCompntTypePropTypeWS(request):
    '''
    Save component type property type
    '''
    return _saveData(request, idodsi.saveComponentTypePropertyType, ['name', 'description'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateCmpntTypePropTypeWS(request):
    '''
    Update component type property type
    '''
    return _updateData(request, idodsi.updateComponentTypePropertyType, ['old_name', 'name', 'description'], {'property_type_id': None})


@require_http_methods(["GET"])
def retrieveInventoryWS(request):
    '''
    Retrieve inventory
    '''
    return _retrieveData(request, idodsi.retrieveInventory, ['name'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInventoryWS(request):
    '''
    Save inventory
    '''
    return _saveData(request, idodsi.saveInventory, ['cmpnt_type', 'name', 'alias', 'serialno', 'vendor', 'props'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInventoryWS(request):
    '''
    Update inventory
    '''
    return _updateData(request, idodsi.updateInventory, ['old_name', 'cmpnt_type', 'name', 'alias', 'serialno', 'vendor', 'props'], {'inventory_id': None})


@require_http_methods(["GET"])
def retrieveInventoryPropTmpltWS(request):
    '''
    Retrieve inventory property template
    '''
    return _retrieveData(request, idodsi.retrieveInventoryPropertyTemplate, ['name'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInventoryPropTmpltWS(request):
    '''
    Save inventory property template
    '''
    return _saveData(request, idodsi.saveInventoryPropertyTemplate, ['cmpnt_type', 'name', 'description', 'default', 'unit'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInventoryPropTmpltWS(request):
    '''
    Update inventory property template
    '''
    return _updateData(request, idodsi.updateInventoryPropertyTemplate, ['tmplt_id', 'cmpnt_type', 'name', 'description', 'default', 'unit'])


@require_http_methods(["GET"])
def retrieveInstallWS(request):
    '''
    Retrieve install
    '''
    startedd = time.time()
    result = _retrieveData(request, idodsi.retrieveInstall, ['name', 'description', 'cmpnt_type', 'coordinatecenter'])
    total = time.time() - startedd
    total = total*1000
    print '=> elapsed time view.retrieveInstall.V: %f ms' % total
    return result


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInstallWS(request):
    '''
    Save install
    '''
    return _saveData(request, idodsi.saveInstall, ['name', 'description', 'cmpnt_type', 'coordinatecenter'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInstallWS(request):
    '''
    Update install
    '''
    return _updateData(request, idodsi.updateInstall, ['old_name', 'name', 'description', 'cmpnt_type', 'coordinatecenter'], {'install_id': None})


@require_http_methods(["GET"])
def retrieveInstallRelWS(request):
    '''
    Retrieve install rel
    '''
    return _retrieveData(request, idodsi.retrieveInstallRel, ['parent_install', 'child_install', 'description', 'order', 'date', 'expected_property'], {'install_rel_id': None})


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInstallRelWS(request):
    '''
    Save install rel
    '''
    return _saveData(request, idodsi.saveInstallRel, ['parent_install', 'child_install', 'description', 'order', 'props'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInstallRelWS(request):
    '''
    Update install rel
    '''
    return _updateData(request, idodsi.updateInstallRel, ['parent_install', 'child_install', 'description', 'order', 'props'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def deleteInstallRelWS(request):
    '''
    Delete install rel
    '''
    return _updateData(request, idodsi.deleteInstallRel, ['parent_install', 'child_install'])


@require_http_methods(["GET"])
def retrieveInstallRelPropTypeWS(request):
    '''
    Retrieve install rel property type
    '''
    return _retrieveData(request, idodsi.retrieveInstallRelPropertyType, ['name'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInstallRelPropTypeWS(request):
    '''
    Save install rel property type
    '''
    return _saveData(request, idodsi.saveInstallRelPropertyType, ['name', 'description', 'unit'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInstallRelPropTypeWS(request):
    '''
    Update install rel property type
    '''
    return _updateData(request, idodsi.updateInstallRelPropertyType, ['old_name', 'name', 'description', 'unit'], {'type_id': None})


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInstallRelPropWS(request):
    '''
    Save install rel property
    '''
    return _saveData(request, idodsi.saveInstallRelProperty, ['install_rel_id', 'install_rel_property_type_name', 'install_rel_property_value'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInstallRelPropWS(request):
    '''
    Update install rel property
    '''
    return _updateData(request, idodsi.updateInstallRelPropertyByMap, ['install_rel_parent', 'install_rel_child', 'install_rel_property_type_name', 'install_rel_property_value'], {})


@require_http_methods(["GET"])
def retrieveInventoryToInstallWS(request):
    '''
    Retrieve inventory to install
    '''
    return _retrieveData(request, idodsi.retrieveInventoryToInstall, ['inventory_to_install_id', 'install_name', 'inv_name'], {'inventory_to_install_id': None})


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInventoryToInstallWS(request):
    '''
    Save inventory to install
    '''
    return _saveData(request, idodsi.saveInventoryToInstall, ['install_name', 'inv_name'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateInventoryToInstallWS(request):
    '''
    Update inventory to install
    '''
    return _updateData(request, idodsi.updateInventoryToInstall, ['inventory_to_install_id', 'install_name', 'inv_name'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def deleteInventoryToInstallWS(request):
    '''
    Delete inventory to install
    '''
    return _updateData(request, idodsi.deleteInventoryToInstall, ['inventory_to_install_id'])


@require_http_methods(["GET"])
def retrieveDataMethodWS(request):
    '''
    Retrieve data method
    '''
    return _retrieveData(request, idodsi.retrieveDataMethod, ['name', 'description'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveDataMethodWS(request):
    '''
    Save data method
    '''
    return _saveData(request, idodsi.saveDataMethod, ['name', 'description'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateDataMethodWS(request):
    '''
    Update data method
    '''
    return _updateData(request, idodsi.updateDataMethod, ['old_name', 'name', 'description'], {'datamethod_id': None})


@require_http_methods(["GET"])
def retrieveRawDataWS(request):
    '''
    Retrieve raw data
    '''
    return _retrieveData(request, idodsi.retrieveRawData, ['raw_data_id'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveRawDataWS(request):
    '''
    Save raw data
    '''
    rawFile = request.FILES.getlist('file')[0]

    res = {}

    try:
        startedd = time.time()

        res = idodsi.saveRawData(rawFile.read())
        transaction.commit_unless_managed()

        total = time.time() - startedd
        total = total*1000
        print '=> elapsed time view.saveRawData.V: %f ms' % total

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


@require_http_methods(["GET"])
def retrieveOfflineDataWS(request):
    '''
    Retrieve offline data
    '''
    return _retrieveData(request, idodsi.retrieveOfflineData, ['offlineid', 'description', 'date', 'gap', 'phase1', 'phase2', 'phase3', 'phase4', 'phasemode', 'polarmode', 'status', 'method_name', 'inventory_name'])


@require_http_methods(["GET"])
def retrieveOfflineDataInstallWS(request):
    '''
    Retrieve offline data (via install)
    '''
    return _retrieveData(request, idodsi.retrieveInstallOfflineData, ['install_name', 'description', 'date', 'gap', 'phase1', 'phase2', 'phase3', 'phase4', 'phasemode', 'polarmode', 'status', 'method_name'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveOfflineDataWS(request):
    '''
    Save offline data
    '''

    startedd = time.time()

    request.POST = request.POST.copy()
    request.POST['username'] = request.user.username

    result = _saveData(request, idodsi.saveOfflineData, [
        'inventory_name',
        'username',
        'description',
        'gap',
        'phase1',
        'phase2',
        'phase3',
        'phase4',
        'phasemode',
        'polarmode',
        'status',
        'data_file_name',
        'data_file_ts',
        'data_id',
        'script_name',
        'script',
        'method_name'
    ])

    total = time.time() - startedd
    total = total*1000
    print '=> elapsed time view.saveOfflineData.V: %f ms' % total

    return result


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveDataMethodOfflineDataWS(request):
    '''
    Save data method and offline data
    '''

    startedd = time.time()
    request.POST = request.POST.copy()
    request.POST['username'] = request.user.username
    result = _saveData(request, idodsi.saveMethodAndOfflineData, ['inventory_name', 'username', 'method', 'method_desc', 'data_desc', 'data_file_name', 'data_id', 'status', 'gap', 'phase1', 'phase2', 'phase3', 'phase4', 'phase_mode', 'polar_mode'])
    total = time.time() - startedd
    total = total*1000
    print '=> elapsed time view.saveDataMethodOfflineData: %f ms' % total

    return result


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateOfflineDataWS(request):
    '''
    Update offline data
    '''
    request.POST = request.POST.copy()
    request.POST['username'] = request.user.username
    return _updateData(request, idodsi.updateOfflineData, [
        'offline_data_id',
        'inventory_name',
        'username',
        'description',
        'gap',
        'phase1',
        'phase2',
        'phase3',
        'phase4',
        'phasemode',
        'polarmode',
        'status',
        'data_file_name',
        'data_file_ts',
        'data_id',
        'script_name',
        'script',
        'method_name'
    ])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def deleteOfflineDataWS(request):
    '''
    Delete offline data
    '''
    return _updateData(request, idodsi.deleteOfflineData, ['offline_data_id'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def uploadFileWS(request):
    '''
    Upload a file
    '''
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


@require_http_methods(["GET"])
def retrieveOnlineDataWS(request):
    '''
    Retrieve online data
    '''
    return _retrieveData(request, idodsi.retrieveOnlineData, ['onlineid', 'install_name', 'username', 'description', 'status'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveOnlineDataWS(request):
    '''
    Save online data
    '''
    print request.POST
    print request.FILES
    request.POST = request.POST.copy()
    request.POST['username'] = request.user.username

    if request.FILES:
        rawFile = request.FILES.getlist('file')[0]
        request.POST['feedforward_data'] = rawFile.read()

    return _saveData(request, idodsi.saveOnlineData, ['install_name', 'username', 'description', 'rawdata_path', 'status', 'feedforward_file_name', 'feedforward_data'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateOnlineDataWS(request):
    '''
    Update online data
    '''
    request.POST = request.POST.copy()
    request.POST['username'] = request.user.username
    return _updateData(request, idodsi.updateOnlineData, ['online_data_id', 'install_name', 'username', 'description', 'rawdata_path', 'status', 'feedforward_file_name', 'feedforward_data'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def deleteOnlineDataWS(request):
    '''
    Delete online data
    '''
    return _updateData(request, idodsi.deleteOnlineData, ['online_data_id'])


@require_http_methods(["GET", "POST"])
@has_perm_or_basicauth('id.can_modify_id')
def idodsInstallWS(request):
    '''
    Install idods
    '''
    return _updateData(request, idodsi.idodsInstall, [])


@require_http_methods(["GET"])
def retrieveTreesWS(request):
    '''
    Retrieve trees
    '''
    return _retrieveData(request, idodsi.retrieveTrees, ['install_name'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def testAuth(request):
    '''
    Test authentication
    '''
    return HttpResponse(json.dumps({'result': True}), mimetype="application/json")


@require_http_methods(["POST"])
def testCall(request):
    '''
    Test rest call without authentication
    '''
    return HttpResponse(json.dumps({'result': True}), mimetype="application/json")


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveInsertionDeviceWS(request):
    '''
    Save insertion device
    '''
    result = _saveData(request, idodsi.saveInsertionDevice, [
        'install_name',
        'coordinate_center',
        'project',
        'beamline',
        'beamline_desc',
        'install_desc',
        'inventory_name',
        'down_corrector',
        'up_corrector',
        'length',
        'gap_max',
        'gap_min',
        'gap_tolerance',
        'phase1_max',
        'phase1_min',
        'phase2_max',
        'phase2_min',
        'phase3_max',
        'phase3_min',
        'phase4_max',
        'phase4_min',
        'phase_tolerance',
        'k_max_circular',
        'k_max_linear',
        'phase_mode_a1',
        'phase_mode_a2',
        'phase_mode_p',
        'type_name',
        'type_desc'
    ])

    return result


@require_http_methods(["GET"])
def retrieveRotCoilDataWS(request):
    '''
    Retrieve rot coil data
    '''
    return _retrieveData(request, idodsi.retrieveRotCoilData, ['inventory_name'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveRotCoilDataWS(request):
    '''
    Save rot coil data
    '''
    request.POST = request.POST.copy()
    request.POST['login_name'] = request.user.username
    return _saveData(request, idodsi.saveRotCoilData, [
        'inventory_name', 'alias', 'meas_coil_id', 'ref_radius', 'magnet_notes', 'login_name', 'cond_curr',
        'meas_loc', 'run_number', 'sub_device', 'current_1', 'current_2', 'current_3', 'up_dn_1', 'up_dn_2', 'up_dn_3',
        'analysis_number', 'integral_xfer_function', 'orig_offset_x', 'orig_offset_y', 'b_ref_int', 'roll_angle',
        'meas_notes', 'author', 'a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'a4_21', 'b4_21', 'data_issues', 'data_usage'
        ])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateRotCoilDataWS(request):
    '''
    Update rot coil data
    '''
    request.POST = request.POST.copy()
    request.POST['login_name'] = request.user.username
    return _updateData(request, idodsi.updateRotCoilData, [
        'rot_coil_data_id', 'inventory_name', 'alias', 'meas_coil_id', 'ref_radius', 'magnet_notes', 'login_name', 'cond_curr',
        'meas_loc', 'run_number', 'sub_device', 'current_1', 'current_2', 'current_3', 'up_dn_1', 'up_dn_2', 'up_dn_3',
        'analysis_number', 'integral_xfer_function', 'orig_offset_x', 'orig_offset_y', 'b_ref_int', 'roll_angle',
        'meas_notes', 'author', 'a1', 'a2', 'a3', 'b1', 'b2', 'b3', 'a4_21', 'b4_21', 'data_issues', 'data_usage'
        ])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def deleteRotCoilDataWS(request):
    '''
    Delete rot coil data
    '''
    return _updateData(request, idodsi.deleteRotCoilData, ['inventory_name', 'rot_coil_data_id'])


@require_http_methods(["GET"])
def retrieveHallProbeDataWS(request):
    '''
    Retrieve hall probe data
    '''
    return _retrieveData(request, idodsi.retrieveHallProbeData, ['inventory_name'])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def saveHallProbeDataWS(request):
    '''
    Save hall probe data
    '''
    request.POST = request.POST.copy()
    request.POST['login_name'] = request.user.username
    return _saveData(request, idodsi.saveHallProbeData, [
        'inventory_name', 'sub_device', 'alias', 'measured_at_location',
        'run_identifier', 'login_name', 'conditioning_current', 'current_1', 'current_2',
        'current_3', 'up_dn1', 'up_dn2', 'up_dn3', 'mag_volt_1', 'mag_volt_2', 'mag_volt_3',
        'x', 'y', 'z', 'bx_t', 'by_t', 'bz_t', 'meas_notes', 'data_issues', 'data_usage'
        ])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def updateHallProbeDataWS(request):
    '''
    Update hall probe data
    '''
    request.POST = request.POST.copy()
    request.POST['login_name'] = request.user.username
    return _updateData(request, idodsi.updateHallProbeData, [
        'hall_probe_id', 'inventory_name', 'sub_device', 'alias', 'measured_at_location',
        'run_identifier', 'login_name', 'conditioning_current', 'current_1', 'current_2',
        'current_3', 'up_dn1', 'up_dn2', 'up_dn3', 'mag_volt_1', 'mag_volt_2', 'mag_volt_3',
        'x', 'y', 'z', 'bx_t', 'by_t', 'bz_t', 'meas_notes', 'data_issues', 'data_usage'
        ])


@require_http_methods(["POST"])
@has_perm_or_basicauth('id.can_modify_id')
def deleteHallProbeDataWS(request):
    '''
    Delete hall probe data
    '''
    return _updateData(request, idodsi.deleteHallProbeData, ['inventory_name', 'hall_probe_id'])


def idodsIndexHtml(request):
    '''
    Load index html file
    '''
    return render_to_response("idods/index.html", context_instance=RequestContext(request))


def idodsHtmls(request, url):
    '''
    Load html files
    '''
    return render_to_response("idods/" + url, context_instance=RequestContext(request))


def measurementIndexHtml(request):
    '''
    Load index html file
    '''
    return render_to_response("measurement/index.html", context_instance=RequestContext(request))


def measurementHtmls(request, url):
    '''
    Load html files
    '''
    return render_to_response("measurement/" + url, context_instance=RequestContext(request))
