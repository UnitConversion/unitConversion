import sys, os
import traceback
import time

import shutil
import errno

import numpy as np
import math

import subprocess

#from decimal import (getcontext, Decimal)
#import time
from time import strftime
from collections import OrderedDict
import copy

import cothread.catools as ca
from cothread import WaitForQuit

from _config import getpvtablefromfile

from savelattice import (savelatticemodel)
from latticepy.LatticeModelClient import LatticeModelClient

#isrunning = False
#iscommanded = False
#runagain = False

#normalizedvalue={}

monitorspvals = {}
monitorrbvals = {}

energyforsimulation = 3.000
energysppv = 'SR-BI{RUNMODEL}ENERGY-SP'

#beamcurrentpv = 'SR:C03-BI{DCCT:1}I:Total-I'

wfrectemplate = '''record(waveform, "%s") {
    field(DTYP, "Soft Channel")
    field(SCAN, "Passive")
    field(NELM, "%s")
    field(FTVL, "%s")
}
'''

scalarrectemplate = '''record(ai, "%s") {
    field(DTYP, "Soft Channel")
    field(SCAN, "Passive")
    field(PREC, "5")
}
'''

commandsppv = 'SR-BI{RUNMODEL}SP-CMD'
commandsppvdb = '''
record(bo, "%s") {
    field(DTYP, "Soft Channel")
    field(SCAN, "Passive")
    field(HIGH, "2.0")
}
'''%(commandsppv)

commandrbpv = 'SR-BI{RUNMODEL}RB-CMD'
commandrbpvdb = '''
record(bo, "%s") {
    field(DTYP, "Soft Channel")
    field(SCAN, "Passive")
    field(HIGH, "2.0")
}
'''%(commandrbpv)

statustemp='''
record(stringin, "%s") {
    field(DTYP, "Soft Channel")
    field(DESC, "Simulation running status")
    field(SCAN, "Passive")
}
record(calc, "%s")
{
        field(DESC, "Counter")
        field(CALC, "A+1")
        field(INPA, "%s  NPP NMS")
        field(FLNK, "%s")
}
record(longin, "%s") {
    field(DESC, "Simulation counter")
    field(DTYP, "Soft Channel")
    field(SCAN, "Passive")
    field(INP, "%s.VAL  NPP NMS")
    field(EGU, "Counts")
}
'''

statussppv = 'SR-BI{RUNMODEL}SP-STATUS'
_runcountsppv = 'SR-BI{RUNMODEL}SP-COUNT_'
runcountsppv = 'SR-BI{RUNMODEL}SP-COUNT'
statussppvdb = statustemp%(statussppv, _runcountsppv, runcountsppv, runcountsppv, runcountsppv, _runcountsppv)

statusrbpv = 'SR-BI{RUNMODEL}RB-STATUS'
_runcountrbpv = 'SR-BI{RUNMODEL}RB-COUNT_'
runcountrbpv = 'SR-BI{RUNMODEL}RB-COUNT'
statusrbpvdb = statustemp%(statusrbpv, _runcountrbpv, runcountrbpv, runcountrbpv, runcountrbpv, _runcountrbpv)

betaxdesignval = None
betaydesignval = None
# design value from official lattice
alphaxdesign = "SR-BI{ALPHA:DESIGN}X-I"
alphaydesign = "SR-BI{ALPHA:DESIGN}Y-I"
betaxdesign = "SR-BI{BETA:DESIGN}X-I"
betaydesign = "SR-BI{BETA:DESIGN}Y-I"
etaxdesign = "SR-BI{ETA:DESIGN}X-I"
etaydesign = "SR-BI{ETA:DESIGN}Y-I"
namedesign = "SR-BI{NAME:DESIGN}I"
orbitxdesign = "SR-BI{ORBIT:DESIGN}X-I"
orbitydesign = "SR-BI{ORBIT:DESIGN}Y-I"
phixdesign = "SR-BI{PHI:DESIGN}X-I"
phiydesign = "SR-BI{PHI:DESIGN}Y-I"
posdesign = "SR-BI{POS:DESIGN}I"

tunexdesign = "SR-BI{TUNE:DESIGN}X-I"
tuneydesign = "SR-BI{TUNE:DESIGN}Y-I"
chromxdesign = "SR-BI{CHROM:DESIGN}X-I"
chromydesign = "SR-BI{CHROM:DESIGN}Y-I"
alphacdesign = "SR-BI{ALPHAC:DESIGN}I"
energydesign = "SR-BI{ENERGY:DESIGN}I"

designpvlist = {'wf':[alphaxdesign, alphaydesign, betaxdesign, betaydesign, 
                      etaxdesign, etaydesign, namedesign, orbitxdesign, orbitydesign,
                      phixdesign, phiydesign, posdesign],
                'scalar': [tunexdesign, tuneydesign, chromxdesign, chromydesign, alphacdesign, energydesign]
                }    

# live value from set points
alphaxsplive = "SR-BI{ALPHA:LIVE4SP}X-I"
alphaysplive = "SR-BI{ALPHA:LIVE4SP}Y-I"
betaxsplive = "SR-BI{BETA:LIVE4SP}X-I"
betaysplive = "SR-BI{BETA:LIVE4SP}Y-I"
etaxsplive = "SR-BI{ETA:LIVE4SP}X-I"
etaysplive = "SR-BI{ETA:LIVE4SP}Y-I"
namesplive = "SR-BI{NAME:LIVE4SP}I"
orbitxsplive = "SR-BI{ORBIT:LIVE4SP}X-I"
orbitysplive = "SR-BI{ORBIT:LIVE4SP}Y-I"
phixsplive = "SR-BI{PHI:LIVE4SP}X-I"
phiysplive = "SR-BI{PHI:LIVE4SP}Y-I"
possplive = "SR-BI{POS:LIVE4SP}I"

tunexsplive = "SR-BI{TUNE:LIVE4SP}X-I"
tuneysplive = "SR-BI{TUNE:LIVE4SP}Y-I"
chromxsplive = "SR-BI{CHROM:LIVE4SP}X-I"
chromysplive = "SR-BI{CHROM:LIVE4SP}Y-I"
alphacsplive = "SR-BI{ALPHAC:LIVE4SP}I"
energysplive = "SR-BI{ENERGY:LIVE4SP}I"

deltabetaxsplive = "SR-BI{BETA:LIVE4SP}DELTAx-I"
deltabetaysplive = "SR-BI{BETA:LIVE4SP}DELTAy-I"

splivepvlist = {'wf':[alphaxsplive, alphaysplive, betaxsplive, betaysplive, 
                      etaxsplive, etaysplive, namesplive, orbitxsplive, orbitysplive,
                      phixsplive, phiysplive, possplive,
                      deltabetaxsplive, deltabetaysplive],
              'scalar': [tunexsplive, tuneysplive, chromxsplive, chromysplive, alphacsplive, energysplive]
              }

# live value from read back
alphaxrblive = "SR-BI{ALPHA:LIVE4RB}X-I"
alphayrblive = "SR-BI{ALPHA:LIVE4RB}Y-I"
betaxrblive = "SR-BI{BETA:LIVE4RB}X-I"
betayrblive = "SR-BI{BETA:LIVE4RB}Y-I"
etaxrblive = "SR-BI{ETA:LIVE4RB}X-I"
etayrblive = "SR-BI{ETA:LIVE4RB}Y-I"
namerblive = "SR-BI{NAME:LIVE4RB}I"
orbitxrblive = "SR-BI{ORBIT:LIVE4RB}X-I"
orbityrblive = "SR-BI{ORBIT:LIVE4RB}Y-I"
phixrblive = "SR-BI{PHI:LIVE4RB}X-I"
phiyrblive = "SR-BI{PHI:LIVE4RB}Y-I"
posrblive = "SR-BI{POS:LIVE4RB}I"

tunexrblive = "SR-BI{TUNE:LIVE4RB}X-I"
tuneyrblive = "SR-BI{TUNE:LIVE4RB}Y-I"
chromxrblive = "SR-BI{CHROM:LIVE4RB}X-I"
chromyrblive = "SR-BI{CHROM:LIVE4RB}Y-I"
alphacrblive = "SR-BI{ALPHAC:LIVE4RB}I"
energyrblive = "SR-BI{ENERGY:LIVE4RB}I"

deltabetaxrblive = "SR-BI{BETA:LIVE4RB}DELTAx-I"
deltabetayrblive = "SR-BI{BETA:LIVE4RB}DELTAy-I"

rblivepvlist = {'wf':[alphaxrblive, alphayrblive, betaxrblive, betayrblive, 
                      etaxrblive, etayrblive, namerblive, orbitxrblive, orbityrblive,
                      phixrblive, phiyrblive, posrblive, 
                      deltabetaxrblive, deltabetayrblive],
              'scalar': [tunexrblive, tuneyrblive, chromxrblive, chromyrblive, alphacrblive, energyrblive]
              }


elefile_template = '''! This is a for %s running on %s
&run_setup
    lattice =%s.lte,
    use_beamline = "RING",
    p_central=5870.841,
    magnets = %s.mag,
    final = %s.fin
    centroid=%s.cen
    sigma=%s.sig
    parameters = %s.par
    print_statistics = 0
    tracking_updates = 0
&end

&alter_elements name=*, type=CSBEND,item=N_KICKS, value=25, allow_missing_elements=1 &end
&alter_elements name=*, type=KSEXT, item=N_KICKS, value=4,  allow_missing_elements=1 &end
&alter_elements name=*, type=KQUAD, item=N_KICKS, value=25, allow_missing_elements=1 &end

%s

&run_control
    n_steps = 1,
&end

&floor_coordinates
    filename= "%s.flr",
&end

&twiss_output
    filename = "%s.twi",
    matched =1,
    radiation_integrals=1
&end

&closed_orbit
    output = %s.orb,
    output_monitors_only=0,
    closed_orbit_accuracy = 1e-10,
    closed_orbit_iterations = 500,
    iteration_fraction = 0.1,
    verbosity = 1,
&end

&matrix_output
    SDDS_output="%s.ma1"
    output_at_each_step=1
&end

&bunched_beam
    bunch="%s.bun"
&end

&track &end
%s

&stop  &end
'''

elefile_alter_template = '''&alter_elements name=%s, item=%s, value=%s &end
'''

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

sddsprintout  %s.list %s-par.txt -noTitle -noLabel "-col=ElementName" "-col=ElementType"  "-col=s" "-col=L" "-col=K1" "-col=K2" "-col=Angle" "-col=Volt" "-col=Phase"  "-col=Freq" "-col=Kickmap";
sddsprintout  %s.twi  %s-twiss.txt -noTitle -noLabel "-col=ElementName" "-col=ElementType" "-col=s" "-col=alphax" "-col=betax" "-col=psix" "-col=etax" "-col=etaxp" "-col=alphay" "-col=betay" "-col=psiy" "-col=etay" "-col=etayp" "-col=pCentral0" "-col=xAperture" "-col=yAperture";
sddsprintout  %s.twi  %s-bpm.txt -noTitle -noLabel -parameters=*  -spreadsheet=csv;
sddsprintout  %s.orb  %s-orb.txt -noTitle -noLabel "-col=ElementName" "-col=ElementType" "-col=s" "-col=x" "-col=xp" "-col=y" "-col=yp";
sddsprintout  %s.ma1  %s-matrix.txt -noTitle -noLabel "-col=ElementName" "-col=ElementType" "-col=s" "-column=R*";
cd -
'''

runelegantdir = 'runelegant'


def callback4sp(value, index):
    # run on command mode only
    global elems
    global monitorspvals
    
    if value.ok:
        if value != monitorspvals[elems[index]]:
            monitorspvals[elems[index]] = value
    else:
        monitorspvals[elems[index]] = 0.0

def callback4rb(value, index):
    # run on command mode only
    global elems
    global monitorrbvals
    
    if value.ok:
        if value != monitorrbvals[elems[index]]:
            monitorrbvals[elems[index]] = value 
    else:
        monitorrbvals[elems[index]] = 0.0 
    
def startmonitorsp(pvs):
    monstub = ca.camonitor(pvs, callback4sp, notify_disconnect = True)
    return monstub

def startmonitorrb(pvs):
    monstub = ca.camonitor(pvs, callback4rb, notify_disconnect = True)
    return monstub

def callback4command(value, index):
    is4setpoint = True
    if index == 1:
        is4setpoint = False

    if value == 1:
        #start = time.time()
        runlatticemodel(is4setpoint)
        #print "cost time: %s"%(time.time()-start)

        print '#####################################'
        print '#'
        print '# caused by %s on %s'%(value.name, strftime("%a, %d %b %Y, %H:%M:%S %Z"))
        print '#'
        print '#####################################'
        print 'finished running model'

def startmonitorcommand():
    monstub = ca.camonitor([commandsppv, commandrbpv], callback4command, notify_disconnect = True)
    return monstub

def callback4energy(value):
    global energyforsimulation
    if value.ok:
        energyforsimulation = value
    else:
        energyforsimulation = 0.0

def startmonitorenergy():
    monstub = ca.camonitor(energysppv, callback4energy, notify_disconnect = True)
    return monstub


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

def _readelegantresult(elename, ltename):
    '''
    Read simulation result from a text output file
    
    return a structure as below:
        { 
            'tune': ,      [x, y]             # horizontal tune
            'chrom': ,     [x0, y0]           # linear horizontal chromaticity
            'energy':      pCentral/0.511/1.0e3,    # the final beam energy in GeV
            'idx':         element_order:     #element_order starts with 0, which is the begin of simulation with s=0.
            'alphac':      alphac,
            'name': ,
            's': ,
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
         }, elemcount
    '''
    datafile=[]
    # global beam parameter
    datafile.append('/'.join((runelegantdir, "%s-bpm.txt"%(elename))))
    # closed orbit
    datafile.append('/'.join((runelegantdir, "%s-orb.txt"%(elename))))
    # twiss parameter
    datafile.append('/'.join((runelegantdir, "%s-twiss.txt"%(elename))))
    # flat lattice
    datafile.append('/'.join((runelegantdir, "%s-par.txt"%(elename))))
    # transfer matrix
    datafile.append('/'.join((runelegantdir, "%s-matrix.txt"%(elename))))
    
    for f in datafile:
        if not os.path.isfile(f):
            raise RuntimeError('Fail to run elegant simulation. Could not find data file: %s'%f)

    modeldata={'tune': [0.0, 0.0],
               'chrom': [0.0, 0.0],
               'alphac': 0.0,
               'energy': 0.0}

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
                    modeldata['tune'][0] = float(dvals[1].strip())
                elif dvals[0] == 'nuy':
                    modeldata['tune'][1] = float(dvals[1].strip())
                elif dvals[0] == 'dnux/dp':
                    modeldata['chrom'][0] = float(dvals[1].strip())
                elif dvals[0] == 'dnuy/dp':
                    modeldata['chrom'][1] = float(dvals[1].strip())
                elif dvals[0] == 'alphac':
                    modeldata['alphac'] = float(dvals[1].strip())
                elif dvals[0] == 'pCentral':
                    modeldata['energy'] = float(dvals[1].strip())*0.511e-3 # convert to GeV

    # read closed orbit data
    cod = np.loadtxt(datafile[1], dtype=str)
    modeldata['name'] = cod[:, 0]
    modeldata['s'] = [float(x) for x in cod[:,2]]
    modeldata['xcod'] = [float(x) for x in cod[:,3]]
    modeldata['ycod'] = [float(x) for x in cod[:,5]]

    twiss = np.loadtxt(datafile[2], dtype=str)
    modeldata['alphax'] = [float(x) for x in twiss[:,3]]
    modeldata['betax']  = [float(x) for x in twiss[:,4]]
    modeldata['nux']    = [float(x) for x in twiss[:,5]]
    modeldata['etax']   = [float(x) for x in twiss[:,6]]
    modeldata['etapx']  = [float(x) for x in twiss[:,7]]
    modeldata['alphay'] = [float(x) for x in twiss[:,8]]
    modeldata['betay']  = [float(x) for x in twiss[:,9]]
    modeldata['nuy']    = [float(x) for x in twiss[:,10]]
    modeldata['etay']   = [float(x) for x in twiss[:,11]]
    modeldata['etapy']  = [float(x) for x in twiss[:,12]]

    return modeldata, len(cod)

def runelegant(elefile, ltefile, runit=True):
    '''elefile {'name': , 'content': }
    ltefile {'name': , 'content': }
    '''

    global elegant_cmd
    msg = ''

    ltename, _ = os.path.splitext(ltefile['name'])
    elename, _ = os.path.splitext(elefile['name'])
    if runit:
        try:
            os.makedirs(runelegantdir)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(runelegantdir):
                pass
            else: 
                raise Exception("Could not create a directory to save lattice file")
        
        with file('/'.join((runelegantdir, elefile['name'])), 'w') as f:
            f.write(elefile['content'])
        with file('/'.join((runelegantdir, ltefile['name'])), 'w') as f:
            f.write(ltefile['content'])
        
        proc = subprocess.Popen(elegantscript%(runelegantdir, elegant_cmd, elefile['name'], 
                                               elename, elename, elename, elename, elename,
                                               elename, elename, elename, elename, elename,
                                               elename, elename, elename, elename, elename,
                                               elename, elename, elename, elename, elename,
                                               elename, elename, elename, elename, elename,
                                               elename, elename, elename, elename, elename,
                                               elename, elename, elename, elename, elename,
                                               elename, elename, elename, elename, elename), 
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdoutdata, _ = proc.communicate()
        
        #for line in stdoutdata:
        if 'beamline unstable' in stdoutdata:
            msg = "beamline unstable"
        elif 'closed orbit did not converge' in stdoutdata:
            msg = 'closed orbit did not converge'
        else:
            msg = 'elegant runs successfully'
    else:
        global elemtypes
        tmp = np.loadtxt('/'.join((runelegantdir, "%s-par.txt"%(elename))), dtype=str)
        ename = tmp[:, 0]
        length = [float(x) for x in tmp[:,3]]
        k1 = tmp[:,4]
        k2 = tmp[:,5]
        for i in range(len(ename)):
            # handle quadropule only
            if elemtypes.has_key(ename[i]):
                if elemtypes[ename[i]].has_key('length'):
                    raise ValueError("duplicated entry for element %s"%(ename[i]))
                elemtypes[ename[i]]['length'] = length[i]
                if elemtypes[ename[i]]['etype'] == 'QUAD':
                    elemtypes[ename[i]]['strength'] = float(k1[i])
                elif elemtypes[ename[i]]['etype'] == 'SEXT':
                    elemtypes[ename[i]]['strength'] = float(k2[i])
            elif ename[i].startswith('SM2'):
                tmpname = ename[i].replace('SM2H', 'SM2')
                elemtypes[tmpname]['length'] = length[i]*2
                elemtypes[tmpname]['strength'] = float(k2[i])

    modeldata, elemcount = _readelegantresult(elename, ltename)
    return modeldata, elemcount, msg

def _createdb(dbname, pvlist, elemno, withenergy=False, issetpoint=False):
    pvbuffer = ""
    
    for pv in pvlist['wf']:
        if 'NAME' in pv:
            pvbuffer = "".join((pvbuffer, wfrectemplate%(pv, elemno, 'STRING')))
        else:
            pvbuffer = "".join((pvbuffer, wfrectemplate%(pv, elemno, 'DOUBLE')))

    for pv in pvlist['scalar']:
        pvbuffer = "".join((pvbuffer, scalarrectemplate%(pv)))

    if withenergy:
        pvbuffer = "".join((pvbuffer, scalarrectemplate%(energysppv)))

    try:
        os.remove(dbname)
    except OSError:
        pass
    
    with file(dbname, 'w') as f:
        f.write(pvbuffer)
        if issetpoint:
            f.write(commandsppvdb)
            f.write(statussppvdb)
        else:
            f.write(commandrbpvdb)
            f.write(statusrbpvdb)


def runlatticemodel(is4setpoint):
    global elemtypes
    global ltecontent
    global lattemplate
    global designdict
    global betaxdesignval
    global betaydesignval
    
    if is4setpoint:
        try:
            #consume status output error
            ca.caput(statussppv, 'Running...', wait=True)
        except ca.ca_nothing:
            print traceback.format_exc()
        pvs = [alphaxsplive, alphaysplive, 
               betaxsplive, betaysplive, 
               etaxsplive, etaysplive, 
               namesplive, 
               orbitxsplive, orbitysplive,
               phixsplive, phiysplive, 
               possplive, 
               tunexsplive, tuneysplive, 
               chromxsplive, chromysplive, 
               alphacsplive, 
               energysplive,
               statussppv,
               deltabetaxsplive, deltabetaysplive]
        counterpv = _runcountsppv
        locstatuspv = statussppv
        source = 'set point'
    else:
        try:
            #consume status output error
            ca.caput(statusrbpv, 'Running...', wait=True)
        except ca.ca_nothing:
            print traceback.format_exc()
        pvs = [alphaxrblive, alphayrblive, 
               betaxrblive, betayrblive, 
               etaxrblive, etayrblive, 
               namerblive, 
               orbitxrblive, orbityrblive,
               phixrblive, phiyrblive, 
               posrblive, 
               tunexrblive, tuneyrblive, 
               chromxrblive, chromyrblive, 
               alphacrblive, 
               energyrblive,
               statusrbpv,
               deltabetaxrblive, deltabetayrblive]
        counterpv = _runcountrbpv
        locstatuspv = statusrbpv
        source = 'read back'
    
    ele_pre, _ = os.path.splitext(ele_name)
    alter_elem = ""

    global monitorspvals
    global monitorrbvals
    
    if is4setpoint:
        values = copy.deepcopy(monitorspvals)
    else:
        values = copy.deepcopy(monitorrbvals)


    for ename, value in values.iteritems():
        if ename.startswith('SQ'):
            # not going to do anything with Skew Quadrupole for now
            print "SKEW Quad (element: %s) is not supported yet."%(ename, elemtypes[ename]['etype'])
        else:
            if ename.startswith('SM2'):
                lename = ename.replace('SM2', 'SM2H')
                valtmp = value/elemtypes[ename]['length']
                valdesign = value/elemtypes[ename]['strength']
#                if abs(abs(valdesign) - valtmp) >= 1.0e-4:
                alter_elem += elefile_alter_template%(lename, 'K2', math.copysign(valtmp, valdesign))
            else:
                if elemtypes[ename]['etype'] == 'QUAD':
                    valtmp = value/elemtypes[ename]['length']
                    valdesign = value/elemtypes[ename]['strength']
#                    if abs(abs(valdesign) - valtmp) >= 1.0e-4:
                    alter_elem += elefile_alter_template%(ename, 'K1', math.copysign(valtmp, valdesign))
                elif elemtypes[ename]['etype'] == 'SEXT':
                    valtmp = value/elemtypes[ename]['length']
                    valdesign = value/elemtypes[ename]['strength']
#                    if abs(abs(valdesign) - valtmp) >= 1.0e-4:
                    alter_elem += elefile_alter_template%(ename, 'K2', math.copysign(valtmp, valdesign))
                elif elemtypes[ename]['etype'] in ['HCOR', 'VCOR']:
#                    if abs(value) >= 1.0e-8:
                    alter_elem += elefile_alter_template%(ename, 'KICK', value)
                else:
                    print "%s (type: %s) is not supported yet"%(ename, elemtypes[ename]['etype'])

    curtime = time.time()
    version = int(curtime)
    
    ele_new = "_".join((ele_pre,  time.strftime("%Y%m%d_%H%M%S", time.localtime(curtime))))
    save_lattice = savelattice_template%(ele_new)
    elecontent = elefile_template%(source, time.strftime("%a, %d %b %Y, %H:%M:%S %Z", time.localtime(curtime)), 
                                   ele_pre, 
                                   ele_new, ele_new, ele_new, ele_new, ele_new,
                                   alter_elem, ele_new, ele_new, ele_new, ele_new, ele_new, 
                                   save_lattice)

    liveresult, _, msg = runelegant({'name': ele_new+'.ele', 'content': elecontent}, 
                                    {'name': ele_pre+".lte", 'content': ltecontent},
                                    runit=True)
    
    vals = [liveresult['alphax'], liveresult['alphay'],
            liveresult['betax'], liveresult['betay'],
            liveresult['etax'], liveresult['etay'],
            liveresult['name'],
            liveresult['xcod'], liveresult['ycod'],
            liveresult['nux'], liveresult['nuy'],
            liveresult['s'],
            liveresult['tune'][0], liveresult['tune'][1],
            liveresult['chrom'][0], liveresult['chrom'][1],
            liveresult['alphac'],
            liveresult['energy'],
            msg,
            ((np.matrix(liveresult['betax'])-betaxdesignval)/betaxdesignval).tolist()[0], 
            ((np.matrix(liveresult['betay'])-betaydesignval)/betaydesignval).tolist()[0],
            ]
    try:
        ca.caput(pvs, vals, wait=True)
        try:
            ca.caput("%s.PROC"%counterpv, 1, wait=True)
        except ca.ca_nothing as e:
            print "Error when counting up", e
            #msg = "Exception when setting value to %s"%counterpv
    except ca.ca_nothing as e:
        print "Error to set optics", e
        if e.name != locstatuspv:
            # last try to report an error message
            try:
                msg = "Exception when setting value to %s"%e.name
                ca.caput(locstatuspv, msg)
            except ca.ca_nothing as e:
                pass

#    global lmc
#    if msg != 'error: lattice unstable. ' and lmc != None:
#        latname, _ = os.path.splitext(livelat)
#        savelatticemodel(livelat, '%s.pm'%latname, lmc, source=source, name=latname, version=version, branch='live')

savelattice_template = '''&save_lattice
   filename = %s.lte
   output_seq = 0
&end
'''

def main(designlat, designversion, init=True):
    global energyforsimulation
    ele_pre, _ = os.path.splitext(ele_name)
    if init:
        # clean directory
        if os.path.isdir(runelegantdir):
            shutil.rmtree(runelegantdir)
        
        save_lattice= ""
        alter_elem = ""
        elecontent = elefile_template%('design', time.strftime("%a, %d %b %Y, %H:%M:%S %Z"),
                                       ele_pre, ele_pre, ele_pre, ele_pre, ele_pre, ele_pre,
                                       alter_elem, ele_pre, ele_pre, ele_pre, ele_pre, ele_pre, 
                                       save_lattice)
        designresult, elemcount, _ = runelegant({'name': ele_name, 'content': elecontent}, designlat, runit=True)
        
        _createdb('design.db', designpvlist, elemcount) 
        _createdb('livesp.db', splivepvlist, elemcount, withenergy=True)
        _createdb('liverb.db', rblivepvlist, elemcount, issetpoint=True)
        
    else:
        global elems
        global monitorspvals
        global monitorrbvals
        global elemtypes

        pvspsdict, pvrbsdict, elemtypes = getpvtablefromfile('pvtable.txt')

        save_lattice= ""
        alter_elem = ""
        elecontent = elefile_template%('design', time.strftime("%a, %d %b %Y, %H:%M:%S %Z"),
                                       ele_pre, ele_pre, ele_pre, ele_pre, ele_pre, ele_pre,
                                       alter_elem, ele_pre, ele_pre, ele_pre, ele_pre, ele_pre, 
                                       save_lattice)
        designresult, elemcount, _ = runelegant({'name': ele_name, 'content': elecontent}, designlat, runit=False)

#        global lmc
#        if lmc != None:
#            latname, _ = os.path.splitext(designlat)
#            savelatticemodel(designlat, '%s.pm'%latname, lmc, source='design', name=latname, version=designversion, branch='design')
#
        pvs = [alphaxdesign, alphaydesign, 
               betaxdesign, betaydesign, 
               etaxdesign, etaydesign, 
               namedesign, 
               orbitxdesign, orbitydesign,
               phixdesign, phiydesign, 
               posdesign, 
               tunexdesign, tuneydesign, 
               chromxdesign, chromydesign, 
               alphacdesign, 
               energydesign,
               energysppv,
               ]

        global betaxdesignval
        global betaydesignval
        betaxdesignval = np.matrix(designresult['betax'])
        betaydesignval = np.matrix(designresult['betay'])
        
        vals = [designresult['alphax'], designresult['alphay'],
                designresult['betax'], designresult['betay'],
                designresult['etax'], designresult['etay'],
                designresult['name'],
                designresult['xcod'], designresult['ycod'],
                designresult['nux'], designresult['nuy'],
                designresult['s'],
                designresult['tune'][0], designresult['tune'][1],
                designresult['chrom'][0], designresult['chrom'][1],
                designresult['alphac'],
                designresult['energy'],
                energyforsimulation,
               ]
        
        # do not need to capture the error.
        ca.caput(pvs, vals, wait=True)
        
        elems = []
        sppvs = []
        rbpvs = []
        
        global lattemplate
        global designdict
        
        for k, v in pvspsdict.iteritems():
            elems.append(k)
            sppvs.append(v['K'])

        for k, v in pvrbsdict.iteritems():
            rbpvs.append(v['K'])
        
        # do not need to capture the error.
        vals = ca.caget(sppvs)
        for i in range(len(elems)):
            assert sppvs[i] == vals[i].name
            monitorspvals [elems[i]] = vals[i]

        vals = ca.caget(rbpvs)
        for i in range(len(elems)):
            assert rbpvs[i] == vals[i].name
            monitorrbvals [elems[i]] = vals[i]

        startmonitorsp(sppvs)
        startmonitorrb(rbpvs)
        startmonitorenergy()
        startmonitorcommand()
        
        print 'starting to monitor'
        
        # run for set points
        runlatticemodel(True)
        
        # run for read back
        runlatticemodel(False)
        
        print 'finish initialization'
        
if __name__ == '__main__':
    
    dbonly = True
    if len(sys.argv) > 1:
        dbonly = sys.argv[1]
    if dbonly in ['false', 'False', 'FALSE', 'F', 'f']:
        dbonly = False

    global elegant_cmd
    elegant_cmd='elegant'
    if os.environ.has_key('ELEGANT_CMD'):
        elegant_cmd=os.environ['ELEGANT_CMD']
    if not os.path.isfile(elegant_cmd):
        raise RuntimeError("Cannot locate ELEGANT simulation engine.")

#    # need to update to production server url
#    latticeurl = 'http://localhost:8000/lattice'
#    user =''
#    pw = ''
#    
#    global lmc 
#    lmc = None
#    try:
#        lmc = LatticeModelClient(BaseURL=latticeurl, username=user, password=pw)
#    except:
#        pass

    degign_lattice = 'comm-ring.lte'
    livelat = 'comm-ring.lte'
    ele_name = 'comm-ring.ele'
    # need to change the version every time there is a new design lattice released
    design_lattice_version = '20140313'
    with file(degign_lattice, 'r') as f:
        ltecontent = f.read()
    main({'name': degign_lattice, 'content': ltecontent}, design_lattice_version, init = dbonly)
    if not dbonly:
        WaitForQuit()

