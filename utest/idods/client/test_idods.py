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
        
        # Clean inventory property
        cleanInventoryProperty('name', 'alpha')
        cleanInventoryProperty('name2', 'alpha')
        
        # Clean inventory
        cleanInventory(['name', 'name2'])
        
        # Clean vendor table
        cleanVendor(['test vendor'])
        
        # Clean inventory property template table
        cleanInventoryPropertyTemplate(['alpha', 'beta'])
        
        # Clean component type property
        cleanComponentTypeProperty('Magnet', 'length')
        
        # Clean component type property type
        cleanComponentTypePropertyType(['length', 'width'])
        
        # Clean if there is something left from previous runs
        cleanComponentType(['test cmpnt', 'test cmpnt2','test cmpnt3', 'test cmpnt4','Magnet'])

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

    '''
    Test saving, retrieving and updating vendor
    '''
    def testVendor(self):
        
        # Save new vendor
        url = 'http://localhost:8000/id/device/savevendor/'
        
        # Set parameters
        params={
            'name': 'test vendor',
            'description': 'desc'
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Try to retrieve vendor
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
        
        # Try to update vendor
        url = 'http://localhost:8000/id/device/updatevendor/'
        
        # Set parameters
        params={
            'old_name': 'test vendor',
            'name': 'test vendor',
            'description': 'desc2'
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Try to retrieve vendor
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

    '''
    Test saving, retrieving and updating component type
    '''
    def testCmpntType(self):
        
        # Prepare component type property type
        url = 'http://localhost:8000/id/device/savecmpnttypeproptype/'
        r=self.client.post(url, data={'name': 'length', 'description': 'desc'})
        r.raise_for_status()
        
        # Save new component type
        url = 'http://localhost:8000/id/device/savecmpnttype/'
        
        # Set parameters
        params={
            'name': 'Magnet',
            'description': 'desc',
            'props': json.dumps({'length': '123'})
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Try to retrieve component type
        url = 'http://localhost:8000/id/device/cmpnttype/'
        r=self.client.get(url, params={'name': 'Mag*'}, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        existing = len(result)
        
        # Test the number of component types
        self.assertEqual(existing, 1, 'There should be one item in the database!')
        
        # Test returned component type name
        self.assertEqual(resultObject['name'], 'Magnet', 'There is no no item with that name in the database!')
        
        # Test returned component type description
        self.assertEqual(resultObject['description'], 'desc', 'There is no item with that description in the database!')
        
        # Test returned component type property
        self.assertEqual(resultObject['length'], '123', 'There is no property with that value in the database!')
        
        # Try to update component type
        url = 'http://localhost:8000/id/device/updatecmpnttype/'
        
        # Set parameters
        params={
            'old_name': 'Magnet',
            'name': 'Magnet',
            'description': 'desc2',
            'props': json.dumps({'length': '1234'})
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Try to retrieve component type
        url = 'http://localhost:8000/id/device/cmpnttype/'
        r=self.client.get(url, params={'name': 'Mag*'}, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        existing = len(result)
        
        # Test the number of component types
        self.assertEqual(existing, 1, 'There should be one item in the database!')
        
        # Test returned component type name
        self.assertEqual(resultObject['name'], 'Magnet', 'There is no no item with that name in the database!')
        
        # Test returned component type description
        self.assertEqual(resultObject['description'], 'desc2', 'There is no item with that description in the database!')
        
        # Test returned component type property
        self.assertEqual(resultObject['length'], '1234', 'There is no property with that value in the database!')

    '''
    Test saving, retrieving and updating component type property type
    '''
    def testCmpntTypePropType(self):
        
        # Save new component type property type
        url = 'http://localhost:8000/id/device/savecmpnttypeproptype/'
        
        # Set parameters
        params={
            'name': 'length',
            'description': 'desc'
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Try to retrieve component type property type
        url = 'http://localhost:8000/id/device/cmpnttypeproptype/'
        
        # Set parameters
        params={
            'name': '*'
        }
        
        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        existing = len(result)
        
        # Test the number of property types
        self.assertEqual(existing, 1, 'There is more then one property type in the database!')
        
        # Test returned property type name
        self.assertEqual(resultObject['name'], 'length', 'There is no property type with name length!')
        
        # Test returned property type description
        self.assertEqual(resultObject['description'], 'desc', 'There is no property tpye with that description!')
        
        # Try to update property type
        url = 'http://localhost:8000/id/device/updatecmpnttypeproptype/'
        
        # Set parameters
        params={
            'old_name': 'length',
            'name': 'width',
            'description': 'desc2'
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Try to retrieve property type
        url = 'http://localhost:8000/id/device/cmpnttypeproptype/'
        
        # Set parameters
        params={
            'name': '*'
        }
        
        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        existing = len(result)
        
        # Test the number of property types
        self.assertEqual(existing, 1, 'There is more then one property type in the database!')
        
        # Test returned property type name
        self.assertEqual(resultObject['name'], 'width', 'There is no property type with name width!')
        
        # Test returned property type description
        self.assertEqual(resultObject['description'], 'desc2', 'There is no property type with that description!')

    '''
    Test saving, retrieving and updating inventory
    '''
    def testInventory(self):
        
        # Save new component type
        url = 'http://localhost:8000/id/device/savecmpnttype/'
        
        # Set parameters
        params={
            'name': 'Magnet',
            'description': 'desc'
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Save new vendor
        url = 'http://localhost:8000/id/device/savevendor/'
        
        r=self.client.post(url, data={'name': 'test vendor', 'description': 'desc'})
        r.raise_for_status()
        
        # Save new inventory
        url = 'http://localhost:8000/id/device/saveinventory/'
        
        # Set parameters
        params={
            'name': 'name',
            'cmpnt_type': 'Magnet',
            'vendor': 'test vendor',
            'serialno': '123'
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Try to retrieve inventory
        url = 'http://localhost:8000/id/device/inventory/'
        r=self.client.get(url, params={'name': 'na*'}, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        # Test returned inventory name
        self.assertEqual(resultObject['name'], 'name', 'There is no no item with that name in the database!')
        
        # Test returned inventory vendor
        self.assertEqual(resultObject['vendor'], 'test vendor', 'There is no item with that vendor in the database!')
        
        # Test returned inventory serial number
        self.assertEqual(resultObject['serialno'], '123', 'There is no serial number with that value in the database!')
        
        # Try to update inventory
        url = 'http://localhost:8000/id/device/updateinventory/'
        
        # Set parameters
        params={
            'old_name': 'name',
            'name': 'name2',
            'cmpnt_type': 'Magnet',
            'vendor': 'test vendor',
            'serialno': '1234'
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Try to retrieve inventory
        url = 'http://localhost:8000/id/device/inventory/'
        r=self.client.get(url, params={'name': 'nam*'}, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        # Test returned inventory name
        self.assertEqual(resultObject['name'], 'name2', 'There is no no item with that name in the database!')
        
        # Test returned inventory vendor
        self.assertEqual(resultObject['vendor'], 'test vendor', 'There is no item with that vendor in the database!')
        
        # Test returned inventory serial number
        self.assertEqual(resultObject['serialno'], '1234', 'There is no serial number with that value in the database!')

    '''
    Test saving, retrieving and updating inventory property template
    '''
    def testInventoryPropTmplt(self):
        
        # Save new component type
        url = 'http://localhost:8000/id/device/savecmpnttype/'
        
        # Set parameters
        params={
            'name': 'Magnet',
            'description': 'desc'
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Save new inventory property template
        url = 'http://localhost:8000/id/device/saveinventoryproptmplt/'
        
        # Set parameters
        params={
            'name': 'alpha',
            'description': 'desc',
            'cmpnt_type': 'Magnet',
            'default': 'a',
            'unit': 'M'
            
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Try to retrieve inventory property template
        url = 'http://localhost:8000/id/device/inventoryproptmplt/'
        
        # Set parameters
        params={
            'name': 'alpha'
        }
        
        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        existing = len(result)
        
        # Test the number of inventory property templates
        self.assertEqual(existing, 1, 'There should be one item in the database!')
        
        # Test returned inventory property template name
        self.assertEqual(resultObject['name'], 'alpha', 'There is no no item with that name in the database!')
        
        # Test returned inventory property template description
        self.assertEqual(resultObject['description'], 'desc', 'There is no item with that description in the database!')
        
        # Try to update inventory property template
        url = 'http://localhost:8000/id/device/updateinventoryproptmplt/'
        
        # Set parameters
        params={
            'tmplt_id': resultObject['id'],
            'cmpnt_type': 'Magnet',
            'name': 'beta',
            'description': 'desc2'
        }
        
        r=self.client.post(url, data=params)
        r.raise_for_status()
        
        # Try to retrieve inventory property template
        url = 'http://localhost:8000/id/device/inventoryproptmplt/'
        
        # Set parameters
        params={
            'name': 'be*'
        }
        
        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        existing = len(result)
        
        # Test the number of inventory property templates
        self.assertEqual(existing, 1, 'There should be one item in the database!')
        
        # Test returned inventory property template name
        self.assertEqual(resultObject['name'], 'beta', 'There is no no item with that name in the database!')
        
        # Test returned inventory property template description
        self.assertEqual(resultObject['description'], 'desc2', 'There is no item with that description in the database!')

if __name__ == "__main__":
    unittest.main()