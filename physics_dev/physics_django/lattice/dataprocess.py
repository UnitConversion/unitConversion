'''
Created on May 9, 2013

@author: shengb
'''
from django.db import connection, transaction

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

