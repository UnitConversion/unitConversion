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

def _getxmlheader():
    return '<?xml version="1.0" encoding="iso-8859-1" ?>'

def _gettreexml(data):
    xml = '<system>'
    for res in data:
        xml += "<name>%s</name><br>" %(res)
    xml += '</system>'
    return xml

def magnets_help(request):
    return render_to_response("magnets/magnets_help.html")

def magnets_home(request):
    return render_to_response("magnets/index.html")

def magnets_content_home(request):
    return render_to_response("magnets/content.html")

def systemlistweb(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['name'])
        res = retrievesystemdata(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))
    return render_to_response("magnets/magnets.html", res)

def systemlist(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['name'])
        res = retrievesystemdata(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))
    return HttpResponse(json.dumps(res), mimetype="application/json")
#    if 'application/xml' in request.META['CONTENT_TYPE'] or 'text/xml' in request.META['CONTENT_TYPE']:
#        return HttpResponse(_getxmlheader()+_gettreexml(res), mimetype=request.META['CONTENT_TYPE'])
#    else:
#        return HttpResponse(json.dumps({ "system": res}), mimetype="application/json")

def magnetdevicesweb(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['name', 'cmpnt_type', 'system', 'serialno'])
        res = retrievemagnetinfo(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))

    return render_to_response("magnets/magnets.html", res)

def magnetdevices(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['name', 'cmpnt_type', 'system', 'serialno'])
        res = retrievemagnetinfo(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))

    return HttpResponse(json.dumps(res), mimetype="application/json")
#    if 'application/xml' in request.META['CONTENT_TYPE'] or 'text/xml' in request.META['CONTENT_TYPE']:
#        return HttpResponse(_getxmlheader()+_gettreexml(res), mimetype=request.META['CONTENT_TYPE'])
#    else:
#        return HttpResponse(json.dumps(res), mimetype="application/json")

def conversionweb(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['id','name','from','to','value','unit','energy','mcdata','cache','direction'])
        res = retrieveconversioninfo()
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))

    return render_to_response("magnets/magnets.html", res)
    
def conversion(request):
    params = _retrievecmddict(request)
    try:
        _checkkeys(params.keys(), ['id','name','from','to','value','unit','energy','mcdata','cache','direction'])
        res = retrieveconversioninfo(params)
    except ValueError as e:
        return HttpResponseBadRequest(HttpResponse(content=e))
    return HttpResponse(json.dumps(res), mimetype="application/json")
#    if 'application/xml' in request.META['CONTENT_TYPE'] or 'text/xml' in request.META['CONTENT_TYPE']:
#        return HttpResponse(_getxmlheader()+_gettreexml(res), mimetype=request.META['CONTENT_TYPE'])
#    else:
#        return HttpResponse(json.dumps(res), mimetype="application/json")

