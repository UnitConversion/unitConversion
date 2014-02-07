# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pyidods.idods import *

from pyidods.logger import _setup_idods_logger
idods_log = _setup_idods_logger('idods')

@require_http_methods(["GET", "POST", "PUT"])
def vendor(request):
    
    if request.method == "GET":
        return retrieveVendor(request)

'''
Retrieve vendor information
'''
def retrieveVendor(request):
    
    res = {'message': 'No function specified.'}
    
    try:
        finalres = json.dumps(res)
    except Exception as e:
        idods_log.exception(e)
        raise e
    
    return HttpResponse(finalres, mimetype="application/json")