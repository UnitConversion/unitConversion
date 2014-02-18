'''
Created on Feb 17, 2014

@author: dejan.dezman@cosylab.com
'''
import os, sys

import unittest
import logging
import requests
import random

import inspect

from idods.rdbutils.preparerdb import *

libPath = os.path.abspath("../../../clientapi/")
sys.path.append(libPath)

from idodspy.idodsclient import IDODSClient

class Test(unittest.TestCase):

    __url = 'http://localhost:8000/id/device/'
    __jsonheader = {'content-type':'application/json', 'accept':'application/json'}

    def cleanTables(self):
        # Clean offline data
        cleanOfflineData(['spec1234desc'])
        
        # Clean install rel prop
        cleanInstallRelProp(['testprop'])
        
        # Clean install rel prop type
        cleanInstallRelPropType(['testprop', 'prop2'])
        
        # Clean install rel
        cleanInstallRel('test child', 'test parent')
        cleanInstallRel('test parent', 'test child')
        
        # Clean online data
        cleanOnlineData(['desc1234'])
        
        # Clean inventory install map
        cleanInventoryToInstall('test parent', 'name')
        cleanInventoryToInstall('test parent', 'name2')
        
        # Clean install table
        cleanInstall(['test parent', 'test child'])
        
        # Clean vendor table
        cleanVendor(['test vendor', 'test vendor2'])
        
        # Clean data method
        cleanDataMethod(['method', 'method2', 'test'])
        
        # Clean inventory property
        cleanInventoryProperty('name', 'alpha')
        cleanInventoryProperty('name2', 'alpha')
        # Clean inventory
        cleanInventory(['name', 'name2'])
        # Clean inventory property template table
        cleanInventoryPropertyTemplate(['alpha', 'beta'])
        
        # Clean component type property
        cleanComponentTypeProperty('test cmpnt3', 'length')
        cleanComponentTypeProperty('Magnet', 'length')
        # Clean component type property type
        cleanComponentTypePropertyType(['length', 'width'])
        # Clean if there is something left from previous runs
        cleanComponentType(['test cmpnt', 'test cmpnt2','test cmpnt3', 'test cmpnt4','Magnet'])

    def setUp(self):
        self.cleanTables()
        self.client = IDODSClient(BaseURL=self.__url)

        try:
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
            self.client = requests.session()
        except:
            raise

    def tearDown(self):
        self.cleanTables()
        self.client.close()

    def testTest(self):
        pass

if __name__ == "__main__":
    unittest.main()