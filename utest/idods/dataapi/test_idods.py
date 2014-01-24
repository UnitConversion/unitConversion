'''
Created on Jan 10, 2014

@author: dejan.dezman@cosylab.com
'''

import unittest
import os, sys

from preparerdb import *

libPath = os.path.abspath("../../../dataapi/")
sys.path.append(libPath)

from pyidods.idods import idods

class TestIdods(unittest.TestCase):
    
    def cleanTables(self):
        # Clean vendor table
        cleanVendor(['test vendor']);
        
        # Clean data method
        cleanDataMethod(['method', 'method2'])
        
        # Clean inventory property
        cleanInventoryProperty('name', 'alpha')
        # Clean inventory
        cleanInventory(['name'])
        # Clean inventory property template table
        cleanInventoryPropertyTemplate(['alpha', 'beta'])
        
        # Clean component type property
        cleanComponentTypeProperty('test cmpnt3', 'length')
        # Clean component type property type
        cleanComponentTypePropertyType(['length'])
        # Clean if there is something left from previous runs
        cleanComponentType(['test cmpnt', 'test cmpnt2','test cmpnt3', 'test cmpnt4','Magnet'])

    def setUp(self):
        self.con = connect()
        self.api = idods(self.con)
        self.cleanTables()

    def tearDown(self):
        self.cleanTables()
        self.con.close()

    '''
    Try to retrieve a vendor by its name
    '''
    def testRetrieveVendor(self):

        # Save new vendor
        self.api.saveVendor('test vendor');

        # Test retrieving vendor by name
        result = self.api.retrieveVendor('test vendor');
        resultKeys = result.keys()
        
        self.assertEqual(result[resultKeys[0]]['name'], 'test vendor', 'Verdor retrieved')

        # Test retrieving vendor without a name
        self.assertRaises(ValueError, self.api.retrieveVendor, None)
        
        

    '''
    Test different options of retrieving component type
    '''
    def testRetrieveComponentType(self):

        # Save new component type
        self.api.saveComponentType('test cmpnt', 'test description')
        self.api.saveComponentType('test cmpnt2', 'test description')

        # Test retrieving component type by whole name
        result = self.api.retrieveComponentType('test cmpnt')
        keys = result.keys()
        self.assertEqual(result[keys[0]]['name'], 'test cmpnt', 'Correct component type retrieved')

        # If we insert * as a name, al component types should be returned
        result = self.api.retrieveComponentType('*')
        self.assertTrue(len(result) > 1, "We got more than one result back from the database")

        # If we insert wilcard character into the name parameter, all the results matching this criteria should be returned
        result = self.api.retrieveComponentType('* cmpnt')
        keys = result.keys()
        self.assertEqual(result[keys[0]]['name'], 'test cmpnt', 'Correct component type retrieved')

        # If we do not include name, we should get an Exception
        self.assertRaises(ValueError, self.api.retrieveComponentType, None)

        # Test retrieving component type by whole desciprtion
        result = self.api.retrieveComponentType('*', 'test description');
        keys = result.keys()
        self.assertEqual(result[keys[0]]['description'], 'test description', 'Correct component type retrieved')

        # Test retrieving component type by description with wildcard characters
        result = self.api.retrieveComponentType('*', '*descripti*');
        keys = result.keys()
        self.assertEqual(result[keys[0]]['description'], 'test description', 'Correct component type retrieved')

    '''
    Test different options of saving component type
    '''
    def testSaveComponentType(self):
        
        # Save component type property type
        self.api.saveComponentTypePropertyType('length', 'test description')

        # Save new component type
        cmpntid = self.api.saveComponentType('test cmpnt3', 'test description', props = {'length': 4.354})
        result = self.api.retrieveComponentType('test cmpnt3')
        
        # Check if returned name is the same as saved one
        self.assertEqual(result[cmpntid['id']]['name'], 'test cmpnt3', 'We got back the right component type')
        
        # Check if property was successfully saved in the database
        self.assertTrue('length' in result[cmpntid['id']] and result[cmpntid['id']]['length'] == '4.354', "Component type property in the database")

        # Save new component type with the same name and same description, it should raise an error
        self.assertRaises(ValueError, self.api.saveComponentType, 'test cmpnt3', 'test description')

        # Try to save new component type without description
        cmpntid = self.api.saveComponentType('test cmpnt4')
        result = self.api.retrieveComponentType('test cmpnt4')
        self.assertEqual(result[cmpntid['id']]['name'], 'test cmpnt4', 'We got back the right component type')

        # Try to save new component type without a name
        self.assertRaises(ValueError, self.api.saveComponentType, None)

    '''
    Save inventory property template into database
    '''
    def testSaveInventoryPropertyTemplate(self):

        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')

        # Try to save new inventory property template
        self.api.saveInventoryPropertyTemplate('Magnet', 'alpha')
        
        # Retrieve save inventory property template
        resultRetrieve = self.api.retrieveInventoryPropertyTemplate('alpha')
        resultRetrieveKeys = resultRetrieve.keys()
        
        # Check if names match
        self.assertEqual('alpha', resultRetrieve[resultRetrieveKeys[0]]['name'], 'Correct inventory property template retrieved')
        
        # Try to save inventory property template without a name
        self.assertRaises(ValueError, self.api.saveInventoryPropertyTemplate, 'Magnet', None)
        
        # Try to save inventory property template without a component type
        self.assertRaises(ValueError, self.api.saveInventoryPropertyTemplate, None, 'beta')
        
        # Try to save inventory property template with a non existing component type
        self.assertRaises(ValueError, self.api.saveInventoryPropertyTemplate, 'bla', 'beta')
        
        # Try to save inventory property template with all the parameters filled in
        resultId = self.api.saveInventoryPropertyTemplate('Magnet', 'beta', 'description', 'default', 'm')
        result = self.api.retrieveInventoryPropertyTemplate('bet*')
        resultKeys = result.keys()
        
        # Check ids
        self.assertEqual(resultId['id'], result[resultKeys[0]]['id'], "We got the object that we saved.")
        
        # Check all the other properties
        self.assertTrue(
            result[resultKeys[0]]['name'] == 'beta' and
            result[resultKeys[0]]['description'] == 'description' and
            result[resultKeys[0]]['default'] == 'default' and
            result[resultKeys[0]]['unit'] == 'm' and
            result[resultKeys[0]]['cmpnttype'] == 'Magnet'
        , "Check all the properties in the returned object")
    
    '''
    Try a couple of scenarios of saving inventory property into database
    '''
    def testSaveInventoryProperty(self):
        
        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')
        # Try to save new inventory property template
        template = self.api.saveInventoryPropertyTemplate('Magnet', 'alpha')
        
        # Create inventory
        inventory = self.api.saveInventory('name', compnttype='Magnet')
        
        # Create property
        prop = self.api.saveInventoryProperty('name', 'alpha', 'value')
        
        # Retrieve property
        retrieveProperty = self.api.retrieveInventoryProperty('name', 'alpha', 'value')
        retrievePropertyKeys = retrieveProperty.keys()
        
        self.assertEqual('value', retrieveProperty[retrievePropertyKeys[0]]['value'], "Property save and property retrieved have the same value.")
    
    '''
    Try  to save new inventory into database
    '''
    def testSaveInventory(self):
        
        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')
        
        # Try to save new inventory property template
        template = self.api.saveInventoryPropertyTemplate('Magnet', 'alpha')
        
        # Create inventory
        idObject = self.api.saveInventory('name', compnttype='Magnet', alias='name2', props={'alpha': 42})
        
        inventory = self.api.retrieveInventory('name')
        inventoryKeys = inventory.keys()
        
        # Check names
        self.assertEqual(inventory[inventoryKeys[0]]['name'], 'name', "Names are correct")
        
        # Check properties
        self.assertTrue('alpha' in inventory[inventoryKeys[0]], "Key in returned object")
        
        # Exception should be raised if component type doesn't exist
        self.assertRaises(ValueError, self.api.saveInventory, 'name')
        
        # Exception should be raised if inventory property template doesn't exist
        self.assertRaises(ValueError, self.api.saveInventory, 'name', compnttype='Magnet', props={'beta': 43})
        
    '''
    Try to save offline data method
    '''
    def testSaveDataMethod(self):
        
        # Save data method with name and description
        saveDataMethod = self.api.saveDataMethod('method', 'description')
        retrieveDataMethod = self.api.retrieveDataMethod('method')
        retrieveDataMethodKeys = retrieveDataMethod.keys()
        
        # Try to save another data method with the same name
        self.assertRaises(ValueError, self.api.saveDataMethod, 'method')
        
        # Test id
        self.assertTrue(retrieveDataMethod[retrieveDataMethodKeys[0]]['id'] == saveDataMethod['id'], "Saved and retrieved data method id are the same")
        
        # Test name and description
        self.assertTrue(retrieveDataMethod[retrieveDataMethodKeys[0]]['name'] == 'method' and retrieveDataMethod[retrieveDataMethodKeys[0]]['description'] == 'description', "Saved name and description are the same")
    
        # Test saving data method without name
        self.assertRaises(ValueError, self.api.saveDataMethod, None)
    
    def testRetrieveDataMethod(self):
        
        # Prepare table
        saveDataMethod = self.api.saveDataMethod('method', 'description')
        self.api.saveDataMethod('method2', 'description')
        
        # Try to get data method with the same parameters
        dataMethod = self.api.retrieveDataMethod('method', 'description')
        dataMethodKeys = dataMethod.keys()
        
        # Test both parameters
        self.assertTrue(dataMethod[dataMethodKeys[0]]['id'] == saveDataMethod['id'] and dataMethod[dataMethodKeys[0]]['name'] == 'method' and dataMethod[dataMethodKeys[0]]['description'] == 'description', "We got back the right data method")

        dataMethod2 = self.api.retrieveDataMethod('meth*')
        
        # Try to get both methods back from the database
        self.assertTrue(len(dataMethod2) == 2, "We got back two methods")

    def testSaveOfflineData(self):
        
        # Prepare data method
        savedDataMethod = self.api.saveDataMethod('method', 'description')
        
        # Prepare component type
        savedComponentType = self.api.saveComponentType('Magnet')

        # Prepare inventory
        savedInventory = self.api.saveInventory('name', compnttype='Magnet', alias='name2')
        
        # Prepare raw data
        with open('download_4', 'rb') as f:
            savedData = self.api.saveRawData(f.read())
        
        # Create save offline data
        savedOfflineData = self.api.saveOfflineData(inventory_name='name', method_name='test', status=1, data_file_name='datafile', gap=3.4)
        
        # Delete offline data
        cleanOfflineData([savedOfflineData['id']])

if __name__ == '__main__':
    unittest.main()