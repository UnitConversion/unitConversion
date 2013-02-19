'''
Created on Feb 15, 2013

@author: shengb
'''
from django.db import connection
try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pymuniconv.municonvdata import municonvdata
from pymuniconv.municonvprop import (proptmplt, proptmpltdesc)
from pymuniconv.municonvprop import (proptmplt_chain, proptmpltdesc_chain)
from pymuniconv.municonvprop import (magneticlen, magneticlendesc)

municonv = municonvdata(connection)

def _getfirst(inst, getnone=True):
    '''
    get the first value if inst is a list or tuple.
    
    if inst is None, or empty string, return None when getnone is False,
    otherwise, return "*". 
    '''
    res = None
    if isinstance(inst, (list, tuple)):
        res=inst[0]
    else:
        res=inst
    if res=="" or res == None:
        if getnone:
            return None
        else:
            return "*"
    else:
        return res

def retrievesystemdata(params):
    '''
    acceptable key words:
     -- name
     
    return: a list of system name
    '''
    res=[]
    if params.has_key('name'):
        names = params['name']
        if isinstance(names, (list, tuple)):
            if "" in names:
                res = municonv.retrievesystem()
            else:
                for name in names:
                    temp = municonv.retrievesystem(name)
                    for x in temp:
                        res.append(x)
        elif name=="":
            res = municonv.retrievesystem()
        else:
            res = municonv.retrievesystem(names)
    else:
        res = municonv.retrievesystem()
    
    return res

def retrievemagnetinfo(params):
    '''
    acceptable key words:
     -- name
     -- cmpnt_type
     -- system
     -- serialno
    
    return: a 2-D array with format 
            [[install_id, inventory_id, field_name, location, serial_no, cmpnt_type_name, description, vendor_name], ...]
    '''
    if params.has_key('name'):
        name = _getfirst(params['name'], getnone=False)
    else:
        name = "*"

    cmpnt_type = None
    if params.has_key('cmpnt_type'):
        cmpnt_type = _getfirst(params['cmpnt_type'])

    location = None
    if params.has_key('system'):
        location = _getfirst(params['system'])
    
    serialno=None
    if params.has_key('serialno'):
        # get a list of devices from inventory which have been installed
        serialno = _getfirst(params['serialno'], getnone=False)

    if name == "*" and location == None:
        # returned data format 
        # ((inventory_id, serial_no, cmpnt_type_name, description, vendor_name), ...)
        res = municonv.retrieveinventory(serialno, ctypename=cmpnt_type)
        # convert to:
        # [[install_id, inventory_id, field_name, location, serial_no, cmpnt_type_name, description, vendor_name], ...]
        if len(res) >0:
            res = list(res)
            for i in range(len(res)):
                data = list(res[i])
                data.insert(1, '') # location place
                data.insert(1, '') # field name place
                data.insert(0, '') # install id place
                res[i] = data
    elif serialno == None:
        # returned data format
        # ((install id, field name, location, component type name, description, vendor), ...)
        res=municonv.retrieveinstall(name, ctypename=cmpnt_type, location=location)
        # convert to:
        # [[install_id, inventory_id, field_name, location, serial_no, cmpnt_type_name, description, vendor_name], ...]
        if len(res) >0:
            res = list(res)
            for i in range(len(res)):
                data = list(res[i])
                data.insert(3,'') # serial no place
                data.insert(1,'') # inventory id place
                res[i] = data
    else:
        # returned data format
        # ((install id, inventory id, field name, location, serial no, component type name, description, vendor), ...)
        res = municonv.retrieveinstalledinventory(name, serialno, ctypename=cmpnt_type, location=location)
    return res
   
def _conversioninfobyinvid(invid):
    '''
    retrieve conversion information by inventory id
    Try to get each magnet measurement data. If not, use common info for that type.
    '''
    localdict={}
    resfrominv = municonv.retrievemuniconv4inventory(invid, proptmplt, proptmpltdesc)
    if resfrominv != None:
        localdict['municonv'] = json.loads(resfrominv[2])
    else:
        resfromctype = municonv.retrievemuniconvbycmpnttype4inventory(invid, proptmplt, proptmpltdesc)
        if resfromctype != None:
            localdict['municonv'] = json.loads(resfromctype[2])
        
    resfrominvchain = municonv.retrievemuniconv4inventory(invid, proptmplt_chain, proptmpltdesc_chain)
    if resfrominvchain != None:
        localdict['municonv_chain'] = json.loads(resfrominv[2])
    else:
        resfromctypechain = municonv.retrievemuniconvbycmpnttype4inventory(invid, proptmplt_chain, proptmpltdesc_chain)
        if resfromctypechain != None:
            localdict['municonv_chain'] = json.loads(resfromctypechain[2])
    
    res4magenticlen = municonv.retrievemuniconvbycmpnttype4inventory(invid, magneticlen, magneticlendesc)
    if res4magenticlen != None:
        localdict['serial'] = res4magenticlen[0]
        localdict['type'] = res4magenticlen[1]
        localdict['design length'] = res4magenticlen[2]
    
    return localdict
    
def _conversioninfobyfieldname(fieldname):
    '''
    get conversion information by field name.
    Since there is no way to identify the inventory id, use the common info for that type.
    '''
    localdict = {}
    resfromctype = municonv.retrievemuniconv4install(fieldname, proptmplt, proptmpltdesc)
    if len(resfromctype) != 0:
        localdict['municonv'] = json.loads(resfromctype[2])
    
    resfromctypechain = municonv.retrievemuniconv4install(fieldname, proptmplt_chain, proptmpltdesc_chain)
    if len(resfromctypechain) != 0:
        localdict['municonv_chain'] = json.loads(resfromctypechain[2])
    
    res4magenticlen = municonv.retrievemuniconv4install(fieldname, magneticlen, magneticlendesc)
    if res4magenticlen != None:
        localdict['type'] = res4magenticlen[1]
        localdict['design length'] = res4magenticlen[2]
    
    return localdict
    
def retrieveconversioninfo(params):
    '''
    acceptable key words to identify device(s):
     -- id: inventory id
     or
     -- name: field name/device name
     
    for conversion:
     -- from (i, b, k)
     -- to (i, b, k)
     -- value
     -- unit
     -- energy
    '''
    resdict = {}
    names = None
    invids = None
    fieldnames = None
    if params.has_key('id'):
        invids = params['id']

        if isinstance(invids, (list, tuple)):
            temp = []
            for i in invids:
                if i != "":
                    temp.append(i)
            if len(temp) > 0:
                invids = temp
            else:
                invids = None
        else:
            if invids == "":
                invids=None
            else:
                invids=[invids]
    elif params.has_key('name'):
        names = params['name']
        if isinstance(names, (list, tuple)):
            invids = []
            fieldnames = []
            for name in names:
                if name != "":
                    res = municonv.retrieveinventoryid(name)
                    for r in res:
                        invids.append(r[1])
                        fieldnames.append(r[0])
        elif names != "":
            res = municonv.retrieveinventoryid(names)
            if len(res) == 0:
                invids = None
                fieldnames=None
            else:
                invids = []
                fieldnames = []
                for r in res:
                    invids.append(r[1])
                    fieldnames.append(r[0])
        else:
            invids = None
            fieldnames = None
    if len(invids) == 0:
        invids=None
    if len(fieldnames) == 0:
        fieldnames = None

    if fieldnames != None:
        # use field name as key
        for i in range(len(invids)):
            invid = invids[i]
            if invid == None:
                resdict[fieldnames[i]] = _conversioninfobyfieldname(fieldnames[i])
            else:
                resdict[fieldnames[i]] = _conversioninfobyinvid(invid)
    elif invids != None:
        # use inventory id as key
        for invid in invids:
            resdict[invid] = _conversioninfobyinvid(invid)
    else:
        #no enough information, nothing can do.
        return resdict
    
    if params.has_key('from') and params.has_key('to') and params.has_key('value'):
        energy=None
        if params.has_key('energy'):
            energy = params['energy']
        src = params['from']
        dst = params['to']
        value = params['value']
        
        keys = ['municonv', 'municonv_chain']
        for k, v in resdict.iteritems():
            for key in keys:
                if v.has_key(key):
                    municonvparams = v[key]
                    result = conversion(src, dst, value, municonvparams, energy=energy)
                    if result != None:
                        v[key] = result
                        resdict[k] = v
        return resdict
    else:
        return resdict
    
def conversion(src, dst, value, paramsdict, energy=None):
    '''
    Carry out the unit conversion for given value between unit system source and destination.
    The conversion parameters are saved in paramdict.
    '''
    if src == dst:
        return None
        #raise ValueError('Do not support conversion in the same unit system.')
    if src == 'i':
        if dst == 'b':
            pass
        elif dst == 'k':
            pass
    elif src == 'b':
        if dst == 'i':
            pass
        elif dst == 'k':
            pass
    elif src == 'k':
        if dst == 'i':
            pass
        elif dst == 'b':
            pass
    
    if paramsdict.has_key('i2b'):
        paramsdict['result'] = 3.456
    else:
        keys = ['1','2','3']
        for key in keys:
            if paramsdict.has_key(key):
                subparams = paramsdict[key]
                subparams['result'] = 1.234
                paramsdict[key] = subparams
    return paramsdict