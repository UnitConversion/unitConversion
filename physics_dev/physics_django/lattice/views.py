import re
import sys
#from cStringIO import StringIO
import zipfile
import traceback
import base64

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods

from django.shortcuts import render_to_response
from django.template import RequestContext

try:
    from django.utils import simplejson as json
except ImportError:
    import json

#import requests

from django.contrib.auth.decorators import permission_required
from authentication import has_perm_or_basicauth

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
    try:
        #params = json.loads(request.raw_post_data)
        params = _retrievecmddict(request.POST.copy())
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

"""
Call saveLattice but before that check if user is logged in and if he has needed permissions
"""
@require_http_methods(["POST"])
@has_perm_or_basicauth('lattice.can_upload')
def saveLattice(request):
    try:
        #params = json.loads(request.raw_post_data)
        params = _retrievecmddict(request.POST.copy())
        #print params
        params['function'] = 'saveLattice'
        res = savelattice(params)
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

'''
Load modal window template
'''
def lattice_modal(request):
    path_parts = request.path.split("/")
    file_name = path_parts[len(path_parts)-1]
    return render_to_response("lattice/modal/" + file_name)

"""
Method reads the file, checks it and returns file contents
"""
def handle_uploaded_file(f):
    fileContent = ""
    
    for chunk in f.chunks():
        fileContent += chunk
    
    return fileContent

# Check if string has binary characters. Based on
# https://github.com/hamilyon/status/blob/8d05f9b7d95caa1bd1e52966ae8be9b23c442972/grin.py#26
textchars = ''.join(map(chr, [7,8,9,10,12,13,27] + range(0x20, 0x100)))
is_binary_string = lambda isbytes: bool(isbytes.translate(None, textchars))

"""
Open kickmap archive and return file contents in an array. File contents
can be plain text or binary. If files are plain text, they have to be split
into lines and if they are binary they have to be encoded to base64 and returned
"""
def handle_uploaded_archive(f):
    kmdict = {}
    
    try:
        zipf = zipfile.ZipFile(f)
        
        # Go through files in a zip
        for libitem in zipf.namelist():
            
            # Skip directories
            if libitem.endswith('/'):
                continue

            bytesf = zipf.read(libitem)
            
            if is_binary_string(bytesf):
                filecontent = base64.b64encode(bytesf)
            
            else:
                # Repair utf8 problems
                #zipContent = unicode(bytesf, errors="ignore")
                #filecontent = zipContent.splitlines()
                filecontent = []
                for line in bytesf.splitlines():
                    tmp = unicode(line, errors="ignore")
                    if tmp.endswith('\n'):
                        filecontent.append(tmp)
                    else:
                        filecontent.append(tmp+'\n')
            
            kmdict[libitem] = filecontent
        
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        raise e
        
    return kmdict
    
'''
Save lattice helper function that parses uploaded files and prepares data for saving lattice
'''
#import time
@require_http_methods(["POST"])
def saveLatticeHelper(request):
    
    # Define file types
    latticeFileTypes = ['lat', 'lte', 'txt']
    controlFileFileTypes = ['ele']
    archiveFileFileTypes = ['zip']
    
    latticeType = json.loads(request.POST['latticetype'])
    latticeFile = None
    kickmapFile = None
    controlFile = None
    #latticeName = None
    
    # Go through all the uploaded files
    for fileObject in request.FILES.getlist('files'):
        fileNameParts = fileObject.name.split('.')
        fileType = fileNameParts[len(fileNameParts)-1]
        
        # This can only be control file
        if fileType in controlFileFileTypes:
            controlFile = fileObject
            continue
        
        # Find lattice file
        if fileType in latticeFileTypes:
            latticeFile = fileObject
            continue
            
        # Find kickmap archive
        if fileType in archiveFileFileTypes:
            kickmapFile = fileObject
            continue

    try:
        lattice = {}
        #lattice['name'] = request.POST['name']
        lattice['name'] = latticeFile.name
        
        # In plain lattice, data must be put into data parameter
        if latticeFile != None:
            fileContent = handle_uploaded_file(latticeFile)
            newcontent = []
            for line in fileContent.splitlines():
                tmp=unicode(line, errors="ignore")
                if tmp.endswith('\n'):
                    newcontent.append(tmp)
                else:
                    newcontent.append(tmp+'\n')

            if latticeType['format'] == 'txt':
                #lattice['data'] = unicode(fileContent, errors="ignore").splitlines()
                lattice['data'] = newcontent
            else:
                #lattice['raw'] = unicode(fileContent, errors="ignore").splitlines()
                lattice['raw'] = newcontent
        
        # Handle kickmap archive
        if kickmapFile != None:
            kmdict = handle_uploaded_archive(kickmapFile);
            lattice['map'] = kmdict
        
        # Handle control file
        if controlFile != None:
            controlFileContent = handle_uploaded_file(controlFile)
            lattice['control'] = {}
            lattice['control']['name'] = controlFile.name
            #lattice['control']['data'] = unicode(controlFileContent, errors="ignore").splitlines()
            newcontrolFileContent = []
            for line in controlFileContent.splitlines():
                tmp=unicode(line, errors="ignore")
                if tmp.endswith('\n'):
                    newcontrolFileContent.append(tmp)
                else:
                    newcontrolFileContent.append(tmp+'\n')
                
            lattice['control']['data'] = newcontrolFileContent
        
        # Prepare lattice type
        request.POST['latticetype'] = json.dumps(latticeType)
        
        # Prepare lattice data
        request.POST['lattice'] = json.dumps(lattice)
        
        # Prepare creator
        request.POST['creator'] = request.user.username
        
        # Call the save lattice function
        result = saveLattice(request)
        return result
    
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        raise e
