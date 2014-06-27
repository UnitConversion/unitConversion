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
from pyphysics.physics import physics


class TestIdods(unittest.TestCase):

    def cleanTables(self):
        cleanDB()

    def setUp(self):
        self.con = connect()
        self.api = municonvdata(self.con)
        self.phyapi = physics(self.con)
        self.cleanTables()

    def tearDown(self):
        self.cleanTables()
        self.con.close()

    def testComponentType(self):
        '''
        Test component type
        '''

        # Save new component types
        cmpnttype = self.api.savecmpnttype('cmpnt', 'desc', 'vendor')
        self.api.savecmpnttype('cmpnt2', 'desc', 'vendor')
        cmpnttype3 = self.api.savecmpnttype('cmpnt3', 'desc')
        cmpnttype4 = self.api.savecmpnttype('cmpnt4', 'desc')

        # Retrieve component type
        objs = self.api.retrievecmpnttype('cmpnt', vendor='vendor2')

        self.assertEqual(len(objs), 0)

        # Retrieve component type
        objs = self.api.retrievecmpnttype('cmpnt', vendor='vendor')

        self.assertEqual(len(objs), 1)
        self.assertEqual(len(objs[0]), 5)
        self.assertEqual(objs[0][0], cmpnttype[0])
        self.assertEqual(objs[0][1], 'cmpnt')
        self.assertEqual(objs[0][2], 'desc')
        self.assertEqual(objs[0][3], 'vendor')

        # Retrieve component types with None for name
        objs = self.api.retrievecmpnttype(None)

        self.assertEqual(len(objs), 0)

        # Retrieve component type
        objs = self.api.retrievecmpnttype('cmpnt3', vendor='vendor')

        self.assertEqual(len(objs), 0)

        # Retrieve component type
        objs = self.api.retrievecmpnttype('cmpnt3')

        self.assertEqual(len(objs), 1)
        self.assertEqual(len(objs[0]), 3)
        self.assertEqual(objs[0][0], cmpnttype3)
        self.assertEqual(objs[0][1], 'cmpnt3')
        self.assertEqual(objs[0][2], 'desc')

        # Save existing component type
        self.assertRaises(ValueError, self.api.savecmpnttype, 'cmpnt3', 'desc')

        # Save existing component type just to connect it to vendor
        res = self.api.savecmpnttype('cmpnt3', 'desc', 'vendor')

        # Tuple should be returned
        self.assertEqual(len(res), 2)

        # Save existing component type just to connect it to non existing vendor
        res = self.api.savecmpnttype('cmpnt3', 'desc', 'vendor12')

        cvmap = self.phyapi.retrieveComponentTypeVendor(res[0], res[1])

        # There should be a map between component type and newly created vendor
        self.assertEqual(len(cvmap), 1)

        # Tuple should be returned
        self.assertEqual(len(res), 2)

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
        typeid = self.api.savecmpnttype('component type', 'desc', 'vendor')

        # Save inventory
        invid = self.api.saveinventory('bane', 'component type', 'vendor')

        # Prepare property template
        tmpltid = self.api.saveinventoryproptmplt('prop', typeid[0])

        # Save inventory property with value set to int
        self.assertRaises(Exception, self.api.saveinventoryprop, 1, invid, tmpltid)

        # Normal save
        propid = self.api.saveinventoryprop('1', invid, tmpltid)

        # Save again with different value but same ids
        self.assertRaises(Exception, self.api.saveinventoryprop, '2', invid, tmpltid)

        # Retrieve with all parameters set to None
        props = self.api.retrieveinventoryprop(None, None, '1')

        # Test length and value
        self.assertEqual(len(props), 0)

        # Retrieve with all parameters set to None
        props = self.api.retrieveinventoryprop(invid, tmpltid, '1')

        # Test length and value
        self.assertEqual(len(props), 1)

        # Retrieve with all parameters set to None
        props = self.api.retrieveinventoryprop(invid, None, '1')

        # Test length and value
        self.assertEqual(len(props), 0)

        # Retrieve with all parameters set to None
        props = self.api.retrieveinventoryprop(None, tmpltid, '1')

        # Test length and value
        self.assertEqual(len(props), 0)

        # Update with all parameters set to None
        self.assertRaises(Exception, self.api.updateinventoryprop, None, None, None)

        # Update with ids set to None
        self.assertRaises(Exception, self.api.updateinventoryprop, '3', None, None)

        # Normal update
        self.assertTrue(self.api.updateinventoryprop('3', invid, tmpltid))

        # Retrieve and check value
        props = self.api.retrieveinventoryprop(invid, tmpltid)

        self.assertEqual(props[0][1], '3')

    def testInventory(self):
        '''
        Test inventory
        '''

        # Prepare component type
        typeid = self.api.savecmpnttype('component type', 'desc', 'vendor')

        # Save inventory with int serial
        self.assertRaises(Exception, self.api.saveinventory, 123, 'component type', 'vendor')

        # Save inventory without vendor
        self.assertRaises(Exception, self.api.saveinventory, '123', 'component type', None)

        # Save inventory with vendor not connected to component type
        self.assertRaises(Exception, self.api.saveinventory, '123', 'component type', 'vendor2')

        # Normal save
        invid = self.api.saveinventory('bane', 'component type', 'vendor')

        # Check id
        self.assertNotEqual(invid, 0)

        # Retrieve inventory
        res = self.api.retrieveinventory('bane')

        self.assertEqual(res[0][1], invid)
        self.assertEqual(res[0][4], 'bane')
        self.assertEqual(res[0][5], 'component type')
        self.assertEqual(res[0][7], 'vendor')

    def testInstall(self):
        '''
        Test install
        '''

        # Prepare component type
        typeid = self.api.savecmpnttype('component type', 'desc', 'vendor')
        typeid = typeid[0]

        # Save install
        installid = self.api.saveinstall('name', typeid, 'loc')

        # Test returned id
        self.assertNotEqual(installid, 0)

        # Retrieve install by name
        installObj = self.api.retrieveinstall('name')

        # There should be one record
        self.assertEqual(len(installObj), 1)

        # Prepare component type
        typeid = self.api.savecmpnttype('component type2', 'desc')

        # Save install
        installid = self.api.saveinstall('name2', typeid, 'loc')

        # Test returned id
        self.assertNotEqual(installid, 0)

        # Retrieve install by name
        installObj = self.api.retrieveinstall('name2')

        # There should be one record
        self.assertEqual(len(installObj), 1)

    def testInventoryToInstall(self):
        '''
        Test inventory to install
        '''

        # Prepare component type
        typeid = self.api.savecmpnttype('component type', 'desc', 'vendor')
        typeid = typeid[0]

        # Prepare install
        installid = self.api.saveinstall('name', typeid, 'loc')
        installid2 = self.api.saveinstall('name2', typeid, 'loc')

        # Prepare inventory
        invid = self.api.saveinventory('bane', 'component type', 'vendor')
        invid2 = self.api.saveinventory('bane2', 'component type', 'vendor')

        # Try with none parameters
        self.assertRaises(ValueError, self.api.inventory2install, None, None)
        self.assertRaises(ValueError, self.api.inventory2install, installid, None)
        self.assertRaises(ValueError, self.api.inventory2install, None, invid)

        # Normal save
        ii = self.api.inventory2install(installid, invid)

        self.assertNotEqual(ii, 0)

        # Normal save again
        ii = self.api.inventory2install(installid, invid)

        self.assertNotEqual(ii, 0)

        # Update link
        self.assertRaises(Exception, self.api.updateinventory2install, installid, None)
        self.assertRaises(Exception, self.api.updateinventory2install, None, invid2)
        self.assertRaises(Exception, self.api.updateinventory2install, None, None)

        # Normal save
        ii = self.api.inventory2install(installid, invid2)

        # Normal save
        ii = self.api.inventory2install(installid2, invid2)

        # Expecting exception
        self.assertRaises(ValueError, self.api.inventory2install, installid2, invid)

if __name__ == '__main__':
    unittest.main()