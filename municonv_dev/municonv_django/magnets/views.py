# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.db import connection #, transaction
try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pymuniconv.municonvdata import municonvdata
municonv = municonvdata(connection)

def __wildcardformat(regxval):
    """
    The LIKE condition allows user to use wildcards in the where clause of an SQL statement.
    This allows user to perform pattern matching. The LIKE condition can be used in any valid
    SQL statement - select, insert, update, or delete.
    The patterns that a user can choose from are:
        % allows you to match any string of any length (including zero length)
        _ allows you to match on a single character
 
    The client uses "*" for multiple match, and "?" for single character match.
    This function replaces "*" with "%", and "?" with "_".

    For example:
    >>> __wildcardformat("a*b?c*d*e?f")
    u'a%b_c%d%e_f'
    """
    return regxval.replace("*","%").replace("?","_")

def _getcmddict(request):
    '''
    Retrieve GET request parameters, lower all keys, and return parameter dictionary.
    '''
    getcmd = request.GET.copy()
    return dict((k.lower(), v.lower()) for k,v in getcmd.iteritems())

def magnets_help(request):
    return render_to_response("magnets/magnets_help.html")

def _retrievemagnetinfo(request):
    '''
    acceptable key words:
     -- name
     -- cmpnt_type
     -- system
     -- serialno
    '''
    getcmd = _getcmddict(request)
    if getcmd.has_key('name'):
        name = getcmd['name']
    else:
        name = "*"
    
    cmpnt_type = None
    if getcmd.has_key('cmpnt_type'):
        cmpnt_type = getcmd['cmpnt_type']

    location = None
    if getcmd.has_key('system'):
        location = getcmd['system']
    
    if getcmd.has_key('serialno'):
        # get a list of devices from inventory which have been installed
        serialno = getcmd['serialno']
    else:
        serialno = "*"
    if name == "*" and location == None:
        # convert data format
        # From: 
        #inv.inventory_id,
        #inv.serial_no, 
        #ctype.cmpnt_type_name, 
        #ctype.description, 
        #vendor.vendor_name
        # To:
        # ''
        #inv.inventory_id,
        # ''
        # ''
        #inv.serial_no, 
        #ctype.cmpnt_type_name, 
        #ctype.description, 
        #vendor.vendor_name
        res = municonv.retrieveinventory(serialno, ctypename=cmpnt_type)
        if len(res) >0:
            res = list(res)
            for i in range(len(res)):
                data = list(res[i])
                data.insert(1, '')
                data.insert(1, '')
                data.insert(0, '')
                res[i] = data
    else:
        #install.install_id, 
        #inventory.inventory_id, 
        #install.field_name, 
        #install.location,
        #inventory.serial_no, 
        #cmpnt_type.cmpnt_type_name, 
        #cmpnt_type.description,
        #vendor.vendor_name
        res = municonv.retrieveinstalledinventory(name, serialno, ctypename=cmpnt_type, location=location)
    return res
    
def magnetdevicesweb(request):
    res = _retrievemagnetinfo(request)
    return render_to_response("magnets/magnets.html", {'device': res})

def magnetdevices(request):
    res = _retrievemagnetinfo(request)
    if 'application/xml' in request.META['CONTENT_TYPE'] or 'text/xml' in request.META['CONTENT_TYPE']:
        return HttpResponse(_getxmlheader()+_gettreexml(res), mimetype=request.META['CONTENT_TYPE'])
    else:
        data = {}
        if len(res) >0:
            for val in res:
                data[val[1]] = list(val)
        return HttpResponse(json.dumps(data), mimetype="application/json")


def _getxmlheader():
    return '<?xml version="1.0" encoding="iso-8859-1" ?>'

def _gettreexml(data):
    xml = '<system>'
    for res in data:
        xml += "<name>%s</name><br>" %(res)
    xml += '</system>'
    return xml

def _retrievesystemdata(request):
    getcmd = _getcmddict(request)
    if getcmd.has_key('name'):
        name = request.GET["name"]
        res = municonv.retrievesystem(name)
    else:
        res = municonv.retrievesystem()
    return res

def systemlistweb(request):
    res = _retrievesystemdata(request)
    return render_to_response("magnets/magnets.html", {'system': res})

def systemlist(request):
    res = _retrievesystemdata(request)

    if 'application/xml' in request.META['CONTENT_TYPE'] or 'text/xml' in request.META['CONTENT_TYPE']:
#        return HttpResponse(_getxmlheader()+_gettreexml(res), mimetype='application/xml')
        return HttpResponse(_getxmlheader()+_gettreexml(res), mimetype=request.META['CONTENT_TYPE'])
    else:
        return HttpResponse(json.dumps({ "system": res}), mimetype="application/json")

def _retrieveconversioninfo(request):
    '''
    acceptable key words to identify device(s):
     -- id: inventory id
     
    for conversion:
     -- from (i, b, k)
     -- to (i, b, k)
     -- value
     -- unit
    '''
    getcmd = _getcmddict(request)
    if getcmd.has_key('from') and getcmd.has_key('to') and getcmd.has_key('value'):
        print('do conversion here.')
    else:
        print('get conversion info only')

def conversionweb(request):
    res = _retrieveconversioninfo(request)
    return render_to_response("magnets/magnets.html", {'system': res})
    
def conversion(request):
    res = _retrieveconversioninfo(request)
    if 'application/xml' in request.META['CONTENT_TYPE'] or 'text/xml' in request.META['CONTENT_TYPE']:
        return HttpResponse(_getxmlheader()+_gettreexml(res), mimetype='application/xml')
        #return HttpResponse(_getxmlheader()+_gettreexml(res), mimetype=request.META['CONTENT_TYPE'])
    else:
        return HttpResponse(json.dumps({ "title": res}), mimetype="application/json")

