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
from requests.adapters import HTTPAdapter
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
                    'bm':{
                        bm data
                    },
                    'id': {
                        id data
                    },
                   'logic': {
                       logic data
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
    