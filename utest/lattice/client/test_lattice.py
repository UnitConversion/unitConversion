'''
Created on May 8, 2013

@author: shengb
'''
import unittest
import logging
import requests

try:
    from django.utils import simplejson as json
except ImportError:
    import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

from preparerdb import cleanlatticetype, deletelattice, truncatelattice

from testlat1 import tracylat as CD3ParID
from testlat2 import tracylat as CD3Par

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

class TestLatticeType(unittest.TestCase):

    __url = 'http://localhost:8000/lattice/'
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}
    
    testlatticetype = [{'name': 'test1', 'format': 'txt'},
                       {'name': 'test2', 'format': 'txt'},
                       {'name': 'test3', 'format': 'lat'},
                       {'name': 'test4', 'format': 'ele'},
                       {'name': 'test5', 'format': 'xdxf'},
                       {'name': 'test6', 'format': 'mad'},
                       ]
    def setUp(self):
        try:
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
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

        # prepare lattice type
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

class TestLatticeInfo(unittest.TestCase):

    __url = 'http://localhost:8000/lattice/'
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}
    
    testlatticetype = [{'name': 'test_plain', 'format': 'txt'},
                       {'name': 'test_tracy3',  'format': 'lat'},
                       {'name': 'test_tracy4',  'format': 'lat'},
                       ]
    versions = [20130511, 20130512, 20130513]
    creators = ['test1', 'test2', 'test3']
    descs  = ['unit test case 1', 'unit test case 2', 'unit test case 3']
        

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

    def testLatticeInfo(self):
        '''
        '''
        # clean pre-existed lattice type for the test purpose
        cleanlatticetype(self.testlatticetype)
        
        name='test lattice'
        version = 'abc'
        branch = 'unit test'
        # clean this entry first
        deletelattice(name, version, branch)
        
        payload={'function': 'saveLatticeInfo',
                 'name': name,
                 'branch': branch
                 }
        r = self.client.post(self.__url, data=payload)
        # should raise an error since version is missing
        self.assertRaises(requests.exceptions.HTTPError, r.raise_for_status)
        self.assertEqual(r.status_code, 404, 'Should raise status code %s'%(r.status_code))
        self.assertEqual(r.text, 
                         'Parameters is missing for function %s'%payload['function'], 
                         'Should raise parameter missing error')

        payload={'function': 'saveLatticeInfo',
                 'name': name,
                 'version': version,
                 'branch': branch
                 }
        r = self.client.post(self.__url, data=payload)
        # should raise an error since version has to be a number or number string
        self.assertRaises(requests.exceptions.HTTPError, r.raise_for_status)

        # should be ready to save a new lattice
        version = 20130510
        payload={'function': 'saveLatticeInfo',
                 'name': name,
                 'version': version,
                 'branch': branch,
                 }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Error when saving a new lattice.\n %s'%(r.text))
        
        # test save lattice with lattice type which exists already
        payload={'function': 'saveLatticeInfo',
                 'name': name,
                 'version': version,
                 'branch': branch,
                 'latticetype': json.dumps(self.testlatticetype[0])
                 }
        r = self.client.post(self.__url, data=payload)
        # should raise an exception since it is there
        self.assertRaises(requests.exceptions.HTTPError, r.raise_for_status)
        self.assertEqual(r.status_code, 404, 'Should return status code %s'%(r.status_code))
        self.assertEqual(r.text, 
                         'lattice (name: %s, version: %s, branch: %s) exists already.'
                         %(name, version, branch),
                         'Should raise a type format error like:\n %s'%(r.text))

        # save a lattice with lattice type/format not in yet.
        payload={'function': 'saveLatticeInfo',
                 'name': name,
                 'version': self.versions[0],
                 'branch': branch,
                 'creator': self.creators[0],
                 'description': self.descs[0],
                 'latticetype': json.dumps(self.testlatticetype[0])
                 }
        r = self.client.post(self.__url, data=payload)
        # should raise an exception since lattice type/format is not there yet.
        self.assertRaises(requests.exceptions.HTTPError, r.raise_for_status)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text, 
                         'Does not support lattice type (%s) with given format (%s).'%(self.testlatticetype[0]['name'],
                                                                                      self.testlatticetype[0]['format'],),
                         'Wrong error message')

        # prepare lattice type
        for testlt in self.testlatticetype:
            payload={'function': 'saveLatticeType',
                     'name': testlt['name'],
                     'format': testlt['format']}
            r = self.client.post(self.__url, data=payload)
            self.assertEqual(r.status_code, 200, 'Should save successfully.')

        for i in range(len(self.versions)):
            payload={'function': 'saveLatticeInfo',
                     'name': name,
                     'version': self.versions[i],
                     'branch': branch,
                     'creator': self.creators[i],
                     'description': self.descs[i],
                     'latticetype': json.dumps(self.testlatticetype[i])
                     }
            r = self.client.post(self.__url, data=payload)
            try:
                self.assertEqual(r.status_code, 200, 'Error when saving a new lattice.\n %s'%(r.text))
            except Exception as e:
                deletelattice(name, version, branch)
                for ver in self.versions:
                    deletelattice(name, ver, branch)
                
                raise e

        ###################################
        #
        # Retrieve lattice info function
        #
        ###################################
        params={'function': 'retrieveLatticeInfo',
                 'name': name,
                 'version': version,
                 'branch': branch,
                 }
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(len(r.json()), 1, 'Should get only one result.')
        for _, v in r.json().iteritems():
            try:
                self.assertEqual(v['name'], name, 'expect lattice name (%s) but get from service (%s)'
                                 %(name, v['name']))
                self.assertEqual(v['version'], version, 'expect lattice version (%s) but get from service (%s)'
                                 %(version, v['version']))
                self.assertEqual(v['branch'], branch, 'expect lattice branch (%s) but get from service (%s)'
                                 %(branch, v['branch']))
            except Exception as e:
                deletelattice(name, version, branch)
                for ver in self.versions:
                    deletelattice(name, ver, branch)
                
                raise e

        params={'function': 'retrieveLatticeInfo',
                 'name': name,
                 }
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        
        try:
            self.assertEqual(len(r.json()), 1+len(self.versions), 'Expecting get %s results.'%(1+len(self.versions)))
            for _, v in r.json().iteritems():
                self.assertEqual(v['name'], name, 'All lattice names should be %s'%name)
                self.assertEqual(v['branch'], branch, 'expect lattice version (%s) but get from service (%s)'
                     %(branch, v['branch']))
                for i in range(len(self.versions)):
                    if v['version'] == self.versions[i]:
                        self.assertEqual(self.creators[i], v['creator'], 'expect lattice version (%s) but get from service (%s)'
                             %(self.creators[i], v['creator']))                        
                        self.assertEqual(self.descs[i], v['description'], 'expect lattice creator (%s) but get from service (%s)'
                             %(self.descs[i], v['description']))                        
                        self.assertEqual(self.testlatticetype[i]['name'], v['latticeType'], 'expect lattice type (%s) but get from service (%s)'
                             %(self.testlatticetype[i]['name'], v['latticeType']))                        
                        self.assertEqual(self.testlatticetype[i]['format'], v['latticeFormat'], 'expect lattice type (%s) but get from service (%s)'
                             %(self.testlatticetype[i]['format'], v['latticeFormat']))                        

        except Exception as e:
            deletelattice(name, version, branch)
            for ver in self.versions:
                deletelattice(name, ver, branch)
            
            raise e

        ###################################
        #
        # Update lattice info function
        #
        ###################################
        payload={'function': 'updateLatticeInfo',
                 'name': name,
                 'version': version,
                 'branch': branch,
                 'latticetype': json.dumps(self.testlatticetype[0])
             }
        r = self.client.post(self.__url, data=payload)
        try:
            self.assertEqual(r.status_code, 200, 'Error happened during updating lattice')
            for _, v in r.json().iteritems():
                self.assertEqual(v, True, 'Expecting true')
        except Exception as e:
            deletelattice(name, version, branch)
            raise e

        params={'function': 'retrieveLatticeInfo',
                 'name': name,
                 'version': version,
                 'branch': branch,
                 }
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(len(r.json()), 1, 'Should get only one result.')
        for _, v in r.json().iteritems():
            try:
                self.assertEqual(v['name'], name, 'expect lattice name (%s) but get from service (%s)'
                                 %(name, v['name']))
                self.assertEqual(v['version'], version, 'expect lattice version (%s) but get from service (%s)'
                                 %(version, v['version']))
                self.assertEqual(v['branch'], branch, 'expect lattice branch (%s) but get from service (%s)'
                                 %(branch, v['branch']))
                self.assertEqual(self.testlatticetype[0]['name'], v['latticeType'], 'expect lattice type (%s) but get from service (%s)'
                     %(self.testlatticetype[0]['name'], v['latticeType']))                        
                self.assertEqual(self.testlatticetype[0]['format'], v['latticeFormat'], 'expect lattice type (%s) but get from service (%s)'
                     %(self.testlatticetype[0]['format'], v['latticeFormat']))                        
            except Exception as e:
                deletelattice(name, version, branch)
                for ver in self.versions:
                    deletelattice(name, ver, branch)
                
                raise e

        # clean this entry first
        deletelattice(name, version, branch)
        for ver in self.versions:
            deletelattice(name, ver, branch)
        cleanlatticetype(self.testlatticetype)

class TestPlainLattice(unittest.TestCase):
    __url = 'http://localhost:8000/lattice/'
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}


    wrongplainlat = '''
 ElementName  ElementType      L          s       K1          K2    Angle
 ......
                               m          m      1/m2       1/m3     rad
-------------------------------------------------------------------------------
 _BEG_        MARK          0        0           0            0         0        
 DH05G1C30A   DRIF          4.29379  4.29379     1.2          0         0
 FH2G1C30A    FTRIM         0.044    4.33779     0            0         0         
 DH1G1A       DRIF          0.31221  4.65        1.3          0         0       
 GEG1C30A     MARK          0        4.65        0            0         0        
 GSG2C30A     MARK          0        4.65        0            0         0        
 SH1G2C30A    SEXT          0.2      4.85        0            24.1977   0        
 DH1AG2A      DRIF          0.085    4.935       1.2          0         0       
 PH1G2C30A    BPM           0        4.935       0            0         0        
 DBPM01       DRIF          0.0775   5.0125      1.4          0         0       
 QH1G2C30A    QUAD          0.275    5.2875      -0.633004    0         0         
 DH2AG2A      DRIF          0.145    5.4325      1.5          0         0
 SQHHG2C30A   QUAD          0.1      5.5325      0            0         0 
'''

    plainlat1 = '''
 ElementName  ElementType      L          s       K1          K2    Angle
                               m          m      1/m2       1/m3     rad
-------------------------------------------------------------------------------
 _BEG_        MARK          0        0           0            0         0        
 DH05G1C30A   DRIF          4.29379  4.29379     1.2          0         0
 FH2G1C30A    FTRIM         0.044    4.33779     0            0         0         
 DH1G1A       DRIF          0.31221  4.65        1.3          0         0       
 GEG1C30A     MARK          0        4.65        0            0         0        
 GSG2C30A     MARK          0        4.65        0            0         0        
 SH1G2C30A    SEXT          0.2      4.85        0            24.1977   0        
 DH1AG2A      DRIF          0.085    4.935       1.2          0         0       
 PH1G2C30A    BPM           0        4.935       0            0         0        
 DBPM01       DRIF          0.0775   5.0125      1.4          0         0       
 QH1G2C30A    QUAD          0.275    5.2875      -0.633004    0         0         
 DH2AG2A      DRIF          0.145    5.4325      1.5          0         0
 SQHHG2C30A   QUAD          0.1      5.5325      0            0         0 
'''

    plainlat2 = '''
 ElementName  ElementType      L          s       K1          K2    Angle
                               m          m      1/m2       1/m3     rad
-------------------------------------------------------------------------------
 DH05G1C30A   DRIF          4.29379  4.29379     1.2          0         0
 FH2G1C30A    FTRIM         0.044    4.33779     0            0         0         
 DH1G1A       DRIF          0.31221  4.65        1.3          0         0       
 GEG1C30A     MARK          0        4.65        0            0         0        
 GSG2C30A     MARK          0        4.65        0            0         0        
 SH1G2C30A    SEXT          0.2      4.85        12.3456      24.1977   0        
 DH1AG2A      DRIF          0.085    4.935       1.2          0         0       
 PH1G2C30A    BPM           0        4.935       0            0         0        
 DBPM01       DRIF          0.0775   5.0125      1.4          0         0       
 QH1G2C30A    QUAD          0.275    5.2875      -0.633004    0         0         
 DH2AG2A      DRIF          0.145    5.4325      1.5          0         0
 SQHHG2C30A   QUAD          0.1      5.5325      0            0         0 
 B1G2C30A     BEND          2.6      8.1325      0            0         0.123456 
'''
    plainlat3 = 'examplelattice/CD3-Oct3-12-30Cell-par.txt'
    plainlat4 = 'examplelattice/CD3-Oct3-12-30Cell-addID-par.txt'
    
    testlatticetype = [{'name': 'plain', 'format': 'txt'},
                       {'name': 'tracy3',  'format': 'lat'},
                       {'name': 'tracy4',  'format': 'lat'},
                       {'name': 'elegant', 'format': 'lte'},
                       {'name': 'xal',     'format': 'xdxf'},
                       
                       {'name': 'test_plain', 'format': 'txt'},
                       {'name': 'test_tracy3',  'format': 'lat'},
                       {'name': 'test_tracy4',  'format': 'lat'},
                       ]
    
    name = ['test plain 1', 'test plain 2', 'CD3 bare lattice', 'CD3 bare lattice with ID']
    branch = ['unit test', 'unit test', 'Design', 'Design']

    
    versions = [20130511, 20130512, 20121003, 20121003]
    creators = ['Guobao', 'Guobao', 'Weiming', 'Yongjun']
    descs  = ['unit test case 1 example', 'unit test case 2 example', 
              'bare lattice for unit test case 3', 'bare lattice with id for unit test case 4']


    kickmap = ['examplelattice/kickmap/EU49_2m_ver.txt',
               'examplelattice/kickmap/U20_3m_FY09.txt',
               'examplelattice/kickmap/U21NX_boostmag.txt',
               'examplelattice/kickmap/U22_6m_5th_112510.txt',
               'examplelattice/kickmap/W100_pole90mm_40div_7m_060611.txt',
               'examplelattice/kickmap/W100_pole90mm_40div_7m_060611_0kick.txt']


    def setUp(self):
        try:
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
            self.client = requests.session()
        except:
            raise

    def tearDown(self):
        self.client.close()

    def testLattice(self):
        ''''''
        truncatelattice()
        # clean lattice type
        cleanlatticetype(self.testlatticetype)
        # save a lattice that its type is not defined yet.
        payload = {'function': 'saveLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[0],
                   'latticetype': json.dumps(self.testlatticetype[0])}
        r = self.client.post(self.__url, data=payload)
        # should raise an exception since lattice type/format is not there yet.
        self.assertRaises(requests.exceptions.HTTPError, r.raise_for_status)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text, 
                         'Does not support lattice type (%s) with given format (%s).'%(self.testlatticetype[0]['name'],
                                                                                      self.testlatticetype[0]['format']),
                         'Wrong error message. Get \n -- %s'%r.text)

        # prepare lattice type
        for testlt in self.testlatticetype:
            payload={'function': 'saveLatticeType',
                     'name': testlt['name'],
                     'format': testlt['format']}
            r = self.client.post(self.__url, data=payload)
            self.assertEqual(r.status_code, 200, 'Should save successfully.')
        
        # save without lattice type & data
        payload = {'function': 'saveLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[0]}
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        
        # retrieve lattice info which is just saved.
        params={'function': 'retrieveLattice',
                'name': self.name[0],
                'version': self.versions[0],
                'branch': self.branch[0],
                'withdata': False, 
                'rawdata': False}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        try:
            self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
            result = r.json()
            for _, v in result.iteritems():
                self.assertEqual(self.name[0], v[u'name'], 
                                 'Expecting lattice name (%s), but got (%s)'%(self.name[0], v['name']))
                self.assertEqual(self.versions[0], v[u'version'], 
                                 'Expecting lattice version (%s), but got (%s)'%(self.versions[0], v['version']))
                self.assertEqual(self.branch[0], v[u'branch'], 
                                 'Expecting lattice branch (%s), but got (%s)'%(self.branch[0], v['branch']))
                self.assertEqual(self.creators[0], v[u'creator'], 
                                 'Expecting lattice creator (%s), but got (%s)'%(self.creators[0], v['creator']))
                self.assertEqual(self.descs[0], v[u'description'], 
                                 'Expecting lattice description (%s), but got (%s)'%(self.descs[0], v['description']))
        except Exception as e:
            # clean this lattice entry
            for i in range(len(self.name)):
                deletelattice(self.name[i], self.versions[i], self.branch[i])
            
            # clean latticetype
            cleanlatticetype(self.testlatticetype)
            raise e

        # retrieve lattice info which is just saved, but wrong description.
        params={'function': 'retrieveLattice',
                'name': self.name[0],
                'version': self.versions[0],
                'branch': self.branch[0],
                'description': 'That is a wrong description', 
                'withdata': False, 
                'rawdata': False}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Finish this method successfully.')
        self.assertEqual(r.json(), {}, "Should get an empty result")
        
        # retrieve lattice info which is just saved, but mismatched lattice type.
        params={'function': 'retrieveLattice',
                'name': self.name[0],
                'version': self.versions[0],
                'branch': self.branch[0],
                'latticetype': json.dumps(self.testlatticetype[0]), 
                'withdata': False, 
                'rawdata': False}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        try:
            self.assertEqual(r.status_code, 200, 'Finish this method successfully.')
            self.assertEqual(r.json(), {}, "Should get an empty result")
        except Exception as e:
            print r.json()
            # clean this lattice entry
            for i in range(len(self.name)):
                deletelattice(self.name[i], self.versions[i], self.branch[i])
            
            # clean latticetype
            cleanlatticetype(self.testlatticetype)
            raise e

        # prepare lattice type
        cleanlatticetype(self.testlatticetype)
        for testlt in self.testlatticetype:
            payload={'function': 'saveLatticeType',
                     'name': testlt['name'],
                     'format': testlt['format']}
            r = self.client.post(self.__url, data=payload)
            self.assertEqual(r.status_code, 200, 'Should save successfully.')
        # update lattice, adding lattice type information.
        payload={'function': 'updateLattice',
                 'name': self.name[0],
                 'version': self.versions[0],
                 'branch': self.branch[0],
                 'creator': self.creators[3],
                 'latticetype': json.dumps(self.testlatticetype[0]), 
                 }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
        self.assertTrue(r.json()=={'result':True}, 'Expecting updating successfully.')

        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        try:
            self.assertEqual(r.status_code, 200, 'Finish this method successfully.')
            result = r.json()
            self.assertTrue(len(result) == 1, 'Expecting one lattice, but got %s'%(len(result)))
            for _, v in result.iteritems():
                self.assertEqual(v['name'], self.name[0], 
                                 'Expecting lattice (%s) but got (%s)'%(self.name[0],v['name'], ))
                self.assertEqual(v['version'], self.versions[0], 
                                 'Expecting lattice version (%s) but got (%s)'%(self.versions[0],v['version'], ))
                self.assertEqual(v['branch'], self.branch[0], 
                                 'Expecting lattice branch (%s) but got (%s)'%(self.branch[0],v['branch'], ))
                self.assertEqual(v['description'], self.descs[0], 
                                 'Expecting description (%s) but got (%s)'%(self.descs[0],v['description'], ))
                self.assertEqual(v['latticeFormat'], self.testlatticetype[0]['format'], 
                                 'Expecting lattice format (%s) but got (%s)'%(self.testlatticetype[0]['format'],v['latticeFormat'], ))
                self.assertEqual(v['latticeType'], self.testlatticetype[0]['name'], 
                                 'Expecting lattice type (%s) but got (%s)'%( self.testlatticetype[0]['name'],v['latticeType'],))
                self.assertEqual(v['creator'], self.creators[0], 
                                 'Expecting lattice created by (%s) but by (%s)'%(self.creators[0],v['creator'], ))
                self.assertEqual(v['updated'], self.creators[3], 
                                 'Expecting lattice updated by (%s) but by (%s)'%(self.creators[3],v['creator'], ))
        except Exception as e:
            print r.text
            # clean this lattice entry
            for i in range(len(self.name)):
                deletelattice(self.name[i], self.versions[i], self.branch[i])
            
            # clean latticetype
            cleanlatticetype(self.testlatticetype)
            raise e

        params={'function': 'retrieveLattice',
                'name': self.name[0],
                'version': self.versions[0],
                'branch': self.branch[0],
                'latticetype': json.dumps(self.testlatticetype[0]), 
                'withdata': True, 
                'rawdata': True}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        try:
            self.assertEqual(r.status_code, 200, 'Finish this method successfully.')
            result = r.json()
            self.assertTrue(len(result) == 1, 'Expecting one lattice, but got %s'%(len(result)))
            for _, v in result.iteritems():
                self.assertEqual(v['name'], self.name[0], 
                                 'Expecting lattice (%s) but got (%s)'%(self.name[0],v['name'], ))
                self.assertEqual(v['version'], self.versions[0], 
                                 'Expecting lattice version (%s) but got (%s)'%(self.versions[0],v['version'], ))
                self.assertEqual(v['branch'], self.branch[0], 
                                 'Expecting lattice branch (%s) but got (%s)'%(self.branch[0],v['branch'], ))
                self.assertEqual(v['description'], self.descs[0], 
                                 'Expecting description (%s) but got (%s)'%(self.descs[0],v['description'], ))
                self.assertEqual(v['latticeFormat'], self.testlatticetype[0]['format'], 
                                 'Expecting lattice format (%s) but got (%s)'%(self.testlatticetype[0]['format'],v['latticeFormat'], ))
                self.assertEqual(v['latticeType'], self.testlatticetype[0]['name'], 
                                 'Expecting lattice type (%s) but got (%s)'%( self.testlatticetype[0]['name'],v['latticeType'],))
                self.assertEqual(v['creator'], self.creators[0], 
                                 'Expecting lattice created by (%s) but by (%s)'%(self.creators[0],v['creator'], ))
                self.assertEqual(v['updated'], self.creators[3], 
                                 'Expecting lattice updated by (%s) but by (%s)'%(self.creators[3],v['creator'], ))
                self.assertEqual(v['lattice'], {}, 
                                 'Expecting lattice updated by (%s) but by (%s)'%(self.creators[3],v['creator'], ))
        except Exception as e:
            print r.text
            # clean this lattice entry
            for i in range(len(self.name)):
                deletelattice(self.name[i], self.versions[i], self.branch[i])
            
            # clean latticetype
            cleanlatticetype(self.testlatticetype)
            raise e

        # delete saved lattice entry
        deletelattice(self.name[0], self.versions[0], self.branch[0])
        
        # save with lattice type but no data
        for i in range(len(self.name)):
            payload = {'function': 'saveLattice',
                       'name': self.name[i],
                       'version': self.versions[i],
                       'branch': self.branch[i],
                       'creator': self.creators[i],
                       'description': self.descs[i],
                       'latticetype': json.dumps(self.testlatticetype[0])}
            r = self.client.post(self.__url, data=payload)
            self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)

        # save again with lattice type but no data
        # should get an error
        for i in range(len(self.name)):
            payload = {'function': 'saveLattice',
                       'name': self.name[i],
                       'version': self.versions[i],
                       'branch': self.branch[i],
                       'creator': self.creators[i],
                       'description': self.descs[i],
                       'latticetype': json.dumps(self.testlatticetype[0])}
            r = self.client.post(self.__url, data=payload)
            self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
            self.assertEqual(r.text,
                             'lattice (name: %s, version: %s, branch: %s) description information exists already. Please update it.'
                             %(self.name[i], self.versions[i], self.branch[i]),
                             'Wrong error message. Get:\n -- %s'%r.text)

        # update without data
        for i in range(len(self.name)):
            payload = {'function': 'updateLattice',
                       'name': self.name[i],
                       'version': self.versions[i],
                       'branch': self.branch[i],
                       'creator': self.creators[i],
                       'description': self.descs[i],
                       'latticetype': json.dumps(self.testlatticetype[4])}
            r = self.client.post(self.__url, data=payload)
            self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
            self.assertEqual(r.json(), {"result": True}, 'Failed to update lattice')
            
        params={'function': 'retrieveLattice',
                'name': "*"}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text,
                         'Parameters is missing for function %s'%(params['function']),
                         'Wrong error message. Get:\n -- %s'%r.text)
        params={'function': 'retrieveLattice',
                'name': "*",
                'version': "*",
                'branch': "*",}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        result = r.json()
        for _, v in result.iteritems():
            self.assertEqual(v['latticeType'],self.testlatticetype[4]['name'],
                             'Expecting lattice type (%s) but by (%s)'%(self.testlatticetype[4]['name'], v['latticeType']))
            self.assertEqual(v['latticeFormat'],self.testlatticetype[4]['format'],
                             'Expecting lattice format (%s) but by (%s)'%(self.testlatticetype[4]['format'], v['latticeFormat']))
        
        # update without data
        for i in range(len(self.name)):
            payload = {'function': 'updateLattice',
                       'name': self.name[i],
                       'version': self.versions[i],
                       'branch': self.branch[i],
                       'creator': self.creators[i],
                       'description': self.descs[i],
                       'latticetype': json.dumps(self.testlatticetype[0])}
            r = self.client.post(self.__url, data=payload)
            self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
            self.assertEqual(r.json(), {"result": True}, 'Failed to update lattice')
            
        params={'function': 'retrieveLattice',
                'name': "*",
                'version': "*",
                'branch': "*",}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        result = r.json()
        for _, v in result.iteritems():
            self.assertEqual(v['latticeType'],self.testlatticetype[0]['name'],
                             'Expecting lattice type (%s) but by (%s)'%(self.testlatticetype[0]['name'], v['latticeType']))
            self.assertEqual(v['latticeFormat'],self.testlatticetype[0]['format'],
                             'Expecting lattice format (%s) but by (%s)'%(self.testlatticetype[0]['format'], v['latticeFormat']))

        # update with empty data
        payload = {'function': 'updateLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[0],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text, 'No lattice data found.', 'Failed to update lattice')

        # update with empty data
        payload = {'function': 'updateLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[0],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.name[0],
                                          'data': None})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text, 'Lattice data is not complete.', 'Failed to update lattice')

        # update with wrong lattice head
        payload = {'function': 'updateLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[0],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.name[0],
                                          'data': self.wrongplainlat.splitlines()})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 404, 'Expecting 400 status code, but got %s'%r.status_code)
        self.assertEqual(r.text, 'Incomplete lattice data header.', 'Failed to update lattice')

        # update with data
        payload = {'function': 'updateLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[0],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.name[0],
                                          'data': self.plainlat1.splitlines()})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        self.assertEqual(r.json(), {"result": True}, 'Failed to update lattice')

        truncatelattice()
        # prepare an empty lattice entry
        payload = {'function': 'saveLattice',
                   'name': self.name[3],
                   'version': self.versions[3],
                   'branch': self.branch[3],
                   'creator': self.creators[3],
                   'description': self.descs[3],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Failed to save lattice. Expecting status code 200, but got %s.'%(r.status_code))

        # update lattice with kick map
        # a real NSLS II design lattice with insertion devices
        kmdict = {}
        for km in self.kickmap:
            kmfile="/".join((ROOT,km))
            with file(kmfile, 'r') as f:
                data = f.readlines()
            #kmdict[os.path.splitext(os.path.basename(kmfile))[0]] = data
            kmdict[os.path.basename(kmfile)] = data
        with file("/".join((ROOT,self.plainlat4)), 'r') as f:
            data = f.readlines()
        payload = {'function': 'updateLattice',
                   'name': self.name[3],
                   'version': self.versions[3],
                   'branch': self.branch[3],
                   'creator': self.creators[3],
                   'description': self.descs[3],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.name[3],
                                          'data': data,
                                          'map': kmdict})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Failed to save lattice. Expecting status code 200, but got %s.'%(r.status_code))

        # update a non-exist lattice
        payload = {'function': 'updateLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[0],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.name[0],
                                          'data': self.plainlat1.splitlines()})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text, 
                         'Cannot find lattice (name: %s, version: %s, branch: %s) information.'
                         %(self.name[0], self.versions[0], self.branch[0],), 
                         'Failed to update lattice')

        # save 1st example lattice
        payload = {'function': 'saveLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[0],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.name[0],
                                          'data': self.plainlat1.splitlines()})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Failed to save lattice. Expecting status code 200, but got %s.'%(r.status_code))
        
        # save 2nd example lattice
        payload = {'function': 'saveLattice',
                   'name': self.name[1],
                   'version': self.versions[1],
                   'branch': self.branch[1],
                   'creator': self.creators[1],
                   'description': self.descs[1],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.name[1],
                                          'data': self.plainlat2.splitlines()})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Failed to save lattice. Expecting status code 200, but got %s.'%(r.status_code))

        # save with flat file
        # a real NSLS II design lattice without insertion devices
        with file("/".join((ROOT,self.plainlat3)), 'r') as f:
            data = f.readlines()
        payload = {'function': 'saveLattice',
                   'name': self.name[2],
                   'version': self.versions[2],
                   'branch': self.branch[2],
                   'creator': self.creators[2],
                   'description': self.descs[2],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.name[2],
                                          'data': data})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Failed to save lattice. Expecting status code 200, but got %s.'%(r.status_code))

        # update existing lattice
        # should get an error
        payload = {'function': 'updateLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[0],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.name[0],
                                          'data': self.plainlat1.splitlines()})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 404, 'Expecting status code 404, but got %s.'%(r.status_code))
        self.assertEqual(r.text,
                         'Lattice geometric and strength is there already. Give up.',
                         'Expecting an error message. But got wrong:\n  -- %s'%(r.text))
        
        # retrieve without data
        params={'function': 'retrieveLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0]
        }
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
        result = r.json()
        self.assertEqual(len(result), 1, 'Should get only one lattice')
        for _, v in result.iteritems():
            self.assertEqual(self.testlatticetype[0]['name'], 
                             v["latticeType"],
                             'Expecting lattice type (%s), but got (%s)'
                             %(self.testlatticetype[0]['name'],  v["latticeType"]))
            self.assertEqual(self.testlatticetype[0]['format'], 
                             v["latticeFormat"],
                             'Expecting lattice format (%s), but got (%s)'
                             %(self.testlatticetype[0]['format'],  v["latticeFormat"]))
            self.assertEqual(self.name[0], 
                             v["name"],
                             'Expecting lattice name (%s), but got (%s)'
                             %(self.name[0],  v['name']))
            self.assertEqual(self.versions[0], 
                             v["version"],
                             'Expecting lattice version (%s), but got (%s)'
                             %(self.versions[0],  v['version']))
            self.assertEqual(self.branch[0], 
                             v["branch"],
                             'Expecting lattice branch (%s), but got (%s)'
                             %(self.branch[0],  v['branch']))
            self.assertEqual(self.creators[0], 
                             v["creator"],
                             'Expecting lattice created by (%s), but by (%s)'
                             %(self.creators[0], v["creator"]))
            self.assertEqual(self.descs[0], 
                             v["description"],
                             'Expecting lattice description (%s), but got (%s)'
                             %(self.descs[0], v["description"]))
        
        # retrieve without data with wrong version
        # should get nothing
        params={'function': 'retrieveLattice',
                   'name': self.name[0],
                   'version': self.versions[1],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[0],
        }
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
        self.assertEqual(r.json(), {}, 'Expecting status code 200, but got %s'%(r.status_code))

        # retrieve without data with wrong branch
        # should get nothing
        params={'function': 'retrieveLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[2],
                   'creator': self.creators[0],
                   'description': self.descs[0],
        }
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
        self.assertEqual(r.json(), {}, 'Expecting status code 200, but got %s'%(r.status_code))

        # retrieve without data with wrong description
        # should get nothing
        params={'function': 'retrieveLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[3],
        }
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
        self.assertEqual(r.json(), {}, 'Expecting status code 200, but got %s'%(r.status_code))

        # retrieve with data
        params={'function': 'retrieveLattice',
                   'name': self.name[0],
                   'version': self.versions[0],
                   'branch': self.branch[0],
                   'creator': self.creators[0],
                   'description': self.descs[0],
                   'withdata': True,
                   'rawdata': True,
        }
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
        lattice = r.json()
        self.assertEqual(len(lattice), 1, 'Expecting getting only one lattice, but got %s' %(len(lattice)))
        for _, v in lattice.iteritems():
            self.assertEqual(self.testlatticetype[0]['name'], 
                             v["latticeType"],
                             'Expecting lattice type (%s), but got (%s)'
                             %(self.testlatticetype[0]['name'],  v["latticeType"]))
            self.assertEqual(self.testlatticetype[0]['format'], 
                             v["latticeFormat"],
                             'Expecting lattice format (%s), but got (%s)'
                             %(self.testlatticetype[0]['format'],  v["latticeFormat"]))
            self.assertEqual(self.name[0], 
                             v["name"],
                             'Expecting lattice name (%s), but got (%s)'
                             %(self.name[0],  v['name']))
            self.assertEqual(self.versions[0], 
                             v["version"],
                             'Expecting lattice version (%s), but got (%s)'
                             %(self.versions[0],  v['version']))
            self.assertEqual(self.branch[0], 
                             v["branch"],
                             'Expecting lattice branch (%s), but got (%s)'
                             %(self.branch[0],  v['branch']))
            self.assertEqual(self.creators[0], 
                             v["creator"],
                             'Expecting lattice created by (%s), but by (%s)'
                             %(self.creators[0], v["creator"]))
            self.assertEqual(self.descs[0], 
                             v["description"],
                             'Expecting lattice description (%s), but got (%s)'
                             %(self.descs[0], v["description"]))
            rawdata = v['rawlattice']['data']
            databody = self.plainlat1.splitlines()
            for i in range(len(rawdata)):
                # raw data save in file is ended with line break
                self.assertEqual(rawdata[i][:-1], databody[i], 'wrong raw data')
            
            # elements length: one empty line + 3 header lines
            self.assertEqual(len(databody)-4, len(v['lattice'])-2, 'lattice elements do not match original one')
        # retrieve CD3 lattice without insertion device
        params={'function': 'retrieveLattice',
                   'name': self.name[2],
                   'version': self.versions[2],
                   'branch': self.branch[2],
                   'creator': self.creators[2],
                   'description': self.descs[2],
                   'withdata': True,
                   'rawdata': True,
        }
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
        lattice = r.json()
        self.assertEqual(len(lattice), 1, 'Expecting getting only one lattice, but got %s' %(len(lattice)))
        for _, v in lattice.iteritems():
            
            self.assertEqual(self.testlatticetype[0]['name'], 
                             v["latticeType"],
                             'Expecting lattice type (%s), but got (%s)'
                             %(self.testlatticetype[0]['name'],  v["latticeType"]))
            self.assertEqual(self.testlatticetype[0]['format'], 
                             v["latticeFormat"],
                             'Expecting lattice format (%s), but got (%s)'
                             %(self.testlatticetype[0]['format'],  v["latticeFormat"]))
            self.assertEqual(self.name[2], 
                             v["name"],
                             'Expecting lattice name (%s), but got (%s)'
                             %(self.name[2],  v['name']))
            self.assertEqual(self.versions[2], 
                             v["version"],
                             'Expecting lattice version (%s), but got (%s)'
                             %(self.versions[2],  v['version']))
            self.assertEqual(self.branch[2], 
                             v["branch"],
                             'Expecting lattice branch (%s), but got (%s)'
                             %(self.branch[2],  v['branch']))
            self.assertEqual(self.creators[2], 
                             v["creator"],
                             'Expecting lattice created by (%s), but by (%s)'
                             %(self.creators[2], v["creator"]))
            self.assertEqual(self.descs[2], 
                             v["description"],
                             'Expecting lattice description (%s), but got (%s)'
                             %(self.descs[2], v["description"]))
            rawdata = v['rawlattice']['data']
            with file("/".join((ROOT,self.plainlat3)), 'r') as f:
                databody = f.readlines()
            for i in range(len(rawdata)):
                self.assertEqual(rawdata[i], databody[i], 'wrong raw data')
            self.assertEqual(len(databody)-3, len(v['lattice'])-2, 'lattice elements do not match original one')        

        # retrieve CD3 lattice with insertion device
        params={'function': 'retrieveLattice',
                   'name': self.name[3],
                   'version': self.versions[3],
                   'branch': self.branch[3],
                   'creator': self.creators[3],
                   'description': self.descs[3],
                   'withdata': True,
                   'rawdata': True,
        }
        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
        lattice = r.json()
        self.assertEqual(len(lattice), 1, 'Expecting getting only one lattice, but got %s' %(len(lattice)))
        for _, v in lattice.iteritems():
            self.assertEqual(self.testlatticetype[0]['name'], 
                             v["latticeType"],
                             'Expecting lattice type (%s), but got (%s)'
                             %(self.testlatticetype[0]['name'],  v["latticeType"]))
            self.assertEqual(self.testlatticetype[0]['format'], 
                             v["latticeFormat"],
                             'Expecting lattice format (%s), but got (%s)'
                             %(self.testlatticetype[0]['format'],  v["latticeFormat"]))
            self.assertEqual(self.name[3], 
                             v["name"],
                             'Expecting lattice name (%s), but got (%s)'
                             %(self.name[3],  v['name']))
            self.assertEqual(self.versions[3], 
                             v["version"],
                             'Expecting lattice version (%s), but got (%s)'
                             %(self.versions[3],  v['version']))
            self.assertEqual(self.branch[3], 
                             v["branch"],
                             'Expecting lattice branch (%s), but got (%s)'
                             %(self.branch[3],  v['branch']))
            self.assertEqual(self.creators[3], 
                             v["creator"],
                             'Expecting lattice created by (%s), but by (%s)'
                             %(self.creators[3], v["creator"]))
            self.assertEqual(self.descs[3], 
                             v["description"],
                             'Expecting lattice description (%s), but got (%s)'
                             %(self.descs[3], v["description"]))
            rawdata = v['rawlattice']['data']
            with file("/".join((ROOT,self.plainlat4)), 'r') as f:
                databody = f.readlines()
            for i in range(len(rawdata)):
                self.assertEqual(rawdata[i], databody[i], 'wrong raw data')
            self.assertEqual(len(databody)-3, len(v['lattice'])-2, 'lattice elements do not match original one')            
            fieldmap=v['map']
            self.assertTrue(len(self.kickmap) == len(fieldmap), 'Wrong kick map files')
            for km in self.kickmap:
                kmfile="/".join((ROOT,km))
                with file(kmfile, 'r') as f:
                    data = f.readlines()
                serverdata = fieldmap[os.path.basename(kmfile)]
                for i in range(len(data)):
                    self.assertEqual(serverdata[i], data[i], 'kick map data does not match.')
            
        # clean whole lattice domain
        truncatelattice()

class TestTracyLattice(unittest.TestCase):
    __url = 'http://localhost:8000/lattice/'
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}

    testlat1 = {'name': 'CD3-Oct3-12-30Cell-addID-par',
                'version': 20121003,
                'branch': 'Design',
                'lattice': {'name': CD3ParID['name'],
                            'data': CD3ParID['data'],
                            'map':  CD3ParID['map'],
                            'raw': 'examplelattice/CD3-Oct3-12-30Cell-addID-par.lat',
                            },
                'creator': 'Guobao',
                'description': 'This is a CD3 design lattice released on Oct 3rd, 2012'
                }
    

    testlat2 = {'name': 'CD3-Apr07-10-30cell-par',
                'version': 20100407,
                'branch': 'Design',
                'lattice': {'name': CD3Par['name'],
                            'data': CD3Par['data'],
                            'map':  CD3Par['map'],
                            'raw': 'examplelattice/CD3-Apr07-10-30cell-par.lat',
                            },
                'creator': 'Guobao',
                'description': 'This is a CD3 design lattice released on Apr 7th, 2010'
                }
    
    testlatticetype = [{'name': 'tracy3',  'format': 'lat'},
                       {'name': 'tracy4',  'format': 'lat'},
                       ]
    def setUp(self):
        try:
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
            self.client = requests.session()
        except:
            raise

    def tearDown(self):
        self.client.close()

    def testTracyLattice(self):
        '''
        '''
        truncatelattice()
        # clean lattice type
        cleanlatticetype(self.testlatticetype)
        # save a lattice that its type is not defined yet.
        payload = {'function': 'saveLattice',
                   'name': self.testlat1['name'],
                   'version': self.testlat1['version'],
                   'branch': self.testlat1['branch'],
                   'creator': self.testlat1['creator'],
                   'description': self.testlat1['description'],
                   'latticetype': json.dumps(self.testlatticetype[0])}
        r = self.client.post(self.__url, data=payload)
        # should raise an exception since lattice type/format is not there yet.
        self.assertRaises(requests.exceptions.HTTPError, r.raise_for_status)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text, 
                         'Does not support lattice type (%s) with given format (%s).'%(self.testlatticetype[0]['name'],
                                                                                      self.testlatticetype[0]['format']),
                         'Wrong error message. Get \n -- %s'%r.text)

        # prepare lattice type
        for testlt in self.testlatticetype:
            payload={'function': 'saveLatticeType',
                     'name': testlt['name'],
                     'format': testlt['format']}
            r = self.client.post(self.__url, data=payload)
            self.assertEqual(r.status_code, 200, 'Should save successfully.')
        
        # save without lattice type & data
        payload = {'function': 'saveLattice',
                   'name': self.testlat1['name'],
                   'version': self.testlat1['version'],
                   'branch': self.testlat1['branch'],
                   'creator': self.testlat1['creator'],
                   'description': self.testlat1['description']
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        
        # retrieve lattice info which is just saved.
        params={'function': 'retrieveLattice',
                'name': self.testlat1['name'],
                'version': self.testlat1['version'],
                'branch': self.testlat1['branch'],
                'creator': self.testlat1['creator'],
                'description': self.testlat1['description'],
                'withdata': False, 
                'rawdata': False}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        try:
            self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
            result = r.json()
            for _, v in result.iteritems():
                self.assertEqual(self.testlat1['name'], v[u'name'], 
                                 'Expecting lattice name (%s), but got (%s)'%(self.testlat1['name'], v['name']))
                self.assertEqual(self.testlat1['version'], v[u'version'], 
                                 'Expecting lattice version (%s), but got (%s)'%(self.testlat1['version'], v['version']))
                self.assertEqual(self.testlat1['branch'], v[u'branch'], 
                                 'Expecting lattice branch (%s), but got (%s)'%(self.testlat1['branch'], v['branch']))
                self.assertEqual(self.testlat1['creator'], v[u'creator'], 
                                 'Expecting lattice creator (%s), but got (%s)'%(self.testlat1['creator'], v['creator']))
                self.assertEqual(self.testlat1['description'], v[u'description'], 
                                 'Expecting lattice description (%s), but got (%s)'%(self.testlat1['description'], v['description']))
        except Exception as e:
            # clean this lattice entry
            deletelattice(self.testlat1['name'],self.testlat1['version'],self.testlat1['branch'])
            
            # clean latticetype
            cleanlatticetype(self.testlatticetype)
            raise e

        # retrieve lattice info which is just saved, but wrong description.
        params={'function': 'retrieveLattice',
                'name': self.testlat1['name'],
                'version': self.testlat1['version'],
                'branch': self.testlat1['branch'],
                'creator': self.testlat1['creator'],
                'description': self.testlat2['description'],
                'withdata': False, 
                'rawdata': False}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Finish this method successfully.')
        self.assertEqual(r.json(), {}, "Should get an empty result")
        
        # retrieve lattice info which is just saved, but mismatched lattice type.
        params={'function': 'retrieveLattice',
                'name': self.testlat1['name'],
                'version': self.testlat1['version'],
                'branch': self.testlat1['branch'],
                'creator': self.testlat1['creator'],
                'description': self.testlat1['description'],
                'latticetype': json.dumps(self.testlatticetype[1]), 
                'withdata': False, 
                'rawdata': False}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        try:
            self.assertEqual(r.status_code, 200, 'Finish this method successfully.')
            self.assertEqual(r.json(), {}, "Should get an empty result")
        except Exception as e:
            # clean this lattice entry
            deletelattice(self.testlat1['name'],self.testlat1['version'],self.testlat1['branch'])
            
            # clean latticetype
            cleanlatticetype(self.testlatticetype)
            raise e

        # prepare lattice type
        cleanlatticetype(self.testlatticetype)
        for testlt in self.testlatticetype:
            payload={'function': 'saveLatticeType',
                     'name': testlt['name'],
                     'format': testlt['format']}
            r = self.client.post(self.__url, data=payload)
            self.assertEqual(r.status_code, 200, 'Should save successfully.')
        # update lattice, adding lattice type information.
        payload={'function': 'updateLattice',
                 'name': self.testlat1['name'],
                 'version': self.testlat1['version'],
                 'branch': self.testlat1['branch'],
                 'creator': self.testlat1['creator'],
                 'description': self.testlat1['description'],
                 'latticetype': json.dumps(self.testlatticetype[1]), 
                 }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
        self.assertTrue(r.json()=={'result':True}, 'Expecting updating successfully.')

        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        try:
            self.assertEqual(r.status_code, 200, 'Finish this method successfully.')
            result = r.json()
            self.assertTrue(len(result) == 1, 'Expecting one lattice, but got %s'%(len(result)))
            for _, v in result.iteritems():
                self.assertEqual(v['name'], self.testlat1['name'], 
                                 'Expecting lattice (%s) but got (%s)'%(self.testlat1['name'],v['name'], ))
                self.assertEqual(int(v['version']), self.testlat1['version'], 
                                 'Expecting lattice version (%s) but got (%s)'%(self.testlat1['version'],v['version'], ))
                self.assertEqual(v['branch'], self.testlat1['branch'], 
                                 'Expecting lattice branch (%s) but got (%s)'%(self.testlat1['branch'],v['branch'], ))
                self.assertEqual(v['description'], self.testlat1['description'], 
                                 'Expecting lattice description (%s) but got (%s)'%(self.testlat1['description'],v['description'], ))
                self.assertEqual(v['latticeFormat'], self.testlatticetype[1]['format'], 
                                 'Expecting lattice format (%s) but got (%s)'%(self.testlatticetype[1]['format'],v['latticeFormat'], ))
                self.assertEqual(v['latticeType'], self.testlatticetype[1]['name'], 
                                 'Expecting lattice type (%s) but got (%s)'%( self.testlatticetype[1]['name'],v['latticeType'],))
                self.assertEqual(v['creator'], self.testlat1['creator'], 
                                 'Expecting lattice created by (%s) but by (%s)'%(self.testlat1['creator'],v['creator'], ))
        except Exception as e:
            # clean this lattice entry
            deletelattice(self.testlat1['name'],self.testlat1['version'],self.testlat1['branch'])
            
            # clean latticetype
            cleanlatticetype(self.testlatticetype)
            raise e

        # delete saved lattice entry
        deletelattice(self.testlat1['name'],self.testlat1['version'],self.testlat1['branch'])
        
        # save with lattice type but no data
        # save 1st test lattice
        payload = {'function': 'saveLattice',
                 'name': self.testlat1['name'],
                 'version': self.testlat1['version'],
                 'branch': self.testlat1['branch'],
                 'creator': self.testlat1['creator'],
                 'description': self.testlat1['description'],
                 'latticetype': json.dumps(self.testlatticetype[0]),}
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        # save 1st test lattice
        payload = {'function': 'saveLattice',
                 'name': self.testlat2['name'],
                 'version': self.testlat2['version'],
                 'branch': self.testlat2['branch'],
                 'creator': self.testlat2['creator'],
                 'description': self.testlat2['description'],
                 'latticetype': json.dumps(self.testlatticetype[1]),}
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)

        # save again with lattice type but no data
        # should get an error
        payload = {'function': 'saveLattice',
                 'name': self.testlat1['name'],
                 'version': self.testlat1['version'],
                 'branch': self.testlat1['branch'],
                 'creator': self.testlat1['creator'],
                 'description': self.testlat1['description'],
                 'latticetype': json.dumps(self.testlatticetype[0]),}
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text,
                         'lattice (name: %s, version: %s, branch: %s) description information exists already. Please update it.'
                         %(self.testlat1['name'], self.testlat1['version'], self.testlat1['branch']),
                         'Wrong error message. Get:\n -- %s'%r.text)
        payload = {'function': 'saveLattice',
                 'name': self.testlat2['name'],
                 'version': self.testlat2['version'],
                 'branch': self.testlat2['branch'],
                 'creator': self.testlat2['creator'],
                 'description': self.testlat2['description'],
                 'latticetype': json.dumps(self.testlatticetype[1]),}
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text,
                         'lattice (name: %s, version: %s, branch: %s) description information exists already. Please update it.'
                         %(self.testlat2['name'], self.testlat2['version'], self.testlat2['branch']),
                         'Wrong error message. Get:\n -- %s'%r.text)

        # update without data
        payload = {'function': 'updateLattice',
                 'name': self.testlat1['name'],
                 'version': self.testlat1['version'],
                 'branch': self.testlat1['branch'],
                 'creator': self.testlat1['creator'],
                 'description': self.testlat1['description'],
                 'latticetype': json.dumps(self.testlatticetype[1]),}
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        self.assertEqual(r.json(), {"result": True}, 'Failed to update lattice')
        payload = {'function': 'updateLattice',
                 'name': self.testlat2['name'],
                 'version': self.testlat2['version'],
                 'branch': self.testlat2['branch'],
                 'creator': self.testlat2['creator'],
                 'description': self.testlat2['description'],
                 'latticetype': json.dumps(self.testlatticetype[1]),}
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        self.assertEqual(r.json(), {"result": True}, 'Failed to update lattice')
                
        # retrieve lattice
        # with incomplete parameters
        params={'function': 'retrieveLattice',
                'name': "*"}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text,
                         'Parameters is missing for function %s'%(params['function']),
                         'Wrong error message. Get:\n -- %s'%r.text)
        # should get all lattice
        params={'function': 'retrieveLattice',
                'name': "*",
                'version': "*",
                'branch': "*",}
        r = self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        result = r.json()
        for _, v in result.iteritems():
            self.assertEqual(v['latticeType'],self.testlatticetype[1]['name'],
                             'Expecting lattice type (%s) but by (%s)'%(self.testlatticetype[1]['name'], v['latticeType']))
            self.assertEqual(v['latticeFormat'],self.testlatticetype[1]['format'],
                             'Expecting lattice format (%s) but by (%s)'%(self.testlatticetype[1]['format'], v['latticeFormat']))
        
        # update without data
        payload = {'function': 'updateLattice',
                 'name': self.testlat1['name'],
                 'version': self.testlat1['version'],
                 'branch': self.testlat1['branch'],
                 'creator': self.testlat1['creator'],
                 'description': self.testlat1['description'],
                 'latticetype': json.dumps(self.testlatticetype[0]),}
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        self.assertEqual(r.json(), {"result": True}, 'Failed to update lattice')
        payload = {'function': 'updateLattice',
                 'name': self.testlat2['name'],
                 'version': self.testlat2['version'],
                 'branch': self.testlat2['branch'],
                 'creator': self.testlat2['creator'],
                 'description': self.testlat2['description'],
                 'latticetype': json.dumps(self.testlatticetype[1]),}
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        self.assertEqual(r.json(), {"result": True}, 'Failed to update lattice')

        # update with empty data
        payload = {'function': 'updateLattice',
                   'name': self.testlat1['name'],
                   'version': self.testlat1['version'],
                   'branch': self.testlat1['branch'],
                   'creator': self.testlat1['creator'],
                   'description': self.testlat1['description'],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text, 'No lattice data found.', 'Failed to update lattice')

        # update with empty data
        payload = {'function': 'updateLattice',
                   'name': self.testlat1['name'],
                   'version': self.testlat1['version'],
                   'branch': self.testlat1['branch'],
                   'creator': self.testlat1['creator'],
                   'description': self.testlat1['description'],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.testlat1['name'],
                                          'data': None})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
        self.assertEqual(r.text, 'No lattice data found.', 'Failed to update lattice')

        # update with wrong lattice head
        payload = {'function': 'updateLattice',
                   'name': self.testlat1['name'],
                   'version': self.testlat1['version'],
                   'branch': self.testlat1['branch'],
                   'creator': self.testlat1['creator'],
                   'description': self.testlat1['description'],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.testlat1['lattice']['name'],
                                          'data': self.testlat1['lattice']['data'],
                                          'map': self.testlat2['lattice']['map'],})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 404, 'Expecting 400 status code, but got %s'%r.status_code)
        self.assertEqual(r.text, 'Cannot save field map files since raw lattice is missing.', 'Failed to update lattice')

        # update with data
        payload = {'function': 'updateLattice',
                   'name': self.testlat1['name'],
                   'version': self.testlat1['version'],
                   'branch': self.testlat1['branch'],
                   'creator': self.testlat1['creator'],
                   'description': self.testlat1['description'],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.testlat1['lattice']['name'],
                                          'data': self.testlat1['lattice']['data']})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Expecting 200 status code, but got %s'%r.status_code)
        self.assertEqual(r.json(), {"result": True}, 'Failed to update lattice')

        truncatelattice()
        # prepare an empty lattice entry
        payload = {'function': 'saveLattice',
                   'name': self.testlat1['name'],
                   'version': self.testlat1['version'],
                   'branch': self.testlat1['branch'],
                   'creator': self.testlat1['creator'],
                   'description': self.testlat1['description'],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Failed to save lattice. Expecting status code 200, but got %s.'%(r.status_code))

        # update lattice with kick map
        # a real NSLS II design lattice with insertion devices
        rawlat = self.testlat1['lattice']['raw']
        rawlatfile="/".join((ROOT,rawlat))
        with file(rawlatfile, 'r') as f:
            rawdata = f.readlines()
        
        kmdict = {}
        kmroot = os.path.dirname(rawlatfile)
        for km in self.testlat1['lattice']['map']:
            kmfile="/".join((kmroot,km))
            with file(kmfile, 'r') as f:
                data = f.readlines()
            kmdict[os.path.basename(kmfile)] = data
        payload = {'function': 'updateLattice',
                   'name': self.testlat1['name'],
                   'version': self.testlat1['version'],
                   'branch': self.testlat1['branch'],
                   'creator': self.testlat1['creator'],
                   'description': self.testlat1['description'],
                   'latticetype': json.dumps(self.testlatticetype[0]),
                   'lattice': json.dumps({'name': self.testlat1['lattice']['name'],
                                          'data': self.testlat1['lattice']['data'],
                                          'map': kmdict,
                                          'raw': rawdata})
                   }
        r = self.client.post(self.__url, data=payload)
        self.assertEqual(r.status_code, 200, 'Failed to save lattice. Expecting status code 200, but got %s.'%(r.status_code))
#
#        # update a non-exist lattice
#        payload = {'function': 'updateLattice',
#                   'name': self.name[0],
#                   'version': self.versions[0],
#                   'branch': self.branch[0],
#                   'creator': self.creators[0],
#                   'description': self.descs[0],
#                   'latticetype': json.dumps(self.testlatticetype[0]),
#                   'lattice': json.dumps({'name': self.name[0],
#                                          'data': self.plainlat1.splitlines()})
#                   }
#        r = self.client.post(self.__url, data=payload)
#        self.assertEqual(r.status_code, 404, 'Expecting 404 status code, but got %s'%r.status_code)
#        self.assertEqual(r.text, 
#                         'Cannot find lattice (name: %s, version: %s, branch: %s) information.'
#                         %(self.name[0], self.versions[0], self.branch[0],), 
#                         'Failed to update lattice')
#
#        # save 1st example lattice
#        payload = {'function': 'saveLattice',
#                   'name': self.name[0],
#                   'version': self.versions[0],
#                   'branch': self.branch[0],
#                   'creator': self.creators[0],
#                   'description': self.descs[0],
#                   'latticetype': json.dumps(self.testlatticetype[0]),
#                   'lattice': json.dumps({'name': self.name[0],
#                                          'data': self.plainlat1.splitlines()})
#                   }
#        r = self.client.post(self.__url, data=payload)
#        self.assertEqual(r.status_code, 200, 'Failed to save lattice. Expecting status code 200, but got %s.'%(r.status_code))
#        
#        # save 2nd example lattice
#        payload = {'function': 'saveLattice',
#                   'name': self.name[1],
#                   'version': self.versions[1],
#                   'branch': self.branch[1],
#                   'creator': self.creators[1],
#                   'description': self.descs[1],
#                   'latticetype': json.dumps(self.testlatticetype[0]),
#                   'lattice': json.dumps({'name': self.name[1],
#                                          'data': self.plainlat2.splitlines()})
#                   }
#        r = self.client.post(self.__url, data=payload)
#        self.assertEqual(r.status_code, 200, 'Failed to save lattice. Expecting status code 200, but got %s.'%(r.status_code))
#
#        # save with flat file
#        # a real NSLS II design lattice without insertion devices
#        with file("/".join((ROOT,self.plainlat3)), 'r') as f:
#            data = f.readlines()
#        payload = {'function': 'saveLattice',
#                   'name': self.name[2],
#                   'version': self.versions[2],
#                   'branch': self.branch[2],
#                   'creator': self.creators[2],
#                   'description': self.descs[2],
#                   'latticetype': json.dumps(self.testlatticetype[0]),
#                   'lattice': json.dumps({'name': self.name[2],
#                                          'data': data})
#                   }
#        r = self.client.post(self.__url, data=payload)
#        self.assertEqual(r.status_code, 200, 'Failed to save lattice. Expecting status code 200, but got %s.'%(r.status_code))
#
#        # update existing lattice
#        # should get an error
#        payload = {'function': 'updateLattice',
#                   'name': self.name[0],
#                   'version': self.versions[0],
#                   'branch': self.branch[0],
#                   'creator': self.creators[0],
#                   'description': self.descs[0],
#                   'latticetype': json.dumps(self.testlatticetype[0]),
#                   'lattice': json.dumps({'name': self.name[0],
#                                          'data': self.plainlat1.splitlines()})
#                   }
#        r = self.client.post(self.__url, data=payload)
#        self.assertEqual(r.status_code, 404, 'Expecting status code 404, but got %s.'%(r.status_code))
#        self.assertEqual(r.text,
#                         'Lattice geometric and strength is there already. Give up.',
#                         'Expecting an error message. But got wrong:\n  -- %s'%(r.text))
#        
#        # retrieve without data
#        params={'function': 'retrieveLattice',
#                   'name': self.name[0],
#                   'version': self.versions[0],
#                   'branch': self.branch[0],
#                   'creator': self.creators[0]
#        }
#        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
#        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
#        result = r.json()
#        self.assertEqual(len(result), 1, 'Should get only one lattice')
#        for _, v in result.iteritems():
#            self.assertEqual(self.testlatticetype[0]['name'], 
#                             v["latticeType"],
#                             'Expecting lattice type (%s), but got (%s)'
#                             %(self.testlatticetype[0]['name'],  v["latticeType"]))
#            self.assertEqual(self.testlatticetype[0]['format'], 
#                             v["latticeFormat"],
#                             'Expecting lattice format (%s), but got (%s)'
#                             %(self.testlatticetype[0]['format'],  v["latticeFormat"]))
#            self.assertEqual(self.name[0], 
#                             v["name"],
#                             'Expecting lattice name (%s), but got (%s)'
#                             %(self.name[0],  v['name']))
#            self.assertEqual(self.versions[0], 
#                             v["version"],
#                             'Expecting lattice version (%s), but got (%s)'
#                             %(self.versions[0],  v['version']))
#            self.assertEqual(self.branch[0], 
#                             v["branch"],
#                             'Expecting lattice branch (%s), but got (%s)'
#                             %(self.branch[0],  v['branch']))
#            self.assertEqual(self.creators[0], 
#                             v["creator"],
#                             'Expecting lattice created by (%s), but by (%s)'
#                             %(self.creators[0], v["creator"]))
#            self.assertEqual(self.descs[0], 
#                             v["description"],
#                             'Expecting lattice description (%s), but got (%s)'
#                             %(self.descs[0], v["description"]))
#        
#        # retrieve without data with wrong version
#        # should get nothing
#        params={'function': 'retrieveLattice',
#                   'name': self.name[0],
#                   'version': self.versions[1],
#                   'branch': self.branch[0],
#                   'creator': self.creators[0],
#                   'description': self.descs[0],
#        }
#        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
#        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
#        self.assertEqual(r.json(), {}, 'Expecting status code 200, but got %s'%(r.status_code))
#
#        # retrieve without data with wrong branch
#        # should get nothing
#        params={'function': 'retrieveLattice',
#                   'name': self.name[0],
#                   'version': self.versions[0],
#                   'branch': self.branch[2],
#                   'creator': self.creators[0],
#                   'description': self.descs[0],
#        }
#        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
#        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
#        self.assertEqual(r.json(), {}, 'Expecting status code 200, but got %s'%(r.status_code))
#
#        # retrieve without data with wrong description
#        # should get nothing
#        params={'function': 'retrieveLattice',
#                   'name': self.name[0],
#                   'version': self.versions[0],
#                   'branch': self.branch[0],
#                   'creator': self.creators[0],
#                   'description': self.descs[3],
#        }
#        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
#        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
#        self.assertEqual(r.json(), {}, 'Expecting status code 200, but got %s'%(r.status_code))
#
#        # retrieve with data
#        params={'function': 'retrieveLattice',
#                   'name': self.name[0],
#                   'version': self.versions[0],
#                   'branch': self.branch[0],
#                   'creator': self.creators[0],
#                   'description': self.descs[0],
#                   'withdata': True,
#                   'rawdata': True,
#        }
#        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
#        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
#        lattice = r.json()
#        self.assertEqual(len(lattice), 1, 'Expecting getting only one lattice, but got %s' %(len(lattice)))
#        for _, v in lattice.iteritems():
#            self.assertEqual(self.testlatticetype[0]['name'], 
#                             v["latticeType"],
#                             'Expecting lattice type (%s), but got (%s)'
#                             %(self.testlatticetype[0]['name'],  v["latticeType"]))
#            self.assertEqual(self.testlatticetype[0]['format'], 
#                             v["latticeFormat"],
#                             'Expecting lattice format (%s), but got (%s)'
#                             %(self.testlatticetype[0]['format'],  v["latticeFormat"]))
#            self.assertEqual(self.name[0], 
#                             v["name"],
#                             'Expecting lattice name (%s), but got (%s)'
#                             %(self.name[0],  v['name']))
#            self.assertEqual(self.versions[0], 
#                             v["version"],
#                             'Expecting lattice version (%s), but got (%s)'
#                             %(self.versions[0],  v['version']))
#            self.assertEqual(self.branch[0], 
#                             v["branch"],
#                             'Expecting lattice branch (%s), but got (%s)'
#                             %(self.branch[0],  v['branch']))
#            self.assertEqual(self.creators[0], 
#                             v["creator"],
#                             'Expecting lattice created by (%s), but by (%s)'
#                             %(self.creators[0], v["creator"]))
#            self.assertEqual(self.descs[0], 
#                             v["description"],
#                             'Expecting lattice description (%s), but got (%s)'
#                             %(self.descs[0], v["description"]))
#            rawdata = v['rawlattice']['data']
#            databody = self.plainlat1.splitlines()
#            for i in range(len(rawdata)):
#                # raw data save in file is ended with line break
#                self.assertEqual(rawdata[i][:-1], databody[i], 'wrong raw data')
#            
#            # elements length: one empty line + 3 header lines
#            self.assertEqual(len(databody)-4, len(v['lattice'])-2, 'lattice elements do not match original one')
#        # retrieve CD3 lattice without insertion device
#        params={'function': 'retrieveLattice',
#                   'name': self.name[2],
#                   'version': self.versions[2],
#                   'branch': self.branch[2],
#                   'creator': self.creators[2],
#                   'description': self.descs[2],
#                   'withdata': True,
#                   'rawdata': True,
#        }
#        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
#        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
#        lattice = r.json()
#        self.assertEqual(len(lattice), 1, 'Expecting getting only one lattice, but got %s' %(len(lattice)))
#        for _, v in lattice.iteritems():
#            
#            self.assertEqual(self.testlatticetype[0]['name'], 
#                             v["latticeType"],
#                             'Expecting lattice type (%s), but got (%s)'
#                             %(self.testlatticetype[0]['name'],  v["latticeType"]))
#            self.assertEqual(self.testlatticetype[0]['format'], 
#                             v["latticeFormat"],
#                             'Expecting lattice format (%s), but got (%s)'
#                             %(self.testlatticetype[0]['format'],  v["latticeFormat"]))
#            self.assertEqual(self.name[2], 
#                             v["name"],
#                             'Expecting lattice name (%s), but got (%s)'
#                             %(self.name[2],  v['name']))
#            self.assertEqual(self.versions[2], 
#                             v["version"],
#                             'Expecting lattice version (%s), but got (%s)'
#                             %(self.versions[2],  v['version']))
#            self.assertEqual(self.branch[2], 
#                             v["branch"],
#                             'Expecting lattice branch (%s), but got (%s)'
#                             %(self.branch[2],  v['branch']))
#            self.assertEqual(self.creators[2], 
#                             v["creator"],
#                             'Expecting lattice created by (%s), but by (%s)'
#                             %(self.creators[2], v["creator"]))
#            self.assertEqual(self.descs[2], 
#                             v["description"],
#                             'Expecting lattice description (%s), but got (%s)'
#                             %(self.descs[2], v["description"]))
#            rawdata = v['rawlattice']['data']
#            with file("/".join((ROOT,self.plainlat3)), 'r') as f:
#                databody = f.readlines()
#            for i in range(len(rawdata)):
#                self.assertEqual(rawdata[i], databody[i], 'wrong raw data')
#            self.assertEqual(len(databody)-3, len(v['lattice'])-2, 'lattice elements do not match original one')        
#
#        # retrieve CD3 lattice with insertion device
#        params={'function': 'retrieveLattice',
#                   'name': self.name[3],
#                   'version': self.versions[3],
#                   'branch': self.branch[3],
#                   'creator': self.creators[3],
#                   'description': self.descs[3],
#                   'withdata': True,
#                   'rawdata': True,
#        }
#        r=self.client.get(self.__url, params=params, verify=False, headers=self.__jsonheader)
#        self.assertEqual(r.status_code, 200, 'Expecting status code 200, but got %s'%(r.status_code))
#        lattice = r.json()
#        self.assertEqual(len(lattice), 1, 'Expecting getting only one lattice, but got %s' %(len(lattice)))
#        for _, v in lattice.iteritems():
#            self.assertEqual(self.testlatticetype[0]['name'], 
#                             v["latticeType"],
#                             'Expecting lattice type (%s), but got (%s)'
#                             %(self.testlatticetype[0]['name'],  v["latticeType"]))
#            self.assertEqual(self.testlatticetype[0]['format'], 
#                             v["latticeFormat"],
#                             'Expecting lattice format (%s), but got (%s)'
#                             %(self.testlatticetype[0]['format'],  v["latticeFormat"]))
#            self.assertEqual(self.name[3], 
#                             v["name"],
#                             'Expecting lattice name (%s), but got (%s)'
#                             %(self.name[3],  v['name']))
#            self.assertEqual(self.versions[3], 
#                             v["version"],
#                             'Expecting lattice version (%s), but got (%s)'
#                             %(self.versions[3],  v['version']))
#            self.assertEqual(self.branch[3], 
#                             v["branch"],
#                             'Expecting lattice branch (%s), but got (%s)'
#                             %(self.branch[3],  v['branch']))
#            self.assertEqual(self.creators[3], 
#                             v["creator"],
#                             'Expecting lattice created by (%s), but by (%s)'
#                             %(self.creators[3], v["creator"]))
#            self.assertEqual(self.descs[3], 
#                             v["description"],
#                             'Expecting lattice description (%s), but got (%s)'
#                             %(self.descs[3], v["description"]))
#            rawdata = v['rawlattice']['data']
#            with file("/".join((ROOT,self.plainlat4)), 'r') as f:
#                databody = f.readlines()
#            for i in range(len(rawdata)):
#                self.assertEqual(rawdata[i], databody[i], 'wrong raw data')
#            self.assertEqual(len(databody)-3, len(v['lattice'])-2, 'lattice elements do not match original one')            
#            fieldmap=v['map']
#            self.assertTrue(len(self.kickmap) == len(fieldmap), 'Wrong kick map files')
#            for km in self.kickmap:
#                kmfile="/".join((ROOT,km))
#                with file(kmfile, 'r') as f:
#                    data = f.readlines()
#                serverdata = fieldmap[os.path.basename(kmfile)]
#                for i in range(len(data)):
#                    self.assertEqual(serverdata[i], data[i], 'kick map data does not match.')
            
        # clean whole lattice domain
        truncatelattice()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()