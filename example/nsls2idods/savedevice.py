'''
Created on September 12, 2014

@author: dejan.dezman@cosylab.com
'''
import os
import sys
import time

import unittest
import logging
import requests
import random

import inspect
from requests import HTTPError

from idodspy.idodsclient import IDODSClient
from utils.profiler import *

__url = 'http://localhost:8000/id/device/'
__jsonheader = {'content-type': 'application/json', 'accept': 'application/json'}
client = IDODSClient(BaseURL=__url)

# Save component type if it does not exist

if len(client.retrieveComponentType('device type')) == 0:
    client.saveComponentType('device type')

# Save device
if len(client.retrieveInstall('name')) == 0:
    client.saveInstall('name', cmpnt_type_name='device type')

# Update install
if len(client.retrieveInstall('new name')) == 0:
    client.updateInstall('name', 'new name')

# Save online data
savedOnlineData = client.saveOnlineData('new name', status=1)

# Update online data
client.updateOnlineData(savedOnlineData['id'], rawdata_path='/usr/sth')


# Update online data with feedforward binary data
client.updateOnlineData(savedOnlineData['id'], feedforward_file_name='text data', feedforward_data='data')

# Retrieve online data by status
data = client.retrieveOnlineData(status=1)
print data

# Retrieve online data by rawdata path
data = client.retrieveOnlineData(rawdata_path='/usr/sth')
print data
