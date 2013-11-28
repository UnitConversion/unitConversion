import re

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods

from django.shortcuts import render_to_response
from django.template import RequestContext

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pylattice import _setup_lattice_model_logger
latticemodel_log = _setup_lattice_model_logger('latticemodel_view')

from dataprocess import retrievelatticetype, savelatticetype
from dataprocess import savelatticeinfo, retrievelatticeinfo, updatelatticeinfo
from dataprocess import savelattice, retrievelattice, updatelattice
from dataprocess import savelatticestatus, retrievelatticestatus

from dataprocess import savemodelcodeinfo, retrievemodelcodeinfo
from dataprocess import savemodelstatus, retrievemodelstatus
from dataprocess import savemodel, updatemodel, retrievemodel, retrievemodellist
from dataprocess import retrievetransfermatrix, retrieveclosedorbit, retrievetwiss, retrievebeamparameters

from django.contrib.auth.decorators import permission_required
import requests

from authentication import *

def _retrievecmddict(httpcmd):
    '''
    Retrieve GET request parameters, lower all keys, and return parameter dictionary.
    '''
    #postcmd = request.POST.copy()
    # multiple values support.
    cmddict = {}
    for k, v in httpcmd.iteritems():
        vlist = httpcmd.getlist(k)
        if len(vlist) > 1:
            cmddict[k.lower()] = list(set(vlist))
        else:
            cmddict[k.lower()] = v
    return cmddict

post_actions = (('saveLatticeType', savelatticetype),
                ('saveLatticeInfo', savelatticeinfo),
                ('updateLatticeInfo', updatelatticeinfo),
                ('saveLattice', savelattice),
                ('updateLattice', updatelattice),
                ('saveLatticeStatus', savelatticestatus),

                ('saveModelCodeInfo', savemodelcodeinfo),
                ('saveModelStatus', savemodelstatus),
                ('saveModel', savemodel),
                ('updateModel', updatemodel),
                )
get_actions = (('retrieveLatticeType', retrievelatticetype),
               ('retrieveLatticeInfo', retrievelatticeinfo),
               ('retrieveLattice', retrievelattice),
               ('retrieveLatticeStatus', retrievelatticestatus),
               
               ('retrieveModelCodeInfo', retrievemodelcodeinfo),
               ('retrieveModelStatus', retrievemodelstatus),
               ('retrieveModel', retrievemodel),
               ('retrieveModelList', retrievemodellist),
               
               ('retrieveTransferMatrix', retrievetransfermatrix),
               ('retrieveClosedOrbit', retrieveclosedorbit),
               ('retrieveTwiss', retrievetwiss),
               ('retrieveBeamParameters', retrievebeamparameters),
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
def lattices(request):
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
            latticemodel_log.debug('Unsupported HTTP method %s'%request.method)
            return HttpResponseBadRequest(HttpResponse(content='Unsupported HTTP method'), mimetype="application/json")
    except ValueError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content=e), mimetype="application/json")
    except KeyError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), mimetype="application/json")
    except Exception as e:
        latticemodel_log.exception(e)
        return HttpResponseBadRequest(content=e, mimetype="application/json")
    try:
        finalres = json.dumps(res)
    except Exception as e:
        latticemodel_log.exception(e)
        raise e
    return HttpResponse(finalres, mimetype="application/json")

"""
Call saveLatticeInfo but before that check if user is logged in and if he has needed permissions
"""
@require_http_methods(["POST"])
@has_perm_or_basicauth('lattice.can_upload')
def saveLatticeInfo(request):
    print "in"
    
    try:
        params = json.loads(request.raw_post_data)
        #params = _retrievecmddict(request.POST.copy())
        print params
        params['function'] = 'saveLatticeInfo'
        res = savelatticeinfo(params)
    except ValueError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content=e), mimetype="application/json")
    except KeyError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), mimetype="application/json")
    except Exception as e:
        latticemodel_log.exception(e)
        return HttpResponseBadRequest(content=e, mimetype="application/json")
    try:
        finalres = json.dumps(res)
    except Exception as e:
        latticemodel_log.exception(e)
        raise e

    return HttpResponse(finalres, mimetype="application/json")

#@require_http_methods(["GET", "POST"])
#def models(request):
#    try:
#        res = {'message': 'Did not found any entry.'}
#        if request.method == 'GET':
#            params = _retrievecmddict(request.GET.copy())
#            if params.has_key('function'):
#                for p, _ in post_actions:
#                    if re.match(p, params['function']): 
#                        return HttpResponseBadRequest(HttpResponse(content='Wrong HTTP method for function %s'%p))
#                res = dispatch(params, get_actions)
#            else:
#                res = {'message': 'No function specified.'}
#            print res
#            
#        elif request.method == 'POST':
#            params = _retrievecmddict(request.POST.copy())
#            if params.has_key('function'):
#                for p, _ in get_actions:
#                    if re.match(p, params['function']): 
#                        return HttpResponseBadRequest(HttpResponse(content='Wrong HTTP method for function %s'%p))
#                res = dispatch(params, post_actions)
#            else:
#                res = {'message': 'No function specified.'}
#        else:
#            return HttpResponseBadRequest(HttpResponse(content='Unsupported HTTP method'))
#    except ValueError as e:
#        return HttpResponseNotFound(HttpResponse(content=e), mimetype="application/json")
#    except KeyError as e:
#        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), mimetype="application/json")
#    except Exception as e:
#        return HttpResponseBadRequest(content=e, mimetype="application/json")
#    
#    return HttpResponse(json.dumps(res), mimetype="application/json")

def lattice_home(request):
    return render_to_response("lattice/index.html")

def lattice_content_home(request):
    return render_to_response("lattice/content.html", context_instance = RequestContext(request))

def lattice_content_search(request):
    return render_to_response("lattice/search.html")

def lattice_content_list(request):
    return render_to_response("lattice/list.html")

def lattice_content_model_list(request):
    return render_to_response("lattice/model_list.html")

def lattice_content_details(request):
    return render_to_response("lattice/details.html")

def lattice_content_model_details(request):
    return render_to_response("lattice/model_details.html")

def lattice_upload(request):
    
    # Define result
    result = {}
    data = {}
    
    result = saveLatticeInfo(request)
    print result
    
    return HttpResponse(json.dumps(result), mimetype="application/json")
    
    try:
        data = json.loads(request.raw_post_data)
    except ValueError as e:
        result['result'] = 'error'
    
    print data
    
    url = 'http://localhost:8000/lattice/savelatticeinfo/'
    
    # Define payload variables
    name = ''
    branch = ''
    version = -1
    
    # Check if keys are defined
    if('name' in data):
        name = data['name']
    
    if('branch' in data):
        branch = data['branch']
    
    if('version' in data):
        version = int(data['version'])

    # Create payload
    payload={'name': name,
             'version': version,
             'branch': branch
    }
    
    # Make a request
    """
    r = requests.post(url, data=payload)
    print r.headers
    
    # Check status, 200 is OK
    if(r.status_code == 200):
        # Return response
        return HttpResponse(json.dumps(result), mimetype="application/json")
    
    else:
        return HttpResponse('Unauthorized', status=401)
    """
    
