'''
Created on May 9, 2013

@author: shengb
'''
from django.db import connection, transaction
try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pylattice.lattice import (lattice)
from pylattice.model import (model)

latinst = lattice(connection, transaction=transaction)
modelinst = model(connection)

def retrievelatticetype(params):
    '''
    The params is a dictionary with format: {'name': , 'format': }
    the name is supported lattice type name, and format is type format such as 'lat', 'ele', and/or 'txt'.
    '''
    names = params['name']
    formats = params['format']
    if not isinstance(names, list) and not isinstance(formats, list):  
        results = latinst.retrievelatticetype(names, formats)
        resdict = {}
        for res in results:
            resdict[res[0]] = {'name': res[1], 'format': res[2]}
        return resdict
    else:
        raise ValueError('No multiple searches for either name or format are implemented yet.')

def savelatticetype(params):
    '''
    The params is a dictionary with format: {'name': , 'format': }
    the name is supported lattice type name, and format is type format such as 'lat', 'ele', and/or 'txt'.
    '''
    result = latinst.savelatticetype(params['name'], params['format'])
    
    return {'result': result}

def savelatticeinfo(params):
    '''
    parameters:
        name:        lattice name
        version:     version number
        branch:      branch name
        latticetype: a dictionary which consists of {'name': , 'format': }
                     it is a predefined structure: [{'name': 'plain', 'format': 'txt'},
                                                    {'name': 'tracy3',  'format': 'lat'},
                                                    {'name': 'tracy4',  'format': 'lat'},
                                                    {'name': 'elegant', 'format': 'lte'}]
        
        description: description for this lattice, allow user put any info here (< 255 characters)
        creator:     original creator
        lattice:     lattice data, a dictionary:
                     {'name': ,
                      'data': ,
                      'raw':  ,
                      'map':  {'name': 'value'},
                     }
                     name: file name to be saved into disk, it is same with lattice name by default
                     data: lattice geometric and strength with predefined format
                     raw:  raw data that is same with data but in original lattice format
                     map:  name-value pair dictionary
    '''
    name = params['name']
    version = params['version']
    branch=params['branch']
    latticetype=None
    if params.has_key('latticetype'):
        latticetype = params['latticetype']
        latticetype = json.loads(latticetype)
        if not isinstance(latticetype, dict):
            raise TypeError("Lattice type data parameter format error.")
    description = None
    if params.has_key('description'):
        description = params['description']
    creator = None
    if params.has_key('creator'):
        creator = params['creator']

    result = latinst.savelatticeinfo(name, version, branch, latticetype=latticetype, description=description, creator=creator)
    
    return {"id": result}

def retrievelatticeinfo(params):
    '''
    '''
    name=params['name']
    if params.has_key('version'):
        version = params['version']
    else:
        version = None        
    if params.has_key('branch'):
        branch = params['branch']
    else:
        branch = None

    urls, lattices = latinst.retrievelatticeinfo(name, version=version, branch=branch)
    for k, v in lattices.iteritems():
        if urls[k] != None:
            v['url'] = urls[k]
            lattices[k] = v
    return lattices
    
def updatelatticeinfo(params):
    '''
    '''
    name = params['name']
    version = params['version']
    branch=params['branch']
    latticetype=None
    if params.has_key('latticetype'):
        latticetype = params['latticetype']
        latticetype = json.loads(latticetype)
        if not isinstance(latticetype, dict):
            raise TypeError("Lattice type data parameter format error.")
    description = None
    if params.has_key('description'):
        description = params['description']
    creator = None
    if params.has_key('creator'):
        creator = params['creator']
    
    result = latinst.updatelatticeinfo(name, version, branch, latticetype=latticetype, description=description, creator=creator)
    
    return {"result": result}
    
def savelattice(params):
    '''
    Save lattice data.
    parameters:
        name:        lattice name
        version:     version number
        branch:      branch name
        latticetype: a dictionary which consists of {'name': , 'format': }
                     it is a predefined structure: [{'name': 'plain', 'format': 'txt'},
                                                    {'name': 'tracy3',  'format': 'lat'},
                                                    {'name': 'tracy4',  'format': 'lat'},
                                                    {'name': 'elegant', 'format': 'lte'},
                                                    {'name': 'xal',     'format': 'xdxf'}]
        
        description: description for this lattice, allow user put any info here (< 255 characters)
        creator:     original creator
        lattice:     lattice data, a dictionary:
                     {'name': ,
                      'data': ,
                      'map': {'name': 'value'},
                     }
                     name: file name to be saved into disk, it is same with lattice name by default
                     data: lattice geometric and strength with predefined format
                     raw:  raw data that is same with data but in original lattice format
                     map:  name-value pair dictionary
    '''
    name=params['name']
    version=params['version']
    branch=params['branch']
    if params.has_key('latticetype'):
        latticetype = params['latticetype']
        latticetype = json.loads(latticetype)
        if not isinstance(latticetype, dict):
            raise TypeError("Lattice type data parameter format error.")
    else:
        latticetype=None
    if params.has_key('creator'):
        creator = params['creator']
    else:
        creator = None
        
    if params.has_key('description'):
        description = params['description']
    else:
        description = None
    if params.has_key('lattice'):
        lattice = params['lattice']
        lattice = json.loads(lattice)
        if not isinstance(lattice, dict):
            raise TypeError("Lattice type data parameter format error.")
    else:
        lattice = None
    
    result = latinst.savelattice(name, version, branch, creator=creator, description=description, 
                        latticetype=latticetype, lattice=lattice)
    return {'id': result}

def updatelattice(params):
    '''
    '''
    name=params['name']
    version=params['version']
    branch=params['branch']
    if params.has_key('latticetype'):
        latticetype = params['latticetype']
        latticetype = json.loads(latticetype)
        if not isinstance(latticetype, dict):
            raise TypeError("Lattice type data parameter format error.")
    else:
        latticetype=None
    if params.has_key('creator'):
        creator = params['creator']
    else:
        creator = None
        
    if params.has_key('description'):
        description = params['description']
    else:
        description = None
    if params.has_key('lattice'):
        lattice = params['lattice']
        lattice = json.loads(lattice)
        if not isinstance(lattice, dict):
            raise TypeError("Lattice type data parameter format error.")
    else:
        lattice = None
    
    result = latinst.updatelattice(name, version, branch, creator=creator, description=description, 
                                   latticetype=latticetype, lattice=lattice)
    return {'result': result}
    
def retrievelattice(params):
    '''
    '''
    name = params['name']
    version = params['version']
    branch=params['branch']
    if params.has_key('description'):
        description = params['description']
    else:
        description = None
    if params.has_key('latticetype'):
        latticetype = params['latticetype']
        latticetype = json.loads(latticetype)
        if not isinstance(latticetype, dict):
            raise TypeError("Lattice type data parameter format error.")
    else:
        latticetype = None  
    if params.has_key('withdata'):
        withdata = bool(json.loads(params['withdata'].lower()))
    else:
        withdata = False  
    if params.has_key('rawdata'):
        rawdata = bool(json.loads(params['rawdata'].lower()))
    else:
        rawdata = False  
        
    result = latinst.retrievelattice(name, version, branch, description=description, latticetype=latticetype, withdata=withdata, rawdata=rawdata)
    
    return result
    