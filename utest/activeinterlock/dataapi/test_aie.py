'''
Created on Aug 20, 2013

@author: shengb
'''
import os
import inspect

import unittest

import json
import base64
import random

from dataapi.pyactiveinterlock.epsai import epsai
from utest.activeinterlock.dataapi.rdbprepare import (close, connect)

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
        self.aie = epsai(self.conn)
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

    def tearDown(self):
        # clean active interlock RDB after finish
        #self.__cleanrdb()
        close(self.conn)

    def test_activeinterlocklogic(self):
#        print("======test active interlock logic=========")
        # should save successfully
        labels = self.aie_logic['label']
        logiccount = len(self.aie_logic[labels[0]])
        
        # check logic table
        for lbs in labels:
            self.assertEqual(logiccount, len(self.aie_logic[lbs]), 
                             'logic table length does not match for column: %s'%(lbs))
        
        ids=[]
        for i in range(logiccount):
            ids.append(
                self.aie.saveactiveinterlocklogic(self.aie_logic['name'][i], 
                                                  self.aie_logic['shape'][i], 
                                                  self.aie_logic['logic'][i], 
                                                  self.aie_logic['code'][i],
                                                  self.aie_logic['author'][i])
                       )

        # compare with original data
        res = self.aie.retrieveactiveinterlocklogic('*')
        self.assertEqual(ids, res['id'], 'internal id does not match')
        for lbs in labels:
            self.assertEqual(self.aie_logic[lbs], res[lbs], 'column (%s) does not match'%(lbs))
        
        for i in range(logiccount):
            res = self.aie.retrieveactiveinterlocklogic(self.aie_logic['name'][i], 
                                                        shape=self.aie_logic['shape'][i], 
                                                        logic=self.aie_logic['logic'][i] 
                                                        )
            self.assertEqual(res['code'][0], self.aie_logic['code'][i], 'logic code does not match')
            self.assertEqual(res['id'][0], ids[i], 'internal id does not match')
        
        # Be there already, could not be saved again.
        # Should raise a ValueError exception.
        for i in range(logiccount):
            self.assertRaises(ValueError, 
                              self.aie.saveactiveinterlocklogic,
                              self.aie_logic['name'][i], 
                              self.aie_logic['shape'][i], 
                              self.aie_logic['logic'][i], 
                              self.aie_logic['code'][i],
                              self.aie_logic['author'][i]
                              )
#        print("======test active interlock finished=========")
        
    def test_activeinterlockproptype(self):
        ''''''
        # should save successfully
#        print("======test active interlock property type=========")
        labels = self.aie_prop_type['label']
        proptypecount = len(self.aie_prop_type[labels[0]])
        
        # check logic table
        for lbs in labels:
            self.assertEqual(proptypecount, len(self.aie_prop_type[lbs]), 
                             'logic table length does not match for column: %s'%(lbs))

        ids=[]
        for i in range(proptypecount):
            ids.append(
                self.aie.saveactiveinterlockproptype(self.aie_prop_type['name'][i], 
                                                     unit=self.aie_prop_type['unit'][i], 
                                                     description=self.aie_prop_type['description'][i] 
                                                     )
                       )

        # compare with original data
        res = self.aie.retrieveactiveinterlockproptype('*')
        self.assertEqual(ids, res['id'], 'internal id does not match')
        for lbs in labels:
            self.assertEqual(self.aie_prop_type[lbs], res[lbs], 'column (%s) does not match'%(lbs))
        
        for i in range(proptypecount):
            res = self.aie.retrieveactiveinterlockproptype(self.aie_prop_type['name'][i], 
                                                           unit=self.aie_prop_type['unit'][i], 
                                                           )
            self.assertEqual(res['description'][0],
                             self.aie_prop_type['description'][i], 
                             'description does not match')
            self.assertEqual(res['id'][0], ids[i], 'internal id does not match')
        
        # Be there already, could not be saved again.
        # Should raise a ValueError exception.
        for i in range(proptypecount):
            self.assertRaises(ValueError, 
                              self.aie.saveactiveinterlockproptype,
                              self.aie_prop_type['name'][i], 
                              unit=self.aie_prop_type['unit'][i],
                              description=self.aie_prop_type['description'][i] 
                              )
#        print("======test active interlock property type finished=========")
        
        
    def test_activeinterlock(self):
#        print("======test active interlock=========")
        # id has to be a positive integer
        self.assertRaises(ValueError, self.aie.updateactiveinterlockstatus, -1L, 0, 'author')
        
        # status has to be either 0 (inactive) or 1 (active) in current implementation.
        self.assertRaises(AttributeError, self.aie.updateactiveinterlockstatus, 0L, 2, 'author')

        self.__cleanrdb()
        #prepare interlock logic
        labels = self.aie_logic['label']
        logiccount = len(self.aie_logic[labels[0]])
        for i in range(logiccount):
            self.aie.saveactiveinterlocklogic(self.aie_logic['name'][i], 
                                              self.aie_logic['shape'][i], 
                                              self.aie_logic['logic'][i], 
                                              self.aie_logic['code'][i],
                                              self.aie_logic['author'][i])
        # prepare property types 
        labels = self.aie_prop_type['label']
        proptypecount = len(self.aie_prop_type[labels[0]])
        for i in range(proptypecount):
            self.aie.saveactiveinterlockproptype(self.aie_prop_type['name'][i], 
                                                 unit=self.aie_prop_type['unit'][i], 
                                                 description=self.aie_prop_type['description'][i] 
                                                 )
        #
        # prepare data set

        # script filename (usually with path)
        #inspect.getfile(inspect.currentframe()) 
        # script directory
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 

        datafile = 'Ilinski_AI_DB_20130731.xls'
        # read raw data in
        exceldata=None
        with file('/'.join((path, datafile)), 'r') as f:
            bindata = base64.b64encode(f.read())
            exceldata=json.dumps({'name': datafile,
                                  'data': bindata})

        # save first example data set
        desc1 = 'Latest data for active interlock published on 2013-07-31'
        self.aie.saveactiveinterlock(self.aie_data, 
                                     description=desc1, 
                                     rawdata=exceldata, 
                                     active=True, 
                                     author='unit test')
        
        # get full data set without raw data
        res = self.aie.retrieveactiveinterlock('1', withdata=True, rawdata=False)
        self.assertEqual(res.values()[0]['status'], 1, 'Wrong status')
        self.assertEqual(res.values()[0]['description'], desc1, 'Description does not match each other.')

        data = res.values()[0]['data']
        # check all units are same.
        for i in range(len(self.aie_data['label'])):
            colname = self.aie_data['label'][i]
            self.assertEqual(self.aie_data['units'][i], 
                             data['units'][data['label'].index(colname)], 
                             'unit does not match for %s'%colname)
        # check data
        self._checkdata(self.aie_data, data)
        
        # save 2nd example data set
        desc2='Latest data for active interlock published on 2013-07-31, data scaled by factor %s' %self.scale
        self.aie.saveactiveinterlock(self.aie_data2, 
                                     description=desc2, 
                                     rawdata=exceldata, 
                                     active=True, 
                                     author='unit test')

        # test old data set
        res = self.aie.retrieveactiveinterlock('0', withdata=True, rawdata=False)
        self.assertEqual(res.values()[0]['status'], 0, 'Wrong status')
        self.assertEqual(res.values()[0]['description'], desc1, 'Description does not match each other.')
        data = res.values()[0]['data']
        # check data
        self._checkdata(self.aie_data, data)

        # test new data set
        res = self.aie.retrieveactiveinterlock('1', withdata=True, rawdata=False)
        self.assertEqual(res.values()[0]['status'], 1, 'Wrong status')
        self.assertEqual(res.values()[0]['description'], desc2, 'Description does not match each other.')
        data = res.values()[0]['data']
        # check data
        self._checkdata(self.aie_data2, data)
        
#        print("======test active interlock end=========")

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



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
    