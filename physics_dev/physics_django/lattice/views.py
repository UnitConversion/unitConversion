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

#post_actions = (('saveLatticeType', savelatticetype),
#                ('saveLatticeInfo', savelatticeinfo),
#                ('updateLatticeInfo', updatelatticeinfo),
#                #('saveLattice', savelattice),
#                ('updateLattice', updatelattice),
#                #('saveLatticeStatus', savelatticestatus),
#
#                ('saveModelCodeInfo', savemodelcodeinfo),
#                #('saveModelStatus', savemodelstatus),
#                #('saveModel', savemodel),
#                ('updateModel', updatemodel),
#                )
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
#                for p, _ in post_actions:
#                    if re.match(p, params['function']): 
#                        return HttpResponseBadRequest(HttpResponse(content='Wrong HTTP method for function %s'%p))
                res = dispatch(params, get_actions)
            else:
                res = {'message': 'No function specified.'}
#        elif request.method == 'POST':
#            params = _retrievecmddict(request.POST.copy())
#            if params.has_key('function'):
#                for p, _ in get_actions:
#                    if re.match(p, params['function']): 
#                        return HttpResponseBadRequest(HttpResponse(content='Wrong HTTP method for function %s'%p))
#                res = dispatch(params, post_actions)
#            else:
#                res = {'message': 'No function specified.'}
        else:
            latticemodel_log.debug('Unsupported HTTP method %s'%request.method)
            return HttpResponseBadRequest(HttpResponse(content='Unsupported HTTP method'), content_type="application/json")
    except ValueError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content=e), content_type="application/json")
    except KeyError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), content_type="application/json")
    except Exception as e:
        latticemodel_log.exception(e)
        return HttpResponseBadRequest(content=e, content_type="application/json")
    try:
        finalres = json.dumps(res)
    except Exception as e:
        latticemodel_log.exception(e)
        raise e
    return HttpResponse(finalres, content_type="application/json")

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
        return HttpResponseNotFound(HttpResponse(content=e), content_type="application/json")
    except KeyError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), content_type="application/json")
    except Exception as e:
        latticemodel_log.exception(e)
        return HttpResponseBadRequest(content=e, content_type="application/json")
    try:
        finalres = json.dumps(res)
    except Exception as e:
        latticemodel_log.exception(e)
        raise e

    return HttpResponse(finalres, content_type="application/json")

"""
Call saveLattice but before that check if user is logged in and if he has needed permissions
"""
@require_http_methods(["POST"])
@has_perm_or_basicauth('lattice.can_upload')
def saveLattice(request):
    try:
        params = _retrievecmddict(request.POST.copy())
        if not params.has_key('function'):
            params['function'] = 'saveLattice'
        if not params.has_key('creator'):
            params['creator'] = request.user.username
        res = savelattice(params)
    except ValueError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content=e), content_type="application/json")
    except KeyError as e:
        traceback.print_exc()
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), content_type="application/json")
    except Exception as e:
        latticemodel_log.exception(e)
        return HttpResponseBadRequest(content=e, content_type="application/json")
    try:
        finalres = json.dumps(res)
    except Exception as e:
        latticemodel_log.exception(e)
        raise e

    return HttpResponse(finalres, content_type="application/json")

"""
Call saveLatticeStatus but before that check if user is logged in and if he has needed permissions
"""
@require_http_methods(["POST"])
@has_perm_or_basicauth('lattice.can_upload')
def saveLatticeStatus(request):
    try:
        params = _retrievecmddict(request.POST.copy())
        params['function'] = 'saveLatticeStatus'
        res = savelatticestatus(params)
    except ValueError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content=e), content_type="application/json")
    except KeyError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), content_type="application/json")
    except Exception as e:
        latticemodel_log.exception(e)
        return HttpResponseBadRequest(content=e, content_type="application/json")
    try:
        finalres = json.dumps(res)
    except Exception as e:
        latticemodel_log.exception(e)
        raise e

    return HttpResponse(finalres, content_type="application/json")

"""
Call saveLatticeType but before that check if user is logged in and if he has needed permissions
"""
@require_http_methods(["POST"])
@has_perm_or_basicauth('lattice.can_upload')
def saveLatticeType(request):
    try:
        params = _retrievecmddict(request.POST.copy())
        params['function'] = 'saveLatticeType'
        res = savelatticetype(params)
    except ValueError as e:
        latticemodel_log.exception(e)
        return HttpResponseBadRequest(HttpResponse(content=e), content_type="application/json")
    except KeyError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), content_type="application/json")
    except Exception as e:
        latticemodel_log.exception(e)
        return HttpResponseBadRequest(content=e, content_type="application/json")
    try:
        finalres = json.dumps(res)
    except Exception as e:
        latticemodel_log.exception(e)
        raise e

    return HttpResponse(finalres, content_type="application/json")

"""
Call saveModel but before that check if user is logged in and if he has needed permissions
"""
@require_http_methods(["POST"])
@has_perm_or_basicauth('lattice.can_upload')
def saveModel(request):
    try:
        params = _retrievecmddict(request.POST.copy())
        if not params.has_key('function'):
            params['function'] = 'saveModel'
        res = savemodel(params, defaultuser = request.user.username)
    except ValueError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content=e), content_type="application/json")
    except KeyError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), content_type="application/json")
    except Exception as e:
        latticemodel_log.exception(e)
        return HttpResponseBadRequest(content=e, content_type="application/json")
    try:
        finalres = json.dumps(res)
    except Exception as e:
        latticemodel_log.exception(e)
        raise e

    return HttpResponse(finalres, content_type="application/json")

"""
Call saveModelStatus but before that check if user is logged in and if he has needed permissions
"""
@require_http_methods(["POST"])
@has_perm_or_basicauth('lattice.can_upload')
def saveModelStatus(request):
    try:
        params = _retrievecmddict(request.POST.copy())
        params['function'] = 'saveModelStatus'
        res = savemodelstatus(params)
    except ValueError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content=e), content_type="application/json")
    except KeyError as e:
        latticemodel_log.exception(e)
        return HttpResponseNotFound(HttpResponse(content="Parameters is missing for function %s"%(params['function'])), content_type="application/json")
    except Exception as e:
        latticemodel_log.exception(e)
        return HttpResponseBadRequest(content=e, content_type="application/json")
    try:
        finalres = json.dumps(res)
    except Exception as e:
        latticemodel_log.exception(e)
        raise e

    return HttpResponse(finalres, content_type="application/json")

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
    return render_to_response("lattice/details.html", context_instance = RequestContext(request))

def lattice_content_model_details(request):
    return render_to_response("lattice/model_details.html", context_instance = RequestContext(request))

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
@require_http_methods(["POST"])
def saveLatticeHelper(request):
    
    # Define file types
    latticeFileTypes = ['lat', 'lte', 'txt', 'in']
    controlFileFileTypes = ['ele']
    archiveFileFileTypes = ['zip']
    
    latticeType = json.loads(request.POST['latticetype'])
    latticeFile = None
    kickmapFile = None
    controlFile = None
    
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
                lattice['data'] = newcontent
            else:
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


'''
Save lattice type helper function prepares data for saving lattice status
'''
@require_http_methods(["POST"])
def saveLatticeTypeHelper(request):
    try:
        # Call the save lattice status function
        request.POST = request.POST.copy()
        result = saveLatticeType(request)
        return result

    except Exception as e:
        traceback.print_exc(file=sys.stdout)

'''
Save lattice status helper function prepares data for saving lattice status
'''
@require_http_methods(["POST"])
def saveLatticeStatusHelper(request):
    
    try:
        # Call the save lattice status function
        request.POST = request.POST.copy()
        request.POST['creator'] = request.user.username
        result = saveLatticeStatus(request)
        return result

    except Exception as e:
        traceback.print_exc(file=sys.stdout)

'''
Save model helper function that parses uploaded files and prepares data for saving model
'''
@require_http_methods(["POST"])
def saveModelHelper(request):
    
    # Define file types
    resultFileFileTypes = ['pm', 'csv' ]
    controlFileFileTypes = ['ele']
    
    resultFile = None
    controlFile = None
    
    # Go through all the uploaded files
    for fileObject in request.FILES.getlist('files'):
        fileNameParts = fileObject.name.split('.')
        fileType = fileNameParts[len(fileNameParts)-1]
        
        # Find lattice file
        if fileType in resultFileFileTypes:
            resultFile = fileObject
            continue
        
        # This can only be control file
        if fileType in controlFileFileTypes:
            controlFile = fileObject
            continue

    try:
        modelName = request.POST['modelname']
        simCodeAlg = request.POST['simcodealg'].split('/')
        model = {}
        model[modelName] = {}
        model[modelName]['description'] = request.POST['description']
        model[modelName]['creator'] = request.user.username
        
        if request.POST['tunex'] != "":
            model[modelName]['tunex'] = request.POST['tunex']
            
        if request.POST['tuney'] != "":
            model[modelName]['tuney'] = request.POST['tuney']
            
        if request.POST['alphac'] != "":
            model[modelName]['alphac'] = request.POST['alphac']
            
        if request.POST['chromX0'] != "":
            model[modelName]['chromX0'] = request.POST['chromX0']
            
        if request.POST['chromX1'] != "":
            model[modelName]['chromX1'] = request.POST['chromX1']
            
        if request.POST['chromX2'] != "":
            model[modelName]['chromX2'] = request.POST['chromX2']
            
        if request.POST['chromY0'] != "":
            model[modelName]['chromY0'] = request.POST['chromY0']
            
        if request.POST['chromY1'] != "":
            model[modelName]['chromY1'] = request.POST['chromY1']
            
        if request.POST['chromY2'] != "":
            model[modelName]['chromY2'] = request.POST['chromY2']
            
        if request.POST['finalEnergy'] != "":
            model[modelName]['finalEnergy'] = request.POST['finalEnergy']
            
        model[modelName]['simulationCode'] = simCodeAlg[0]
        model[modelName]['sumulationAlgorithm'] = simCodeAlg[1]
        
        # Remove parameters from the first level of POST dictionary
        del request.POST['description']
        del request.POST['simcodealg']
        del request.POST['tunex']
        del request.POST['tuney']
        del request.POST['alphac']
        del request.POST['chromX0']
        del request.POST['chromX1']
        del request.POST['chromX2']
        del request.POST['chromY0']
        del request.POST['chromY1']
        del request.POST['chromY2']
        del request.POST['finalEnergy']
        
        # Handle result file
        beamParameters = {}
        if resultFile != None:
            fileContent = handle_uploaded_file(resultFile)
            beamParametersHeaderLineParts = []
            
            # For each liin in a result file, split it and prepare necessary objects
            for line in fileContent.splitlines():
                # Skip comments, find beam parameter header line and save it
                if line.startswith(('#', '!', '//')):
                    commentLineParts = line.split()
                    
                    # Save header line for beam parameters and delete first element with # inside
                    if len(commentLineParts) > 2 and commentLineParts[1] == 'i':
                        beamParametersHeaderLineParts = commentLineParts
                        del beamParametersHeaderLineParts[0]
                    
                    continue
                
                # Split every line
                lineParts = line.split()
                
                # Insert model info
                #if len(lineParts) >= 2 and lineParts[0].isdigit() == False:
                #    model[modelName][lineParts[0]] = lineParts[1]
                
                # Insert beam parameters lines
                if len(beamParametersHeaderLineParts) > 0:
                    beamParametersRow = {}
                    transferMatrix = []
                    
                    # Add all parameters that are in the header. Last parameter is transfer matrix which shoud be dealth with separately
                    for column in range(1, len(beamParametersHeaderLineParts)-1):
                        beamParametersRow[beamParametersHeaderLineParts[column]] = lineParts[column]
                    
                    # Create pos property
                    beamParametersRow['position'] = beamParametersRow['s']
                    
                    # Correct codx property
                    if 'xcod' in beamParametersRow:
                        beamParametersRow['codx'] = beamParametersRow['xcod']
                    
                    # Correct cody property
                    if 'ycod' in beamParametersRow:
                        beamParametersRow['cody'] = beamParametersRow['ycod']
                    
                    # Correct phasex property
                    if 'nux' in beamParametersRow:
                        beamParametersRow['phasex'] = beamParametersRow['nux']
                    
                    # Correct phasey property
                    if 'nuy' in beamParametersRow:
                        beamParametersRow['phasey'] = beamParametersRow['nuy']
                    
                    # Add transfer matrix that should be at the end
                    matrixIndex = 1
                    transferMatrixRow = []
                    
                    # Last 36 values represent tranform matrix
                    for column in range(len(beamParametersHeaderLineParts)-1, len(lineParts)):
                        transferMatrixRow.append(float(lineParts[column]))
                        
                        # Make 6x6 matrix
                        if matrixIndex%6 == 0:
                            transferMatrix.append(transferMatrixRow)
                            transferMatrixRow = []
                            
                        matrixIndex += 1
                        
                    beamParametersRow['transferMatrix'] = transferMatrix
                    beamParameters[lineParts[0]] = beamParametersRow
        model[modelName]['beamParameter'] = beamParameters
        
        # Handle control file
        if controlFile != None:
            controlFileContent = handle_uploaded_file(controlFile)
            newcontrolFileContent = []
            for line in controlFileContent.splitlines():
                
                tmp=unicode(line, errors="ignore")
                if tmp.endswith('\n'):
                    newcontrolFileContent.append(tmp)
                else:
                    newcontrolFileContent.append(tmp+'\n')
            
            model[modelName]['simulationControlFile'] = controlFile.name
            model[modelName]['simulationControl'] = newcontrolFileContent
        
        # Prepare model data
        request.POST['model'] = json.dumps(model)
        
        # Call the save model function
        result = saveModel(request)
        return result
    
    except Exception as e:
        traceback.print_exc(file=sys.stdout)

'''
Save model status helper function prepares data for saving model status
'''
@require_http_methods(["POST"])
def saveModelStatusHelper(request):
    try:
        # Call the save model status function
        request.POST = request.POST.copy()
        request.POST['creator'] = request.user.username
        result = saveModelStatus(request)
        return result

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
