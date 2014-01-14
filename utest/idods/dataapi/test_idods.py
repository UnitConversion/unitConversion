'''
Created on Jan 10, 2014

@author: dejan.dezman@cosylab.com
'''

import unittest
import os

from dataapi.pyidods.idods import idods

from preparerdb import connect, cleanVendor, cleanComponentType

class TestIdods(unittest.TestCase):

    def setUp(self):
        self.con = connect()
        self.api = idods(self.con)

    def tearDown(self):
        self.con.close()

    '''
    Try to retrieve a vendor by its name
    '''
    def testRetrieveVendor(self):

        # Clean vendor table
        cleanVendor(['test vendor']);

        # Save new vendor
        self.api._saveVendor('test vendor');

        # Test retrieving vendor by name
        result = self.api._retrieveVendor('test vendor');
        self.assertEqual(result['name'], 'test vendor', 'Verdor retrieved')

        # Test retrieving vendor without a name
        self.assertRaises(AttributeError, self.api._retrieveVendor, None)

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
        self.assertRaises(AttributeError, self.api.retrieveComponentType, None)

        # Test retrieving component type by whole desciprtion
        result = self.api.retrieveComponentType('*', 'test description');
        keys = result.keys()
        self.assertEqual(result[keys[0]]['description'], 'test description', 'Correct component type retrieved')

        # Test retrieving component type by description with wildcard characters
        result = self.api.retrieveComponentType('*', '*descripti*');
        keys = result.keys()
        self.assertEqual(result[keys[0]]['description'], 'test description', 'Correct component type retrieved')

        # Clean after myself
        cleanComponentType(['test cmpnt', 'test cmpnt2'])

    '''
    Test different options of saving component type
    '''
    def testSaveComponentType(self):

        # Save new component type
        cmpntid = self.api.saveComponentType('test cmpnt3', 'test description')
        result = self.api.retrieveComponentType('test cmpnt3')
        self.assertEqual(result[cmpntid['id']]['name'], 'test cmpnt3', 'We got back the right component type')

        # Save new component type with the same name and same description, it should return existing record
        cmpntid2 = self.api.saveComponentType('test cmpnt3', 'test description')
        self.assertEqual(cmpntid, cmpntid2, 'Exsisting record returned')

        # Save new component type with the same name and different description
        # TODO !!!

        # Try to save new component type without desciption
        cmpntid = self.api.saveComponentType('test cmpnt4')
        result = self.api.retrieveComponentType('test cmpnt4')
        self.assertEqual(result[cmpntid['id']]['name'], 'test cmpnt4', 'We got back the right component type')

        # Try to save new component type without a name
        self.assertRaises(AttributeError, self.api.saveComponentType, None)

        # Clean after myself
        cleanComponentType(['test cmpnt3', 'test cmpnt4'])

    def testSaveInventoryPropertyTemplate(self):

        # Prepare component type
        componentType = self.api.saveComponentType('Magnet');

        # Try to save new inventory property template
        result = self.api._saveInventoryPropertyTemplate('Magnet', 'alpha');

if __name__ == '__main__':
    unittest.main()