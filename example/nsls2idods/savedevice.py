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

# Initialize connection with credentials in etc/idodsclient.conf
client = IDODSClient(BaseURL=__url)

# Variable initialization
cmpnt_type_name = 'New Test Type 5'
cmpnt_type_description = 'Component type description'
device_name = 'NTT4-2'
device_name_new = 'NTT4XX-2'
device_description = 'Device description.'
device_location = 'Device location.'

# Save a new device, here are all possible parameters. Necesary parameters are device_name and cmpnt_type_name. Returns an id of a newly saved device.
deviceID = client.saveDevice(device_name=device_name, cmpnt_type_name=cmpnt_type_name, device_description=device_description, device_coordinatecenter=None, cmpnt_type_description=cmpnt_type_description, cmpnt_type_props=None)

# Retrieve a device using all parameters.
client.retrieveDevice(device_name, description=None, cmpnt_type_name=None, coordinatecenter=None)

# Update a device using all parameters.
if len(client.retrieveDevice(device_name_new, description=None, cmpnt_type_name=None, coordinatecenter=None).keys()) == 0:
    client.updateDevice(device_name, device_name_new, description=None, cmpnt_type_name=None, coordinatecenter=None)

# Save online data
savedOnlineData = client.saveOnlineData(device_name_new, status=1, meas_time='2014-09-16')

# Update online data
client.updateOnlineData(savedOnlineData['id'], rawdata_path='/usr/sth')

# Update online data with feedforward binary data
with open('Desert.jpg', 'rb') as f:
    client.updateOnlineData(savedOnlineData['id'], feedforward_file_name='desert image', feedforward_data=f)

# Retrieve online data by status
data = client.retrieveOnlineData(status=1)

# Write retrieved image to a file
if len(data.keys()) > 0 and data[data.keys()[0]]['feedforward_data'] is not None:
    fh = open("retrieved_image.jpg", "wb")
    fh.write(data[data.keys()[0]]['feedforward_data'].decode('base64'))
    fh.close()

# Retrieve online data by rawdata path
data = client.retrieveOnlineData(rawdata_path='/usr/sth')

# Retrieve online data by rawdata path
data = client.retrieveOnlineData(meas_time=json.dumps(['2014-09-01', '2014-09-15']))
