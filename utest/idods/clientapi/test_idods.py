'''
Created on Feb 17, 2014

@author: dejan.dezman@cosylab.com
'''
import os, sys

import unittest
import logging
import requests
import random

import inspect
from requests import HTTPError

from idods.rdbutils.preparerdb import *

libPath = os.path.abspath("../../../clientapi/")
sys.path.append(libPath)

from idodspy.idodsclient import IDODSClient

class Test(unittest.TestCase):

    __url = 'http://localhost:8000/id/device/'
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}

    def cleanTables(self):
        # Clean offline data
        cleanOfflineData(['spec1234desc'])
        
        # Clean install rel prop
        cleanInstallRelProp(['testprop'])
        
        # Clean install rel prop type
        cleanInstallRelPropType(['testprop', 'prop2'])
        
        # Clean install rel
        cleanInstallRel('test child', 'test parent')
        cleanInstallRel('test parent', 'test child')
        
        # Clean online data
        cleanOnlineData(['desc1234'])
        
        # Clean inventory install map
        cleanInventoryToInstall('test parent', 'name')
        cleanInventoryToInstall('test parent', 'name2')
        
        # Clean install table
        cleanInstall(['test parent', 'test child'])
        
        # Clean vendor table
        cleanVendor(['test vendor', 'test vendor2'])
        
        # Clean data method
        cleanDataMethod(['method', 'method2', 'test'])
        
        # Clean inventory property
        cleanInventoryProperty('name', 'alpha')
        cleanInventoryProperty('name2', 'alpha')
        # Clean inventory
        cleanInventory(['name', 'name2'])
        # Clean inventory property template table
        cleanInventoryPropertyTemplate(['alpha', 'beta'])
        
        # Clean component type property
        cleanComponentTypeProperty('test cmpnt3', 'length')
        cleanComponentTypeProperty('Magnet', 'length')
        # Clean component type property type
        cleanComponentTypePropertyType(['length', 'width'])
        # Clean if there is something left from previous runs
        cleanComponentType(['test cmpnt', 'test cmpnt2','test cmpnt3', 'test cmpnt4','Magnet'])

    def setUp(self):
        self.cleanTables()
        self.client = IDODSClient(BaseURL=self.__url)

        try:
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)

        except:
            raise

    def tearDown(self):
        self.cleanTables()

    '''
    Try to save and update a vendor
    '''
    def testVendor(self):

        # Save new vendor
        self.client.saveVendor('test vendor');

        # Test retrieving vendor by its name
        result = self.client.retrieveVendor('test vendor');
        resultKeys = result.keys()
        
        self.assertEqual(result[resultKeys[0]]['name'], 'test vendor', 'Verdor retrieved')

        # Test retrieving vendor without a name
        self.assertRaises(HTTPError, self.client.retrieveVendor, None)
        
        # Update vendor
        self.client.updateVendor('test vendor', 'test vendor2', description='desc')
        
        # Test retrieving vendor by its name
        result = self.client.retrieveVendor('test vendor2');
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        # Test name
        self.assertEqual(resultObject['name'], 'test vendor2')
        
        # Test description
        self.assertEqual(resultObject['description'], 'desc')

    '''
    Test saving, retrieving and updating component type
    '''
    def testCmpntType(self):
        
        # Save component type property type
        self.client.saveComponentTypePropertyType('length', 'test description')
        
        # Save new component type
        cmpntid = self.client.saveComponentType('test cmpnt3', 'test description', props = {'length': 4.354})
        
        # Retrieve component type
        result = self.client.retrieveComponentType('test cmpnt3')
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        # Check if returned name is the same as saved one
        self.assertEqual(resultObject['name'], 'test cmpnt3', 'We got back the right component type')
        
        # Check if property was successfully saved in the database
        self.assertTrue('length' in resultObject and resultObject['length'] == '4.354', "Component type property in the database")
        
        # Save new component type with the same name and same description, it should raise an error
        self.assertRaises(HTTPError, self.client.saveComponentType, 'test cmpnt3', 'test description')
        
        # Try to save new component type without a name
        self.assertRaises(HTTPError, self.client.saveComponentType, None)
        
        # Try updating
        self.assertTrue(self.client.updateComponentType('test cmpnt3', 'Magnet', description = 'desc', props = {'length': 3}))
        
        # Retrieve component type
        result = self.client.retrieveComponentType('Magnet')
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]
        
        # Check if returned name is the same as saved one
        self.assertEqual(resultObject['name'], 'Magnet', 'We got back the right component type')
        
        # Check returned description
        self.assertEqual(resultObject['description'], 'desc')
        
        # Check returned length
        self.assertEqual(resultObject['length'], '3')

    '''
    Test saving, retrieving and updating component type property type
    '''
    def testCmpntTypePropType(self):
        
        # Save component type property type
        propertyType = self.client.saveComponentTypePropertyType('length', 'test description')
        
        # Retrieve component type property type
        retrievedPropertyType = self.client.retrieveComponentTypePropertyType('length')
        retrievedPropertyTypeKeys = retrievedPropertyType.keys()
        retrievedPropertyTypeObject = retrievedPropertyType[retrievedPropertyTypeKeys[0]]
        
        # Check if name was saved
        self.assertEqual(retrievedPropertyTypeObject['name'], 'length')
        
        # Check if description was saved
        self.assertEqual(retrievedPropertyTypeObject['description'], 'test description')
        
        # Try to update with a new name by old name
        self.assertTrue(self.client.updateComponentTypePropertyType('length', 'width'))
        
    '''
    Test saving, retrieving and updating inventory
    '''
    def testInventory(self):
        
        # Prepare component type
        self.client.saveComponentType('Magnet')
        
        # Try to save new inventory property template
        self.client.saveInventoryPropertyTemplate('Magnet', 'alpha')
        
        # Create inventory
        idObject = self.client.saveInventory('name', cmpnt_type='Magnet', alias='name2', props={'alpha': 42})
        
        # Update inventory
        self.assertTrue(self.client.updateInventory('name', 'name2', cmpnt_type='Magnet', alias='name3', props={'alpha': 43}))
        
        # Get updated inventory
        inventory = self.client.retrieveInventory('name2')
        inventoryKeys = inventory.keys()
        inventoryObject = inventory[inventoryKeys[0]]
        
        # Check if ids are the same
        self.assertEqual(inventoryObject['id'], idObject['id'], "Ids should stay the same!")
        
        # Check if alpha property value has changed
        self.assertEqual(inventoryObject['alpha'], '43', "Check if property has changed")
        
        # Check component type
        self.assertEqual(inventoryObject['cmpnt_type'], 'Magnet')
        
        # Check alias
        self.assertEqual(inventoryObject['alias'], 'name3')
        
        # Check vendor
        self.assertEqual(inventoryObject['vendor'], None)
        
    '''
    Test saving, retrieving and updating inventory property template
    '''
    def testInventoryPropTmplt(self):
        
        # Prepare component type
        self.client.saveComponentType('Magnet')
        
        # Try to save new inventory property template
        idObject = self.client.saveInventoryPropertyTemplate('Magnet', 'alpha', 'desc', 'default', 'units')
        
        # Update template
        self.assertTrue(self.client.updateInventoryPropertyTemplate(idObject['id'], 'Magnet', 'beta'))
        
        # Retrieve updated template
        template = self.client.retrieveInventoryPropertyTemplate('beta')
        templateKeys = template.keys()
        templateObject = template[templateKeys[0]]
        
        # Check if ids are the same
        self.assertEqual(idObject['id'], templateObject['id'], "Ids should be the same")
        
        # Check if description stayed the same
        self.assertEqual(templateObject['description'], 'desc')
        
        # Check name
        self.assertEqual(templateObject['name'], 'beta')

if __name__ == "__main__":
    unittest.main()