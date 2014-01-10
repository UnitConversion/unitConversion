'''
Created on Jan 10, 2014

@author: dejan.dezman@cosylab.com
'''

import unittest
import os

from dataapi.pyidods.idods import idods

from preparerdb import connect

class TestIdods(unittest.TestCase):

    def setUp(self):
        self.con = connect()
        self.api = idods(self.con)

    def tearDown(self):
        self.con.close()

    def testRetrieveVendor(self):
        result = self.api._retrievevendor('RI');
        self.assertEqual(result[0][1], 'RI', 'Verdor retrieved')

if __name__ == '__main__':
    unittest.main()