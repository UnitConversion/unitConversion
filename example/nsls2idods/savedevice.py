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

try:
    from django.utils import simplejson as json
except ImportError:
    import json

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
savedOnlineData = client.saveOnlineData('new name', status=1, meas_time='2014-09-16')

# Update online data
client.updateOnlineData(savedOnlineData['id'], rawdata_path='/usr/sth')


# Update online data with feedforward binary data
with open('Desert.jpg', 'rb') as f:
    client.updateOnlineData(savedOnlineData['id'], feedforward_file_name='desert image', feedforward_data=f)

# Retrieve online data by status
data = client.retrieveOnlineData(status=1)
print data.keys()

# Write retrieved image to a file
if len(data.keys()) > 0 and data[data.keys()[0]]['feedforward_data'] is not None:
    fh = open("retrieved_image.jpg", "wb")
    fh.write(data[data.keys()[0]]['feedforward_data'].decode('base64'))
    fh.close()

# Retrieve online data by rawdata path
data = client.retrieveOnlineData(rawdata_path='/usr/sth')
print data.keys()

# Retrieve online data by rawdata path
data = client.retrieveOnlineData(meas_time=json.dumps(['2014-09-01', '2014-09-15']))
print data.keys()
