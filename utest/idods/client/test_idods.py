'''
Created on Feb 10, 2014

@author: dejan.dezman@cosylab.com
'''
import unittest
import logging
import requests

try:
    from django.utils import simplejson as json
except ImportError:
    import json

import os, sys

libPath = os.path.abspath("../../../utest/")
sys.path.append(libPath)

from idods.dataapi.preparerdb import *

class TestIdods(unittest.TestCase):

    __url = 'http://localhost:8000/id/device/'
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}

    def cleanTables(self):
        # Clean vendor table
        cleanVendor(['test vendor'])

    def setUp(self):
        self.cleanTables()
        
        try:
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
            self.client = requests.session()
        except:
            raise

    def tearDown(self):
        self.cleanTables()
        self.client.close()

    def testVendor(self):
        
        '''
        Save new vendor
        '''
        url = 'http://localhost:8000/id/device/savevendor/'
        
        # Set parameters
        params={
            'name': 'test vendor',
            'description': 'desc'
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        '''
        Try to retrieve vendor
        '''
        url = 'http://localhost:8000/id/device/vendor/'
        
        # Set parameters
        params={
            'name': '*',
            'description': '*'
        }
        
        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        existing = len(result)
        
        # Test the number of vendors
        self.assertEqual(existing, 1, 'There is more then one vendor in the database!')
        
        # Test returned vendor name
        self.assertEqual(resultObject['name'], 'test vendor', 'There is no vendor with name test vendor!')
        
        # Test returned vendor description
        self.assertEqual(resultObject['description'], 'desc', 'There is no vendor with that description!')
        
        '''
        Try to update vendor
        '''
        url = 'http://localhost:8000/id/device/updatevendor/'
        
        # Set parameters
        params={
            'old_name': 'test vendor',
            'name': 'test vendor',
            'description': 'desc2'
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        '''
        Try to retrieve vendor
        '''
        url = 'http://localhost:8000/id/device/vendor/'
        
        # Set parameters
        params={
            'name': '*',
            'description': '*'
        }
        
        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        existing = len(result)
        
        # Test the number of vendors
        self.assertEqual(existing, 1, 'There is more then one vendor in the database!')
        
        # Test returned vendor name
        self.assertEqual(resultObject['name'], 'test vendor', 'There is no vendor with name test vendor!')
        
        # Test returned vendor description
        self.assertEqual(resultObject['description'], 'desc2', 'There is no vendor with that description!')

if __name__ == "__main__":
    unittest.main()