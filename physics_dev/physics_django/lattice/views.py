# Create your views here.
import re

#from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from dataprocess import retrievelatticetype, savelatticetype
from dataprocess import savelatticeinfo, retrievelatticeinfo, updatelatticeinfo
from dataprocess import savelattice, retrievelattice, updatelattice
from dataprocess import savegoldenlattice, retrievegoldenlattice

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
                ('saveGoldenLattice', savegoldenlattice),
                )
get_actions = (('retrieveLatticeType', retrievelatticetype),
               ('retrieveLatticeInfo', retrievelatticeinfo),
               ('retrieveLattice', retrievelattice),
               ('retrieveGoldenLattice', retrievegoldenlattice),
               )

def dispatch(params, actions):
    '''
    '''
    for p, f in actions:
        if re.match(p, params['function']):
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
            return HttpResponseBadRequest(HttpResponse(content='Unsupported HTTP method'), mimetype="application/json")
    except ValueError as e:
        return HttpResponseNotFound(HttpResponse(content=e), mimetype="application/json")
    except KeyError as e:
        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), mimetype="application/json")
    except Exception as e:
        return HttpResponseBadRequest(content=e, mimetype="application/json")
    return HttpResponse(json.dumps(res), mimetype="application/json")

@require_http_methods(["GET", "POST"])
def models(request):
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
            return HttpResponseBadRequest(HttpResponse(content='Unsupported HTTP method'))
    except ValueError as e:
        return HttpResponseNotFound(HttpResponse(content=e))

    return HttpResponse(json.dumps(res), mimetype="application/json")
