'''
Created on Aug 20, 2013

@author: shengb
@updated: dejan.dezman@cosylab.com Mar 19, 2014
'''

import unittest

import json
from pyactiveinterlock.epsai import epsai
from activeinterlock.rdbutils import (close, connect)

class Test(unittest.TestCase):

    def __cleanrdb(self):
        '''
        clean up existing data
        '''

        sql = '''
        delete from active_interlock_prop;
        delete from active_interlock_device;
        delete from active_interlock;
        delete from active_interlock_logic;
        delete from active_interlock_prop_type;
        '''
    
        self.conn.cursor().execute(sql)
        self.conn.commit()

    def setUp(self):
        self.conn = connect()
        self.api = epsai(self.conn)

        # clean active interlock RDB before use.
        self.__cleanrdb()

    def tearDown(self):
        # clean active interlock RDB after finish
        self.__cleanrdb()
        close(self.conn)

    '''
    Test saving and retrieving active interlock
    '''
    def testActiveInterlockHeader(self):
        
        # Save active interlock
        aih = self.api.saveActiveInterlockHeader('desc', 'admin')
        
        # Retrieve active interlock
        ai = self.api.retrieveActiveInterlockHeader(None, aih['id'])
        aiKeys = ai.keys()
        aiObject = ai[aiKeys[0]]
        
        # Test description
        self.assertEqual(aiObject['description'], 'desc')
        
        # Test created by
        self.assertEqual(aiObject['created_by'], 'admin')
        
        # Test status
        self.assertEqual(aiObject['status'], 0)

    def testCopyActiveInterloc(self):
        
        # Save active interlock
        self.api.saveActiveInterlockHeader('header desc', 'admin')
        
        # Prepare logic
        self.api.saveActiveInterlockLogic('log', 'shape', 'logic', 10, 'author')
        
        # Save device
        devId = self.api.saveDevice(0, 'device name', 'bm', 'log', {})
        
        for prop in self.api.bm_props:
            self.api.saveActiveInterlockProp(devId['id'], prop[0], 'sth')
        
        # Try to change status
        self.assertTrue(self.api.updateActiveInterlockStatus(None, 0, 2, "admin"))
        
        # The number of datasets with status 0 should be 0
        status0 = self.api.retrieveActiveInterlockHeader(0)
        self.assertEqual(len(status0), 0)
        
        # The number of datasets with status 2 should be 1
        status1 = self.api.retrieveActiveInterlockHeader(2)
        self.assertEqual(len(status1), 1)
        
        # Copy AI to editable
        self.assertTrue(self.api.copyActiveInterlock(2, "user"))
        
        # The number of datasets with status 0 should be 1
        status0 = self.api.retrieveActiveInterlockHeader(0)
        self.assertEqual(len(status0), 1)
        
        # The number of datasets with status 2 should be 1
        status1 = self.api.retrieveActiveInterlockHeader(2)
        self.assertEqual(len(status1), 1)

    def testActiveInterlockStatusChange(self):
        
        # Save active interlock
        self.api.saveActiveInterlockHeader('header desc', 'admin')
        
        # Prepare logic
        self.api.saveActiveInterlockLogic('log', 'shape', 'logic', 10, 'author')
        
        # Save device
        self.api.saveDevice(0, 'device name', 'bm', 'log', {'cell': 'test'})
        
        # Try to change status
        self.assertTrue(self.api.updateActiveInterlockStatus(None, 0, 1, "admin"))
        
        # The number of datasets with status 0 should be 0
        status0 = self.api.retrieveActiveInterlockHeader(0)
        self.assertEqual(len(status0), 0)
        
        # The number of datasets with status 1 should be 1
        status1 = self.api.retrieveActiveInterlockHeader(1)
        self.assertEqual(len(status1), 1)
        
        # Save another active interlock
        self.api.saveActiveInterlockHeader('second header desc', 'admin')
        
        # Save another device
        self.api.saveDevice(0, 'device name2', 'bm', 'log', {'cell': 'test'})
        
        # The number of datasets with status 0 should be 1
        status0 = self.api.retrieveActiveInterlockHeader(0)
        self.assertEqual(len(status0), 1)
        
        # The number of datasets with status 1 should be 1
        status1 = self.api.retrieveActiveInterlockHeader(1)
        self.assertEqual(len(status1), 1)
        
        # Try to change status, the old one should be removed
        self.assertTrue(self.api.updateActiveInterlockStatus(None, 0, 1, "admin"))
        
        # The number of datasets with status 0 should be 0
        status0 = self.api.retrieveActiveInterlockHeader(0)
        self.assertEqual(len(status0), 0)
        
        # The number of datasets with status 1 should be 1
        status1 = self.api.retrieveActiveInterlockHeader(1)
        self.assertEqual(len(status1), 1)

    def testActiveInterlockDownload(self):
        
        # Save active interlock
        self.api.saveActiveInterlockHeader('header desc', 'admin')
        
        # Prepare logic
        self.api.saveActiveInterlockLogic('log', 'shape', 'logic', 10, 'author')
        
        # Save device
        self.api.saveDevice(0, 'device name', 'bm', 'log', {'cell': 'test'})
        
        # Try to change status
        self.assertTrue(self.api.updateActiveInterlockStatus(None, 0, 1, "admin"))
        
        self.api.downloadActiveInterlock(1, "admin")
        
        # The number of datasets with status 1 should be 1
        status1 = self.api.retrieveActiveInterlockHeader(1)
        self.assertEqual(len(status1), 0)
        
        # The number of datasets with status 2 should be 1
        status2 = self.api.retrieveActiveInterlockHeader(2)
        self.assertEqual(len(status2), 1)

    '''
    Test saving and retrieving devices
    '''
    def testDevice(self):

        # Prepare active interlock header
        aih = self.api.saveActiveInterlockHeader('desc', 'admin')
        
        # Prepare logic
        self.api.saveActiveInterlockLogic('name', 'shape', 'logic', 10, 'author')
        
        # Save device
        savedDevice = self.api.saveDevice(0, 'device name', 'bm', 'name', {'cell': 'test'})
        
        # Retrieve device
        device = self.api.retrieveDevice(aih['id'], None, 'device name', 'bm')
        deviceObject = device[savedDevice['id']]
        
        # Test device name
        self.assertEqual(deviceObject['name'], 'device name')
        
        # Test definition
        self.assertEqual(deviceObject['definition'], 'bm')
        
        # Test logic name
        self.assertEqual(deviceObject['logic'], 'name')
        
        # Test retrieving a property
        self.assertEqual(deviceObject['cell'], 'test')
        
        # Retrieve logic usage
        result = self.api.isLogicUsed("name")
        
        # Test usage count
        self.assertEqual(result['num'], 1)

    '''
    Test saving and retrieving active interlock property type
    '''
    def testPropType(self):
        
        # Save property type
        self.api.saveActiveInterlockPropType('length', 'm', 'some length')
        
        # Retrieve property type
        propType = self.api.retrieveActiveInterlockPropType('length')
        typeKeys = propType.keys()
        typeObject = propType[typeKeys[0]]
        
        # Test name
        self.assertEqual(typeObject['name'], 'length')
        
        # Test unit
        self.assertEqual(typeObject['unit'], 'm')
        
        # Test description
        self.assertEqual(typeObject['description'], 'some length')
        
        # Try to save prop type with same name and unit
        self.assertRaises(ValueError, self.api.saveActiveInterlockPropType, 'length', unit='m')

    '''
    Test saving, retrieving and updating active interlock property
    '''
    def testProp(self):
        
        # Save property type
        self.api.saveActiveInterlockPropType('length', 'm', 'some length')
        self.api.saveActiveInterlockPropType('length2', 'm', 'approvable')
        
        # Prepare active interlock header
        self.api.saveActiveInterlockHeader('desc', 'admin')
        
        # Prepare logic
        self.api.saveActiveInterlockLogic('name', 'shape', 'logic', 10, 'author')
        
        # Save device
        savedDevice = self.api.saveDevice(0, 'device name', 'bm', 'name', {'length': 'test'})
        
        # Save property
        self.api.saveActiveInterlockProp(savedDevice['id'], 'length2', '123')
        
        # Retrieve property
        prop = self.api.retrieveActiveInterlockProp(savedDevice['id'], 'length2')
        propKeys = prop.keys()
        propObject = prop[propKeys[0]]
        
        # Test value
        self.assertEqual(propObject['value'], '123')
        
        # Update property
        self.assertTrue(self.api.updateActiveInterlockProp(savedDevice['id'], 'length2', '1234'))
        
        # Retrieve property
        prop = self.api.retrieveActiveInterlockProp(savedDevice['id'], 'length2')
        propKeys = prop.keys()
        propObject = prop[propKeys[0]]
        
        # Test value
        self.assertEqual(propObject['value'], '1234')
        
        # Test status
        self.assertEqual(propObject['status'], 2)
        
        # Try to approve length2 property
        self.assertTrue(self.api.approveCells(savedDevice['id'], json.dumps(['length2'])))
        
        # Retrieve property
        prop = self.api.retrieveActiveInterlockProp(savedDevice['id'], 'length2')
        propKeys = prop.keys()
        propObject = prop[propKeys[0]]
        
        # Test status
        self.assertEqual(propObject['status'], 3)

    '''
    Test saving and retrieving logic
    '''
    def testLogic(self):
        
        # Save logic
        self.api.saveActiveInterlockLogic('name', 'shape', 'logic', 10, 'author')
        
        # Retrieve logic
        logic = self.api.retrieveActiveInterlockLogic('name')
        logicKeys = logic.keys()
        logicObject = logic[logicKeys[0]]
        
        # Test name
        self.assertEqual(logicObject['name'], 'name')
        
        # Test shape
        self.assertEqual(logicObject['shape'], 'shape')
        
        # Test logic
        self.assertEqual(logicObject['logic'], 'logic')
        
        # Test code
        self.assertEqual(logicObject['code'], 10)
        
        # Test author
        self.assertEqual(logicObject['created_by'], 'author')
        
        # Test updating logic
        self.assertTrue(self.api.updateActiveInterlockLogic(logicObject['id'], code=11))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    