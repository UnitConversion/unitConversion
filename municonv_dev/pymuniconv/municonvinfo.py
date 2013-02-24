'''
Created on Feb 15, 2013

@author: shengb
'''
from django.db import connection
try:
    from django.utils import simplejson as json
except ImportError:
    import json

from scipy import optimize
from scipy.interpolate import InterpolatedUnivariateSpline

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
        localdict['municonv_chain'] = json.loads(resfrominvchain[2])
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
    if resfromctype != None:
        localdict['municonv'] = json.loads(resfromctype[2])
    
    resfromctypechain = municonv.retrievemuniconv4install(fieldname, proptmplt_chain, proptmpltdesc_chain)
    if resfromctypechain != None:
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
    if invids == None or len(invids) == 0:
        invids=None
    if fieldnames == None or len(fieldnames) == 0:
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
        mcdata=False
        if params.has_key('mcdata'):
            mcdata = True
        src = params['from']
        dst = params['to']
        value = params['value']
        
        keys = ['municonv', 'municonv_chain']
        
        for k, v in resdict.iteritems():
            for key in keys:
                if v.has_key(key):
                    municonvparams = v[key]
                    efflen=None
                    if v.has_key('design length'):
                        efflen = v['design length']
                    result = conversion(src, dst, value, municonvparams, energy=energy, mcdata=mcdata, efflen=efflen)
                    if result != None:
                        v[key] = result
                        resdict[k] = v
        return resdict
    else:
        return resdict

def _makei2b(expr, revert=False, y=0.0):
    f=None
    
    if revert:
        funcstr='''def f(input):
        return {e} - {y}
        '''.format(e=expr, y=y)        
    else:
        funcstr='''def f(input):
        return {e}
        '''.format(e=expr)
    exec(funcstr)
    return f

def _makeb2k(expr, revert=False, y=0.0):
    f=None
    
    if revert:
        funcstr='''def f(input, energy=None):
        if(energy == None):
            raise ValueError("Cannnot get beam energy")
        return {e} - {y}
        '''.format(e=expr, y=y)        
    else:
        funcstr='''def f(input, energy=None):
        if(energy == None):
            raise ValueError("Cannnot get beam energy")
        return {e}
        '''.format(e=expr)
    exec(funcstr)
    return f

def _doi2b(paramsdict, value, revert=False, key='i2b'):
    res = None
    if revert:
        message = 'successfully convert magnetic field to current.'
    else:
        message = 'successfully convert current to magnetic field.'
    if paramsdict.has_key(key):
        funcexpr = paramsdict[key]
        if funcexpr[0] == 0:
            # linear fitting with given function
            if revert:
                res = optimize.fsolve(_makei2b(funcexpr[1], revert=True, y = value), 0.0)[0]
            else:
                func = _makei2b(funcexpr[1])
                res = func(value)
        elif funcexpr[0] == 1:
            # high order polynomial fitting with given function.
            # need b2i to perform reversed calculation.
            if revert:
                message = "No algorithm found to convert magnetic field to current."
            else:
                func = _makei2b(funcexpr[1])
                res = func(value)
        elif funcexpr[0] == 2:
            # linear fitting without function given. Use raw data to do fitting.
            # to be implemented later
            if revert:
                message = "No algorithm found to convert magnetic field to current."
            else:
                message = "fitting raw data with linear function to be implemented later."
        elif funcexpr[0] == 3:
            # 1D interpolating with raw magnetic data
            # use up curve for current stage
            # user selection to be implemented later
            current = paramsdict['current']
            field = paramsdict['field']
            direction = paramsdict['direction']
            cur=[]
            fld=[]
            for i in range(len(direction)):
                if str(direction[i]).upper() in ['UP', 'NA', 'N/A']:
                    cur.append(current[i])
                    fld.append(field[i])
            if len(cur) != 0:
                if revert:
                    # fit field to current
                    # spline order: 1 linear, 2 quadratic, 3 cubic ... 
                    order = 1 
                    # do inter/extrapolation
                    func = InterpolatedUnivariateSpline(fld, cur, k=order)
#                    func = interp1d(fld, cur, kind='cubic')
                    res = func(value).item()
                else:
                    # fit current to field
                    # spline order: 1 linear, 2 quadratic, 3 cubic ... 
                    order = 3 
                    # do inter/extrapolation
                    func = InterpolatedUnivariateSpline(cur, fld, k=order)
                    res = func(value).item()
            else:
                message = "Data is not consistent, cannnot do interpolating."
        else:
            message = "Fitting algorithm is not supported yet."
    else:
        message = "No conversion algorithm available to convert magnet current to magnet field."
        
    return res, message

def _dob2k(paramsdict, value, energy, revert=False, efflen=None):
    res = None
    message = 'successfully convert magnetic field to K value.'
    if paramsdict.has_key('b2k'):
        funcexpr = paramsdict['b2k']
        if funcexpr[0] == 0:
            # linear fitting with given function
            if revert:
                res = optimize.fsolve(_makeb2k(funcexpr[1], revert=True, y = value), 0.0, energy)[0]
                if efflen != None:
                    res = res*efflen
            else:
                func = _makeb2k(funcexpr[1])
                res = func(value, energy)
                if efflen != None:
                    res = res/efflen
        elif funcexpr[0] == 1:
            # high order polynomial fitting with given function.
            # need b2i to perform reversed calculation.
            if revert:
                message = "No algorithm found to convert K value to magnetic field."
            else:
                func = _makeb2k(funcexpr[1])
                res = func(value, energy)
                if efflen != None:
                    res = res/efflen
        elif funcexpr[0] == 2:
            # linear fitting without function given. Use raw data to do fitting.
            # to be implemented later
            if revert:
                message = "No algorithm found to convert K value to magnetic field."
            else:
                message = "fitting raw data with linear function to be implemented later."
        elif funcexpr[0] == 3:
            # 1 D interpolating
            # to be implemented later
            message = "interpolating method to be implemented later."
        else:
            message = "Fitting algorithm is not supported yet."
    else:
        message = "No conversion algorithm available to convert magnet current to magnet field."
    
    return res, message

def doconversion(src, dst, value, paramsdict, energy=None, efflen=None):
    '''
    Carry out the unit conversion for given value between unit system source and destination.
    The conversion parameters are saved in paramdict.
    '''
    if (src == 'k' or dst == 'k') and energy == None and paramsdict.has_key('energy_default'):
        # use default energy
        energy = paramsdict['energy_default']
    
    value = _strunicode2num(value)
    energy = _strunicode2num(energy)
    if paramsdict.has_key('magnetic_len_means'):
        efflen=paramsdict['magnetic_len_meas']
    elif  paramsdict.has_key('magnetic_len_design'):
        efflen=paramsdict['magnetic_len_design']
    efflen = _strunicode2num(efflen)
    
    res = None
    message = ""
    if src == dst:
        message = "Conversion in the same unit system is not supported."
        #raise ValueError('Do not support conversion in the same unit system.')
    if src == 'i':
        if dst == 'b':
            res, message = _doi2b(paramsdict, value)
        elif dst == 'k':
            if energy == None:
                message = "No energy value given. Cannnot calculate the K value."
            else:
                if paramsdict.has_key('i2b'):
                    if paramsdict.has_key('b2k'):
                        res, message = _doi2b(paramsdict, value)
                        if res == None:
                            message = 'Failed to convert current to K value.'
                        else:
                            res, message = _dob2k(paramsdict, res, energy, efflen=efflen)
                            if res == None:
                                message = 'Failed to convert current to K value.'
                    else:
                        message = "Cannot find algorithm to convert current to K value."
                elif paramsdict.has_key('i2k'):
                    message = "Converting current directly to K value to be implemented later."
                else:
                    message = "Cannot find algorithm to convert current to K value."
    elif src == 'b':
        if dst == 'i':
            if paramsdict.has_key('b2i'):
                res, message = _doi2b(paramsdict, value, key='b2i')
            elif paramsdict.has_key('i2b'):
                res, message = _doi2b(paramsdict, value, revert=True)
        elif dst == 'k':
            res, message = _dob2k(paramsdict, value, energy, efflen=efflen)
            if res == None:
                message = 'Failed to convert magnetic field to K value.'
    elif src == 'k':
        if energy == None:
            message = "No energy value given. Cannnot calculate the magnetic field with given K value."
        else:
            if dst == 'i':
                if paramsdict.has_key('b2k'):
                    if paramsdict.has_key('i2b'):
                        res, message = _dob2k(paramsdict, value, energy, revert=True, efflen=efflen)
                        if res == None:
                            message = 'Failed to convert current to K value.'
                        else:
                            res, message = _doi2b(paramsdict, res, revert=True)
                            if res == None:
                                message = 'Failed to convert current to K value.'
                    elif paramsdict.has_key('b2i'):
                        res, message = _dob2k(paramsdict, value, energy, revert=True, efflen=efflen)
                        if res == None:
                            message = 'Failed to convert current to K value.'
                        else:
                            res, message = _doi2b(paramsdict, res, key='b2i')
                            if res == None:
                                message = 'Failed to convert current to K value.'
                    else:
                        message = "Cannot find algorithm to convert current to K value."
                elif paramsdict.has_key('k2i') or paramsdict.has_key('i2k'):
                    message = "Converting K value directly to current to be implemented later."
                else:
                    message = "Cannot find algorithm to convert K value to current."
            elif dst == 'b':
                res, message = _dob2k(paramsdict, value, energy, revert=True, efflen=efflen)
                if res == None:
                    message = 'Failed to convert K value to magnetic field.'
    
    return res, message

def _strunicode2num(value):
    if isinstance(value, str):
        res = float(value)
    elif isinstance(value, unicode):
        res = float(str(value))
    else:
        res=value
    return res

def conversion(src, dst, value, paramsdict, energy=None, mcdata=False, efflen=None):    
    if mcdata:
        resdict = paramsdict.copy()
    else:
        resdict={}
            
    if (src == 'k' or dst == 'k') and energy == None and paramsdict.has_key('energy_default'):
        # use default energy
        energy = paramsdict['energy_default']
    
    keys = ['1','2','3']
    for key in keys:
        if paramsdict.has_key(key):
            if mcdata:
                subparams = paramsdict[key]
            else:
                subparams = {}
            res, message = doconversion(src, dst, value, paramsdict[key], energy=energy, efflen=efflen)
            if res != None:
                subparams['result'] = res
            subparams['message'] = message
            resdict[key] = subparams
    if paramsdict.has_key('i2b') or paramsdict.has_key('b2k')  or paramsdict.has_key('b2i'):
        res, message = doconversion(src, dst, value, paramsdict, energy=energy, efflen=efflen)
        if res != None:
            resdict['result'] = res
        resdict['message'] = message

    return resdict
