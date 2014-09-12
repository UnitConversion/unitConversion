'''
Created on Feb 10, 2014

@author: dejan.dezman@cosylab.com
'''
import unittest
import logging
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

from requests import auth
from requests import HTTPError

try:
    from django.utils import simplejson as json
except ImportError:
    import json

import os
import sys

libPath = os.path.abspath("../../../utest/")
sys.path.append(libPath)

from idods.rdbutils.preparerdb import *


class TestIdods(unittest.TestCase):

    __url = 'http://localhost:8000/id/device/'
    __jsonheader = {'content-type': 'application/json', 'accept': 'application/json'}

    def cleanTables(self):
        cleanDB()

    def setUp(self):
        self.cleanTables()

        try:
            self.__userName = 'user'
            self.__password = 'user'

            if self.__userName and self.__password:
                # self.__auth = (self.__userName, self.__password)
                self.__auth = auth.HTTPBasicAuth(self.__userName, self.__password)

            else:
                self.__auth = None

            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
            self.client = requests.Session()
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

        # Save new inventory
        url = 'http://localhost:8000/id/device/saveinventory/'

        # Set parameters
        params={
            'name': 'name',
            'cmpnt_type': 'Magnet',
            'vendor': 'test vendor',
            'serialno': '123',
            'props': json.dumps({'alpha': 3})
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

        # Test returned property
        self.assertEqual(resultObject['alpha'], '3', 'There is no property with that value in the database!')

        # Try to update inventory
        url = 'http://localhost:8000/id/device/updateinventory/'

        # Set parameters
        params={
            'old_name': 'name',
            'name': 'name2',
            'cmpnt_type': 'Magnet',
            'vendor': 'test vendor',
            'serialno': '1234',
            'props': json.dumps({'alpha': 4})
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

        # Test returned property
        self.assertEqual(resultObject['alpha'], '4', 'There is no property with that value in the database!')

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

    '''
    Test saving, retrieving and updating install entries
    '''
    def testInstall(self):

        # Save new component type
        url = 'http://localhost:8000/id/device/savecmpnttype/'
        r=self.client.post(url, data={'name': 'Magnet', 'description': 'desc'})
        r.raise_for_status()

        # Save new install
        url = 'http://localhost:8000/id/device/saveinstall/'

        # Set parameters
        params={
            'name': 'test parent',
            'description': 'desc',
            'cmpnt_type': 'Magnet',
            'coordinatecenter': 3.4
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Try to retrieve install
        url = 'http://localhost:8000/id/device/install/'

        # Set parameters
        params={
            'name': 'test parent'
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned install name
        self.assertEqual(resultObject['name'], 'test parent', 'There is no item with that name!')

        # Test returned install description
        self.assertEqual(resultObject['description'], 'desc', 'There is no item with that description!')

        # Test returned install component type
        self.assertEqual(resultObject['cmpnt_type'], 'Magnet', 'There is no item with that component type!')

        # Test returned install coordinate center
        self.assertEqual(resultObject['coordinatecenter'], 3.4, 'There is no item with that coordinate center!')

        # Update install
        url = 'http://localhost:8000/id/device/updateinstall/'

        # Set parameters
        params={
            'old_name': 'test parent',
            'name': 'test parent',
            'description': 'desc2',
            'cmpnt_type': 'Magnet',
            'coordinatecenter': 3.5
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Try to retrieve updated install
        url = 'http://localhost:8000/id/device/install/'

        # Set parameters
        params={
            'name': 'test parent'
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned install name
        self.assertEqual(resultObject['name'], 'test parent', 'There is no item with that name!')

        # Test returned install description
        self.assertEqual(resultObject['description'], 'desc2', 'There is no item with that description!')

        # Test returned install component type
        self.assertEqual(resultObject['cmpnt_type'], 'Magnet', 'There is no item with that component type!')

        # Test returned install coordinate center
        self.assertEqual(resultObject['coordinatecenter'], 3.5, 'There is no item with that coordinate center!')

    '''
    Try to save, retrieve and update install rel
    '''
    def testInstallRel(self):

        # Save new component type
        url = 'http://localhost:8000/id/device/savecmpnttype/'
        r=self.client.post(url, data={'name': 'Magnet', 'description': 'desc'})
        r.raise_for_status()

        # Save new install rel property type
        url = 'http://localhost:8000/id/device/saveinstallrelproptype/'

        # Set parameters
        params={
            'name': 'testprop',
            'description': 'desc',
            'unit': 'M'
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Save new install
        url = 'http://localhost:8000/id/device/saveinstall/'

        # Set parameters for the parent
        params={
            'name': 'test parent',
            'description': 'desc',
            'cmpnt_type': 'Magnet',
            'coordinatecenter': 3.4
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Set parameters for the child
        params={
            'name': 'test child',
            'description': 'desc',
            'cmpnt_type': 'Magnet',
            'coordinatecenter': 3.2
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Save install rel
        url = 'http://localhost:8000/id/device/saveinstallrel/'

        # Set parameters
        params={
            'parent_install': 'test parent',
            'child_install': 'test child',
            'description': 'desc',
            'order': 3,
            'props': json.dumps({'testprop': 'abc'})
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Try to retrieve updated install rel
        url = 'http://localhost:8000/id/device/installrel/'

        # Set parameters
        params={
            'parent_install': 'test parent',
            'child_install': 'test child'
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned install rel parent name
        self.assertEqual(resultObject['parentname'], 'test parent', 'There is no item with that name!')

        # Test returned install rel child name
        self.assertEqual(resultObject['childname'], 'test child', 'There is no item with that name!')

        # Test returned install description
        self.assertEqual(resultObject['description'], 'desc', 'There is no item with that description!')

        # Test returned install rel order
        self.assertEqual(resultObject['order'], 3, 'There is no item with that order!')

        # Test returned install rel property
        self.assertEqual(resultObject['testprop'], 'abc', 'There is no property with that value!')

        # Update install rel
        url = 'http://localhost:8000/id/device/updateinstallrel/'

        # Set parameters
        params={
            'parent_install': 'test parent',
            'child_install': 'test child',
            'description': 'desc2',
            'order': 4,
            'props': json.dumps({'testprop': 'abcd'})
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Try to retrieve updated install rel
        url = 'http://localhost:8000/id/device/installrel/'

        # Set parameters
        params={
            'parent_install': 'test parent',
            'child_install': 'test child'
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned install rel parent name
        self.assertEqual(resultObject['parentname'], 'test parent', 'There is no item with that name!')

        # Test returned install rel child name
        self.assertEqual(resultObject['childname'], 'test child', 'There is no item with that name!')

        # Test returned install description
        self.assertEqual(resultObject['description'], 'desc2', 'There is no item with that description!')

        # Test returned install component type
        self.assertEqual(resultObject['order'], 4, 'There is no item with that order!')

        # Test returned install rel property
        self.assertEqual(resultObject['testprop'], 'abcd', 'There is no property with that value!')

    '''
    Test saving, retrieving and updating install rel property type
    '''
    def testInstallRelPropType(self):

        # Save new install rel property type
        url = 'http://localhost:8000/id/device/saveinstallrelproptype/'

        # Set parameters
        params={
            'name': 'testprop',
            'description': 'desc',
            'unit': 'M'
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Try to retrieve install rel property type
        url = 'http://localhost:8000/id/device/installrelproptype/'

        # Set parameters
        params={
            'name': '*'
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned install rel property type name
        self.assertEqual(resultObject['name'], 'testprop', 'There is no item with that name!')

        # Test returned install rel property type description
        self.assertEqual(resultObject['description'], 'desc', 'There is no item with that description!')

        # Test returned install rel property type unit
        self.assertEqual(resultObject['unit'], 'M', 'There is no item with that unit!')

        # Try to update install rel property type
        url = 'http://localhost:8000/id/device/updateinstallrelproptype/'

        # Set parameters
        params={
            'old_name': 'testprop',
            'name': 'prop2',
            'description': 'desc2',
            'unit': 'M'
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Try to retrieve install rel property type
        url = 'http://localhost:8000/id/device/installrelproptype/'

        # Set parameters
        params={
            'name': '*'
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned install rel property type name
        self.assertEqual(resultObject['name'], 'prop2', 'There is no item with that name!')

        # Test returned install rel property type description
        self.assertEqual(resultObject['description'], 'desc2', 'There is no item with that description!')

        # Test returned install rel property type description
        self.assertEqual(resultObject['unit'], 'M', 'There is no item with that unit!')

    '''
    Save, retrieve and update inventory to install map
    '''
    def testInventoryToInstall(self):

        # Save new component type
        url = 'http://localhost:8000/id/device/savecmpnttype/'
        r=self.client.post(url, data={'name': 'Magnet', 'description': 'desc'})
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

        # Save new install
        url = 'http://localhost:8000/id/device/saveinstall/'

        # Set parameters for the parent
        params={
            'name': 'test parent',
            'description': 'desc',
            'cmpnt_type': 'Magnet',
            'coordinatecenter': 3.4
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Save new inventory to install map
        url = 'http://localhost:8000/id/device/saveinventorytoinstall/'

        # Set parameters
        params={
            'install_name': 'test parent',
            'inv_name': 'name'
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()
        idObject = r.json()

        # Retrieve inventory to install map
        url = 'http://localhost:8000/id/device/inventorytoinstall/'

        # Set parameters
        params={
            'install_name': 'test parent',
            'inv_name': 'name'
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned map id
        self.assertEqual(resultObject['id'], idObject['id'], 'Saved and updated ids are not the same!')

        # Update inventory to install map
        url = 'http://localhost:8000/id/device/updateinventorytoinstall/'

        # Set parameters
        params={
            'inventory_to_install_id': resultObject['id'],
            'install_name': 'test parent',
            'inv_name': 'name'
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()
        result = r.json()

        # Check if update returned True
        self.assertTrue(result)

    '''
    Test saving, retrieving and updating data method
    '''
    def testDataMethod(self):

        # Save new data method
        url = 'http://localhost:8000/id/device/savedatamethod/'

        # Set parameters
        params={
            'name': 'method',
            'description': 'name'
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Retrieve data method
        url = 'http://localhost:8000/id/device/datamethod/'

        # Set parameters
        params={
            'name': 'met*'
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned name
        self.assertEqual(resultObject['name'], 'method', 'There is no item with that name in the database!')

        # Test returned description
        self.assertEqual(resultObject['description'], 'name', 'There is no item with that description in the database!')

        # Update data method
        url = 'http://localhost:8000/id/device/updatedatamethod/'

        # Set parameters
        params={
            'old_name': 'method',
            'name': 'method',
            'description': 'desc'
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Retrieve data method
        url = 'http://localhost:8000/id/device/datamethod/'

        # Set parameters
        params={
            'name': 'met*'
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned name
        self.assertEqual(resultObject['name'], 'method', 'There is no item with that name in the database!')

        # Test returned description
        self.assertEqual(resultObject['description'], 'desc', 'There is no item with that description in the database!')

    '''
    Test saving and retrieving raw data
    '''
    def testRawData(self):

        # Save raw data
        url = 'http://localhost:8000/id/device/saverawdata/'

        # Open file
        with open('../dataapi/download_128', 'rb') as f:
            rawData=self.client.post(url, files={'file': f})
            rawData.raise_for_status()

        # Retrieve data
        url = 'http://localhost:8000/id/device/rawdata/'

        r=self.client.get(url, params={'raw_data_id': rawData.json()['id']}, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Check if we got data
        self.assertNotEqual(resultObject['data'], '')

    '''
    Test saving, retrieving and updating offline data
    '''
    def testOfflineData(self):

        # Save new vendor
        url = 'http://localhost:8000/id/device/savevendor/'

        r=self.client.post(url, data={'name': 'test vendor', 'description': 'desc'})
        r.raise_for_status()

        # Save new component type
        url = 'http://localhost:8000/id/device/savecmpnttype/'

        # Set parameters
        params={
            'name': 'Magnet',
            'description': 'desc'
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Save new data method
        url = 'http://localhost:8000/id/device/savedatamethod/'

        # Set parameters
        params={
            'name': 'method',
            'description': 'name'
        }

        r=self.client.post(url, data=params)
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

        # Save raw data
        url = 'http://localhost:8000/id/device/saverawdata/'

        # Open file
        with open('../dataapi/download_128', 'rb') as f:
            rawData=self.client.post(url, files={'file': f})
            rawData.raise_for_status()

        # Save offline data
        url = 'http://localhost:8000/id/device/saveofflinedata/'

        # Set parameters
        params={
            'inventory_name': 'name',
            'description': 'spec1234desc',
            'method_name': 'method',
            'status': 1,
            'data_id': rawData.json()['id'],
            'data_file_name': 'file name',
            'gap': 2
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Retrieve offline data
        url = 'http://localhost:8000/id/device/offlinedata/'

        # Set parameters
        params={
            'gap': (1,5)
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned gap
        self.assertEqual(resultObject['gap'], 2, 'There is no item with that gap in the database!')

        # Update offline data
        url = 'http://localhost:8000/id/device/updateofflinedata/'

        # Set parameters
        params={
            'offline_data_id': resultObject['id'],
            'inventory_name': 'name',
            'description': 'spec1234desc',
            'method_name': 'method',
            'status': 1,
            'data_file_name': 'file name',
            'gap': 2,
            'phase1': 4.34
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Retrieve offline data
        url = 'http://localhost:8000/id/device/offlinedata/'

        # Set parameters
        params={
            'gap': (1,5)
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned gap
        self.assertEqual(resultObject['phase1'], 4.34, 'There is no item with that phase1 in the database!')

    '''
    Test saving, retrieving and updating online data
    '''
    def testOnlineData(self):

        # Save new component type
        url = 'http://localhost:8000/id/device/savecmpnttype/'
        r=self.client.post(url, data={'name': 'Magnet', 'description': 'desc'})
        r.raise_for_status()

        # Save new install
        url = 'http://localhost:8000/id/device/saveinstall/'

        # Set parameters
        params={
            'name': 'test parent',
            'description': 'desc',
            'cmpnt_type': 'Magnet',
            'coordinatecenter': 3.4
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Save online data
        url = 'http://localhost:8000/id/device/saveonlinedata/'

        # Set parameters
        params={
            'install_name': 'test parent',
            'username': 'admin',
            'description': 'desc1234',
            'url': 'url',
            'status': 1
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

        # Retrieve online data
        url = 'http://localhost:8000/id/device/onlinedata/'

        # Set parameters
        params={
            'install_name': 'test parent'
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned install name
        self.assertEqual(resultObject['install_name'], 'test parent', 'There is no item with that install name in the database!')

        # Update online data
        url = 'http://localhost:8000/id/device/updateonlinedata/'

        # Set parameters
        params={
            'online_data_id': resultObject['id'],
            'install_name': 'test parent',
            'username': 'admin2',
            'description': 'desc1234',
            'url': 'url2',
            'status': 1
        }

        r=self.client.post(url, data=params)
        r.raise_for_status()

                # Retrieve online data
        url = 'http://localhost:8000/id/device/onlinedata/'

        # Set parameters
        params={
            'install_name': 'test parent'
        }

        r=self.client.get(url, params=params, verify=False, headers=self.__jsonheader)
        r.raise_for_status()
        result = r.json()
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        # Test returned install name
        self.assertEqual(resultObject['install_name'], 'test parent', 'There is no item with that install name in the database!')

        # Test returned url
        self.assertEqual(resultObject['url'], 'url2', 'There is no item with that url in the database!')

if __name__ == "__main__":
    unittest.main()