from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.http import require_http_methods
import traceback
import sys
from django.db import connection, transaction
from django.db.transaction import TransactionManagementError

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pyidods.idods import (idods)

# Init idods
idodsi = idods(connection, transaction)

from _mysql_exceptions import MySQLError

from pyidods.logger import _setup_idods_logger
idods_log = _setup_idods_logger('idods')

from utils.utils import _checkkeys, _retrievecmddict

'''
Retrieve vendor information
'''
@require_http_methods(["GET"])
def retrieveVendorWS(request):
    params = _retrievecmddict(request.GET.copy())
    res = {}
    
    try:
        _checkkeys(params.keys(), ['name', 'description'])
        res = idodsi.retrieveVendor(**params)
    
    except TypeError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except ValueError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except MySQLError as e:
        idods_log.exception(e)
        return HttpResponseServerError(HttpResponse(content=e))
    
    except Exception as e:
        idods_log.exception(e)
        raise e
    
    return HttpResponse(json.dumps(res), mimetype="application/json")

'''
Save new vendor
'''
@require_http_methods(["POST"])
def saveVendorWS(request):
    params = _retrievecmddict(request.POST.copy())
    res = {}
    
    try:
        _checkkeys(params.keys(), ['name', 'description'])
        res = idodsi.saveVendor(**params)
        transaction.commit_unless_managed()
    
    except TypeError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except ValueError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except MySQLError as e:
        idods_log.exception(e)
        return HttpResponseServerError(HttpResponse(content=e))
    
    except TransactionManagementError as e:
        idods_log.exception(e)
        transaction.rollback_unless_managed()
        return HttpResponseServerError(HttpResponse(content=e))
    
    except Exception as e:
        idods_log.exception(e)
        raise e
    
    return HttpResponse(json.dumps(res), mimetype="application/json")

'''
Update vendor
'''
@require_http_methods(["POST"])
def updateVendorWS(request):
    params = _retrievecmddict(request.POST.copy())
    res = {}
    
    try:
        _checkkeys(params.keys(), ['old_name', 'name', 'description'])
        res = idodsi.updateVendor(vendor_id=None, **params)
        transaction.commit_unless_managed()
    
    except TypeError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except ValueError as e:
        idods_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e))
    
    except MySQLError as e:
        idods_log.exception(e)
        return HttpResponseServerError(HttpResponse(content=e))
    
    except TransactionManagementError as e:
        idods_log.exception(e)
        transaction.rollback_unless_managed()
        return HttpResponseServerError(HttpResponse(content=e))
    
    except Exception as e:
        idods_log.exception(e)
        raise e
    
    return HttpResponse(json.dumps(res), mimetype="application/json")

'''
Load index html file
'''
def idodsIndexHtml(request):
    return render_to_response("idods/index.html")

'''
Load html files
'''
def idodsHtmls(request):
    path_parts = request.path.split("/")
    file_name = path_parts[len(path_parts)-1]
    return render_to_response("idods/" + file_name)