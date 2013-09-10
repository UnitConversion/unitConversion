""" 
Created on May 9th, 2013

.. module:: activeinterlock.views
    :platform: Unix, Windows
    :synopsis: RESTful interface for active interlock service 

"""
import re

#from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from utils.logger import _setup_logger
activeinterlock_log = _setup_logger('activeinterlock_view', 'activeinterlock.log')

from dataprocess import (retrieveactiveinterlock, retrieveactiveinterlocklogic,retrieveactiveinterlockproptype,saveactiveinterlock,saveactiveinterlocklogic,saveactiveinterlockproptype,updateactiveinterlockstatus)

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
