'''
Created on Feb 15, 2013

@author: shengb
'''
from django.db import connection
try:
    from django.utils import simplejson as json
except ImportError:
    import json

import copy

from pymuniconv.municonvdata import municonvdata
from pymuniconv.municonvprop import (proptmplt, proptmpltdesc)
from pymuniconv.municonvprop import (proptmplt_chain, proptmpltdesc_chain)
from pymuniconv.municonvprop import (magneticlen, magneticlendesc)

from .conversion import conversion

municonv = municonvdata(connection)


def retrieveMeasurementDataInfo(params):
    '''
    Retrieve info about measurement data
    '''
    return municonv.retrieveMeasurementData(params['inventory_id'], params['cmpnt_type_name'])


def retrievesystemdata(params):
    '''
    acceptable key words:
     -- name

    return: a list of system name
    '''
    res = []
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
        elif names == "":
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

    return: list of dictionary
            [{'installId': ,
              'inventoryId': ,
              'name': ,
              'system': ,
              'serialNumber': ,
              'componentType': ,
              'typeDescription': ,
              'vendor': },
             ...
            ]
    '''
    if params.has_key('name'):
        name = params['name']
        if isinstance(name, (list, tuple)) and "" in name:
            name = "*"
    else:
        name = "*"

    cmpnt_type = None
    if params.has_key('cmpnt_type'):
        cmpnt_type = params['cmpnt_type']
        if isinstance(cmpnt_type, (list, tuple)) and "" in cmpnt_type:
            cmpnt_type = "*"

    location = None
    if params.has_key('system'):
        location = params['system']
        if isinstance(location, (list, tuple)) and "" in location:
            location = "*"

    serialno = None
    if params.has_key('serialno'):
        serialno = params['serialno']
        if isinstance(serialno, (list, tuple)) and "" in serialno:
            serialno = "*"

    if name == "*" and location == None:
        if serialno==None:
            tmps = municonv.retrieveinventory("*", ctypename=cmpnt_type)
        else:
            tmps = municonv.retrieveinventory(serialno, ctypename=cmpnt_type)
        key = ['installId', 'inventoryId', 'name', 'system', 'serialNumber', 'componentType', 'typeDescription', 'vendor']
        res = []
        for tmp in tmps:
            sub={}
            for i in range(len(key)):
                sub[key[i]] = tmp[i]
            res.append(sub)
    else:
        if serialno == None:
            serialno = "*"
        tmps = municonv.retrieveinstalledinventory(name, serialno, ctypename=cmpnt_type, location=location)
        key = ['installId', 'inventoryId', 'name', 'system', 'serialNumber', 'componentType', 'typeDescription', 'vendor']
        res = []
        for tmp in tmps:
            sub={}
            for i in range(len(key)):
                sub[key[i]] = tmp[i]
            res.append(sub)
    return res

def _updateconversioninfo(res4magenticlen, localdict):
    ''''''
    if res4magenticlen != None:
        tempdict = {'designLength': res4magenticlen[4]}

        for k, v in localdict.iteritems():
            for subk, subv in v.iteritems():
                subv.update(tempdict)
                v[subk] = subv
            localdict[k] = v

    return localdict


def _conversioninfobyinvid(invid):
    '''
    retrieve conversion information by inventory id
    Try to get each magnet measurement data. If not, use common info for that type.
    '''

    # select install.field_name, install.location, inventory.serial_no, cmpnt_type.cmpnt_type_name, cmpnt_type_prop.cmpnt_type_prop_value
    localdict = {}
    resfrominv = municonv.retrievemuniconv4inventory(invid, proptmplt, proptmpltdesc)

    if resfrominv != None:
        localdict['municonv'] = json.loads(resfrominv[4])

    else:
        resfromctype = municonv.retrievemuniconvbycmpnttype4inventory(invid, proptmplt, proptmpltdesc)
        if resfromctype != None:
            localdict['municonv'] = json.loads(resfromctype[4])

    resfrominvchain = municonv.retrievemuniconv4inventory(invid, proptmplt_chain, proptmpltdesc_chain)

    if resfrominvchain != None:
        localdict['municonvChain'] = json.loads(resfrominvchain[4])
    else:
        resfromctypechain = municonv.retrievemuniconvbycmpnttype4inventory(invid, proptmplt_chain, proptmpltdesc_chain)
        if resfromctypechain != None:
            localdict['municonvChain'] = json.loads(resfromctypechain[4])

    res4magenticlen = municonv.retrievemuniconvbycmpnttype4inventory(invid, magneticlen, magneticlendesc)
    localdict = _updateconversioninfo(res4magenticlen, localdict)
    return localdict

def _conversioninfobyfieldname(fieldname):
    '''
    get conversion information by field name.
    Since there is no way to identify the inventory id, use the common info for that type.
    '''
    localdict = {}
    resfromctype = municonv.retrievemuniconv4install(fieldname, proptmplt, proptmpltdesc)
    if resfromctype != None:
        localdict['municonv'] = json.loads(resfromctype[4])

    resfromctypechain = municonv.retrievemuniconv4install(fieldname, proptmplt_chain, proptmpltdesc_chain)
    if resfromctypechain != None:
        localdict['municonvChain'] = json.loads(resfromctypechain[4])

    res4magenticlen = municonv.retrievemuniconv4install(fieldname, magneticlen, magneticlendesc)
    localdict = _updateconversioninfo(res4magenticlen, localdict)
    return localdict


def retrieveconversioninfo(params, cache=False):
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
     -- complex: identify which complex it will convert

    Some global switch
     -- mcdata: return conversion information with result, False by default.
     -- cache: use cached value, False by default.
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
                invids = None
            else:
                invids = [invids]

    elif params.has_key('name'):
        names = params['name']

        if isinstance(names, (list, tuple)):
            invids = []
            fieldnames = []
            res = municonv.retrieveinventoryid(names)
            for r in res:
                invids.append(r[1])
                fieldnames.append(r[0])
        elif names != "":
            res = municonv.retrieveinventoryid(names)
            if len(res) == 0:
                invids = None
                fieldnames = None
            else:
                invids = []
                fieldnames = []
                for r in res:
                    invids.append(r[1])
                    fieldnames.append(r[0])
        else:
            invids = None
            fieldnames = None

    if invids == None or len(invids) == 0:
        invids = None

    if fieldnames == None or len(fieldnames) == 0:
        fieldnames = None

    # cache = True
    if params.has_key('cache'):
        cache = bool(json.loads(params['cache'].lower()))

    if fieldnames != None:

        # use field name as key
        for i in range(len(invids)):

            if cache and municonv.cachedconversioninfo.has_key(fieldnames[i]):
                resdict[fieldnames[i]] = copy.deepcopy(municonv.cachedconversioninfo[fieldnames[i]])

            else:
                invid = invids[i]

                if invid == None:
                    tmpres = _conversioninfobyfieldname(fieldnames[i])

                else:
                    tmpres = _conversioninfobyinvid(invid)

                resdict[fieldnames[i]] = copy.deepcopy(tmpres)
                municonv.cachedconversioninfo.update({fieldnames[i]: copy.deepcopy(tmpres)})

    elif invids != None:

        # use inventory id as key
        for invid in invids:

            if cache and municonv.cachedconversioninfo.has_key(invid):
                resdict[invid] = copy.deepcopy(municonv.cachedconversioninfo[invid])

            else:
                tmpres = _conversioninfobyinvid(invid)
                resdict[invid] = copy.deepcopy(tmpres)
                municonv.cachedconversioninfo.update({invid: copy.deepcopy(tmpres)})
    else:
        # no enough information, nothing can do.
        return resdict

    # If from and to are set, do conversion
    if params.has_key('from') and params.has_key('to') and params.has_key('value'):
        energy = None

        if params.has_key('energy'):
            energy = params['energy']
            if isinstance(energy, (list, tuple)):
                resdict['message'] = 'multiple beam energy found'
                return resdict
        mcdata = False

        if params.has_key('mcdata'):
            mcdata = bool(json.loads(params['mcdata'].lower()))

        src = params['from']
        dst = params['to']
        value = params['value']

        if isinstance(src, (list, tuple)) or isinstance(dst, (list, tuple)) or isinstance(value, (list, tuple)):
            resdict['message'] = 'too many conversion info found. Please check from, to, and/or value parameter.'
            return resdict

        if params.has_key('complex'):
            cmplxkey = params['complex']

        else:
            cmplxkey = None
        keys = ['municonv', 'municonvChain']

        for k, v in resdict.iteritems():
            for key in keys:
                if v.has_key(key):
                    municonvparams = v[key]
                    result = conversion(src, dst, value, municonvparams, energy=energy, mcdata=mcdata, cmplxkey=cmplxkey)
                    if result != None:
                        v[key] = result
                        resdict[k] = v
        return resdict
    else:
        return resdict

