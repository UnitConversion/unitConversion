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

    def testComponentTypeProperty(self):
        '''
        Test component type property
        '''

        # Prepare component type
        typeid = self.api.savecmpnttype('cmpnt', 'desc', 'vendor')
        typeid = typeid[0]

        # Prepare component type property type
        typepropid = self.api.savecmpnttypeproptype('name', 'desc')

        # Save property
        self.api.savecmpnttypeprop("1", typeid, typepropid)

        # Check value exception
        self.assertRaises(Exception, self.api.savecmpnttypeprop, 1, typeid, typepropid)

        # Try to set value again
        self.assertRaises(ValueError, self.api.savecmpnttypeprop, "2", typeid, typepropid)

        # Test mysql error
        self.assertRaises(Exception, self.api.savecmpnttypeprop, "2", typepropid, typeid)

        # Retrieve property
        prop = self.api.retrievecmpnttypeprop(typeid, typepropid)

        # Check value
        self.assertEqual(prop[0][1], '1')

        # Update with int value
        self.assertRaises(Exception, self.api.updatecmpnttypeprop, 1, typeid, typepropid)

        # Update undefined property
        self.assertRaises(Exception, self.api.updatecmpnttypeprop, '1', 123, 321)

        # Successfully update
        self.assertTrue(self.api.updatecmpnttypeprop('3', typeid, typepropid))

        # Retrieve property
        prop = self.api.retrievecmpnttypeprop(typeid, typepropid)

        # Check value
        self.assertEqual(prop[0][1], '3')

    def testInventoryPropertyTemplate(self):
        '''
        Test inventory property template
        '''

        # Prepare component type
        typeid = self.api.savecmpnttype('component type', 'desc')

        # Save template with int name
        self.assertRaises(Exception, self.api.saveinventoryproptmplt, 123, 321)

        # Save template
        templateid = self.api.saveinventoryproptmplt('tmplt', typeid, 'desc', 'default', 'units')

        # Save template with existing name
        self.assertRaises(Exception, self.api.saveinventoryproptmplt, 'tmplt', typeid)

        # Retrieve with int name
        self.assertRaises(Exception, self.api.retrieveinventoryproptmplt, 12)

        # Normal retrieve
        template = self.api.retrieveinventoryproptmplt('tmplt')

        # Test id
        self.assertEqual(template[0][0], templateid)

        # Test name
        self.assertEqual(template[0][1], 'tmplt')

        # Test desc
        self.assertEqual(template[0][2], 'desc')

        # Test default
        self.assertEqual(template[0][3], 'default')

        # Test units
        self.assertEqual(template[0][4], 'units')

    def testInventoryProperty(self):
        '''
        Test inventory property
        '''

        # Prepare component type
        typeid = self.api.savecmpnttype('component type', 'desc')

        # prepare inventory
        #invid = self.api.saveinventory('123', 'component type', None)

if __name__ == '__main__':
    unittest.main()