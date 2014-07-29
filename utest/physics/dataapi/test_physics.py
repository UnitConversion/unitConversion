'''
Created on Jun 26, 2014

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

from pyphysics.physics import physics


class TestIdods(unittest.TestCase):

    def cleanTables(self):
        cleanDB()

    def setUp(self):
        self.con = connect()
        self.api = physics(self.con)
        self.cleanTables()

    def tearDown(self):
        self.cleanTables()
        self.con.close()

    def testRotCoilData(self):
        '''
        Test rot coil data
        '''
        cmpnt = self.api.saveComponentType('cmpnt')
        inv = self.api.saveInventory('inv', cmpnt, 'asd', 'das', None)
        rcd = self.api.saveRotCoilData(inv, 'alias2')
        self.assertNotEqual(rcd, 0)

        # Retrieve rot coil data
        data = self.api.retrieveRotCoilData(inv)

        # Test the number of items in the table
        self.assertEqual(len(data), 1)

        # Test update
        self.assertTrue(self.api.updateRotCoilData(rcd, magnet_notes='magnet notes'))

        # Retrieve rot coil data
        data = self.api.retrieveRotCoilData(inv)

        # Test the number of items in the table
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][1], inv)
        self.assertEqual(data[0][2], 'alias2')
        self.assertEqual(data[0][5], 'magnet notes')

    def testHallProbeData(self):
        '''
        Test hall probe data
        '''
        cmpnt = self.api.saveComponentType('cmpnt')
        inv = self.api.saveInventory('inv', cmpnt, 'asd', 'das', None)
        hpd = self.api.saveHallProbeData(inv, 'sub device')
        self.assertNotEqual(hpd, 0)

        # Retrieve hall probe data
        data = self.api.retrieveHallProbeData(inv)

        # Test the number of items in the table
        self.assertEqual(len(data), 1)

        # Test update
        self.assertTrue(self.api.updateHallProbeData(hpd, login_name='admin'))

        # # Retrieve rot coil data
        data = self.api.retrieveHallProbeData(inv)

        # # Test the number of items in the table
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0][1], inv)
        self.assertEqual(data[0][5], 'sub device')
        self.assertEqual(data[0][7], 'admin')

if __name__ == '__main__':
    unittest.main()