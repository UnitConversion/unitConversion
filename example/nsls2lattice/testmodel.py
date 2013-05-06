'''
Created on Apr 16, 2013

@author: shengb
'''
from collections import OrderedDict
import MySQLdb

from pylattice import model

from .rdbinbfo import host, user, pw, db, port

tracyhead = '''
define lattice; ringtype = 0;
energy=0.200;
dP = 1e-8; CODeps = 1e-6;
Meth = 4; Nbend = 4; Nquad = 4;    
pi = 4.0*arctan(1.0);
'''

def cleanmodeldb(conn):
    sql = '''
    delete from beam_parameter;
    delete from model;
    '''
    conn.cursor().execute(sql)
    conn.commit()

def preparetracytwiss(twissfile):
    '''
    '''
    # tracy twiss output
#    twisscols = ['order', 
#                 'name', 
#                 's', 
#                 'code', 
#                 'alphax', 
#                 'betax', 
#                 'nux', 
#                 'etax', 
#                 'etapx', 
#                 'alphay', 
#                 'betay', 
#                 'nuy', 
#                 'etay', 
#                 'etapy', 
#                 'I5']

    # expected key words
    twisscols = ['order', 
                 'name', 
                 'position', 
                 'code', 
                 'alphax', 
                 'betax', 
                 'phasex', 
                 'etax', 
                 'etapx', 
                 'alphay', 
                 'betay', 
                 'phasey', 
                 'etay', 
                 'etapy', 
                 'I5']
    skipcols = [False, 
                False, 
                False, 
                True,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                False,
                True
                ]
    assert len(twisscols) == len(skipcols), 'Tracy TWISS out put headers does not match'
    
    twissdict = OrderedDict()
    with file(twissfile, 'r') as f:
        for line in f.readlines():
            if not line.strip().startswith('#'):
                lineparts = line.split()
                assert len(lineparts) == len(twisscols), 'Twiss header does not match data instance in the body'
                tmpdict = {}
                for i in range(1, len(lineparts)):
                    if skipcols[i]:
                        pass
                    else:
                        tmpdict[twisscols[i]] = lineparts[i]
                twissdict[lineparts[0]] = tmpdict
    return twissdict

if __name__ == '__main__':
    if host.startswith("/"):
        conn = MySQLdb.connect(unix_socket=host, user=user, passwd=pw, db=db)
    else:
        conn = MySQLdb.connect(host=host, user=user, passwd=pw, db=db, port=port)

#    cleanmodeldb(conn)
    modelinst = model(conn)
    
    latticename = 'CD3-Oct3-12-30Cell-addID-par' 
    latticeversion = 20121003 
    latticebranch = 'test'

    modelhead1 = {'CD3-Oct3-12-30Cell-addID-par bare':
                               {  # header information
                                'description': 'an instance for lattice CD3-Oct3-12-30Cell-addID-par',
                                'creator': 'Guobao Shen',
                                'tunex': 16.34,
                                'tuney': 32.56,
                                'finalEnergy': 3.0,
                                'simulationCode': 'tracy',
                                'sumulationAlgorithm': 'SI',
                                #'simulationControl': tracyhead,
                                #'simulationControlFile': 'CD3-Oct3-12-30Cell-addID-par.lat'
                                'beamParameter': {}
                               }
                 }

    modelhead2 = {'CD3-Oct3-12-30Cell-addID-par bare 2':
                               {  # header information
                                'description': 'an instance for lattice CD3-Oct3-12-30Cell-addID-par',
                                'creator': 'Guobao Shen',
                                'tunex': 16.35,
                                'tuney': 32.57,
                                'finalEnergy': 3.0,
                                'simulationCode': 'tracy',
                                #'simulationControl': tracyhead,
                                #'simulationControlFile': 'CD3-Oct3-12-30Cell-addID-par.lat'
                                'beamParameter': {}
                               }
                 }
    modelhead3 = {'CD3-Oct3-12-30Cell-addID-par bare':
                               {  # header information
                                    'description': 'an instance for lattice CD3-Oct3-12-30Cell-addID-par',
                                    'creator': 'Guobao Shen',
                                    'tunex': 16.36,
                                    'tuney': 32.58,
                                    'finalEnergy': 3.0,
                                    'simulationCode': 'tracy',
                                    'sumulationAlgorithm': 'SI',
                                    'simulationControl': tracyhead,
                                    'simulationControlFile': 'CD3-Oct3-12-30Cell-addID-par.lat',
                                    'beamParameter': {}
                               }
                 }
    modelhead4 = {'CD3-Oct3-12-30Cell-addID-par bare 2':
                               {  # header information
                                    'description': 'an instance for lattice CD3-Oct3-12-30Cell-addID-par',
                                    'creator': 'Guobao Shen',
                                    'tunex': 16.37,
                                    'tuney': 32.59,
                                    'finalEnergy': 3.5,
                                    'simulationCode': 'tracy',
                                    'simulationControl': tracyhead,
                                    'simulationControlFile': 'CD3-Oct3-12-30Cell-addID-par.lat',
                                    'beamParameter': {}

                               }
                 }
    savemodel = True
    if savemodel:
        # test with model header only. No really data
        try:
            modelinst.savemodel(latticename, latticeversion, latticebranch, modelhead1)
            modelinst.savemodel(latticename, latticeversion, latticebranch, modelhead2)
            print 'save model'
        except ValueError:
            modelinst.updatemodel(latticename, latticeversion, latticebranch, modelhead3)
            try:
                modelinst.updatemodel(latticename, latticeversion, latticebranch, modelhead4)
            except ValueError:
                print "Yes. It is expected since algorithm is unknown when saving model."
            print 'update model'
            
    latticename = 'CD3-Apr07-10-30cell-par' 
    latticeversion = 20121003 
    latticebranch = 'test'
    beamParameter = preparetracytwiss('CD3-Apr07-10-30cell-par.twiss')
    modeldata1 = {'CD3-Apr07-10-30cell-par':
                               {  # header information
                                    'description': 'an instance for lattice CD3-Oct3-12-30Cell-addID-par',
                                    'creator': 'Guobao Shen',
                                    'tunex': 16.36,
                                    'tuney': 32.58,
                                    'finalEnergy': 3.0,
                                    'simulationCode': 'tracy',
                                    'sumulationAlgorithm': 'SI',
                                    'simulationControl': tracyhead,
                                    'simulationControlFile': 'CD3-Oct3-12-30Cell-addID-par.lat',
                                    'beamParameter': beamParameter
                               }
                 }
    modeldata2 = {'CD3-Apr07-10-30cell-par 2':
                               {  # header information
                                    'description': 'an instance for lattice CD3-Oct3-12-30Cell-addID-par',
                                    'creator': 'Guobao Shen',
                                    'tunex': 16.37,
                                    'tuney': 32.59,
                                    'finalEnergy': 3.5,
                                    'simulationCode': 'tracy',
                                    'simulationControl': tracyhead,
                                    'simulationControlFile': 'CD3-Oct3-12-30Cell-addID-par.lat',
                                    'beamParameter': beamParameter

                               }
                 }
    savemodeldata = True
    if savemodeldata:
        try:
            modelinst.savemodel(latticename, latticeversion, latticebranch, modeldata1)
            print 'save 1st model with twiss'
            modelinst.savemodel(latticename, latticeversion, latticebranch, modeldata2)
            print 'save 2nd model with twiss'
        except ValueError:
            modelinst.updatemodel(latticename, latticeversion, latticebranch, modeldata1)
            print 'update 1st model with twiss'
            try:
                modelinst.updatemodel(latticename, latticeversion, latticebranch, modeldata2)
                print 'update 2nd model with twiss'
            except ValueError:
                print "Yes. It is expected since algorithm is unknown when saving model data."
            print 'update model with twiss'
