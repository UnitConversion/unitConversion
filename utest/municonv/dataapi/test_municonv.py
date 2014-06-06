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

from pymuniconv.municonvdata import municonvdata


class TestIdods(unittest.TestCase):

    def cleanTables(self):
        cleanDB()

    def setUp(self):
        self.con = connect()
        self.api = municonvdata(self.con)
        self.cleanTables()

    def tearDown(self):
        self.cleanTables()
        self.con.close()

    def testComponentType(self):
        '''
        Test component type
        '''

        # Save new component types
        self.api.savecmpnttype('cmpnt', 'desc', 'vendor')
        self.api.savecmpnttype('cmpnt2', 'desc', 'vendor')

        # Retrieve component type
        objs = self.api.retrievecmpnttype('cmpnt', vendor='vendor2')

        self.assertEqual(len(objs), 0)

        # Retrieve component type
        objs = self.api.retrievecmpnttype('cmpnt', vendor='vendor')

        self.assertEqual(len(objs), 1)

        # Retrieve component types with None for name
        objs = self.api.retrievecmpnttype(None)

        self.assertEqual(len(objs), 0)

    def testComponentTypePropertyType(self):
        '''
        Test component type property type
        '''

        # Save it
        self.api.savecmpnttypeproptype('name', 'desc')

        # Try to save another one with the same name
        self.assertRaises(Exception, self.api.savecmpnttypeproptype, 'name')

        # Retrieve it
        typeObj = self.api.retrievecmpnttypeproptype('name', 'desc')

        # Test it
        self.assertEqual(len(typeObj), 1)

        # If retrieved with name set to None it should return an exception
        self.assertRaises(Exception, self.api.retrievecmpnttypeproptype, None)

if __name__ == '__main__':
    unittest.main()