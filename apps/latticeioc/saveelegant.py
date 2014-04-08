'''
Created on Apr 7, 2014

@author: shengb
'''
import os
from collections import OrderedDict
import time

import subprocess

import numpy as np

runelegantdir = 'runelegant'

def _flattenelegantlattice(latfile):
    '''
    '''
    # this is not a general purpose routine very specific to lattice input
    # might fail if there is an extreme example
    latdict=OrderedDict()
    with file(latfile,'r') as f:
        rawlatticedata = f.readlines()
        newline = ""
        for line in rawlatticedata:
            # remove \n of each line
            linevals = line[:-1].strip().split("!")
            tmpline = linevals[0].strip()
            
            if tmpline != "":
                newline += tmpline
                if newline.endswith("&"):
                    newline=newline[:-1]
                else:
                    if ":" in newline:
                        linevals = newline.split(':')
                        if not linevals[1].strip().startswith('LINE'):
                            ename = linevals[0].strip()
                            eprops = linevals[1].strip().split(',')
                            tmpdict = {'type': eprops[0].strip()}
                            if len(eprops) > 1:
                                for eprop in eprops[1:]:
                                    ep = eprop.strip().split('=')
                                    if ep[0].strip().upper() == 'L':
                                        tmpdict['length']=ep[1].strip()
                                    else:
                                        tmpdict[ep[0].strip()]=ep[1].strip()
                            latdict[ename]=tmpdict
                    newline=""
    return latdict

def _readelegantresult(latname, controls=None, flattenlat=False):
    '''
    Read simulation result from a text output file
    
    return a structure as below:
        { # header information
         'description': ,          # description of this model
         'tunex': ,                # horizontal tune
         'tuney': ,                # vertical tune
         'chromX0': ,             # linear horizontal chromaticity
         'chromX1': ,             # non-linear horizontal chromaticity
         'chromX2': ,             # high order non-linear horizontal chromaticity
         'chromY0': ,             # linear vertical chromaticity
         'chromY1': ,             # non-linear vertical chromaticity
         'chromY2': ,             # high order non-linear vertical chromaticity
         'finalEnergy': ,          # the final beam energy in GeV
         'simulationCode': ,       # name of simulation code, Elegant and Tracy for example
         'sumulationAlgorithm': ,  # algorithm used by simulation code, for example serial or parallel,
                                   # and SI, or SI/PTC for Tracy code
         'simulationControl': ,    # various control constrains such as initial condition, beam distribution, 
                                   # and output controls
         'simulationControlFile':  # file name that control the simulation conditions, like a .ele file for elegant
         
         # simulation data
         'beamParameter':          # a dictionary consists of twiss, close orbit, transfer matrix and others
        }
        
        beamParameter sub-structure
        { element_order: #element_order starts with 0, which is the begin of simulation with s=0.
            { 'name': ,
              'position': ,
              'alphax': ,
              'alphay': ,
              'betax': ,
              'betay': ,
              'etax': ,
              'etay': ,
              'etapx': ,
              'etapy': ,
              'phasex': ,
              'phasey': ,
              'codx': ,
              'cody': ,
              'transferMatrix': ,
              'indexSliceCheck': ,
              's': ,
              'energy': ,
              'particleSpecies': ,
              'particleMass': ,
              'particleCharge': ,
              'beamChargeDensity': ,
              'beamCurrent': ,
              'x': ,
              'xp': ,
              'y': ,
              'yp': ,
              'z': ,
              'zp': ,
              'emittancex': ,
              'emittancey': ,
              'emittancexz':  
            }
         }
    '''
    datafile=[]
    # global beam parameter
    datafile.append('/'.join((runelegantdir, "%s-bpm.txt"%(latname))))
    # closed orbit
    datafile.append('/'.join((runelegantdir, "%s-orb.txt"%(latname))))
    # twiss parameter
    datafile.append('/'.join((runelegantdir, "%s-twiss.txt"%(latname))))
    # flat lattice
    datafile.append('/'.join((runelegantdir, "%s-par.txt"%(latname))))
    # transfer matrix
    datafile.append('/'.join((runelegantdir, "%s-matrix.txt"%(latname))))
    
    for f in datafile:
        if not os.path.isfile(f):
            raise RuntimeError('Fail to run elegant simulation. Could not find data file: %s'%f)

    modeldata={'simulationCode': 'elegant',
               'sumulationAlgorithm': 'matrix'}

    if controls != None:
        modeldata['simulationControlFile']=controls['name']
        with file('/'.join((runelegantdir, controls['name'])), 'r') as f:
            modeldata['simulationControl']=f.readlines()
    # read global twiss data
    with file(datafile[0], 'r') as f:
        data=f.readlines()
    if len(data) == 0:
        raise RuntimeError('Empty data. Cannot get any simulation result.')
    else:
        for d in data:
            d=d.replace('"','')
            dvals = d.split(',')
            if len(dvals) == 2:
                if dvals[0] == 'nux':
                    modeldata['tunex'] = dvals[1][:-1].strip()
                elif dvals[0] == 'nuy':
                    modeldata['tuney'] = dvals[1][:-1].strip()
               
                elif dvals[0] == 'dnux/dp':
                    modeldata['chromX0'] = dvals[1][:-1].strip()
                elif dvals[0] == 'dnux/dp2':
                    modeldata['chromX1'] = dvals[1][:-1].strip()
                elif dvals[0] == 'dnux/dp3':
                    modeldata['chromX2'] = dvals[1][:-1].strip()
                
                elif dvals[0] == 'dnuy/dp':
                    modeldata['chromY0'] = dvals[1][:-1].strip()
                elif dvals[0] == 'dnuy/dp2':
                    modeldata['chromY1'] = dvals[1][:-1].strip()
                elif dvals[0] == 'dnuy/dp3':
                    modeldata['chromY2'] = dvals[1][:-1].strip()
                    
                elif dvals[0] == 'alphac':
                    modeldata['alphac'] = dvals[1][:-1].strip()
                elif dvals[0] == 'pCentral':
                    modeldata['finalEnergy'] = dvals[1][:-1].strip()

    # read closed orbit data
    coddata = np.loadtxt(datafile[1], dtype=str)
    if len(coddata) == 0:
        raise RuntimeError('Cannot get simulation result for closed orbit.')
    elemlen = len(coddata)

    twissdata = np.loadtxt(datafile[2], dtype=str)
    if len(twissdata) != elemlen:
        raise RuntimeError('Cannot get simulation result for twiss optics.')

    flatlatdata = np.loadtxt(datafile[3], dtype=str)
    if len(flatlatdata) != elemlen:
        raise RuntimeError('Cannot get simulation result for flat lattice.')

    tmatdata = np.loadtxt(datafile[4], dtype=str)
    if len(tmatdata) != elemlen:
        raise RuntimeError('Cannot get simulation result for transfer matrix.')

    beamparameter={}
    flattenlatdict = OrderedDict()
    ename = coddata[:, 0]
    etype = coddata[:, 1]
    
    for i in range(elemlen):
        if ename[i] != twissdata[i][0] or ename[i] != flatlatdata[i][0] or ename[i] != tmatdata[i][0] or \
           etype[i] != twissdata[i][1] or etype[i] != flatlatdata[i][1] or etype[i] != tmatdata[i][1]:
            raise RuntimeError("Element does not match in simulation results")

        tm=[]
        for j in range(6):
            # transfer matrix data 6x6
            subtm=[]
            for k in range(6):
                subtm.append(float(tmatdata[i][3+j*6+k]))
            tm.append(subtm)

        tmpdict = {'name': ename[i],
                   'position':float(twissdata[i][2]),
                   'alphax':  float(twissdata[i][3]),
                   'betax':   float(twissdata[i][4]),
                   'phasex':  float(twissdata[i][5]),
                   'etax':    float(twissdata[i][6]),
                   'etapx':   float(twissdata[i][7]),
                   'alphay':  float(twissdata[i][8]),
                   'betay':   float(twissdata[i][9]),
                   'phasey':  float(twissdata[i][10]),
                   'etay':    float(twissdata[i][11]),
                   'etapy':   float(twissdata[i][12]),
                   'energy':  float(twissdata[i][13]),
                   'codx':    float(coddata[i][3]),
                   'cody':    float(coddata[i][5]),
                   'transferMatrix':tm}
        beamparameter[str(i)] = tmpdict

        flattenlatdict[str(i)] = {'name': flatlatdata[i][0].upper(),
                                  'type': flatlatdata[i][1],
                                  'position': float(flatlatdata[i][2]),
                                  'length': float(flatlatdata[i][3])}
    modeldata['beamParameter'] = beamparameter
    
    if flattenlat:
        latfile='/'.join((runelegantdir, "%s.lte"%(latname)))
        if not os.path.isfile(latfile):
            raise RuntimeError('Cannot find lattice file.')
        latdict = _flattenelegantlattice(latfile)

        for k, v in flattenlatdict.iteritems():
            ename = v['name']
            etype = v['type']
            if ename.upper() != '_BEG_':
                if latdict.has_key(ename):
                    elemprops = latdict[ename].copy()
                else:
                    raise RuntimeError("Cannot find element %s in lattice deck."%(ename))
                if elemprops['type'] != etype:
                    raise RuntimeError("Element %s type conflict."%(ename))
                elemprops.update(v)
                flattenlatdict[k] = elemprops

    return flattenlatdict, modeldata

def savelatticemodel(latfile, params, lmc, source=None, name=None, version=None, branch='live'):
    if name == None:
        name = os.path.splitext(os.path.basename(latfile))[0]
    
    if version == None:
        version = int(time.time())

    flatlat, modeldata = _readelegantresult(os.path.splitext(os.path.basename(params['name']))[0], 
                                            controls=params, flattenlat=True)
    
    if branch == 'live':
        timestr = time.strftime("%a, %d %b %Y, %H:%M:%S %Z", time.localtime(version))
    else:
        timestr = version
    if source != None:
        description = "This is a lattice from %s for %s machine on %s" %(source, branch, timestr)
    else:
        description = "This is a lattice for %s machine on %s" %(branch, timestr)
    latticetype = {'name': 'elegant',
                   'format': 'lte'}

    try:
        lmc.saveLattice(name, branch, version, latfile, 
                        latdata=flatlat, description=description, latticetype=latticetype,
                        elefile = params['name'],
                        topdir=runelegantdir)
    except:
        print 'Not save lattice for %s (branch %s, version %s)' %(name, branch, version)
    
    modeldata['description'] = '%s machine result performed by lattice IOC on %s'%(branch, timestr)
    if source != None:
        modelname = '%s machine model for %s on %s for %s (branch %s, version %s)'%(branch, source, timestr, name, branch, version)
    else:
        modelname = '%s machine model on %s for %s (branch %s, version %s)'%(branch, timestr, name, branch, version)

    try:
        lmc.saveModel(name, branch, version, {modelname:modeldata})
    except:
        print "Not save mode: %s"%modelname

    try:
        # delete intermediate files except the lte and ele files
        subprocess.Popen('ls |grep -v lte|grep -v ele|xargs rm', 
                         shell=True, 
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    except OSError:
        pass
