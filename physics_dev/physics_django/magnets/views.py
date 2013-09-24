# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pymuniconv.municonvinfo import (retrievemagnetinfo, retrievesystemdata, retrieveconversioninfo)
from utils.utils import _checkkeys

def _retrievecmddict(request):
    '''
    Retrieve GET request parameters, lower all keys, and return parameter dictionary.
    '''
    getcmd = request.GET.copy()
    # multiple values support.
    getdict = {}
    for k, v in getcmd.iteritems():
        vlist = getcmd.getlist(k)
        if len(vlist) > 1:
            getdict[k.lower()] = list(set(vlist))
        else:
            getdict[k.lower()] = v
    return getdict

def magnets_help(request):
    return render_to_response("magnets/magnets_help.html")

def magnets_home(request):
    return render_to_response("magnets/index.html")

def magnets_content_home(request):
    return render_to_response("magnets/content.html")

def magnets_content_search(request):
    return render_to_response("magnets/search.html")

def magnets_content_list(request):
    return render_to_response("magnets/list.html")

def magnets_content_details(request):
    return render_to_response("magnets/details.html")

def magnets_content_results(request):
    return render_to_response("magnets/results.html")

def magnets_measurement_data(request):
    return render_to_response("magnets/measurement_data.html")

def systemlist(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['name'])
        res = retrievesystemdata(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))
    return HttpResponse(json.dumps(res), mimetype="application/json")

def magnetinstall(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['name', 'cmpnt_type', 'system', 'serialno'])
        res = retrievemagnetinfo(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))

    return HttpResponse(json.dumps(res), mimetype="application/json")

def magnetinventory(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['cmpnt_type', 'serialno'])
        res = retrievemagnetinfo(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))

    return HttpResponse(json.dumps(res), mimetype="application/json")

def conversion(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['id','name','from','to','value','unit','energy','mcdata','cache','direction', 'complex'])
        res = retrieveconversioninfo(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))
    return HttpResponse(json.dumps(res), mimetype="application/json")
