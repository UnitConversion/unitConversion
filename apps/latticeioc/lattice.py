import sys, os

from numpy import matrix

import subprocess

#from decimal import (getcontext, Decimal)
#import time
from time import strftime
from collections import OrderedDict
import copy

import cothread.catools as ca
from cothread import WaitForQuit

from _config import getpvtablefromfile

isrunning = False
iscommanded = False
runagain = False

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

lathead = """{
    This lattice is generated from live machine.
    Date: %s
    By:   Guobao Shen
          National Synchrotron Light Source II
          Brookhaven National Laboratory
          Upton, NY, 11973
}

define lattice; ringtype = 1;
Energy = %s;
dP = 1e-8; CODeps = 1e-14;  
Meth = 4; Nbend = 4; Nquad = 10;  
pi = 4.0*arctan(1.0);  
c0 = 2.99792458e8; h_rf = 1320; C = 791.958;  

"""

def latticefromtemplate(latfile):
    '''The template does not support block comment.
    For now, it handles with value for quad and sext.
    '''
    with file(latfile, 'r') as f:
        lines = f.readlines()
    
    elemdict= OrderedDict()
    designdict = {}
    for i in range (len(lines)):
        line = lines[i].strip()
        if line != '' and not line.startswith('{'):
            while not line.endswith(';'):
                i = i+1
                line = '\n'.join((line, lines [i].strip()))
            if line.find (':') != -1:
                lineprop = line.split(':')
                ename = lineprop[0].strip()
                elemdict[ename] = line
                lineprop1 = lineprop[1].replace(" ", "")
                tmp = {}
                if 'QUADRUPOLE' in lineprop1.upper() or 'SEXTUPOLE' in lineprop1.upper():
                    elemprop = lineprop1.split('L=')
                    tmp['length'] = float(elemprop[1].split(',')[0].strip())
                    elemprop = lineprop1.split('K=')
                    tmp['field'] = elemprop[1].split(',')[0].strip()
                    designdict [ename] = tmp
    
    return elemdict, designdict

def callback4sp(value, index):
    # run on command mode only
    global elems
    global monitorspvals
    
    if value != monitorspvals[elems[index]]:
        monitorspvals[elems[index]] = value 

def callback4rb(value, index):
    # run on command mode only
    global elems
    global monitorrbvals
    
    if value != monitorrbvals[elems[index]]:
        monitorrbvals[elems[index]] = value 
    
def generatelivelat(livelat, is4setpoint=True):
    global monitorspvals
    global monitorrbvals
    global lattemplate
    global designdict
    global energyforssimulation
    
    if is4setpoint:
        values = copy.deepcopy(monitorspvals)
    else:
        values = copy.deepcopy(monitorrbvals)
    #lattemp = copy.deepcopy(lattemplate)
    
    with file(livelat, 'w') as f:
        f.write(lathead%(strftime("%a, %d %b %Y, %H:%M:%S %Z"), energyforsimulation))
        for k, v in lattemplate.iteritems():
            #print k
            # hard coding naming conversion here
            if designdict.has_key(k) and not k.startswith('SQ'):
                # not include corrector, and BEND TRIM either
                # do nothing SKEW QUAD for now
                if k.startswith('SM2H'):
                    # process SM2H, which is half length of SM2
                    value = values[k.replace('SM2H', 'SM2')]/2.0/designdict[k]['length']
                else:
                    value = values[k]/designdict[k]['length']
                
                if 'SEXTUPOLE' in v.upper():
                    value=value/2.0
                
                value = abs(value)*cmp(float(designdict[k]['field']), 0)
                
                f.write(v.replace(designdict[k]['field'], str(value))+'\n')
            else:
                f.write(v+'\n')
        
        f.write('\nEND;\n')

def startmonitorsp(pvs):
    monstub = ca.camonitor(pvs, callback4sp)
    return monstub

def startmonitorrb(pvs):
    monstub = ca.camonitor(pvs, callback4rb)
    return monstub

def callback4command(value, index):
    global isrunning
    global runagain
    is4setpoint = True
    if index == 1:
        is4setpoint = False
    if isrunning:
        is4setpoint=True
    elif value == 1:
        #start = time.time()
        runlatticemodel(is4setpoint)
        #print "cost time: %s"%(time.time()-start)
        print 'triggered by command'
        while runagain:
            runagain = False
            #start = time.time()
            runlatticemodel(is4setpoint)
            #print "cost time: %s"%(time.time()-start)
            print 'run again'

        print '#####################################'
        print '#'
        print '# caused by %s'%value.name
        print '#'
        print '#####################################'
        print 'finished running model'
    else:
        assert value == 0

    isrunning = False

def startmonitorcommand():
    monstub = ca.camonitor([commandsppv, commandrbpv], callback4command)
    return monstub

def callback4energy(value):
    global energyforsimulation
    energyforsimulation = value

def startmonitorenergy():
    monstub = ca.camonitor(energysppv, callback4energy)
    return monstub

def _readresult(pmfile):
    with file(pmfile, 'r') as f:
        lines = f.readlines()
    tune = []
    chrom = []
    alphac = 0.0
    energy = 0.0
    
    idx = []
    name = []
    s = []
    alphax = []
    betax = []
    nux = []
    etax = []
    etapx = []
    alphay = []
    betay = []
    nuy = []
    etay = []
    etapy = []
    xcod = []
    ycod = []
    
    
    for line in lines:
        line = line.strip()
        if line != '' and not line.startswith('#'):
            if line.startswith('tune'):
                tune = [float(data.strip()) for data in line.split()[1:]]
            elif line.startswith('chrom'):
                chrom = [float(data.strip()) for data in line.split()[1:]]
            elif line.startswith('alphac'):
                alphac = float(line.split()[1].strip())
            elif line.startswith('energy'):
                energy = float(line.split()[1].strip())
            else:
                data = line.split()
                idx.append(int(data[0].strip()))
                name.append(data[1].strip())
                s.append(float(data[2].strip()))
                alphax.append(float(data[3].strip()))
                betax.append(float(data[4].strip()))
                nux.append(float(data[5].strip()))
                etax.append(float(data[6].strip()))
                etapx.append(float(data[7].strip()))
                alphay.append(float(data[8].strip()))
                betay.append(float(data[9].strip()))
                nuy.append(float(data[10].strip()))
                etay.append(float(data[11].strip()))
                etapy.append(float(data[12].strip()))
                xcod.append(float(data[13].strip()))
                ycod.append(float(data[14].strip()))
    elemno = int(data[0].strip())+1
                
    return {'tune': tune,
            'chrom': chrom,
            'alphac': alphac,
            'energy': energy,
            'idx': idx,
            'name': name,
            's': s,
            'alphax': alphax,
            'betax': betax,
            'nux': nux,
            'etax': etax ,
            'etapx': etapx,
            'alphay': alphay,
            'betay': betay,
            'nuy': nuy,
            'etay': etay,
            'etapy': etapy,
            'xcod': xcod,
            'ycod':ycod}, elemno
            

def runtracy(latfile, runit=True):
    latname, _ = os.path.splitext(latfile)

    msg = ''
    if runit:
        if os.environ.has_key('TRACY3_CMD'):
            tracy_cmd=os.environ['TRACY3_CMD']
        else:
            tracy_cmd='tracy3'
        if not os.path.isfile(tracy_cmd):
            raise RuntimeError("Cannot find TRACY3 simulation code.")

        try:
            # remove existing parameter file
            os.remove('%s.pm'%latname)
        except OSError:
            pass
    
        proc = subprocess.Popen('%s %s %s.pm'
                                %(tracy_cmd, latname, latname),
                                shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
        stdoutdata, _ = proc.communicate()
        
        for tmp in stdoutdata.split('\n'):
            if 'unstable' in tmp:
                #msg = '|'.join((msg, tmp))
                msg = tmp
        if msg == '':
            msg = 'Tracy3 runs successfully.'
        
        sys.stdout.write(stdoutdata)
        #print 'length: ', len(stderrdata)
        #sys.stdout.write(stderrdata)
    
    designresult, elemno = _readresult('%s.pm'%latname)
    
    return designresult, elemno, msg

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
    global livelat
    global lattemplate
    global designdict
    global betaxdesignval
    global betaydesignval
    
    generatelivelat(livelat, is4setpoint=is4setpoint)
    #testtmp = 'Running...'
    if is4setpoint:
        ca.caput(statussppv, 'Running...', wait=True)
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
    else:
        ca.caput(statusrbpv, 'Running...', wait=True)
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
    #assert testtmp == ca.caget(statuspv)
    
    liveresult, _, msg = runtracy(livelat, runit=True)

    #assert liveelemno == elemno
    

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
            ((matrix(liveresult['betax'])-betaxdesignval)/betaxdesignval).tolist()[0], 
            ((matrix(liveresult['betay'])-betaydesignval)/betaydesignval).tolist()[0],
            ]
    ca.caput(pvs, vals, wait=True)
    ca.caput("%s.PROC"%counterpv, 1, wait=True)

def main(designlat, init=True):
    global energyforsimulation
    if init:
        designresult, elemno, _ = runtracy(designlat, runit=True)
    
        _createdb('design.db', designpvlist, elemno) 
        _createdb('livesp.db', splivepvlist, elemno, withenergy=True)
        _createdb('liverb.db', rblivepvlist, elemno, issetpoint=True)
        
    else:
        designresult, elemno, _ = runtracy(designlat, runit=False)

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
        betaxdesignval = matrix(designresult['betax'])
        betaydesignval = matrix(designresult['betay'])
        
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
        ca.caput(pvs, vals, wait=True)
        
        global elems
        global monitorspvals
        global monitorrbvals

        pvspsdict, pvrbsdict = getpvtablefromfile('pvtable.txt')
        
        elems = []
        sppvs = []
        rbpvs = []
        
        global lattemplate
        global designdict
        
        lattemplate, designdict = latticefromtemplate(designlat)
        
        for k, v in pvspsdict.iteritems():
            elems.append(k)
            sppvs.append(v['K'])

        for k, v in pvrbsdict.iteritems():
            rbpvs.append(v['K'])
        
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

    livelat = 'nsls2srlive.lat'
    main('comm-ring-Mar13-tracy.lat', init = dbonly)
    if not dbonly:
        WaitForQuit()

