'''
Created on Mar 19, 2014

@author: shengb
'''

import json
import base64
#import errno

import logging
from copy import copy
import requests
from requests import auth

from _conf import _conf

class LatticeModelClient(object):
    '''
    This class is a client library to lattice/model service, which stores lattice data and its simulation result.
    It currently supports 3 different lattice formats, which are tab formatted lattice, tracy3 lattice, and elegant lattice.
    '''
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}
    __savelatticeResource = '/savelattice'
    __savelatticeinfoResource = '/savelatticeinfo'
    __savelatticetypeResource = '/savelatticetype'
    __savemodelResource = '/savemodel'

    def __init__(self, BaseURL=None, username=None, password=None):
        '''
        BaseURL = the url of the lattice/model service
        username = 
        '''
        try:            
            requests_log = logging.getLogger("lattice_client")
            requests_log.setLevel(logging.DEBUG)

            self.__baseURL = self.__getDefaultConfig('BaseURL', BaseURL)
            self.__userName = self.__getDefaultConfig('username', username)
            self.__password = self.__getDefaultConfig('password', password)
            if username and password:
                self.__auth = auth.HTTPBasicAuth(username, password)
            else:
                self.__auth = None
            requests.get(self.__baseURL, verify=False, headers=copy(self.__jsonheader)).raise_for_status()
        except:
            raise Exception, 'Failed to create client to ' + self.__baseURL
        
    def __getDefaultConfig(self, arg, value):
        '''
        If Value is None, this will try to find the value in one of the configuration files
        '''
        if value == None and _conf.has_option('DEFAULT', arg):
            return _conf.get('DEFAULT', arg)
        else:
            return value
    
    def saveLattice(self, name, branch, version, latfile, latdata=None, description=None, latticetype=None, kickmap=None, elefile=None, binarymap=False, topdir=None):
        '''
        Save lattice
        
        kickmap: a list of all map files
        latticetype: dict with format {'name':, 'format': ,}
        '''

        kmdict = {}
        if kickmap != None:
            for km in kickmap:
                with file(km, 'r') as f:
                    if binarymap:
                        kmdata = base64.b64encode(f.read())
                    else:
                        kmdata = f.readlines()
                kmdict[km] = kmdata
        
        if topdir != None:
            with file('/'.join((topdir, latfile)), 'r') as f:
                rawlatdata = f.readlines()
        else:
            with file(latfile, 'r') as f:
                rawlatdata = f.readlines()
            

        ctrldict = None
        if elefile != None:
            ctrldict = {'name': elefile}
            if topdir != None:
                with file('/'.join((topdir, elefile)), 'r') as f:
                    ctrldict['data'] = f.readlines()
            else:
                with file(elefile, 'r') as f:
                    ctrldict['data'] = f.readlines()
                
        payload = {'name': name,
                   'version': version,
                   'branch': branch,
                   'description': description
                   }
        
        lattice = {'name': latfile,
                   'map': kmdict,
                   'raw': rawlatdata}

        if latdata != None:
            lattice['data'] = latdata
            
        if ctrldict != None:
            lattice['control'] = ctrldict
            
        payload['lattice'] = json.dumps(lattice)

        if latticetype != None:
            payload['latticetype'] = json.dumps(latticetype)
        
        r = requests.post(self.__baseURL + self.__savelatticeResource, \
                          data=payload, \
                          headers=copy(self.__jsonheader), \
                          verify=False, \
                          auth=self.__auth)
        
        r.raise_for_status()
        return r.json()
        
    def retrieveLattice(self, name, branch, version, description=None, withdata=False, rawdata=False):
        '''
        Retrieving lattice according given lattice name, version, branch, and description
        '''
        
        params = {'function': 'retrieveLattice',
                  'name': name,
                  'branch': branch,
                  'version': version,
                  'description': description,
                  'withdata': withdata,
                  'rawdata': rawdata
                  }
        resp = requests.get(self.__baseURL, params=params, verify=False, headers=self.__jsonheader)
        resp.raise_for_status()
        return resp.json()        
        
    def saveModel(self, name, branch, version, modelparams):
        '''
        Save a simulation result.
        
        name:    lattice name that this model belongs to
        branch:  lattice branch name that this model belongs to
        version: lattice version that this model belongs to
        
        modelparams:      a dictionary which holds all data 
            {'model name':                           # model name
                          { # header information
                            'description': ,         # description of this model
                            'tunex': ,               # horizontal tune
                            'tuney': ,               # vertical tune
                            'chromX0': ,             # linear horizontal chromaticity
                            'chromX1': ,             # non-linear horizontal chromaticity
                            'chromX2': ,             # high order non-linear horizontal chromaticity
                            'chromY0': ,             # linear vertical chromaticity
                            'chromY1': ,             # non-linear vertical chromaticity
                            'chromY2': ,             # high order non-linear vertical chromaticity
                            'finalEnergy': ,         # the final beam energy in GeV
                            'simulationCode': ,      # name of simulation code, Elegant and Tracy for example
                            'sumulationAlgorithm': , # algorithm used by simulation code, for example serial or parallel,
                                                     # and SI, or SI/PTC for Tracy code
                            'simulationControl': ,   # various control constrains such as initial condition, beam distribution, 
                                                     # and output controls
                            'simulationControlFile': # file name that control the simulation conditions, like a .ele file for elegant
                            
                            # simulation data
                            'beamParameter':         # a dictionary consists of twiss, close orbit, transfer matrix and others
                          }
             ...
            }
    
        beamparameter is a dictionary which hosts all beam simulation results.
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
                  'transferMatrix': , []
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
        payload={'function': 'saveModel',
                'latticename': name,
                'latticebranch': branch,
                'latticeversion': version,
                'model': json.dumps(modelparams)}
        r = requests.post(self.__baseURL + self.__savemodelResource, \
                          data=payload, \
                          headers=copy(self.__jsonheader), \
                          verify=False, \
                          auth=self.__auth)
        r.raise_for_status()
        return r.json()
        
    def retrieveTwiss(self, name):
        '''
        list all the systems available
        '''
        params = {'function': 'retrieveTwiss',
                  'modelname': name,
                  }
        r=requests.get(self.__baseURL, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        return r.json()

    def retrievelattype(self, name=None, formats=None):
        '''Get supported lattice formats existing in database.
        '''
        if name == None:
            name = "*"
        if formats == None:
            formats = "*"
        params={'function': 'retrieveLatticeType',
                'name': name,
                'format': formats}
        r=requests.get(self.__baseURL, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        return r.json()

    def savelattype(self, name, formats):
        '''Add a new lattice format into in database.
        
        Raise: HTTPError: 400 Client Error: BAD REQUEST if given data exists already
        '''
        payload={'name': name,
                 'format': formats}
        r = requests.post(self.__baseURL + self.__savelatticetypeResource, \
                          data=payload, \
                          headers=copy(self.__jsonheader), \
                          verify=False, \
                          auth=self.__auth)
        r.raise_for_status()
        return r.json()


