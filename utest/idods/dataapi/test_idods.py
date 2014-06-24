'''
Created on Jan 10, 2014

@author: dejan.dezman@cosylab.com
'''

import unittest
import os
import sys

from idods.rdbutils.preparerdb import *

try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pyidods.idods import idods


class TestIdods(unittest.TestCase):

    def cleanTables(self):
        cleanDB()

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
        self.api.saveVendor('test vendor')

        # Test retrieving vendor by name
        result = self.api.retrieveVendor('test vendor')
        resultKeys = result.keys()

        self.assertEqual(result[resultKeys[0]]['name'], 'test vendor', 'Verdor retrieved')

        # Test retrieving vendor without a name
        self.assertRaises(ValueError, self.api.retrieveVendor, None)

    '''
    Test vendor update functionality
    '''
    def testUpdateVendor(self):

        # Save new vendor
        idObject = self.api.saveVendor('test vendor', 'desc')

        # Update vendor name and description
        self.assertTrue(self.api.updateVendor(idObject['id'], None, 'test vendor2', description='desc2'))

        # Try to update without vendor id
        self.assertRaises(ValueError, self.api.updateVendor, None, None, 'test vendor2', description='desc2')

        # Retrieve updated vendor
        vendor = self.api.retrieveVendor('test vendor2')
        vendorKeys = vendor.keys()
        vendorObject = vendor[vendorKeys[0]]

        # Check if id is still the same
        self.assertEqual(idObject['id'], vendorObject['id'], "Ids should be the same")

        # Check new name
        self.assertEqual(vendorObject['name'], 'test vendor2')

        # Check new description
        self.assertEqual(vendorObject['description'], 'desc2')

        # Test updating by name
        self.assertTrue(self.api.updateVendor(None, 'test vendor2', 'test vendor', description=None))

        # Retrieve updated vendor
        vendor = self.api.retrieveVendor('test vendor')
        vendorKeys = vendor.keys()
        vendorObject = vendor[vendorKeys[0]]

        # Check new description
        self.assertEqual(vendorObject['description'], None, "New description should be set to None")

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
        result = self.api.retrieveComponentType('*', 'test description')
        keys = result.keys()
        self.assertEqual(result[keys[0]]['description'], 'test description', 'Correct component type retrieved')

        # Test retrieving component type by description with wildcard characters
        result = self.api.retrieveComponentType('*', '*descripti*')
        keys = result.keys()
        self.assertEqual(result[keys[0]]['description'], 'test description', 'Correct component type retrieved')

    '''
    Test different options of saving component type
    '''
    def testSaveComponentType(self):

        # Save component type property type
        self.api.saveComponentTypePropertyType('length', 'test description')

        # Save new component type
        cmpntid = self.api.saveComponentType('test cmpnt3', 'test description', props={'length': 4.354})
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
    Test updating component type
    '''
    def testUpdateComponentType(self):

        # Save component type property type
        self.api.saveComponentTypePropertyType('length', 'test description')

        # Save new component type
        self.api.saveComponentType('test cmpnt3', 'test description', props={'length': 4.354})

        # Try updating
        self.assertTrue(self.api.updateComponentType(None, 'test cmpnt3', 'Magnet', description='desc', props={'length': 3}))

        # Get updated component type
        cmpnt = self.api.retrieveComponentType('Magnet')
        cmpntKeys = cmpnt.keys()
        cmpntObject = cmpnt[cmpntKeys[0]]

        # Check new description
        self.assertEqual(cmpntObject['description'], 'desc')

        # Check new length property value
        self.assertEqual(cmpntObject['length'], '3')

    '''
    Test saving, retrieving and updating component type property type
    '''
    def testComponentTypePropertyType(self):

        # Save component type property type
        propertyType = self.api.saveComponentTypePropertyType('length', 'test description')

        # Retrieve component type property type
        retrievedPropertyType = self.api.retrieveComponentTypePropertyType('length')
        retrievedPropertyTypeKeys = retrievedPropertyType.keys()
        retrievedPropertyTypeObject = retrievedPropertyType[retrievedPropertyTypeKeys[0]]

        # Check if name was saved
        self.assertEqual(retrievedPropertyTypeObject['name'], 'length')

        # Check if description was saved
        self.assertEqual(retrievedPropertyTypeObject['description'], 'test description')

        # Try to update with a new name by old name
        self.assertTrue(self.api.updateComponentTypePropertyType(None, 'length', 'width'))

        # Retrieve it again
        retrievedPropertyType = self.api.retrieveComponentTypePropertyType('width')
        retrievedPropertyTypeKeys = retrievedPropertyType.keys()
        retrievedPropertyTypeObject = retrievedPropertyType[retrievedPropertyTypeKeys[0]]

        # Check if ids are the same
        self.assertEqual(propertyType['id'], retrievedPropertyTypeObject['id'])

    '''
    Test saving, retrieving and updating component type property
    '''
    def testComponentTypeProperty(self):

        # Save component type property type
        propertyType = self.api.saveComponentTypePropertyType('length', 'test description')
        propertyType2 = self.api.saveComponentTypePropertyType('length2', 'test description')

        # Prepare component type
        savedComponentType = self.api.saveComponentType('Magnet')

        # Save component type property
        property = self.api.saveComponentTypeProperty('Magnet', 'length', 3)

        # Save component type property by id
        propertyId = self.api.saveComponentTypePropertyById(savedComponentType['id'], 'length2', 3)

        # Test if we got back id
        self.assertNotEqual(propertyId['id'], 0)

        # Try to update
        self.assertTrue(self.api.updateComponentTypeProperty('Magnet', 'length', 4))

        # Get updated component type property
        updatedProperty = self.api.retrieveComponentTypeProperty('Magnet', 'length')
        updatedPropertyKeys = updatedProperty.keys()
        updatedPropertyObject = updatedProperty[updatedPropertyKeys[0]]

        # Check value
        self.assertEqual(updatedPropertyObject['value'], '4')

    '''
    Save inventory property template into database
    '''
    def testSaveInventoryPropertyTemplate(self):

        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')

        # Try to save new inventory property template
        self.api.saveInventoryPropertyTemplate('Magnet', 'alpha')

        # Save again
        self.assertRaises(ValueError, self.api.saveInventoryPropertyTemplate, 'Magnet', 'alpha')

        # Save with unknown component type
        self.assertRaises(ValueError, self.api.saveInventoryPropertyTemplate, 'unknown', 'gamma')

        resultRetrieve = self.api.retrieveInventoryPropertyTemplate('alpha', 'Magnet')
        resultRetrieveKeys = resultRetrieve.keys()

        self.assertEqual('alpha', resultRetrieve[resultRetrieveKeys[0]]['name'], 'Correct inventory property template retrieved')

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
            result[resultKeys[0]]['cmpnt_type'] == 'Magnet',
            "Check all the properties in the returned object"
        )

    '''
    Test updating inventory property template
    '''
    def testUpadateInventoryPropertyTemplate(self):
        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')

        # Try to save new inventory property template
        idObject = self.api.saveInventoryPropertyTemplate('Magnet', 'alpha', 'desc', 'default', 'units')

        # Update template
        self.assertTrue(self.api.updateInventoryPropertyTemplate(idObject['id'], 'Magnet', 'beta', description='desc2', default='def', unit='units2'))

        # Retrieve updated template
        template = self.api.retrieveInventoryPropertyTemplate('beta')
        templateKeys = template.keys()
        templateObject = template[templateKeys[0]]

        # Check if ids are the same
        self.assertEqual(idObject['id'], templateObject['id'], "Ids should be the same")

        # Check if description stayed the same
        self.assertEqual(templateObject['description'], 'desc2')

    '''
    Try a couple of scenarios of saving inventory property into database
    '''
    def testSaveInventoryProperty(self):

        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')
        # Try to save new inventory property template
        template = self.api.saveInventoryPropertyTemplate('Magnet', 'alpha')

        # Create inventory
        inventory = self.api.saveInventory('name', cmpnt_type='Magnet')

        # Create property
        prop = self.api.saveInventoryProperty('name', 'alpha', 'value')

        # Retrieve property
        retrieveProperty = self.api.retrieveInventoryProperty('name', 'alpha', 'value')
        retrievePropertyKeys = retrieveProperty.keys()

        self.assertEqual('value', retrieveProperty[retrievePropertyKeys[0]]['value'], "Property save and property retrieved have the same value.")

        # Try to save property with not existing property template without providing component type name
        self.assertRaises(ValueError, self.api.saveInventoryProperty, 'name', 'cmpnt', 1)

        # Try to save property with not existing template by providing component type name
        self.api.saveInventoryProperty('name', 'cmpnt', 1, 'Magnet')

        # Retrieve newly saved property
        result = self.api.retrieveInventoryProperty('name', 'cmpnt')

        self.assertNotEqual(len(result), 0)

    '''
    Test updating inventory property
    '''
    def testUpdateInventoryProperty(self):
        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')
        # Try to save new inventory property template
        template = self.api.saveInventoryPropertyTemplate('Magnet', 'alpha')

        # Create inventory
        inventory = self.api.saveInventory('name', cmpnt_type='Magnet')

        # Create property
        prop = self.api.saveInventoryProperty('name', 'alpha', 'value')

        # Try to update
        self.assertTrue(self.api.updateInventoryProperty('name', 'alpha', 'newvalue'), "Set new value to alpha property")

        # Retrieve property
        retrieveProperty = self.api.retrieveInventoryProperty('name', 'alpha')
        retrievePropertyKeys = retrieveProperty.keys()
        propertyObject = retrieveProperty[retrievePropertyKeys[0]]

        # Check if id stayed the same
        self.assertEqual(prop['id'], propertyObject['id'], "Id should be the same after updating!")

        # Check new value
        self.assertEqual(propertyObject['value'], 'newvalue')

    '''
    Try  to save new inventory into database
    '''
    def testSaveInventory(self):

        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')

        # Try to save new inventory property template
        template = self.api.saveInventoryPropertyTemplate('Magnet', 'alpha')

        # Create inventory
        idObject = self.api.saveInventory('name', cmpnt_type='Magnet', alias='name2', props={'alpha': 42})

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
    Try to update inventory
    '''
    def testUpdateInventory(self):

        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')

        # Try to save new inventory property template
        template = self.api.saveInventoryPropertyTemplate('Magnet', 'alpha')

        # Create inventory
        idObject = self.api.saveInventory('name', cmpnt_type='Magnet', alias='name2', props={'alpha': 42})

        # Update inventory
        self.assertTrue(self.api.updateInventory(None, 'name', 'name2', cmpnt_type='Magnet', alias='name3', props={'alpha': 43}))

        # Get updated inventory
        inventory = self.api.retrieveInventory('name2')
        inventoryKeys = inventory.keys()
        inventoryObject = inventory[inventoryKeys[0]]

        # Check if ids are the same
        self.assertEqual(inventoryObject['id'], idObject['id'], "Ids should stay the same!")

        # Check if alpha property value has changed
        self.assertEqual(inventoryObject['alpha'], '43', "Check if property has changed")

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

    '''
    Test updating data method
    '''
    def testUpdateDataMethod(self):
        # Save data method with name and description
        saveDataMethod = self.api.saveDataMethod('method', 'description')

        # Try updating by old name
        self.assertTrue(self.api.updateDataMethod(None, 'method', 'method2', description='new desc'))

        # Get updated data method
        updatedDataMethod = self.api.retrieveDataMethod('method2')
        updatedDataMethodKeys = updatedDataMethod.keys()
        updatedDataMethodObject = updatedDataMethod[updatedDataMethodKeys[0]]

        # Check ids
        self.assertEqual(saveDataMethod['id'], updatedDataMethodObject['id'])

        # Check new description
        self.assertEqual(updatedDataMethodObject['description'], 'new desc',)

        # Update by an id
        self.assertTrue(self.api.updateDataMethod(updatedDataMethodObject['id'], None, 'method', description='new desc2'))

        # Update should fail if there is no id or old name present
        self.assertRaises(ValueError, self.api.updateDataMethod, None, None, 'method2')

    '''
    Try to retrieve offline data method
    '''
    def testRetrieveDataMethod(self):

        # Prepare table
        saveDataMethod = self.api.saveDataMethod('method', 'description')
        self.api.saveDataMethod('method2', 'description')

        # Try to save data method with the same name
        self.assertRaises(ValueError, self.api.saveDataMethod, 'method')

        # Try to get data method with the same parameters
        dataMethod = self.api.retrieveDataMethod('method', 'description')
        dataMethodKeys = dataMethod.keys()

        # Test both parameters
        self.assertTrue(dataMethod[dataMethodKeys[0]]['id'] == saveDataMethod['id'] and dataMethod[dataMethodKeys[0]]['name'] == 'method' and dataMethod[dataMethodKeys[0]]['description'] == 'description', "We got back the right data method")

        dataMethod2 = self.api.retrieveDataMethod('meth*')

        # Try to get both methods back from the database
        self.assertTrue(len(dataMethod2) == 2, "We got back two methods")

    '''
    Test saving, tetrieving and updating raw data
    '''
    def testRawData(self):

        # Prepare raw data
        with open('download_4', 'rb') as f:
            savedData = self.api.saveRawData(f.read())

        with open('download_128', 'rb') as f:
            # Check if data was successfully updated
            self.assertTrue(self.api.updateRawData(savedData['id'], f.read()))

        # Retrieve data
        result = self.api.retrieveRawData(savedData['id'])
        resultKeys = result.keys()
        resultObject = result[resultKeys[0]]

        self.assertNotEqual(resultObject['data'], '')

    '''
    Save offline data
    '''
    def testSaveOfflineData(self):

        # Prepare data method
        savedDataMethod = self.api.saveDataMethod('method', 'description')

        # Prepare component type
        savedComponentType = self.api.saveComponentType('Magnet')

        # Prepare inventory
        savedInventory = self.api.saveInventory('name', cmpnt_type='Magnet', alias='name2')

        # Prepare method
        savedMethod = self.api.saveDataMethod('test')

        # Prepare raw data
        with open('download_4', 'rb') as f:
            savedData = self.api.saveRawData(f.read())

        # Create save offline data
        savedOfflineData = self.api.saveOfflineData(inventory_name='name', data_id=savedData['id'], method_name='test', status=1, data_file_name='datafile', gap=3.4, description='spec1234desc')

        # Retrieve offline data by gap range
        offlineData = self.api.retrieveOfflineData(gap=json.dumps((3, 4)))
        offlineDataKeys = offlineData.keys()
        offlineDataObject = offlineData[offlineDataKeys[0]]

        # Check if we get back one or more offline data
        self.assertTrue(len(offlineData) > 0, "One or more offline data should be returned")

        # Test inventory name
        self.assertEqual(offlineDataObject['inventory_name'], 'name')

        # Test method name
        self.assertEqual(offlineDataObject['method_name'], 'test')

        # Test status
        self.assertEqual(offlineDataObject['status'], 1)

        # Test data file name
        self.assertEqual(offlineDataObject['data_file_name'], 'datafile')

        # Test gap
        self.assertEqual(offlineDataObject['gap'], 3.4)

        # Test description
        self.assertEqual(offlineDataObject['description'], 'spec1234desc')

    '''
    Try to update offline data
    '''
    def testUpdateOfflineData(self):

        # Prepare data method
        savedDataMethod = self.api.saveDataMethod('method', 'description')

        # Prepare component type
        savedComponentType = self.api.saveComponentType('Magnet')

        # Prepare inventory
        savedInventory = self.api.saveInventory('name', cmpnt_type='Magnet', alias='name2')

        # Prepare raw data
        with open('download_4', 'rb') as f:
            savedData = self.api.saveRawData(f.read())

        # Create offline data
        savedOfflineData = self.api.saveOfflineData(inventory_name='name', data_id=savedData['id'], method_name='method', status=1, data_file_name='datafile', gap=3.4, description='spec1234desc')

        # Update offline data
        self.assertTrue(self.api.updateOfflineData(savedOfflineData['id'], status=2, phase1=2.4, phasemode='p', data_file_ts='2014-02-03'))

        # Retrieve updated offline data by id
        updatedData = self.api.retrieveOfflineData(offlineid=savedOfflineData['id'])
        updatedDataKeys = updatedData.keys()
        updatedDataObject = updatedData[updatedDataKeys[0]]

        # Check status
        self.assertEqual(updatedDataObject['status'], 2)

        # Check gap
        self.assertEqual(updatedDataObject['gap'], 3.4)

        # Check phase mode
        self.assertEqual(updatedDataObject['phasemode'], 'p')

    '''
    Test saving, retrieving and updating install
    '''
    def testInstall(self):
        # Prepare component type
        self.api.saveComponentType('Magnet')

        # Prepare install
        savedInstall = self.api.saveInstall('test parent', cmpnt_type='Magnet', description='desc', coordinatecenter=2.2)

        # Try to update
        self.assertTrue(self.api.updateInstall(None, 'test parent', 'test child', description='desc2'))

        # Try to update by setting component type to None
        self.assertRaises(ValueError, self.api.updateInstall, None, 'test child', 'test child', cmpnt_type=None)

        # Retrieve successfully updated component type
        componentType = self.api.retrieveInstall('test child')
        componentTypeKeys = componentType.keys()
        componentTypeObject = componentType[componentTypeKeys[0]]

        # Check ids
        self.assertEqual(savedInstall['id'], componentTypeObject['id'])

        # Check description
        self.assertEqual(componentTypeObject['description'], 'desc2')

        # Check coordinate center
        self.assertEqual(componentTypeObject['coordinatecenter'], 2.2)

    '''
    Test saving, retrieving and updating install rel property type
    '''
    def testInstallRelPropertyType(self):

        # Prepare prop type
        propType = self.api.saveInstallRelPropertyType('testprop')

        # Try to update
        self.assertTrue(self.api.updateInstallRelPropertyType(None, 'testprop', 'prop2', description='desc', unit='units'))

        # Retrieve updated property type
        updatedPropType = self.api.retrieveInstallRelPropertyType('prop2')
        updatedPropTypeKeys = updatedPropType.keys()
        updatedPropTypeObject = updatedPropType[updatedPropTypeKeys[0]]

        # Check ids
        self.assertEqual(propType['id'], updatedPropTypeObject['id'])

        # Check if units are still the same
        self.assertEqual(updatedPropTypeObject['unit'], 'units')

        # Check if description is still the same
        self.assertEqual(updatedPropTypeObject['description'], 'desc')

    '''
    Try to save, retrieve and update install rel property
    '''
    def testInstallrelProperty(self):

        # Prepare component type
        savedComponentType = self.api.saveComponentType('Magnet')

        # Prepare prop type
        propType = self.api.saveInstallRelPropertyType('testprop')

        # Prepare install parent
        savedInstallParent = self.api.saveInstall('test parent', cmpnt_type='Magnet', description='desc', coordinatecenter=2.2)

        # Prepare install child
        savedInstallChild = self.api.saveInstall('test child', cmpnt_type='Magnet')

        # Save rel
        rel = self.api.saveInstallRel('test parent', 'test child', 'desc', 1)

        # Save install rel property
        prop = self.api.saveInstallRelProperty(rel['id'], 'testprop', 4)

        # Try to update install rel property
        self.assertTrue(self.api.updateInstallRelProperty('test parent', 'test child', 'testprop', value=5))

        # Retrieve updated install rel property
        updatedProp = self.api.retrieveInstallRelProperty(rel['id'], 'testprop')
        updatedPropKeys = updatedProp.keys()
        updatedPropObject = updatedProp[updatedPropKeys[0]]

        # Test value
        self.assertEqual(updatedPropObject['value'], '5')

    '''
    Test saving install relationship
    '''
    def testSaveInstallRel(self):

        # Prepare component type
        savedComponentType = self.api.saveComponentType('Magnet')

        # Prepare install parent
        savedInstallParent = self.api.saveInstall('test parent', cmpnt_type='Magnet', description='desc', coordinatecenter=2.2)

        # Prepare install child
        savedInstallChild = self.api.saveInstall('test child', cmpnt_type='Magnet')

        # Prepare prop type
        propType = self.api.saveInstallRelPropertyType('testprop')

        # Save rel
        rel = self.api.saveInstallRel('test parent', 'test child', 'desc', 1, {'testprop': 'testvalue'})

        # Retrieve rel
        retrievedRel = self.api.retrieveInstallRel(rel['id'])
        retrievedRelKeys = retrievedRel.keys()
        retrievedRelObject = retrievedRel[retrievedRelKeys[0]]

        # Check description
        self.assertEqual(retrievedRelObject['description'], 'desc')

        # Check order
        self.assertEqual(retrievedRelObject['order'], 1)

        # Check test property
        self.assertEqual(retrievedRelObject['testprop'], 'testvalue')

        # Test saving another rel with same parent and child
        self.assertRaises(ValueError, self.api.saveInstallRel, 'test parent', 'test child', None, None)

        # Test saving install rel with property that is not defined
        self.assertRaises(ValueError, self.api.saveInstallRel, 'test child', 'test parent', None, None, {'testprop2': 'testvalue'})

    '''
    Test updating install relationship
    '''
    def testUpdateInstallRel(self):

        # Prepare component type
        savedComponentType = self.api.saveComponentType('Magnet')

        # Prepare install parent
        savedInstallParent = self.api.saveInstall('test parent', cmpnt_type='Magnet', description='desc', coordinatecenter=2.2)

        # Prepare install child
        savedInstallChild = self.api.saveInstall('test child', cmpnt_type='Magnet')

        # Prepare prop type
        propType = self.api.saveInstallRelPropertyType('testprop')

        # Save rel
        rel = self.api.saveInstallRel('test parent', 'test child', 'desc', 1, {'testprop': 'testvalue'})

        self.assertTrue(self.api.updateInstallRel('test parent', 'test child', description='descupd', order=2, props={'testprop': 'value'}))

        # Retrieve rel
        retrievedRel = self.api.retrieveInstallRel(rel['id'])
        retrievedRelKeys = retrievedRel.keys()
        retrievedRelObject = retrievedRel[retrievedRelKeys[0]]

        # Check description
        self.assertEqual(retrievedRelObject['description'], 'descupd')

        # Check order
        self.assertEqual(retrievedRelObject['order'], 2)

        # Check test property
        self.assertEqual(retrievedRelObject['testprop'], 'value')

        # Test saving another rel with same parent and child
        self.assertRaises(ValueError, self.api.saveInstallRel, 'test parent', 'test child', None, None)

        # Test saving install rel with property that is not defined
        self.assertRaises(ValueError, self.api.saveInstallRel, 'test child', 'test parent', None, None, {'testprop2': 'testvalue'})

    '''
    Test saving, retrieving and updating inventory to install map
    '''
    def testInventoryToInstall(self):

        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')

        # Try to save new inventory property template
        template = self.api.saveInventoryPropertyTemplate('Magnet', 'alpha')

        # Create inventory
        idObject = self.api.saveInventory('name', cmpnt_type='Magnet', alias='name2', props={'alpha': 42})
        idObject2 = self.api.saveInventory('name2', cmpnt_type='Magnet', alias='name2')

        # Prepare install parent
        savedInstall = self.api.saveInstall('test parent', cmpnt_type='Magnet', description='desc', coordinatecenter=2.2)

        # Map install to inventory
        map = self.api.saveInventoryToInstall('test parent', 'name')

        # Retrieve saved map
        retrieveMap = self.api.retrieveInventoryToInstall(None, 'test parent', 'name')
        retrieveMapKeys = retrieveMap.keys()
        retrieveMapObject = retrieveMap[retrieveMapKeys[0]]

        # Check if saved and retrieved maps are equal
        self.assertEqual(map['id'], retrieveMapObject['id'])

        # Set install to a new inventory
        self.assertTrue(self.api.updateInventoryToInstall(map['id'], 'test parent', 'name2'))

        # Save online data
        od = self.api.saveOnlineData('test parent', status=1)

        # Delete inventory to install
        self.assertTrue(self.api.deleteInventoryToInstall(map['id']))

        # Get online data
        od = self.api.retrieveOnlineData(onlineid=od['id'])
        odKeys = od.keys()
        odObj = od[odKeys[0]]

        # Test online data count
        self.assertTrue(len(odKeys) == 1)

        # Test status - it should be 0
        self.assertTrue(odObj['status'] == 0)

        # Map install to inventory
        map = self.api.saveInventoryToInstall('test parent', 'name')

        # Delete inventory to install
        self.assertTrue(self.api.deleteInventoryToInstall(map['id'], delete_online_data=True))

    '''
    Test saving online data
    '''
    def testSaveOnlineData(self):

        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')

        # Prepare install parent
        savedInstall = self.api.saveInstall('test parent', cmpnt_type='Magnet', description='desc', coordinatecenter=2.2)

        # Save online data
        onlineid = self.api.saveOnlineData('test parent', username='username', description='desc1234', url='url', status=1)

        # Retrieve online data
        retrievedOnlineData = self.api.retrieveOnlineData(onlineid=onlineid['id'])
        retrievedOnlineDataKeys = retrievedOnlineData.keys()
        retrievedOnlineDataObject = retrievedOnlineData[retrievedOnlineDataKeys[0]]

        # Test install name
        self.assertEqual('test parent', retrievedOnlineDataObject['install_name'])

        # Test description
        self.assertEqual('desc1234', retrievedOnlineDataObject['description'])

        # Test username
        self.assertEqual('username', retrievedOnlineDataObject['username'])

        # Test URL
        self.assertEqual('url', retrievedOnlineDataObject['url'])

        # Test status
        self.assertEqual(1, retrievedOnlineDataObject['status'])

    '''
    Test update online data
    '''
    def testUpdateOnlineData(self):

        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')

        # Prepare install parent
        savedInstall = self.api.saveInstall('test parent', cmpnt_type='Magnet', description='desc', coordinatecenter=2.2)

        # Save online data
        onlineid = self.api.saveOnlineData('test parent', username='username', description='desc1234', url='url', status=1)

        # Update online data
        self.assertTrue(self.api.updateOnlineData(onlineid['id'], username='username2'))

        # Retrieve online data
        retrievedOnlineData = self.api.retrieveOnlineData(onlineid=onlineid['id'])
        retrievedOnlineDataKeys = retrievedOnlineData.keys()
        retrievedOnlineDataObject = retrievedOnlineData[retrievedOnlineDataKeys[0]]

        # Test username
        self.assertEqual('username2', retrievedOnlineDataObject['username'])

        # Test URL
        self.assertEqual('url', retrievedOnlineDataObject['url'])

        # Test status
        self.assertEqual(1, retrievedOnlineDataObject['status'])

    def testOnlineData(self):

        # Prepare component type
        componentType = self.api.saveComponentType('Magnet')

        # Prepare install parent
        savedInstall = self.api.saveInstall('test parent', cmpnt_type='Magnet', description='desc', coordinatecenter=2.2)

        # Save online data
        onlineid = self.api.saveOnlineData('test parent', username='username', description='desc1234', url='url', status=1)

        # Delete online data
        self.assertRaises(IOError, self.api.deleteOnlineData, onlineid['id'])

        fileResult = self.api.saveFile('tmp', 'bla')

        # Save online data
        onlineid = self.api.saveOnlineData('test parent', username='username', description='desc1234', url=fileResult['path'], status=1)

        # Delete online data
        self.assertTrue(self.api.deleteOnlineData(onlineid['id']))

    '''
    Test preparing data for normal functioning of IDODS
    '''
    def testIdodsInstall(self):

        self.assertTrue(self.api.idodsInstall())

    '''
    Test saving insertion device
    '''
    def testSaveInsertionDevice(self):
        self.assertRaises(ValueError, self.api.saveInsertionDevice)

        # If install name or inventory name is defined, component type should also be defined
        self.assertRaises(ValueError, self.api.saveInsertionDevice, inventory_name='inventory')

        # If install name is defined, beamline and project should also be defined
        self.assertRaises(ValueError, self.api.saveInsertionDevice, install_name='install', type_name='type', beamline='beamline')

        # Fail installing because idods install was not ran
        self.assertRaises(ValueError, self.api.saveInsertionDevice, beamline='beam', project='proj', install_name='install')

        # Prepare DB
        self.assertTrue(self.api.idodsInstall())

        # Save install
        self.assertTrue(self.api.saveInsertionDevice(beamline='beam', project='proj', type_name='type', install_name='install'))

        # Save inventory
        self.assertTrue(self.api.saveInsertionDevice(type_name='type', inventory_name='inv'))

        # Fail because of the duplicate install name
        self.assertRaises(ValueError, self.api.saveInsertionDevice, beamline='beam', project='proj', type_name='type', install_name='install', inventory_name='inv2')

        # Fail because of the duplicate inventory name
        self.assertRaises(ValueError, self.api.saveInsertionDevice, beamline='beam', project='proj', type_name='type', install_name='install4', inventory_name='inv')

        # Save inventory and install and install a device
        self.assertTrue(self.api.saveInsertionDevice(beamline='beam', project='proj', type_name='type', install_name='install3', inventory_name='inv3'))

if __name__ == '__main__':
    unittest.main()