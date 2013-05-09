'''
Created on May 8, 2013

@author: shengb
'''
import unittest
import logging
import requests

from preparerdb import addlatticetype, cleanlatticetype

class TestClientConnection(unittest.TestCase):

    __url = 'http://localhost:8000/lattice/'
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
        self.assertEqual(r.status_code, 200, 'Fail to connect to lattice service')

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
    
    def test_fail(self):
        '''this is a demo how to skip a test'''
        raise unittest.SkipTest('this test is not implemented here')

class TestLattice(unittest.TestCase):

    __url = 'http://localhost:8000/lattice/'
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}
    
    testlatticetype = [{'name': 'test1', 'format': 'txt'},
                       {'name': 'test2', 'format': 'txt'},
                       {'name': 'test3', 'format': 'lat'},
                       {'name': 'test4', 'format': 'ele'},
                       {'name': 'test5', 'format': 'xal'},
                       {'name': 'test6', 'format': 'mad'},
                       ]
    def setUp(self):
        try:
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
            #client = requests.get(self.__url, verify=False, headers=self.__jsonheader).raise_for_status()
            self.client = requests.session()
        except:
            raise

    def tearDown(self):
        self.client.close()

    def testRetrieveLatticeType(self):
        ''''''
        # clean to avoid duplicated copies
        cleanlatticetype(self.testlatticetype)
        
        # get existing entries
        params={'function': 'retrieveLatticeType',
                'name': '*',
                'format': '*'}
        #r=self.client.get(self.__url+'?'+urlencode(params), verify=False, headers=self.__jsonheader)
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        existing = len(result)

        # insert into database
        addlatticetype(self.testlatticetype)
        
        params={'function': 'retrieveLatticeType',
                'name': '*',
                'format': '*'}
        #r=self.client.get(self.__url+'?'+urlencode(params), verify=False, headers=self.__jsonheader)
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        self.assertEqual(len(result), existing + len(self.testlatticetype),
                         'lattice types wrong. Should find %s different supported lattice types.'%(existing + len(self.testlatticetype)))
    
        # get one data entry
        params={'function': 'retrieveLatticeType',
                'name': self.testlatticetype[0]['name'],
                'format': self.testlatticetype[0]['format']}
        #r=self.client.get(self.__url+'?'+urlencode(params), verify=False, headers=self.__jsonheader)
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        self.assertEqual(len(result), 1, 'lattice type is not unique')
        for _, v in result.iteritems():
            self.assertEqual(v['name'], self.testlatticetype[0]['name'], 'Lattice type name is wrong')
            self.assertEqual(v['format'], self.testlatticetype[0]['format'], 'Lattice format name is wrong')
        
        # should not get any result since name + format is not in
        params={'function': 'retrieveLatticeType',
                'name': self.testlatticetype[0]['name'],
                'format': self.testlatticetype[3]['format']}
        #r=self.client.get(self.__url+'?'+urlencode(params), verify=False, headers=self.__jsonheader)
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        self.assertEqual(len(result), 0, 'lattice type wrong')
        
        # should raise exception since parameter 'format' is missing
        params={'function': 'retrieveLatticeType',
                'name': '*'}
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.text, 
                         'Parameters is missing for function retrieveLatticeType',
                         'Should raise a parameter missing error')
        self.assertRaises(requests.exceptions.HTTPError, r.raise_for_status)
        self.assertEqual(r.status_code, 404, 'Missing parameter error.')
    
        # should raise exception since parameter 'format' is missing
        params={'function': 'retrieveLatticeType',
                'name': [self.testlatticetype[0]['name'],self.testlatticetype[1]['name']],
                'format': 'lat'}
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertRaises(requests.exceptions.HTTPError, r.raise_for_status)
        self.assertEqual(r.text,
                         'No multiple searches for either name or format are implemented yet.',
                         'Should return multiple searches message.')
        self.assertEqual(r.status_code, 404, 'Missing parameter error.')

        # clean database
        cleanlatticetype(self.testlatticetype)

    def testSaveLatticeType(self):
        '''
        '''
        # clean test data first
        cleanlatticetype(self.testlatticetype)

        # get existing entries
        params={'function': 'retrieveLatticeType',
                'name': '*',
                'format': '*'}
        #r=self.client.get(self.__url+'?'+urlencode(params), verify=False, headers=self.__jsonheader)
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        existing = len(result)

        # test save lattice type
        for testlt in self.testlatticetype:
            payload={'function': 'saveLatticeType',
                     'name': testlt['name'],
                     'format': testlt['format']}
            r = self.client.post(self.__url, data=payload)
            self.assertEqual(r.status_code, 200, 'Should save successfully.')
        
        params={'function': 'retrieveLatticeType',
                'name': '*',
                'format': '*'}
        #r=self.client.get(self.__url+'?'+urlencode(params), verify=False, headers=self.__jsonheader)
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        self.assertEqual(len(result), existing + len(self.testlatticetype),
                         'lattice types wrong. Should find %s different supported lattice types.'
                         %(existing + len(self.testlatticetype)))
    
        # should fail when insert again
        for testlt in self.testlatticetype:
            payload={'function': 'saveLatticeType',
                     'name': testlt['name'],
                     'format': testlt['format']}
            r = self.client.post(self.__url, data=payload)
            self.assertRaises(requests.exceptions.HTTPError, r.raise_for_status)
            self.assertEqual(r.status_code, 404, 'Should exist already.')
            self.assertEqual(r.text,
                             'Lattice type (%s) with given format (%s) exists already.'%(payload['name'], payload['format']),
                             'Wrong content type. Should be application/json')

        # clean all data entries inserted during this test
        cleanlatticetype(self.testlatticetype)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()