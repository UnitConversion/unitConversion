'''
Created on Sep 10, 2013

@author: shengb
'''
import os

import unittest
import logging
import requests
import random

import inspect
import base64

import json


from activeinterlock.rdbutils import (close, connect)

from activeinterlockpy.activeinterlockclient import ActiveInterlockClient

class Test(unittest.TestCase):

    def __cleanrdb(self):
        '''clean up existing data
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
        self.__url = 'http://localhost:8000'

        self.aiclient = ActiveInterlockClient(BaseURL=self.__url)

        self.scale = random.uniform(1.0, 2.0)
        self.aie_prop_type = {'label': ['name', 'unit', 'description'],
                              'name': ['aihal', 'aival', 'aivol', 'aihol', 'safecurrent', 's', 'offset'],
                              'unit': ['mrad', 'mrad', 'mm', 'mm', 'mA', 'm', 'm'],
                              'description': ['active interlock horizontal angle limit',
                                              'active interlock vertical angle limit',
                                              'active interlock vertical offset limit',
                                              'active interlock horizontal offset limit',
                                              'safe beam current to operate machine',
                                              'position in a real lattice',
                                              'position offset relative to center of a straight section'],
                              }
        self.aie_logic = {'label': ['name', 'shape', 'logic', 'code', 'author'],
                          'name': [u'AIE-BM', u'AIE-ID-B', u'AIE-ID-A', u'AIE-ID-D', u'AIE-ID-C'],
                          'shape': [u'diamond',
                                    u'diamond',
                                    u'rectangular',
                                    u'rect+small offset',
                                    u'rect+optimal offset'],
                          'author': ['unit test', 'unit test', 'unit test', 'unit test', 'unit test'],
                          'code': [10L, 10L, 20L, 22L, 21L],
                          'logic': [u'(|x1|<AIOL)&(|x2|<AIOL)',
                                    u'(|x1|<AIOL)&(|x2|<AIOL)',
                                    u'(|(x2-x1)*(s3-s1)/(s2-s1)|<AIOL)&(|(x2-x1)/(s2-s1)|<AIAL)',
                                    u'(|x1|<AIOL)&(|x2|<AIOL)&(|(x2-x1)*(s3-s1)/(s2-s1)|<AIOL)&(|(x2-x1)/(s2-s1)|<AIAL)',
                                    u'(|x1|<AIOL)&(|x2|<AIOL)&(|(x2-x1)/(s2-s1)|<AIAL)'],
                          }

        self.aie_data = { 'label': ['up_name',
                                    'up_definition',
                                    'up_offset',
                                    'up_aihol',
                                    'up_aivol',
                                    'name',
                                    'definition',
                                    'logicname',
                                    'shape',
                                    's',
                                    'offset',
                                    'safecurent',
                                    'aihol',
                                    'aivol',
                                    'aihal',
                                    'aival',
                                    'down_name',
                                    'down_definition',
                                    'down_offset',
                                    'down_aihol',
                                    'down_aivol'],
                         'units': ['',
                                   '',
                                   u'm',
                                   u'mm',
                                   u'mm',
                                   '',
                                   '',
                                   '',
                                   '',
                                   u'm',
                                   u'm',
                                   u'mA',
                                   u'mm',
                                   u'mm',
                                   u'mrad',
                                   u'mrad',
                                   '',
                                   '',
                                   u'm',
                                   u'mm',
                                   u'mm'],

                         'aihal': [0.25, None, None, None, 0.25, 0.25],
                         'aihol': [0.5, None, None, None, 0.5, 0.5],
                         'aival': [0.25, None, None, None, 0.25, 0.25],
                         'aivol': [0.5, None, None, None, 0.5, 0.5],
                         'definition': [u'AIE-ID',
                                        u'AIE-ID',
                                        u'AIE-ID',
                                        u'AIE-ID',
                                        u'AIE-ID',
                                        u'AIE-ID'],
                         'down_aihol': [None, 1.5, 0.75, 0.75, 1.0, 1.5],
                         'down_aivol': [None, 1.5, 1.5, 1.5, 1.0, 1.5],
                         'down_definition': [u'MONI', u'MONI', u'MONI', u'MONI', u'MONI', u'MONI'],
                         'down_name': [u'PU4G1C03A',
                                       u'PU2G1C15A',
                                       u'PU2G1C02A',
                                       u'PU4G1C02A',
                                       u'PU2G1C10A',
                                       u'PU2G1C19A'],
                         'down_offset': [2.67863, 4.0, 0.0, 4.0, 4.0, 4.0],
                         'logicname': [u'AIE-ID-A',
                                       u'AIE-ID-B',
                                       u'AIE-ID-B',
                                       u'AIE-ID-B',
                                       u'AIE-ID-D',
                                       u'AIE-ID-C'],
                         'name': [u'MAD1G1C03A',
                                  u'MAD1G1C15A',
                                  u'MAD1G1C02A',
                                  u'MAD2G1C02A',
                                  u'MAD1G1C10A',
                                  u'MAD1G1C19A'],
                         'offset': [0.0, 0.0, -2.0, 2.0, 0.0, 0.0],
                         's': [None, None, None, None, None, None],
                         'safecurent': [2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
                         'shape': [u'rectangular',
                                   u'diamond',
                                   u'diamond',
                                   u'diamond',
                                   u'rect+small offset',
                                   u'rect+optimal offset'],
                         'up_aihol': [None, 1.5, 0.75, 0.75, 1.0, 1.5],
                         'up_aivol': [None, 1.5, 1.5, 1.5, 1.0, 1.5],
                         'up_definition': [u'MONI', u'MONI', u'MONI', u'MONI', u'MONI', u'MONI'],
                         'up_name': [u'PU1G1C03A',
                                     u'PU1G1C15A',
                                     u'PU1G1C02A',
                                     u'PU2G1C02A',
                                     u'PU1G1C10A',
                                     u'PU1G1C19A'],
                         'up_offset': [-2.54278, -4.0, -4.0, 0.0, -4.0, -4.0]}

        f = lambda x: x*self.scale if x !=None else x
        self.aie_data2 = { 'label': ['up_name',
                                    'up_definition',
                                    'up_offset',
                                    'up_aihol',
                                    'up_aivol',
                                    'name',
                                    'definition',
                                    'logicname',
                                    'shape',
                                    's',
                                    'offset',
                                    'safecurent',
                                    'aihol',
                                    'aivol',
                                    'aihal',
                                    'aival',
                                    'down_name',
                                    'down_definition',
                                    'down_offset',
                                    'down_aihol',
                                    'down_aivol'],
                         'units': ['',
                                   '',
                                   u'm',
                                   u'mm',
                                   u'mm',
                                   '',
                                   '',
                                   '',
                                   '',
                                   u'm',
                                   u'm',
                                   u'mA',
                                   u'mm',
                                   u'mm',
                                   u'mrad',
                                   u'mrad',
                                   '',
                                   '',
                                   u'm',
                                   u'mm',
                                   u'mm'],

                         'aihal': [f(x) for x in self.aie_data['aihal']],
                         'aihol': [f(x) for x in self.aie_data['aihol']],
                         'aival': [f(x) for x in self.aie_data['aival']],
                         'aivol': [f(x) for x in self.aie_data['aivol']],
                         'definition': [u'AIE-ID',
                                        u'AIE-ID',
                                        u'AIE-ID',
                                        u'AIE-ID',
                                        u'AIE-ID',
                                        u'AIE-ID'],
                         'down_aihol': [f(x) for x in self.aie_data['down_aihol']],
                         #[None, 1.5, 0.75, 0.75, 1.0, 1.5],
                         'down_aivol': [f(x) for x in self.aie_data['down_aivol']],
                         #[None, 1.5, 1.5, 1.5, 1.0, 1.5],
                         'down_definition': [u'MONI', u'MONI', u'MONI', u'MONI', u'MONI', u'MONI'],
                         'down_name': [u'PU4G1C03A',
                                       u'PU2G1C15A',
                                       u'PU2G1C02A',
                                       u'PU4G1C02A',
                                       u'PU2G1C10A',
                                       u'PU2G1C19A'],
                         'down_offset': [f(x) for x in self.aie_data['down_offset']],
                         #[2.67863, 4.0, 0.0, 4.0, 4.0, 4.0],
                         'logicname': [u'AIE-ID-A',
                                       u'AIE-ID-B',
                                       u'AIE-ID-B',
                                       u'AIE-ID-B',
                                       u'AIE-ID-D',
                                       u'AIE-ID-C'],
                         'name': [u'MAD1G1C03A',
                                  u'MAD1G1C15A',
                                  u'MAD1G1C02A',
                                  u'MAD2G1C02A',
                                  u'MAD1G1C10A',
                                  u'MAD1G1C19A'],
                         'offset': [f(x) for x in self.aie_data['offset']],
                         #[0.0, 0.0, -2.0, 2.0, 0.0, 0.0],
                         's': [None, None, None, None, None, None],
                         'safecurent': [f(x) for x in self.aie_data['safecurent']],
                         #[2.0, 2.0, 2.0, 2.0, 2.0, 2.0],
                         'shape': [u'rectangular',
                                   u'diamond',
                                   u'diamond',
                                   u'diamond',
                                   u'rect+small offset',
                                   u'rect+optimal offset'],
                         'up_aihol': [f(x) for x in self.aie_data['up_aihol']],
                         #[None, 1.5, 0.75, 0.75, 1.0, 1.5],
                         'up_aivol': [f(x) for x in self.aie_data['up_aivol']],
                         #[None, 1.5, 1.5, 1.5, 1.0, 1.5],
                         'up_definition': [u'MONI', u'MONI', u'MONI', u'MONI', u'MONI', u'MONI'],
                         'up_name': [u'PU1G1C03A',
                                     u'PU1G1C15A',
                                     u'PU1G1C02A',
                                     u'PU2G1C02A',
                                     u'PU1G1C10A',
                                     u'PU1G1C19A'],
                         'up_offset': [f(x) for x in self.aie_data['up_offset']],
                         #[-2.54278, -4.0, -4.0, 0.0, -4.0, -4.0]
                         }
        # clean active interlock RDB before use.
        self.__cleanrdb()

        try:
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
            self.client = requests.session()
        except:
            raise

    def tearDown(self):
        # clean active interlock RDB after finish
        self.__cleanrdb()
        close(self.conn)

    def _checkdata(self, origdata, data):
        #check values
        for i in range(len(origdata['name'])):
            name = origdata['name'][i]
            idx = data['name'].index(name)
            for col in origdata['label']:
                if origdata[col][i] == None:
                    self.assertEqual(origdata[col][i],
                                     data[col][idx],
                                     'data does not match each other for %s property %s'%(name,col))
                else:
                    try:
                        # numeric number
                        self.assertAlmostEquals(origdata[col][i],
                                                float(data[col][idx]),
                                                places=5,
                                                msg='data does not match each other for %s property %s, should be %s, but got %s'%(name,col, origdata[col][i], data[col][idx]),
                                                )
                    except ValueError:
                        # string property
                        self.assertEqual(str(origdata[col][i]),
                                         data[col][idx],
                                         'data does not match each other for %s property %s'%(name,col))
    
    def test_activeinterlocklogic(self):
        ''''''
        self.__cleanrdb()
        labels = self.aie_logic['label']
        logiccount = len(self.aie_logic[labels[0]])
        
        ids = []
        # save a new entry
        for i in range(logiccount):
            ids.append(self.aiclient.saveactiveinterlocklogic(self.aie_logic['name'][i], 
                                                        self.aie_logic['shape'][i], 
                                                        self.aie_logic['logic'][i], 
                                                        self.aie_logic['code'][i], 
                                                        author = self.aie_logic['author'][i]
                                                        )
                       )
        
        aie_logic = self.aie_logic.copy()
        aie_logic['id']=ids

        # save an existing entry
        # should raise a HTTPError
        for i in range(logiccount):
            self.assertRaises(requests.HTTPError, 
                              self.aiclient.saveactiveinterlocklogic,
                              self.aie_logic['name'][i], 
                              self.aie_logic['shape'][i], 
                              self.aie_logic['logic'][i], 
                              self.aie_logic['code'][i], 
                              self.aie_logic['author'][i]
                              )

        for i in range(logiccount):
            res = self.aiclient.retrieveactiveinterlocklogic(self.aie_logic['name'][i], 
                                                       shape = self.aie_logic['shape'][i], 
                                                       logic = self.aie_logic['logic'][i]
                                                       )
            self.assertEqual(res['code'][0], self.aie_logic['code'][i], 'logic code does not match')
            self.assertEqual(res['id'][0], ids[i], 'internal id does not match')

        # retrieve all logics
        res = self.aiclient.retrieveactiveinterlocklogic('*')
        if res.has_key('date'):
            res.pop('date', None)
        self._checkdata(aie_logic, res)

    def test_activeinterlockproptype(self):
        ''''''
        self.__cleanrdb()
        labels = self.aie_prop_type['label']
        proptypecount = len(self.aie_prop_type[labels[0]])
        
        # check logic table
        for lbs in labels:
            self.assertEqual(proptypecount, len(self.aie_prop_type[lbs]), 
                             'logic table length does not match for column: %s'%(lbs))

        ids=[]
        for i in range(proptypecount):
            ids.append(self.aiclient.saveactiveinterlockproptype(self.aie_prop_type['name'][i],
                                                                 unit=self.aie_prop_type['unit'][i],
                                                                 description=self.aie_prop_type['description'][i] 
                                                                 )
                       )
 
        aie_prop_type = self.aie_prop_type.copy()
        aie_prop_type['id']=ids

        # save an existing entry
        for i in range(proptypecount):
            self.assertRaises(requests.HTTPError, 
                              self.aiclient.saveactiveinterlockproptype,
                              self.aie_prop_type['name'][i],
                              self.aie_prop_type['unit'][i],
                              self.aie_prop_type['description'][i] 
                              )
        
        # test retrieve function
        for i in range(proptypecount):
            res = self.aiclient.retrieveactiveinterlockproptype(self.aie_prop_type['name'][i], 
                                                                unit = self.aie_prop_type['unit'][i], 
                                                                description = self.aie_prop_type['description'][i])
            self.assertEqual(res['id'][0], ids[i], 'internal id does not match')

        # retrieve all ptoperties
        res = self.aiclient.retrieveactiveinterlockproptype('*')
        if res.has_key('date'):
            res.pop('date', None)
        self._checkdata(aie_prop_type, res)

    def test_activeinterlock(self):
        ''''''
        # id has to be a positive integer
        self.assertRaises(requests.HTTPError,
                          self.aiclient.updateactiveinterlockstatus,
                          -1L, 
                          0, 
                          'unit test thru client API')

        # status has to be either 0 (inactive) or 1 (active) in current implementation.
        self.assertRaises(requests.HTTPError,
                          self.aiclient.updateactiveinterlockstatus,
                          0L, 
                          2, 
                          'unit test thru client API')

        self.__cleanrdb()
        #prepare interlock logic
        labels = self.aie_logic['label']
        logiccount = len(self.aie_logic[labels[0]])
        for i in range(logiccount):
            self.aiclient.saveactiveinterlocklogic(self.aie_logic['name'][i], 
                                                   self.aie_logic['shape'][i], 
                                                   self.aie_logic['logic'][i], 
                                                   self.aie_logic['code'][i], 
                                                   author = self.aie_logic['author'][i]
                                                   )
        # prepare property types 
        labels = self.aie_prop_type['label']
        proptypecount = len(self.aie_prop_type[labels[0]])
        for i in range(proptypecount):
            self.aiclient.saveactiveinterlockproptype(self.aie_prop_type['name'][i],
                                                      unit=self.aie_prop_type['unit'][i],
                                                      description=self.aie_prop_type['description'][i] 
                                                      )
        # prepare data set
        # script filename (usually with path)
        # inspect.getfile(inspect.currentframe()) 
        # script directory
        # save first example data set
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
        datafile = 'Ilinski_AI_DB_20130731.xls'
        desc1 = 'Latest data for active interlock published on 2013-07-31'        
        id1 = self.aiclient.saveactiveinterlock(self.aie_data, 
                                                description=desc1, 
                                                datafile='/'.join((path, '../dataapi', datafile)), 
                                                active=True, 
                                                author='unit test')

        # get full data set without raw data
        res = self.aiclient.retrieveactiveinterlock(1, withdata=True)
        self.assertEqual(id1, int(res.keys()[0]), 'key does not match, it should be %s, but got %s'%(id1, res.keys()[0]))
        self.assertTrue(len(res)==1, "Should get 1 data set, but get %s"%len(res))
        
        data = res.values()[0]['data']
        # check all units are same.
        for i in range(len(self.aie_data['label'])):
            colname = self.aie_data['label'][i]
            self.assertEqual(self.aie_data['units'][i], 
                             data['units'][data['label'].index(colname)], 
                             'unit does not match for %s'%colname)
        # check data
        self._checkdata(self.aie_data, data)

        # save second example data set
        desc2='Latest data for active interlock published on 2013-07-31, data scaled by factor %s' %self.scale
        id2 = self.aiclient.saveactiveinterlock(self.aie_data2, 
                                                description=desc2, 
                                                datafile='/'.join((path, '../dataapi', datafile)), 
                                                active=True, 
                                                author='unit test')
        # get full data set without raw data
        res = self.aiclient.retrieveactiveinterlock(1, withdata=True)
        self.assertEqual(id2, int(res.keys()[0]), 'key does not match, it should be %s, but got %s'%(id2, res.keys()[0]))
        self.assertTrue(len(res)==1, "Should get 1 data set, but get %s"%len(res))
        
        data = res.values()[0]['data']
        # check all units are same.
        for i in range(len(self.aie_data2['label'])):
            colname = self.aie_data2['label'][i]
            self.assertEqual(self.aie_data2['units'][i], 
                             data['units'][data['label'].index(colname)], 
                             'unit does not match for %s'%colname)
        # check data
        self._checkdata(self.aie_data2, data)
        
        # get full data set without raw data
        res = self.aiclient.retrieveactiveinterlock('*', withdata=True)
        self.assertTrue(len(res)==2, "Should get 2 data sets, but get %s"%len(res))
        for k, v in res.iteritems():
            if int(k) == id1:
                # id1 is inactive data set
                self._checkdata(self.aie_data, v['data'])
                self.assertEqual(0, v['status'], 'The first data set should be inactive')
            elif int(k) == id2:
                self._checkdata(self.aie_data2, v['data'])
                self.assertEqual(1, v['status'], 'The second data set should be active')
            else:
                raise KeyError('unknown internal id: %s'%k)

        # update active interlock status.
        res = self.aiclient.updateactiveinterlockstatus(id1, 1, 'unit test thru client API')
        self.assertTrue(res, 'Should update status successfully')
        
        # get full data set without raw data
        res = self.aiclient.retrieveactiveinterlock('*', withdata=True)
        self.assertTrue(len(res)==2, "Should get 2 data sets, but get %s"%len(res))
        for k, v in res.iteritems():
            if int(k) == id1:
                # id1 is inactive data set
                self._checkdata(self.aie_data, v['data'])
                self.assertEqual(1, v['status'], 'The first data set should be inactive')
            elif int(k) == id2:
                self._checkdata(self.aie_data2, v['data'])
                self.assertEqual(0, v['status'], 'The second data set should be active')
            else:
                raise KeyError('unknown internal id: %s'%k)

        # update active interlock status. do again. Nothing should be changed.
        res = self.aiclient.updateactiveinterlockstatus(id1, 1, 'unit test thru client API')
        self.assertTrue(not res, 'Should update status successfully')
        
        # get full data set without raw data
        res = self.aiclient.retrieveactiveinterlock('*', withdata=True)
        self.assertTrue(len(res)==2, "Should get 2 data sets, but get %s"%len(res))
        for k, v in res.iteritems():
            if int(k) == id1:
                # id1 is inactive data set
                self._checkdata(self.aie_data, v['data'])
                self.assertEqual(1, v['status'], 'The first data set should be inactive')
            elif int(k) == id2:
                self._checkdata(self.aie_data2, v['data'])
                self.assertEqual(0, v['status'], 'The second data set should be active')
            else:
                raise KeyError('unknown internal id: %s'%k)

        # update active interlock status.
        res = self.aiclient.updateactiveinterlockstatus(id1, 0, 'unit test thru client API')
        self.assertTrue(res, 'Should update data set successfully.')
        
        # get full data set without raw data
        res = self.aiclient.retrieveactiveinterlock('*', withdata=True)
        self.assertTrue(len(res)==2, "Should get 2 data sets, but get %s"%len(res))
        for k, v in res.iteritems():
            if int(k) == id1:
                self._checkdata(self.aie_data, v['data'])
                self.assertEqual(0, v['status'], 'Now all data sets should be inactive')
            elif int(k) == id2:
                self._checkdata(self.aie_data2, v['data'])
                self.assertEqual(0, v['status'], 'Now all data sets should be inactive')
            else:
                raise KeyError('unknown internal id: %s'%k)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()