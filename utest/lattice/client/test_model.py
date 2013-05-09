'''
Created on May 8, 2013

@author: shengb
'''
import unittest

import logging
#try:
#    from django.utils import simplejson as json
#except ImportError:
#    import json

import requests

class TestClientConnection(unittest.TestCase):

    __url = 'http://localhost:8000/lattice/model/'
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}
    
    def setUp(self):
        try:
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
            self.client = requests.session()
        except:
            raise

    def tearDown(self):
        ''''''
        self.client.close()

    def testClientConnection(self):
        r = self.client.get(self.__url, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        self.assertIsNotNone(r, 'Failed to create simple client')
        self.assertEqual(r.status_code, 200, 'Fail to connect to model service')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()