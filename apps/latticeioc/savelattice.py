import os
from collections import OrderedDict
import time

def _flattentracy3lattice(latfile):
    '''
    '''
    # this is not a general purpose routine very specific to lattice input
    # might fail if there is an extreme example
    latdict=OrderedDict()
    
    with file(latfile,'r') as f:
        templine = ''
        rawlatticedata = f.readlines()
        end=False
        committedline = False
        for line in rawlatticedata:
            if line.strip().startswith('{'):
                committedline = True
            if line.strip().endswith('}'):
                committedline = False
                line = ''
            if not committedline and line.strip()!='':
                if ';' in line:
                    templine += line
                    end=True
                else:
                    templine += line[:-1]
                    end=False
                if end:
                    if ':' in templine:
                        lineparts = templine.strip()[:-1].split(':')
                        latdict[lineparts[0].strip()] = lineparts[1]
                    templine = ''
    return latdict

def _readtracyresult(latfile, result):
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
    if not os.path.isfile(result):
        raise RuntimeError('Cannot get simulation result.')
    
    with file(result,'r') as f:
        twissdata = f.readlines()
    
    if len(twissdata) == 0:
        raise RuntimeError('Empty data file.')
    
    modeldata={'simulationCode': 'tracy3',
               'sumulationAlgorithm': 'SI'}
    beamparameter={}
    head = ['name','position',
            'alphax','betax','phasex','etax','etapx',
            'alphay','betay','phasey','etay','etapy',
            'codx','cody','dx','dy','pitch','yaw','transferMatrix']
    headlen=len(head)
    flattenlatdict = OrderedDict()
    for d in twissdata:
        fl = d.strip()
        if fl.startswith('#') or fl.startswith('!') or fl.startswith('//'):
            pass
        else:
            dtmps = fl.split()
            if dtmps[0] == 'tune':
                modeldata['tunex'] = dtmps[1]
                modeldata['tuney'] = dtmps[2]
            elif dtmps[0] == 'chrom':
                modeldata['chromX0'] = dtmps[1]
                modeldata['chromY0'] = dtmps[2]
            elif dtmps[0] == 'energy':
                modeldata['finalEnergy'] = dtmps[1]
            elif dtmps[0] == 'alphac':
                modeldata['alphac'] = dtmps[1]
            else:
                tmpdict = {}
                for i in range(headlen):
                    if head[i] != 'transferMatrix':
                        # no transfer matrix data
                        tmpdict[head[i]] = dtmps[i+1]
                    else:
                        # transfer matrix data 6x6
                        tm=[]
                        for j in range(6):
                            subtm=[]
                            for k in range(6):
                                subtm.append(float(dtmps[i+1+j*6+k]))
                            tm.append(subtm)
                        tmpdict[head[i]]=tm
                beamparameter[dtmps[0]] = tmpdict
                flattenlatdict[dtmps[0]] = {'name': dtmps[1].upper(),
                                            'position': dtmps[2]}
    modeldata['beamParameter'] = beamparameter
    
    if not os.path.isfile(latfile):
        raise RuntimeError('Cannot find lattice file.')
    latdict = _flattentracy3lattice(latfile)
    
    for k, v in flattenlatdict.iteritems():
        if k != '0':
            # twiss file includes element 'BEGIN'
            props = [x.strip() for x in latdict[v['name']].split(',')]
            if props[0].upper() == 'CORRECTOR':
                # find direction info for corrector
                etype = props[0]
                for tmp in props[1:]:
                    if '=' not in tmp:
                        etype = ','.join((etype, tmp))
            else:
                etype = props[0]
            v['type'] = etype
            for tmp in props:
                if '=' in tmp:
                    tmpparts = [x.strip() for x in tmp.split('=')]
                    # update value
                    if tmpparts[0] in ['L','l']:
                        v['length'] = tmpparts[1]
                    else:
                        v[tmpparts[0]] = tmpparts[1]
                    
            flattenlatdict[k] = v
        else:
            v['type'] = 'Marker'
            v['length'] = '0.0'
            flattenlatdict[k] = v
    
    return flattenlatdict, modeldata

def savelatticemodel(latfile, pfile, lmc, source=None, name=None, version=None, branch='live'):
    name = os.path.splitext(os.path.basename(latfile))[0]
    
    if version == None:
        version = int(time.time())

    flatlat, modeldata = _readtracyresult(latfile, pfile)

    if branch == 'live':
        timestr = time.strftime("%a, %d %b %Y, %H:%M:%S %Z", time.localtime(version))
    else:
        timestr = version
    if source != None:
        description = "This is a lattice from %s for %s machine on %s" %(source, branch, timestr)
    else:
        description = "This is a lattice for %s machine on %s" %(branch, timestr)
    latticetype = {'name': 'tracy3',
                   'format': 'lat'}

    try:
        lmc.saveLattice(name, branch, version, latfile, latdata=flatlat, description=description, latticetype=latticetype)
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
        #os.remove(latfile)
        os.remove(pfile)
    except OSError:
        pass

if __name__ == '__main__':
    from latticepy.LatticeModelClient import LatticeModelClient
    import time

    url = 'http://localhost:8080/lattice'
    lmc = LatticeModelClient(BaseURL=url, username='', password='')
    
    latticetype = [{'name': 'tracy3', 'format': 'lat'},
                   {'name': 'tracy4', 'format': 'lat'},
                   {'name': 'elegant', 'format': 'lte'},
                   {'name': 'plain', 'format': 'txt'}
                   ]

    for lt in latticetype:
        res = lmc.retrievelattype(lt['name'], lt['format'])
        if len(res) == 0:
            print lmc.savelattype(lt['name'], lt['format'])
        else:
            print "lattice type (name: %s, format: %s) exists already"%(lt['name'], lt['format'])

