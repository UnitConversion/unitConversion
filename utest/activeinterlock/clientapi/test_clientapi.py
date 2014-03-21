'''
Created on Sep 10, 2013

@author: shengb
'''
import os, sys

import unittest
import logging

from activeinterlock.rdbutils import (close, connect)

libPath = os.path.abspath("../../../clientapi/")
sys.path.append(libPath)

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
        #self.conn = connect()
        self.__url = 'http://localhost:8000/ai/'

        self.client = ActiveInterlockClient(BaseURL=self.__url)

        # clean active interlock RDB before use.
        #self.__cleanrdb()

        try:
            requests_log = logging.getLogger("requests")
            requests_log.setLevel(logging.DEBUG)
            #self.client = requests.session()
        
        except:
            raise

    def tearDown(self):
        # clean active interlock RDB after finish
        #self.__cleanrdb()
        #close(self.conn)
        pass
        
    def testDownload(self):
        
        r = self.client.downloadActiveInterlock()
        
        self.assertNotEqual(r, "")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()