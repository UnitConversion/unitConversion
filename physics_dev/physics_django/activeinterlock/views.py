""" 
Created on May 9th, 2013

.. module:: activeinterlock.views
    :platform: Unix, Windows
    :synopsis: RESTful interface for active interlock service 

    @updated dejan.dezman@cosylab.com March 5th, 2014
"""
import re

#from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.views.decorators.http import require_http_methods
from django.shortcuts import render_to_response
from django.db.transaction import TransactionManagementError

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from _mysql_exceptions import MySQLError
from utils.logger import _setup_logger
from utils.utils import _checkkeys, _retrievecmddict
activeinterlock_log = _setup_logger('activeinterlock_view', 'activeinterlock.log')

from dataprocess import (retrieveactiveinterlock, retrieveactiveinterlocklogic,retrieveactiveinterlockproptype,saveactiveinterlock,saveactiveinterlocklogic,saveactiveinterlockproptype,updateactiveinterlockstatus)

from django.db import connection, transaction

from pyactiveinterlock.epsai import (epsai)

# Init active interlock
api = epsai(connection, transaction)

def _retrievecmddict(httpcmd):
    '''
    Retrieve GET request parameters, lower all keys, and return parameter dictionary.
    '''
    cmddict = {}
    for k, v in httpcmd.iteritems():
        vlist = httpcmd.getlist(k)
        if len(vlist) > 1:
            cmddict[k.lower()] = list(set(vlist))
        else:
            cmddict[k.lower()] = v
    return cmddict

post_actions = (('saveActiveInterlock', saveactiveinterlock),
                ('updateActiveInterlockStatus', updateactiveinterlockstatus),
                ('saveActiveInterlockPropType', saveactiveinterlockproptype),
                ('saveActiveInterlockLogic', saveactiveinterlocklogic),
                )
get_actions = (('retrieveActiveInterlock', retrieveactiveinterlock),
               ('retrieveActiveInterlockPropType', retrieveactiveinterlockproptype),
               ('retrieveActiveInterlockLogic', retrieveactiveinterlocklogic)
               )

def dispatch(params, actions):
    '''
    '''
    for p, f in actions:
        if len(p) > len(params['function']):
            if re.match(p, params['function']):
                return f(params)
        else:
            if re.match(params['function'], p):
                return f(params)

@require_http_methods(["GET", "POST"])
def activeinterlock(request):
    '''Interface to response a client request.
    '''
    try:
        res = {'message': 'Did not found any entry.'}
        if request.method == 'GET':
            params = _retrievecmddict(request.GET.copy())
            if params.has_key('function'):
                for p, _ in post_actions:
                    if re.match(p, params['function']): 
                        return HttpResponseBadRequest(HttpResponse(content='Wrong HTTP method for function %s'%p))
                res = dispatch(params, get_actions)
            else:
                res = {'message': 'No function specified.'}
        elif request.method == 'POST':
            params = _retrievecmddict(request.POST.copy())
            if params.has_key('function'):
                for p, _ in get_actions:
                    if re.match(p, params['function']): 
                        return HttpResponseBadRequest(HttpResponse(content='Wrong HTTP method for function %s'%p))
                res = dispatch(params, post_actions)
            else:
                res = {'message': 'No function specified.'}
        else:
            activeinterlock_log.debug('Unsupported HTTP method %s'%request.method)
            return HttpResponseBadRequest(HttpResponse(content='Unsupported HTTP method'), mimetype="application/json")
    except ValueError as e:
        activeinterlock_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content=e), mimetype="application/json")
    except KeyError as e:
        activeinterlock_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), mimetype="application/json")
    except Exception as e:
        activeinterlock_log.exception(e)
        return HttpResponseBadRequest(content=e, mimetype="application/json")
    try:
        finalres = json.dumps(res)
    except Exception as e:
        activeinterlock_log.exception(e)
        raise e
    return HttpResponse(finalres, mimetype="application/json")

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
def saveAiHeaderWS(request):
    '''
    Save active interlock header
    '''
    return _saveData(request, api.saveActiveInterlockHeader, ['description', 'created_by'])

@require_http_methods(["GET"])
def retrieveDeviceWS(request):
    '''
    Retrieve device
    '''
    return _retrieveData(request, api.retrieveDevice, ['ai_id', 'ai_status', 'name', 'definition'], {'ai_id': None})

@require_http_methods(["POST"])
def saveDeviceWS(request):
    '''
    Save device
    '''
    return _saveData(request, api.saveDevice, ['ai_status', 'name', 'definition', 'logic', 'props'])

@require_http_methods(["GET"])
def retrieveLogicWS(request):
    '''
    Retrieve active interlock header information
    '''
    return _retrieveData(request, api.retrieveActiveInterlockLogic, ['name', 'shape', 'logic'])

@require_http_methods(["POST"])
def updatePropWS(request):
    '''
    Update active interlock device property
    '''
    return _updateData(request, api.updateActiveInterlockProp, ['aid_id', 'prop_type_name', 'value'], {})

@require_http_methods(["POST"])
def approveCellsWS(request):
    '''
    Approve active interlock device property
    '''
    return _updateData(request, api.approveCells, ['aid_id', 'prop_types'], {})

@require_http_methods(["POST"])
def saveLogicWS(request):
    '''
    Save active interlock logic
    '''
    return _saveData(request, api.saveActiveInterlockLogic, ['name', 'shape', 'logic', 'code', 'created_by'])

def aiIndexHtml(request):
    '''
    Load index html file
    '''
    return render_to_response("activeinterlock/index.html")

def aiHtmls(request, url):
    '''
    Load html files
    '''
    return render_to_response("activeinterlock/" + url)