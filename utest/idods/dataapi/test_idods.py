'''
Created on Jan 10, 2014

@author: dejan.dezman@cosylab.com
'''

import unittest
import os

from dataapi.pyidods.idods import idods

from preparerdb import connect, cleanvendor, cleancomponenttype

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
        cleanvendor(['test vendor']);

        # Save new vendor
        self.api._savevendor('test vendor');

        # Test retrieving vendor by name
        result = self.api._retrievevendor('test vendor');
        self.assertEqual(result[0][1], 'test vendor', 'Verdor retrieved')

        # Test retrieving vendor without a name
        self.assertRaises(AttributeError, self.api._retrievevendor, None)

    '''
    Test different options of retrieving component type
    '''
    def testRetrieveComponentType(self):

        # Save new component type
        self.api.savecomponenttype('test cmpnt', 'test description');
        self.api.savecomponenttype('test cmpnt2', 'test description');

        # Test retrieving component type by whole name
        result = self.api.retrievecomponenttype('test cmpnt')
        keys = result.keys()
        self.assertEqual(result[keys[0]]['name'], 'test cmpnt', 'Correct component type retrieved')

        # If we insert * as a name, al component types should be returned
        result = self.api.retrievecomponenttype('*')
        self.assertTrue(len(result) > 1, "We got more than one result back from the database")

        # If we insert wilcard character into the name parameter, all the results matching this criteria should be returned
        result = self.api.retrievecomponenttype('*test*')
        keys = result.keys()
        self.assertEqual(result[keys[0]]['name'], 'test cmpnt', 'Correct component type retrieved')

        # If we do not include name, we should get an Exception
        self.assertRaises(AttributeError, self.api.retrievecomponenttype, None);

        # Test retrieving component type by whole desciprtion
        result = self.api.retrievecomponenttype('*', 'test description');
        keys = result.keys()
        self.assertEqual(result[keys[0]]['description'], 'test description', 'Correct component type retrieved')


        # Test retrieving component type by description with wildcard characters
        result = self.api.retrievecomponenttype('*', '*descripti*');
        keys = result.keys()
        self.assertEqual(result[keys[0]]['description'], 'test description', 'Correct component type retrieved')

if __name__ == '__main__':
    unittest.main()