'''
Copyright (c) 2013 Brookhaven National Laboratory

All rights reserved. Use is subject to license terms and conditions.


    Created on Sep 10, 2013

    @author: shengb
    @updated: dejan.dezman@cosylab.com, March 20, 2014

'''

import sys
if sys.version_info[0] != 2 or sys.version_info[1] < 6:
    print("This library requires at least Python version 2.6")
    sys.exit(1)

from copy import copy

import ssl
import requests
if requests.__version__ < '2.0.0':
    print("This library requires at least request version 2.0.0")
    sys.exit(1)

from requests.adapters import HTTPAdapter
try:
    from urllib3.poolmanager import PoolManager
except ImportError:
    from requests.packages.urllib3.poolmanager import PoolManager

from requests import auth
from requests import HTTPError

try: 
    import json
except ImportError: 
    import simplejson as json

from _conf import _conf

class SSLAdapter(HTTPAdapter):
    '''An HTTPS Transport Adapter that uses an arbitrary SSL version.'''
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version

        super(SSLAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=self.ssl_version)

class ActiveInterlockClient(object):
    '''
    The ActiveInterlockClient provides a client connection object to perform 
    save, retrieve, and update operations for NSLS II active interlock service.
    '''
 
    def __init__(self, BaseURL=None, username=None, password=None):
        '''
        BaseURL = the url of the active interlock service
        username = 
        password = 
        '''
        self.__jsonheader = {'content-type':'application/json', 'accept':'application/json'}    
        self.__resource = '/ai/'
        
        try:
            self.__baseURL = self.__getdefaultconfig('BaseURL', BaseURL)
            self.__userName = self.__getdefaultconfig('username', username)
            self.__password = self.__getdefaultconfig('password', password)
            
            if self.__userName and self.__password:
                self.__auth = auth.HTTPBasicAuth(self.__userName, self.__password)
            else:
                self.__auth = None
            
            #self.client = requests.session()
            #requests.get(self.__baseURL + self.__resource, verify=False, headers=copy(self.__jsonheader)).raise_for_status()
            self.__session = requests.Session()
            # specify ssl version. Use SSL v3 for secure connection, https.
            self.__session.mount('https://', SSLAdapter(ssl_version=ssl.PROTOCOL_SSLv3))
            
            #self.__session.post(self.__baseURL + self.__resource, headers=copy(self.__jsonheader), auth=self.__auth).raise_for_status()
            self.__session.get(self.__baseURL + self.__resource+'web', headers=copy(self.__jsonheader), auth=self.__auth).raise_for_status()

        except:
            raise Exception, 'Failed to create client to ' + self.__baseURL + self.__resource
        
    def __getdefaultconfig(self, arg, value):
        if value == None and _conf.has_option('DEFAULT', arg):
            return _conf.get('DEFAULT', arg)
        else:
            return value

    def downloadActiveInterlock(self, status="approved"):
        '''
        Retrieve complete dataset with status approved and set it to active
        
        :param status: AI status we want to download. Acceptable values are **approved** and **active**
        :type status: string
        
        :return:
            A Python dictionary is returned as::

                {
                  'bm': {   # Bending Magnet part of the returned object
                    'id': {
                      'id':                   , #int, id of the device in the database
                      'ai_id':                , #int, id of the active interlock
                      'name':                 , #str, name of the device
                      'definition':           , #str, definition of the device
                      'logic':                , #str, name of the logic
                      'logic_code':           , #int, logic code
                      'shape':                , #str, shape of the logic
                      'bm_cell':              , #str, cell
                      'bm_sequence':          , #str, sequence
                      'bm_type':              , #str, type
                      'bm_s':                 , #str, s
                      'bm_aiolh':             , #str, horizontal offset limit
                      'bm_aiorh':             , #str, horizontal offset origin
                      'bm_aiolv':             , #str, vertical offset limit
                      'bm_aiorv':             , #str, vertical offset origin
                      'bm_safe_current':      , #str, safe current
                      'bm_in_use':            , #str, is element in use
                      'prop_statuses': {
                        'prop1key':           , #int, status of the property,
                        ...
                        'propNkey':           , #int, status of the property
                      },
                      'prop_units': {
                        'prop1key':           , #string, property unit,
                        ...
                        'propNkey':           , #string, property unit
                      }
                    }
                  },
                  'id': {
                    'id': {   # Insertion Device part of the returned object
                      'id':                   , #int, id of the device in the database
                      'ai_id':                , #int, id of the active interlock
                      'name':                 , #str, name of the device and also s3 name
                      'definition':           , #str, definition of the device
                      'logic':                , #str, name of the logic
                      'shape':                , #str, shape of the logic
                      'logic_code':           , #int, logic code
                      'cell':                 , #str, cell
                      'type':                 , #str, type
                      'set':                  , #str, set
                      'str_sect':             , #str, straight section
                      'defined_by':           , #str, defined by
                      's1_name':              , #str, s1 name
                      's1_pos':               , #str, s1 position
                      's1_pos_from':          , #str, s1 position from AIE-ID location
                      's2_name':              , #str, s2 name
                      's2_pos':               , #str, s2 position
                      's2_pos_from':          , #str, s2 position from AIE-ID location
                      's3_pos':               , #str, s3 position
                      's3_pos_from':          , #str, s3 position from center of straight section
                      'max_offset':           , #str, maximum offset
                      'max_angle':            , #str, maximum angle
                      'extra_offset':         , #str, extra offset
                      'x_offset_s1':          , #str, horizontal s1 offset
                      'x_offset_origin_s1':   , #str, horizontal s1 offset origin
                      'x_offset_s2':          , #str, horizontal s2 offset
                      'x_offset_origin_s2':   , #str, horizontal s2 offset origin
                      'x_offset_s3':          , #str, horizontal s3 offset
                      'x_angle':              , #str, horizontal angle
                      'y_offset_s1':          , #str, vertical s1 offset
                      'y_offset_origin_s1':   , #str, vertical s1 offset origin
                      'y_offset_s2':          , #str, vertical s2 offset
                      'y_offset_origin_s2':   , #str, vertical s2 offset origin
                      'y_offset_s3':          , #str, vertical s3 offset
                      'y_angle':              , #str, vertical angle
                      'safe_current':         , #str, safe current
                      'in_use':               , #str, is element in use
                      'prop_statuses': {
                        'prop1key':           , #int, status of the property,
                        ...
                        'propNkey':           , #int, status of the property
                      },
                      'prop_units': {
                        'prop1key':           , #string, property unit,
                        ...
                        'propNkey':           , #string, property unit
                      }
                    }
                  },
                  'logic': {   # Logic part of the returned object
                    'id': {
                      'label':                , # str, column's name
                      'id':                   , # int, internal id of active interlock logic
                      'name':                 , # str, name of active interlock envelop 
                      'shape':                , # str, allowed envelop shape in phase space
                      'logic':                , # str, logic expression
                      'code':                 , # int, logic code for hardware convenience
                      'status':               , # int, satus of the logic
                      'created_by':           , # str, who created this entry
                      'created_date':         , # datetime, when this entry was created
                      'num':                  , # int, usage count of this logic
                    }
                  }
                 }

        :Raises: HTTPError
        '''

        # Set status
        statusParam = 1
        
        if status == "approved":
            statusParam = 1
            
        elif status == "active":
            statusParam = 2
            
        else:
            self.__raise_for_status(400, "Status parameter not acceptable!")

        # Set url
        url = 'download/'
        
        # Set parameters
        params={
            'status': statusParam,
            'modified_by': self.__userName
        }
        
        r=self.__session.post(self.__baseURL+self.__resource+url, data=params, verify=False, headers=self.__jsonheader, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)
        
        return r.json()
    
    @classmethod
    def __raise_for_status(self, status_code, reason):
        http_error_msg = ''

        if 400 <= status_code < 500:
            http_error_msg = '%s Client Error: %s' % (status_code, reason)

        elif 500 <= status_code < 600:
            http_error_msg = '%s Server Error: %s' % (status_code, reason)

        if http_error_msg:
            http_error = HTTPError(http_error_msg)
            http_error.response = self
            raise http_error
    
