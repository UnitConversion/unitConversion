'''
Created on Jun 7, 2013

@author: shengb
'''
import os
import errno
import shutil
import subprocess
from collections import OrderedDict
import base64

runtracydir = 'runtracy'
runelegantdir = 'runelegant'

from .logger import _setup_lattice_model_logger
latticemodel_log = _setup_lattice_model_logger("runsimulation")

#NSLS2_LBT_TWISS_INIT = [-0.5, -0.6, 4.5, 4.6, 0.0, 0.0, 0.0, 0.0]
#NSLS2_BST_TWISS_INIT = [0.663442, 0.936493, 9.35591, 8.63852, 0.148315, 0.0000, 0.0000, 0.0000]

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
                        latdict[lineparts[0]] = lineparts[1]
                    templine = ''
    return latdict

def _flattentracy4lattice(latfile):
    '''
    '''
    raise RuntimeError("Tracy4 support has not been implemented yet.")


def _readtracyresult(latname, tracy='tracy3', flattenlat=False):
    '''
    Read simulation result from a text output file
    
    return a structure as below:
        { # header information
         'description': ,          # description of this model
         'tunex': ,                # horizontal tune
         'tuney': ,                # vertical tune
         'chromex0': ,             # linear horizontal chromaticity
         'chromex1': ,             # non-linear horizontal chromaticity
         'chromex2': ,             # high order non-linear horizontal chromaticity
         'chromey0': ,             # linear vertical chromaticity
         'chromey1': ,             # non-linear vertical chromaticity
         'chromey2': ,             # high order non-linear vertical chromaticity
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
    pmfile='/'.join((runtracydir, "%s.pm"%(latname)))
    if not os.path.isfile(pmfile):
        latticemodel_log.debug('Running tracy simulation failed.')
        raise RuntimeError('Fail to run tracy simulation.')
    
    with file(pmfile,'r') as f:
        data = f.readlines()
    
    if len(data) == 0:
        raise RuntimeError('Empty data. Cannot get any simulation result.')
    
    modeldata={'simulationCode': 'tracy3',
               'sumulationAlgorithm': 'SI'}
    beamparameter={}
    head = ['name','position',
            'alphax','betax','phasex','etax','etapx',
            'alphay','betay','phasey','etay','etapy',
            'codx','cody','dx','dy','pitch','yaw','transferMatrix']
    headlen=len(head)
    flattenlatdict = OrderedDict()
    for d in data:
        fl = d.strip()
        if fl.startswith('#') or fl.startswith('!') or fl.startswith('//'):
            pass
        else:
            dtmps = fl.split()
            if dtmps[0] == 'tune':
                modeldata['tunex'] = dtmps[1]
                modeldata['tuney'] = dtmps[2]
            elif dtmps[0] == 'chrom':
                modeldata['chromex0'] = dtmps[1]
                modeldata['chromey0'] = dtmps[2]
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
    
    if flattenlat:
        latfile='/'.join((runtracydir, "%s.lat"%(latname)))
        if not os.path.isfile(latfile):
            latticemodel_log.debug('Cannot find lattice file.')
            raise RuntimeError('Cannot find lattice file.')
        if tracy=='tracy3':
            latdict = _flattentracy3lattice(latfile)
        elif tracy=='tracy4':
            latdict = _flattentracy4lattice(latfile)

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

def runtracy(latticedata, tracy='tracy3', flattenlat=False):
    '''
    Run tracy simulation
    '''
    if tracy=='tracy3':
        if os.environ.has_key('TRACY3_CMD'):
            tracy_cmd=os.environ['TRACY3_CMD']
        else:
            tracy_cmd='tracy3'
    else:
        if os.environ.has_key('TRACY4_CMD'):
            tracy_cmd=os.environ['TRACY4_CMD']
        else:
            tracy_cmd='tracy4'
    
    latfile=None
    latname=None
    if os.path.isdir(runtracydir):
        shutil.rmtree(runtracydir)

    try:
        os.makedirs(runtracydir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(runtracydir):
            pass
        else: 
            raise Exception("Could not create a directory to save lattice file")
    
    if latticedata.has_key('name') and latticedata['name'] !=None:
        if latticedata['name'].strip().endswith('.lat'):
            latfile = latticedata['name'].strip()
            latname, _ = os.path.splitext(latfile)
        else:
            latname = latticedata['name'].strip()
            latfile = latname+'.lat'
    if latfile ==None or latname == None or len(latname) ==0:
        raise ValueError("Cannot run tracy. Wrong lattice deck name.")
    
    if latticedata.has_key('raw') and latticedata['raw']!=None:
        with file('/'.join((runtracydir,latfile)), 'w') as f:
            for d in latticedata['raw']:
                f.write(d)
    if latticedata.has_key('map') and latticedata['map']!=None:
        for kmkey, kmdata in latticedata['map'].iteritems():
            dirname, _ = os.path.split(kmkey)
            try:
                # create a sub directory to store field map
                os.makedirs('/'.join((runtracydir,dirname)))
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir('/'.join((runtracydir,dirname))):
                    pass
                else: 
                    raise Exception("Can not create a sub directory to store map")
            with file('/'.join((runtracydir, kmkey.lower())), 'w') as f:
                for kmd in kmdata:
                    f.write(kmd)
    
    if latticedata.has_key('alignment'):
        # ignore mis-alignment error for now
        pass

    proc = subprocess.Popen('cd %s; %s %s %s.pm; cd -'
                            %(runtracydir, tracy_cmd, latname, latname), 
                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutdata, stderrdata = proc.communicate()
    latticemodel_log.debug(stdoutdata)
    latticemodel_log.debug('std error - ' + stderrdata)
    latticemodel_log.debug('Finish running tracy simulation')
    
    result = _readtracyresult(latname, tracy=tracy, flattenlat=flattenlat)    
    # clean directory
    shutil.rmtree(runtracydir)
    
    return result


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
         'chromex0': ,             # linear horizontal chromaticity
         'chromex1': ,             # non-linear horizontal chromaticity
         'chromex2': ,             # high order non-linear horizontal chromaticity
         'chromey0': ,             # linear vertical chromaticity
         'chromey1': ,             # non-linear vertical chromaticity
         'chromey2': ,             # high order non-linear vertical chromaticity
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
            latticemodel_log.debug('Running elegant simulation failed. Could not find data file: %s'%f)
            raise RuntimeError('Fail to run elegant simulation. Could not find data file: %s'%f)

    modeldata={'simulationCode': 'elegant',
               'sumulationAlgorithm': 'matrix'}

    if controls != None:
        modeldata['simulationControlFile']=controls['name']
        modeldata['simulationControl']=controls['data']
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
                    modeldata['chromex0'] = dvals[1][:-1].strip()
                elif dvals[0] == 'dnux/dp2':
                    modeldata['chromex1'] = dvals[1][:-1].strip()
                elif dvals[0] == 'dnux/dp3':
                    modeldata['chromex2'] = dvals[1][:-1].strip()
                
                elif dvals[0] == 'dnuy/dp':
                    modeldata['chromey0'] = dvals[1][:-1].strip()
                elif dvals[0] == 'dnuy/dp2':
                    modeldata['chromey1'] = dvals[1][:-1].strip()
                elif dvals[0] == 'dnuy/dp3':
                    modeldata['chromey2'] = dvals[1][:-1].strip()
                    
                elif dvals[0] == 'alphac':
                    modeldata['alphac'] = dvals[1][:-1].strip()
                elif dvals[0] == 'pCentral':
                    modeldata['finalEnergy'] = dvals[1][:-1].strip()

    # read closed orbit data
    with file(datafile[1],'r') as f:
        coddata = f.readlines()
    if len(coddata) == 0:
        raise RuntimeError('Cannot get simulation result for closed orbit.')
    elemlen = len(coddata)
    with file(datafile[2],'r') as f:
        twissdata = f.readlines()
    if len(twissdata) != elemlen:
        raise RuntimeError('Cannot get simulation result for twiss optics.')
    with file(datafile[3],'r') as f:
        flatlatdata = f.readlines()
    if len(flatlatdata) != elemlen:
        raise RuntimeError('Cannot get simulation result for flat lattice.')
    with file(datafile[4],'r') as f:
        tmatdata = f.readlines()
    if len(tmatdata) != elemlen:
        raise RuntimeError('Cannot get simulation result for transfer matrix.')

    beamparameter={}
    flattenlatdict = OrderedDict()
    for i in range(elemlen):
        codvals=coddata[i].replace('"','').split(',')
        twissvals=twissdata[i].replace('"','').split(',')
        flatlatvals=flatlatdata[i].replace('"','').split(',')
        tmatvals=tmatdata[i].replace('"','').split(',')

        ename = codvals[0]
        etype = codvals[1]
        if ename != twissvals[0] or ename != flatlatvals[0] or ename != tmatvals[0] or \
           etype != twissvals[1] or etype != flatlatvals[1] or etype != tmatvals[1]:
            raise RuntimeError("Element does not match in simulation results")

        tm=[]
        for j in range(6):
            # transfer matrix data 6x6
            subtm=[]
            for k in range(6):
                subtm.append(float(tmatvals[3+j*6+k]))
            tm.append(subtm)

        tmpdict = {'name': ename,
                   'position':float(twissvals[2]),
                   'alphax':  float(twissvals[3]),
                   'betax':   float(twissvals[4]),
                   'phasex':  float(twissvals[5]),
                   'etax':    float(twissvals[6]),
                   'etapx':   float(twissvals[7]),
                   'alphay':  float(twissvals[8]),
                   'betay':   float(twissvals[9]),
                   'phasey':  float(twissvals[10]),
                   'etay':    float(twissvals[11]),
                   'etapy':   float(twissvals[12]),
                   'energy':   float(twissvals[13]),
                   'codx':    float(codvals[3]),
                   'cody':    float(codvals[5]),
                   'transferMatrix':tm}
        beamparameter[str(i)] = tmpdict

        flattenlatdict[str(i)] = {'name': flatlatvals[0].upper(),
                             'type': flatlatvals[1],
                             'position': float(flatlatvals[2]),
                             'length': float(flatlatvals[3])}
    modeldata['beamParameter'] = beamparameter
    
    if flattenlat:
        latfile='/'.join((runelegantdir, "%s.new"%(latname)))
        if not os.path.isfile(latfile):
            latfile='/'.join((runelegantdir, "%s.lte"%(latname)))
        if not os.path.isfile(latfile):
            latticemodel_log.debug('Cannot find lattice file.')
            raise RuntimeError('Cannot find lattice file.')
        latdict = _flattenelegantlattice(latfile)

        for k, v in flattenlatdict.iteritems():
            ename = v['name']
            etype = v['type']
            if ename.upper() != '_BEG_':
                if latdict.has_key(ename):
                    elemprops = latdict[ename]
                else:
                    raise RuntimeError("Cannot find element %s in lattice deck."%(ename))
                if elemprops['type'] != etype:
                    raise RuntimeError("Element %s type conflict."%(ename))
                elemprops.update(v)
                flattenlatdict[k] = elemprops
    
    return flattenlatdict, modeldata

elegantscript = '''
cd %s;
%s %s;
sddsprocess %s.par -pipe=out -match=col,ElementParameter=L | sddsprocess -pipe=in %s.L "-define=col,L,ParameterValue,units=m";
sddsprocess %s.par -pipe=out -match=col,ElementParameter=ANGLE | sddsprocess -pipe=in %s.th "-define=col,Angle,ParameterValue,units=rad";
sddsprocess %s.par -pipe=out -match=col,ElementParameter=K1 | sddsprocess -pipe=in %s.K1 "-define=col,K1,ParameterValue,units=1/m2";
sddsprocess %s.par -pipe=out -match=col,ElementParameter=K2 | sddsprocess -pipe=in %s.K2 "-define=col,K2,ParameterValue,units=1/m3";
sddsprocess %s.par -pipe=out -match=col,ElementParameter=VOLT | sddsprocess -pipe=in %s.VOLT "-define=col,Volt,ParameterValue,units=V";
sddsprocess %s.par -pipe=out -match=col,ElementParameter=PHASE | sddsprocess -pipe=in %s.PH "-define=col,Phase,ParameterValue,units=rad";
sddsprocess %s.par -pipe=out -match=col,ElementParameter=FREQ | sddsprocess -pipe=in %s.FR "-define=col,Freq,ParameterValue,units=rad";
sddsprocess %s.par -pipe=out -match=col,ElementParameter=INPUT_FILE | sddsprocess -pipe=in %s.km "-define=col,Kickmap,ParameterValue";

sddsxref %s.twi %s.flr %s.twf -take=X,Z;
sddsxref %s.twf %s.K1 %s.K2 %s.VOLT %s.PH %s.FR %s.km %s.L %s.th %s.flr s1 -nowarning -fillIn -reuse=row -match=ElementName -take=*;
sddsconvert s1 -pipe=out -rename=col,Z=Xcor,X=Ycor  | sddsprocess -pipe=in %s.list  -retain=col,Xcor,Ycor,ElementName,ElementType,s,L,K1,K2,Angle,Volt,Phase,Freq;

sddsprintout  %s.list %s-par.txt -noTitle -noLabel "-col=ElementName" "-col=ElementType"  "-col=s" "-col=L" "-col=K1" "-col=K2" "-col=Angle" "-col=Volt" "-col=Phase"  "-col=Freq" "-col=Kickmap" -spreadsheet=csv;
sddsprintout  %s.twi  %s-twiss.txt -noTitle -noLabel "-col=ElementName" "-col=ElementType" "-col=s" "-col=alphax" "-col=betax" "-col=psix" "-col=etax" "-col=etaxp" "-col=alphay" "-col=betay" "-col=psiy" "-col=etay" "-col=etayp" "-col=pCentral0" "-col=xAperture" "-col=yAperture" -spreadsheet=csv;
sddsprintout  %s.twi  %s-bpm.txt -noTitle -noLabel -parameters=* -spreadsheet=csv;
sddsprintout  %s.orb  %s-orb.txt -noTitle -noLabel "-col=ElementName" "-col=ElementType" "-col=s" "-col=x" "-col=xp" "-col=y" "-col=yp" -spreadsheet=csv;
sddsprintout  %s.ma1  %s-matrix.txt -noTitle -noLabel "-col=ElementName" "-col=ElementType" "-col=s" "-column=R*" -spreadsheet=csv;
cd -
'''

def runelegant(latticedata, flattenlat=False):
    '''
    Run elegant simulation
    '''
    if os.environ.has_key('ELEGANT_CMD'):
        elegant_cmd=os.environ['ELEGANT_CMD']
    else:
        elegant_cmd='elegant'

    latfile=None
    latname=None
    if os.path.isdir(runelegantdir):
        shutil.rmtree(runelegantdir)

    try:
        os.makedirs(runelegantdir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(runelegantdir):
            pass
        else: 
            raise Exception("Could not create a directory to save lattice file")
    
    if latticedata.has_key('name') and latticedata['name'] !=None:
        if latticedata['name'].strip().endswith('.lte'):
            latfile = latticedata['name'].strip()
            latname, _ = os.path.splitext(latfile)
        else:
            latname = latticedata['name'].strip()
            latfile = latname+'.lte'
    if latfile == None or latname == None or len(latname) == 0:
        raise ValueError("Cannot run elegant. Wrong lattice deck name.")
    
    if latticedata.has_key('control') and latticedata['control'] != None:
        ctrlfile = latticedata['control']['name']
        with file('/'.join((runelegantdir,ctrlfile)), 'w') as f:
            for d in latticedata['control']['data']:
                f.write(d)
            f.write('\n&save_lattice\n')
            f.write('  filename = %s.new\n')
            f.write('  output_seq = 1\n')
            f.write('&end\n')
    else:
        raise ValueError("Cannot run elegant. No run control information.")

    if latticedata.has_key('raw') and latticedata['raw']!=None:
        with file('/'.join((runelegantdir,latfile)), 'w') as f:
            for d in latticedata['raw']:
                f.write(d)

    if latticedata.has_key('map') and latticedata['map']!=None:
        for kmkey, kmdata in latticedata['map'].iteritems():
            dirname, _ = os.path.split(kmkey)
            try:
                # create a sub directory to store field map
                os.makedirs('/'.join((runelegantdir,dirname)))
            except OSError as exc:
                if exc.errno == errno.EEXIST and os.path.isdir('/'.join((runelegantdir,dirname))):
                    pass
                else: 
                    raise Exception("Can not create a sub directory to store map")
            with file('/'.join((runelegantdir, kmkey)), 'w') as f:
                f.write(base64.b64decode(kmdata))
                    
    if latticedata.has_key('alignment'):
        # ignore mis-alignment error for now
        pass

    proc = subprocess.Popen(elegantscript%(runelegantdir, elegant_cmd, ctrlfile, 
                                           latname, latname, latname, latname, latname,
                                           latname, latname, latname, latname, latname,
                                           latname, latname, latname, latname, latname,
                                           latname, latname, latname, latname, latname,
                                           latname, latname, latname, latname, latname,
                                           latname, latname, latname, latname, latname,
                                           latname, latname, latname, latname, latname,
                                           latname, latname, latname, latname, latname), 
                            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdoutdata, stderrdata = proc.communicate()
    latticemodel_log.debug(stdoutdata)
    latticemodel_log.debug('std error - ' + stderrdata)
    latticemodel_log.debug('Finish running elegant simulation')
    
    result = _readelegantresult(latname, controls=latticedata['control'], flattenlat=flattenlat)    
    # clean directory
    shutil.rmtree(runelegantdir)

    return result

