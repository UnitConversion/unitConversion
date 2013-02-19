# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pymuniconv.municonvinfo import (retrievemagnetinfo, retrievesystemdata, retrieveconversioninfo)

def _getcmddict(request):
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
    
def systemlistweb(request):
    res = retrievesystemdata(_getcmddict(request))
    return render_to_response("magnets/magnets.html", res)

def systemlist(request):
    res = retrievesystemdata(_getcmddict(request))
    return HttpResponse(json.dumps(res), mimetype="application/json")
#    if 'application/xml' in request.META['CONTENT_TYPE'] or 'text/xml' in request.META['CONTENT_TYPE']:
#        return HttpResponse(_getxmlheader()+_gettreexml(res), mimetype=request.META['CONTENT_TYPE'])
#    else:
#        return HttpResponse(json.dumps({ "system": res}), mimetype="application/json")

def magnetdevicesweb(request):
    res = retrievemagnetinfo(_getcmddict(request))
    return render_to_response("magnets/magnets.html", res)

def magnetdevices(request):
    res = retrievemagnetinfo(_getcmddict(request))
    return HttpResponse(json.dumps(res), mimetype="application/json")
#    if 'application/xml' in request.META['CONTENT_TYPE'] or 'text/xml' in request.META['CONTENT_TYPE']:
#        return HttpResponse(_getxmlheader()+_gettreexml(res), mimetype=request.META['CONTENT_TYPE'])
#    else:
#        return HttpResponse(json.dumps(res), mimetype="application/json")

def conversionweb(request):
    res = retrieveconversioninfo(_getcmddict(request))
    return render_to_response("magnets/magnets.html", res)
    
def conversion(request):
    res = retrieveconversioninfo(_getcmddict(request))
    return HttpResponse(json.dumps(res), mimetype="application/json")
#    if 'application/xml' in request.META['CONTENT_TYPE'] or 'text/xml' in request.META['CONTENT_TYPE']:
#        return HttpResponse(_getxmlheader()+_gettreexml(res), mimetype=request.META['CONTENT_TYPE'])
#    else:
#        return HttpResponse(json.dumps(res), mimetype="application/json")

