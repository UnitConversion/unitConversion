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

import requests
_requests_version=[int(x) for x in requests.__version__.split('.')]
if _requests_version[0] < 1 or sys.version_info[1] < 1:
    print("This library requires at least Python-requests version 1.1.x")
    sys.exit(1)

from requests import auth
from requests import HTTPError

from copy import copy

import base64
try: 
    import json
except ImportError: 
    import simplejson as json

from _conf import _conf

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
        self.__resource = ''
        
        try:
            self.__baseURL = self.__getdefaultconfig('BaseURL', BaseURL)
            self.__userName = self.__getdefaultconfig('username', username)
            self.__password = self.__getdefaultconfig('password', password)
            
            if self.__userName and self.__password:
                self.__auth = auth.HTTPBasicAuth(self.__userName, self.__password)
            else:
                self.__auth = None
            
            #requests.get(self.__baseURL + self.__resource, verify=False, headers=copy(self.__jsonheader)).raise_for_status()
            self.client = requests.session()
        except:
            raise Exception, 'Failed to create client to ' + self.__baseURL + self.__resource
        
    def __getdefaultconfig(self, arg, value):
        if value == None and _conf.has_option('DEFAULT', arg):
            return _conf.get('DEFAULT', arg)
        else:
            return value

    def downloadActiveInterlock(self):
        '''
        Retrieve complete dataset with status approved and set it to active
        
        :return
        {'bm':{
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
        
        # Set url
        url = 'download/'
        
        # Set parameters
        params={
            'modified_by': self.__userName
        }
        
        r=self.client.post(self.__baseURL+url, data=params, verify=False, headers=self.__jsonheader, auth=self.__auth)
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
    