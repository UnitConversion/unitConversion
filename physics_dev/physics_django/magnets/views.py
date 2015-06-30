# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pymuniconv.municonvinfo import (retrievemagnetinfo, retrievesystemdata, retrieveconversioninfo, retrieveMeasurementDataInfo)
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


def magnetsIndexHtml(request):
    '''
    Load index html file
    '''
    return render_to_response("magnets/index.html", context_instance=RequestContext(request))


def magnetsHtmls(request, url):
    '''
    Load html files
    '''
    return render_to_response("magnets/" + url, context_instance=RequestContext(request))


def systemlist(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['name'])
        res = retrievesystemdata(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))
    return HttpResponse(json.dumps(res), content_type="application/json")


def measurementDataInfo(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['inventory_id', 'cmpnt_type_name'])
        res = retrieveMeasurementDataInfo(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))
    return HttpResponse(json.dumps(res), content_type="application/json")


def magnetinstall(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['name', 'cmpnt_type', 'system', 'serialno'])
        res = retrievemagnetinfo(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))

    return HttpResponse(json.dumps(res), content_type="application/json")


def magnetinventory(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['cmpnt_type', 'serialno'])
        res = retrievemagnetinfo(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))

    return HttpResponse(json.dumps(res), content_type="application/json")


def conversion(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['id', 'name', 'from', 'to', 'value', 'unit', 'energy', 'mcdata', 'cache', 'direction', 'complex'])
        res = retrieveconversioninfo(params)

    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))

    return HttpResponse(json.dumps(res), content_type="application/json")
