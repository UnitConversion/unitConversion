'''
Created on May 28, 2014

@author: dejan.dezman@cosylab.com
'''
import os
import sys
import time

import logging
import requests
import random

from requests import HTTPError

from idodspy.idodsclient import IDODSClient
from utils.profiler import *

__url = 'http://192.168.1.203:8000/id/device/'
__jsonheader = {'content-type': 'application/json', 'accept': 'application/json'}
client = IDODSClient(BaseURL=__url)

if len(client.retrieveComponentType("cmpnt").keys()) == 0:
    client.saveComponentType("cmpnt")

if len(client.retrieveInventory("inv").keys()) == 0:
    client.saveInventory("inv", cmpnt_type="cmpnt")

if len(client.retrieveDataMethod("method").keys()) == 0:
    client.saveDataMethod("method")

startedd = time.time()

client.saveOfflineData(
    inventory_name="inv",
    status=1,
    method_name="method",
    data="file10mb.txt",
    data_file_name="file"
)

total = time.time() - startedd
total = total*1000
print '=> elapsed time example.saveOfflineData.E: %f ms' % total
