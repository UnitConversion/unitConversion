import os
import sys

import traceback

import numpy as np

import cothread.catools as ca
from cothread import WaitForQuit

from municonvpy import UCClient
from pymuniconv.conversion import conversion

from _config import getpvfromfile, getpvfromcf

#UCURL = 'http://phyweb.cs.nsls2.local/magnets'
UCURL = 'http://localhost:8000/magnets'
#CFURL = 'http://channelfinder.nsls2.bnl.gov:8080/ChannelFinder/'

def getstandardparamdicts(convdata):
    resdict={}
    for magnets in convdata:
        tier0dict = {}
        for k0, v0 in magnets.conversionInfo.iteritems():
            tier1dict = {}
            for k1, data in v0.iteritems():
                algorithms = {}
                for k, v in data.algorithms.iteritems():
                    if v != None:
                        algorithms[k] = {'algorithmId':  v.algorithmId,
                                         'auxInfo':  v.auxInfo,
                                         'function': v.function,
                                         'initialUnit': v.initialUnit,
                                         'resultUnit':  v.resultUnit
                                         }
                measdata = {'aliasName': data.measurementData.aliasName, 
                            'conditionCurrent': data.measurementData.conditionCurrent, 
                            'current': data.measurementData.current, 
                            'currentUnit': data.measurementData.currentUnit, 
                            'description': data.measurementData.description, 
                            'direction': data.measurementData.direction, 
                            'field': data.measurementData.field, 
                            'fieldUnit': data.measurementData.fieldUnit, 
                            'referenceRadius': data.measurementData.referenceRadius,
                            'integralTransferFunction': data.measurementData.integralTransferFunction, 
                            }
                tier1dict[k1] = {'algorithms': algorithms,
                                 'defaultEnergy': data.defaultEnergy,
                                 'designLength': data.designLength,
                                 'measurementData': measdata
                                 }
            tier0dict[k0] = tier1dict
        resdict[magnets.name] = tier0dict
        
    return resdict

def savebuffertofile(fname, fbuffer):
    '''Save data buffer into file
    '''
    try:
        # remove old file if existing
        os.remove(fname)
    except OSError:
        pass
    with file(fname, 'w') as f:
        f.write(fbuffer)
    
def callback(value):
    """
    callback function
    
    Set value for B & K pvs which could be found from the following a dictionary:
        { 'pv name for I': {'element name': {'B': 'pv name for B',
                                             'K': 'pv name for K'},
                               ...
                           },
        ...
        }
    
    """
    _setpv(value.name, value)

def _setpv(pvname, origval):
    global pvspsdict
    global pvrbsdict
    global quadparams
    global sextparams
    global corrparams

    subpvs = None
    if pvspsdict.has_key(pvname):
        subpvs = pvspsdict[pvname]
    elif pvrbsdict.has_key(pvname):
        subpvs = pvrbsdict[pvname]
    else:
        raise ValueError('Cannot initialize associated pvs for %s'%(pvname))

    pvs = []
    vals = []
    for k, v in subpvs.iteritems():
        if origval.ok:
            if quadparams.has_key(k):
                try:
                    bresult = conversion('i', 'b', origval, quadparams[k]['municonv'])
                    
                    val = bresult['standard']['conversionResult']['value']
                    pvs.append(v['B'])
                    radius = quadparams[k]['municonv']['standard']['measurementData']['referenceRadius']
                    vals.append(val/radius)
                    pvs.append("%s.EGU"%v['B'])
                    unit = bresult['standard']['conversionResult']['unit']
                    if unit == 'T-m':
                        unit = 'T'
                    else:
                        unit = '/'.join((unit, 'm'))
                    vals.append(unit)
                    pvs.append("%s.DESC"%v['B'])
                    vals.append('Conversion succeeded')
                except ValueError:
                    pvs.append(v['B'])
                    vals.append(0.0)
                    pvs.append("%s.DESC"%v['B'])
                    vals.append('Conversion error')
                    pvs.append("%s.EGU"%v['B'])
                    vals.append('T')
                try:
                    kresult = conversion('i', 'k', origval, quadparams[k]['municonv'])
    
                    pvs.append(v['K'])
                    vals.append(kresult['standard']['conversionResult']['value'])
                    unit = kresult['standard']['conversionResult']['unit']
                    if unit == '1/m2':
                        unit = '1/m'
                    else:
                        unit = '*'.join((unit, 'm'))
                    pvs.append("%s.EGU"%v['K'])
                    vals.append(unit)
                    pvs.append("%s.DESC"%v['K'])
                    vals.append('Conversion succeeded')
    
                except ValueError:
                    pvs.append(v['K'])
                    vals.append(0.0)
                    pvs.append("%s.DESC"%v['K'])
                    vals.append('Conversion error')
                    pvs.append("%s.EGU"%v['K'])
                    vals.append('1/m')
            elif sextparams.has_key(k):
                try:
                    bresult = conversion('i', 'b', origval, sextparams[k]['municonv'])
                    
                    pvs.append(v['B'])
                    val = bresult['standard']['conversionResult']['value']
                    radius = sextparams[k]['municonv']['standard']['measurementData']['referenceRadius']
                    vals.append(val/radius**2)
    
                    unit = bresult['standard']['conversionResult']['unit']
                    if unit == 'T-m':
                        unit = 'T/m'
                    else:
                        unit = '/'.join((unit, 'm2'))
                    pvs.append("%s.EGU"%v['B'])
                    vals.append(unit)
                    
                    pvs.append("%s.DESC"%v['B'])
                    vals.append('Conversion succeeded')
                except ValueError:
                    pvs.append(v['B'])
                    vals.append(0.0)
                    pvs.append("%s.DESC"%v['B'])
                    vals.append('Conversion error')
                    pvs.append("%s.EGU"%v['B'])
                    vals.append('T/m')
                try:
                    kresult = conversion('i', 'k', origval, sextparams[k]['municonv'])
    
                    pvs.append(v['K'])
                    vals.append(kresult['standard']['conversionResult']['value'])
                    
                    pvs.append("%s.EGU"%v['K'])
                    unit = kresult['standard']['conversionResult']['unit']
                    if unit == '1/m3':
                        unit = '1/m2'
                    else:
                        unit = '*'.join((unit, 'm'))
                    vals.append(unit)
    
                    pvs.append("%s.DESC"%v['K'])
                    vals.append('Conversion succeeded')
                except ValueError:
                    pvs.append(v['K'])
                    vals.append(0.0)
                    pvs.append("%s.DESC"%v['K'])
                    vals.append('Conversion error')
                    pvs.append("%s.EGU"%v['B'])
                    vals.append('1/m2')
            elif corrparams.has_key(k):
                try:
                    pvs.append(v['B'])
                    vals.append(corrparams[k]*origval)
    
                    unit = 'T-m'
                    pvs.append("%s.EGU"%v['B'])
                    vals.append(unit)
                    
                    pvs.append("%s.DESC"%v['B'])
                    vals.append('Conversion succeeded')
                except ValueError:
                    pvs.append(v['B'])
                    vals.append(0.0)
                    pvs.append("%s.DESC"%v['B'])
                    vals.append('Conversion error')
                    pvs.append("%s.EGU"%v['B'])
                    vals.append('T-m')
                try:
                    pvs.append(v['K'])
                    # B0rho is 10.0007 for NSLS II storage ring
                    vals.append(corrparams[k]*origval/10.007)
    
                    pvs.append("%s.EGU"%v['K'])
                    unit = 'rad'
                    vals.append(unit)
    
                    pvs.append("%s.DESC"%v['K'])
                    vals.append('Conversion succeeded')
                except ValueError:
                    pvs.append(v['K'])
                    vals.append(0.0)
                    pvs.append("%s.DESC"%v['K'])
                    vals.append('Conversion error')
                    pvs.append("%s.EGU"%v['B'])
                    vals.append('rad')
            else:
                raise ValueError('Cannot find element for %s'%(k))
        else:
            if quadparams.has_key(k):
                pvs.append(v['B'])
                vals.append(0.0)
                pvs.append("%s.DESC"%v['B'])
                vals.append('PS Current PV disconnected')
                pvs.append("%s.EGU"%v['B'])
                vals.append('T')
                
                pvs.append(v['K'])
                vals.append(0.0)
                pvs.append("%s.DESC"%v['K'])
                vals.append('PS Current PV disconnected')
                pvs.append("%s.EGU"%v['K'])
                vals.append('1/m')
            elif sextparams.has_key(k):
                pvs.append(v['B'])
                vals.append(0.0)
                pvs.append("%s.DESC"%v['B'])
                vals.append('PS Current PV disconnected')
                pvs.append("%s.EGU"%v['B'])
                vals.append('T/m')
                
                pvs.append(v['K'])
                vals.append(0.0)
                pvs.append("%s.DESC"%v['K'])
                vals.append('PS Current PV disconnected')
                pvs.append("%s.EGU"%v['B'])
                vals.append('1/m2')
            elif corrparams.has_key(k):
                pvs.append(v['B'])
                vals.append(0.0)
                pvs.append("%s.DESC"%v['B'])
                vals.append('PS Current PV disconnected')
                pvs.append("%s.EGU"%v['B'])
                vals.append('T-m')
                
                pvs.append(v['K'])
                vals.append(0.0)
                pvs.append("%s.DESC"%v['K'])
                vals.append('PS Current PV disconnected')
                pvs.append("%s.EGU"%v['B'])
                vals.append('rad')
    try:
        ca.caput(pvs, vals)
    except ca.ca_nothing:
        print traceback.format_exc()
    
def startmonitor(pvsdict, readback=False):
    '''
    start to monitor all value of I.
    '''
    monstub = []
    # monitor alarm & any value change for set point
    evs = 5
    if readback:
        # monitor alarm & within dead band for readback
        evs = 6
        
    for keypv in pvsdict.keys():
        monstub.append(ca.camonitor(keypv, callback, events=evs, notify_disconnect = True))
        try:
            val = ca.caget(keypv)
            _setpv(keypv, val)
        except ca.ca_nothing:
            print traceback.format_exc()
    
    return monstub

def main(dbonly):
    global pvspsdict
    global pvrbsdict

    pvspsdict, pvrbsdict, dbbuffer, pvmappings = getpvfromfile('pvconfig.txt')
    if dbonly:
        savebuffertofile('municonv.db', dbbuffer)
        savebuffertofile('pvtable.txt', pvmappings)
    else:
        uc = UCClient(url=UCURL)
    
        qcs = uc.getConversionData(name="Q*")
        global quadparams
        quadparams = getstandardparamdicts(qcs)
        
        scs = uc.getConversionData(name="S*")
        global sextparams
        sextparams = getstandardparamdicts(scs)
        
        # load transfer function from file
        ccs = np.loadtxt('cor-transfer-func.txt', dtype=str, skiprows=3)
        global corrparams
        corrparams = dict(zip(ccs[:,0], [float(val) for val in ccs[:,1]]))
        
        startmonitor(pvspsdict)
        print 'finish setting monitors for set point pvs'
        startmonitor(pvrbsdict, readback=True)
        print 'finish setting monitors for read back pvs'
    
    print 'finish initialize magnet unit conversion IOC.'

if __name__ == "__main__":
    dbonly = True
    if len(sys.argv) > 1:
        dbonly = sys.argv[1]
    if dbonly in ['false', 'False', 'FALSE', 'F', 'f']:
        dbonly = False
    main(dbonly)
    if not dbonly:
        WaitForQuit()
    