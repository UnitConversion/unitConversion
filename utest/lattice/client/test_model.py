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

from preparerdb import cleanmodelcode

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

    def testPostMethod(self):
        r = self.client.post(self.__url, headers=dict(Referer=self.__url))
        r.raise_for_status()
        self.assertEqual(r.status_code, 200, 'Fail to connect to lattice service')
        self.assertEqual(r.headers.get('content-type'), 'application/json', 'Wrong content type. Should be application/json')

    def testPutMethod(self):
        '''no put method is implemented.'''
        r = self.client.put(self.__url, headers=dict(Referer=self.__url))
        self.assertRaises(requests.exceptions.HTTPError, r.raise_for_status)
        self.assertEqual(r.status_code, 405, 'Service is not allowed. Wrong returned status code.')

class TestModelCode(unittest.TestCase):
    __url = 'http://localhost:8000/lattice/model/'
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}
    
    def setUp(self):
        self.modelcode=[{'name': 'tracy3', 'algorithm': 'SI'},
                        {'name': 'tracy3', 'algorithm': 'PIC'},
                        {'name': 'tracy3'},

                        {'name': 'tracy4', 'algorithm': 'SI'},
                        {'name': 'tracy4', 'algorithm': 'PIC'},
                        {'name': 'tracy4'},
                        
                        {'name': 'elegant', 'algorithm': 'serial'},
                        {'name': 'elegant', 'algorithm': 'parallel'},
                        {'name': 'elegant'},
                        
                        {'name': 'impact', 'algorithm': 'serial'},
                        {'name': 'impact', 'algorithm': 'PIC with Lorenz field'},
                        {'name': 'impact', 'algorithm': 'PIC with Gaussion field'},
                        {'name': 'impact'},
                        ]
    
        try:
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
            self.client = requests.session()
        except:
            raise

    def tearDown(self):
        ''''''
        self.client.close()

    def testModelCode(self):
        # clean existing model model code for testing
        cleanmodelcode(self.modelcode)
        
        # try to get something without enough parameters
        # should get an error
        params={'function': 'retrieveModelCodeInfo',}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 404, 'Expecting status code 404, but got %s'%r.status_code)
        self.assertEqual(r.text, 
                         'No sufficient information provided to retrieve a simulation info (simulation result and algorithm)',
                         'Wrong error message. Got\n  --%s'%r.text)

        # get non existing entries
        # should get empty result
        params={'function': 'retrieveModelCodeInfo',
                'name': '*'}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Fail to get model code info')
        self.assertEqual(r.json(), 
                         {},
                         'Wrong result. Got\n  --%s'%r.text)

        # save info
        for mc in self.modelcode:
            payload={'function': 'saveModelCodeInfo',
                     'name': mc['name']}
            if mc.has_key('algorithm'):
                payload['algorithm'] = mc['algorithm']
            r = self.client.post(self.__url, data=payload)
            try:
                if mc.has_key('algorithm'):
                    self.assertEqual(r.status_code, 200, 'Fail to save model info (code: %s, algorithm: %s)'%(mc['name'], mc['algorithm']))
                else:
                    self.assertEqual(r.status_code, 200, 'Fail to save model info (code: %s, algorithm: None)'%(mc['name']))
            except Exception as e:
                print 'get error code %s, and message:\n  -- %s'%(r.status_code, r.text)
                raise e
        
        params={'function': 'retrieveModelCodeInfo',
                'name': '*'}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Fail to get model code info')

        # get all entries in model code
        params={'function': 'retrieveModelCodeInfo',
                'name': '*',
                'algorithm': '*'}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Fail to get model code info')
        self.assertEqual(len(r.json()), len(self.modelcode),
                         'Expecting %s entries, but got %s'%(len(self.modelcode), len(r.json())))

        # get those have no algorithm
        # there are 4 without algorithm
        params={'function': 'retrieveModelCodeInfo',
                'name': '*',
                'algorithm': None}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Fail to get model code info')
        self.assertEqual(len(r.json()), 4,
                         'Expecting 4 entries, but got %s'%(len(r.json())))
        
        # get those only have algorithm
        # there are 9 having algorithm
        params={'function': 'retrieveModelCodeInfo',
                'name': '*',
                'algorithm': '*?*'}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Fail to get model code info')
        self.assertEqual(len(r.json()), 9,
                         'Expecting 9 entries, but got %s'%(len(r.json())))
        

class TestGoldenModel(unittest.TestCase):
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



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    