""" 
Created on May 9th, 2013

.. module:: activeinterlock.views
    :platform: Unix, Windows
    :synopsis: RESTful interface for active interlock service 

    @updated dejan.dezman@cosylab.com March 5th, 2014
"""

#from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.db.transaction import TransactionManagementError
from django.template import RequestContext

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from _mysql_exceptions import MySQLError
from authentication import has_perm_or_basicauth
from utils.logger import _setup_logger
from utils.utils import _checkkeys, _retrievecmddict
activeinterlock_log = _setup_logger('activeinterlock_view', 'activeinterlock.log')

from django.db import connection, transaction

from pyactiveinterlock.epsai import (epsai)

# Init active interlock
api = epsai(connection, transaction)

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
        activeinterlock_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except ValueError as e:
        activeinterlock_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except MySQLError as e:
        activeinterlock_log.exception(e)
        return HttpResponseServerError(HttpResponse(content=e))
    
    except Exception as e:
        activeinterlock_log.exception(e)
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
        activeinterlock_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except ValueError as e:
        activeinterlock_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except MySQLError as e:
        activeinterlock_log.exception(e)
        return HttpResponseServerError(HttpResponse(content=e))
    
    except TransactionManagementError as e:
        activeinterlock_log.exception(e)
        transaction.rollback_unless_managed()
        return HttpResponseServerError(HttpResponse(content=e))
    
    except Exception as e:
        activeinterlock_log.exception(e)
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
        activeinterlock_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except ValueError as e:
        activeinterlock_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except MySQLError as e:
        activeinterlock_log.exception(e)
        return HttpResponseServerError(HttpResponse(content=e))
    
    except TransactionManagementError as e:
        activeinterlock_log.exception(e)
        transaction.rollback_unless_managed()
        return HttpResponseServerError(HttpResponse(content=e))
    
    except Exception as e:
        activeinterlock_log.exception(e)
        raise e
    
    return HttpResponse(json.dumps(res), mimetype="application/json")

@require_http_methods(["GET"])
def retrieveStatusesWS(request):
    '''
    Retrieve status information
    '''
    return _retrieveData(request, api.retrieveStatusInfo, [])

@require_http_methods(["GET"])
def retrieveAiHeaderWS(request):
    '''
    Retrieve active interlock header
    '''
    return _retrieveData(request, api.retrieveActiveInterlockHeader, ['status', 'id', 'datefrom', 'dateto'])

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def saveAiHeaderWS(request):
    '''
    Save active interlock header
    '''
    request.POST = request.POST.copy()
    request.POST['created_by'] = request.user.username
    return _saveData(request, api.saveActiveInterlockHeader, ['description', 'created_by'])

@require_http_methods(["GET"])
def retrieveDeviceWS(request):
    '''
    Retrieve device
    '''
    return _retrieveData(request, api.retrieveDevice, ['ai_id', 'ai_status', 'name', 'definition', 'aid_id'])

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def saveDeviceWS(request):
    '''
    Save device
    '''
    return _saveData(request, api.saveDevice, ['ai_status', 'name', 'definition', 'logic', 'props'])

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def updateDeviceWS(request):
    '''
    Update device
    '''
    return _updateData(request, api.updateDevice, ['aid_id', 'name', 'logic'])

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def deleteDeviceWS(request):
    '''
    Delete device
    '''
    return _updateData(request, api.deleteDevice, ['aid_id'])

@require_http_methods(["GET"])
def retrieveLogicWS(request):
    '''
    Retrieve active interlock header information
    '''
    return _retrieveData(request, api.retrieveActiveInterlockLogic, ['name', 'shape', 'logic', 'status'])

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def updateStatusWS(request):
    '''
    Update active interlock status
    '''
    request.POST = request.POST.copy()
    request.POST['modified_by'] = request.user.username
    return _updateData(request, api.updateActiveInterlockStatus, ['status', 'new_status', 'modified_by'], {'ai_id': None})

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def copyAiWS(request):
    '''
    Copy active interlock
    '''
    request.POST = request.POST.copy()
    request.POST['modified_by'] = request.user.username
    return _updateData(request, api.copyActiveInterlock, ['status', 'modified_by'], {})

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def updatePropWS(request):
    '''
    Update active interlock device property
    '''
    return _updateData(request, api.updateActiveInterlockProp, ['aid_id', 'prop_type_name', 'value'], {})

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def approveCellsWS(request):
    '''
    Approve active interlock device property
    '''
    return _updateData(request, api.approveCells, ['aid_id', 'prop_types'], {})

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def saveLogicWS(request):
    '''
    Save active interlock logic
    '''
    return _saveData(request, api.saveActiveInterlockLogic, ['name', 'shape', 'logic', 'code', 'created_by'])

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def updateLogicWS(request):
    '''
    Update active interlock logic
    '''
    return _updateData(request, api.updateActiveInterlockLogic, ['id', 'name', 'shape', 'logic', 'code', 'status'], {})

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def deleteLogicWS(request):
    '''
    Delete active interlock logic
    '''
    return _updateData(request, api.deleteActiveInterlockLogic, ['logic_id'], {})

@require_http_methods(["POST"])
@has_perm_or_basicauth('ai.can_modify_ai')
def downloadActiveInterlockWS(request):
    '''
    Download active interlock data
    '''
    return _updateData(request, api.downloadActiveInterlock, ['status', 'modified_by'])

def aiIndexHtml(request):
    '''
    Load index html file
    '''
    return render_to_response("activeinterlock/index.html", context_instance = RequestContext(request))

def aiHtmls(request, url):
    '''
    Load html files
    '''
    return render_to_response("activeinterlock/" + url, context_instance = RequestContext(request))