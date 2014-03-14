'''
Created on Feb 27, 2014

@author: shengb
'''
import numpy as np
from scipy import optimize
#from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.interpolate import interp1d

import copy

scalingfactor = 0.9988

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

def _sortdata(x, y):
    length = len(x)
    if length != len(y):
        raise ValueError('Data set lengths are not equivalent.')
    
    oldset = []
    for i in range(length):
        oldset.append([x[i], y[i]])
    newset = sorted(oldset)
    new_x = []
    new_y = []
    for i in range(length):
        new_x.append(newset[i][0])
        new_y.append(newset[i][1])

    return new_x, new_y

def _quickfind(value, vallist):
    try:
        return vallist.index(value)
    except ValueError:
        length = len(vallist)
        if value < vallist[0]:
            return 0
        elif value > vallist[length-1]:
            return length
        elif value < vallist[length/2]:
            return _quickfind(value, vallist[:length/2])
        else:
            return length/2 + _quickfind(value, vallist[length/2:])

def _getsub(index, val, count=2):
    if index < count:
        return val[:2*count]
    elif index > (len(val)-count):
        return val[len(val)-2*count:]
    else:
        return val[index-count:index+count]

def _doi2b(paramsdict, value, revert=False, key='i2b'):
    res = None
    if revert:
        message = 'successfully convert magnetic field to current.'
    else:
        message = 'successfully convert current to magnetic field.'
    if paramsdict.has_key('algorithms') and paramsdict['algorithms'].has_key(key):
        funcdict = paramsdict['algorithms'][key]
        algorithmId = funcdict['algorithmId']
        funcexpr = funcdict['function']
        if algorithmId == 0:
            # linear fitting with given function
            if revert:
                res = optimize.fsolve(_makei2b(funcexpr, revert=True, y = value), 0.0)[0]
            else:
                func = _makei2b(funcexpr)
                res = func(value)
        elif algorithmId == 1:
            # high order polynomial fitting with given function.
            # need b2i to perform reversed calculation.
            if revert:
                message = "No algorithm found to convert magnetic field to current."
            else:
                func = _makei2b(funcexpr)
                res = func(value)
        elif algorithmId == 2:
            # polynomial fitting using raw data..
            # fitting order is determined by funcexpr
            if funcexpr < 1:
                res = None
                message = "ploy fitting order is zero."
            else:
                measurementdata = paramsdict['measurementData']
                current = measurementdata['current']
                field = measurementdata['field']
                direction = measurementdata['direction']
                fitorder = funcdict['auxInfo']
                cur=[]
                fld=[]
                for i in range(len(direction)):
                    if str(direction[i]).upper() in ['UP', 'NA', 'N/A']:
                        cur.append(current[i])
                        fld.append(field[i])
                
                if len (cur) == 1:
                    cur.insert(0, 0.0)
                    fld.insert(0, 0.0)
                if revert:
                    coeffs=np.polyfit(fld, cur, deg=fitorder)
                else:
                    coeffs=np.polyfit(cur, fld, deg=fitorder)
                res = np.polyval(coeffs, value)
        elif algorithmId == 3:
            # 1D interpolating with raw magnetic data
            # use up curve for current stage
            # user selection to be implemented later
            measurementdata = paramsdict['measurementData']
            current = measurementdata['current']
            field = measurementdata['field']
            direction = measurementdata['direction']
            cur=[]
            fld=[]
            for i in range(len(direction)):
                if str(direction[i]).upper() in ['UP', 'NA', 'N/A']:
                    cur.append(current[i])
                    fld.append(field[i])
            if len (cur) in [1, 2]:
                # if the data length is small, use linear fit instead
                if len (cur) == 1:
                    cur.insert(0, 0.0)
                    fld.insert(0, 0.0)
                x = cur
                y = fld
                if revert:
                    # fit field to current
                    x = fld
                    y = cur
                # sort data to ensure x value to be monotonically increasing
                #x, y = _sortdata(x, y)
                coeffs=np.polyfit(x,y, deg=1)
                res = np.polyfit(coeffs, value)
            elif len(cur) != 0:
                # use linear spline interpolation
                x = cur
                y = fld
                if revert:
                    # fit field to current
                    x = fld
                    y = cur
                # sort data to ensure x value to be monotonically increasing
                x, y = _sortdata(x, y)
                # algorithm 1
                # do inter/extrapolation
                # spline order: 1 linear, 2 quadratic, 3 cubic ... 
                #func = InterpolatedUnivariateSpline(x, y, k=1)
                
                # algorithm 2
                # 2nd order interpolation
                # func = interp1d(x, y, kind='cubic')
                func = interp1d(x, y)
                try:
                    res = func(value).item()
                except ValueError:
                    value *= -1
                    res = -1*func(value).item()
                
                #algorithm 3
                # 2nd order polynomial fitting
                #doit = True
                #reversesign = False
                #if value < x[0] or value > x[len(x)-1]:
                #    value*=-1
                #    if value < x[0] or value > x[len(x)-1]:
                #        doit=False
                #        message = "given value is out of data range, can not do interpolate it."
                #    else:
                #        reversesign = True
                #if doit:
                #    index = _quickfind(value, x)
                #    coeff = np.polyfit(_getsub(index, x), _getsub(index, y), 2)
                #    res = np.polyval(coeff,value)
                #    if reversesign:
                #        res *= -1
            else:
                message = "Data set is empty, cannnot do interpolating."
        else:
            message = "Fitting algorithm is not supported yet."
    else:
        message = "No conversion algorithm available to convert magnet current to magnet field."
        
    return res, message

def _dob2k(paramsdict, value, energy, revert=False, efflen=None):
    res = None
    message = 'successfully convert magnetic field to K value.'
    if paramsdict.has_key('algorithms') and paramsdict['algorithms'].has_key('b2k'):
        funcdict = paramsdict['algorithms']['b2k']
        algorithmId = funcdict['algorithmId']
        funcexpr = funcdict['function']
        if algorithmId == 0:
            # linear fitting with given function
            if revert:
                res = optimize.fsolve(_makeb2k(funcexpr, revert=True, y = value), 0.0, energy)[0]
                #if efflen != None:
                #    res = res*efflen
            else:
                func = _makeb2k(funcexpr)
                res = func(value, energy)
                #if efflen != None:
                #    res = res/efflen
        elif algorithmId == 1:
            # high order polynomial fitting with given function.
            # need b2i to perform reversed calculation.
            if revert:
                message = "No algorithm found to convert K value to magnetic field."
            else:
                func = _makeb2k(funcexpr)
                res = func(value, energy)
                #if efflen != None:
                #    res = res/efflen
        elif algorithmId == 2:
            # linear fitting without function given. Use raw data to do fitting.
            # to be implemented later
            if revert:
                message = "No algorithm found to convert K value to magnetic field."
            else:
                message = "fitting raw data with linear function to be implemented later."
        elif algorithmId == 3:
            # 1 D interpolating
            # to be implemented later
            message = "interpolating method to be implemented later."
        else:
            message = "Fitting algorithm is not supported yet."
    else:
        message = "No conversion algorithm available to convert magnet current to magnet field."
    
    return res, message

def doconversion(src, dst, value, paramsdict, energy=None):
    '''
    Carry out the unit conversion for given value between unit system source and destination.
    The conversion parameters are saved in paramdict.
    '''
    if (src == 'k' or dst == 'k') and energy == None and paramsdict.has_key('defaultEnergy'):
        # use default energy
        energy = paramsdict['defaultEnergy']
    
    value = _strunicode2num(value)
    energy = _strunicode2num(energy)
    efflen = None
    if paramsdict.has_key('measurementData'):
        measurementData = paramsdict['measurementData']
        if measurementData.has_key('averageLength'):
            efflen = _strunicode2num(measurementData['averageLength'])
    elif  paramsdict.has_key('designLength'):
        efflen=_strunicode2num(paramsdict['designLength'])
    
    res = None
    message = ""
    unit = ""
    conversiondict = paramsdict['algorithms']
    if src == dst:
        message = "Conversion in the same unit system is not supported."
        #raise ValueError('Do not support conversion in the same unit system.')
    if src == 'i':
        if dst == 'b':
            res, message = _doi2b(paramsdict, value)
            if res != None:
                unit = conversiondict['i2b']['resultUnit']
        elif dst == 'k':
            if energy == None:
                message = "No energy value given. Cannnot calculate the K value."
            else:
                if conversiondict.has_key('i2b'):
                    if conversiondict.has_key('b2k'):
                        res, message = _doi2b(paramsdict, value)
                        if res == None:
                            message = 'Failed to convert current to K value.'
                        else:
                            res, message = _dob2k(paramsdict, res, energy, efflen=efflen)
                            if res == None:
                                message = 'Failed to convert current to K value.'
                            else:
                                unit = conversiondict['b2k']['resultUnit']
                                message = 'successfully convert current to K value.'
                    else:
                        message = "Cannot find algorithm to convert current to K value."
                elif paramsdict.has_key('i2k'):
                    message = "Converting current directly to K value to be implemented later."
                else:
                    message = "Cannot find algorithm to convert current to K value."
    elif src == 'b':
        if dst == 'i':
            if paramsdict.has_key('algorithms'):
                if paramsdict['algorithms'].has_key('b2i'):
                    res, message = _doi2b(paramsdict, value, key='b2i')
                    if res != None:
                        unit = conversiondict['b2i']['resultUnit']
                elif paramsdict['algorithms'].has_key('i2b'):
                    res, message = _doi2b(paramsdict, value, revert=True)
                    if res != None:
                        unit = conversiondict['i2b']['initialUnit']
            else:
                message = "No conversion algorithm available to convert magnet current to magnet field."
        elif dst == 'k':
            res, message = _dob2k(paramsdict, value, energy, efflen=efflen)
            if res == None:
                message = 'Failed to convert magnetic field to K value.'
            else:
                unit = conversiondict['b2k']['resultUnit']
    elif src == 'k':
        if energy == None:
            message = "No energy value given. Cannnot calculate the magnetic field with given K value."
        else:
            if dst == 'i':
                if conversiondict.has_key('b2k'):
                    if conversiondict.has_key('i2b'):
                        res, message = _dob2k(paramsdict, value, energy, revert=True, efflen=efflen)
                        if res == None:
                            message = 'Failed to convert current to K value.'
                        else:
                            print res
                            res, message = _doi2b(paramsdict, res, revert=True)
                            if res == None:
                                message = 'Failed to convert K value to current.'
                            else:
                                unit = conversiondict['i2b']['initialUnit']
                    elif conversiondict.has_key('b2i'):
                        res, message = _dob2k(paramsdict, value, energy, revert=True, efflen=efflen)
                        if res == None:
                            message = 'Failed to convert current to K value.'
                        else:
                            res, message = _doi2b(paramsdict, res, key='b2i')
                            if res == None:
                                message = 'Failed to convert K value to current.'
                            else:
                                unit = conversiondict['i2b']['resultUnit']
                                message = 'successfully convert K value to current.'
                    else:
                        message = "Cannot find algorithm to convert current to K value."
                elif conversiondict.has_key('k2i') or conversiondict.has_key('i2k'):
                    message = "Converting K value directly to current to be implemented later."
                else:
                    message = "Cannot find algorithm to convert K value to current."
            elif dst == 'b':
                res, message = _dob2k(paramsdict, value, energy, revert=True, efflen=efflen)
                if res == None:
                    message = 'Failed to convert K value to magnetic field.'
                else:
                    unit = conversiondict['b2k']['initialUnit']
    
    res *= scalingfactor
    
    return res, message, unit

def _strunicode2num(value):
    if isinstance(value, str):
        res = float(value)
    elif isinstance(value, unicode):
        res = float(str(value))
    else:
        res=value
    return res

def conversion(src, dst, value, paramsdict, energy=None, mcdata=False, cmplxkey=None):
    resdict={}

    if cmplxkey != None:
        res, message, unit = doconversion(src, dst, value, paramsdict[cmplxkey], energy=energy)
        conversionresultdict = {'message': message,
                                'unit': unit,
                                'value': res
                                }
        tempdict = {}
        if mcdata:
            tempdict =  copy.deepcopy(paramsdict[cmplxkey])
        tempdict.update({'conversionResult':conversionresultdict})
        if energy != None:
            tempdict.update({'realEnergy': energy})
        resdict[cmplxkey] = tempdict
    else:
        for k, v in paramsdict.iteritems():
            # k would be either standard, complex:1, complex:2, complex:3, ...
            res, message, unit = doconversion(src, dst, value, v, energy=energy)
            conversionresultdict = {'message': message,
                                    'unit': unit,
                                    'value': res
                                    }
            tempdict = {}
            if mcdata:
                tempdict =  copy.deepcopy(v)
            tempdict.update({'conversionResult':conversionresultdict})
            if energy != None:
                tempdict.update({'realEnergy': energy})
            resdict[k] = tempdict

    return resdict