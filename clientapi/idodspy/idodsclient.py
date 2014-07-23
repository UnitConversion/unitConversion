'''
Copyright (c) 2013 Brookhaven National Laboratory

All rights reserved. Use is subject to license terms and conditions.

Created on Feb 17, 2014
@author: dejan.dezman@cosylab.com

'''

import sys
import time

if sys.version_info[0] != 2 or sys.version_info[1] < 6:
    print("This library requires at least Python version 2.6")
    sys.exit(1)

import requests
# _requests_version=[int(x) for x in requests.__version__.split('.')]
# if _requests_version[0] < 1 or sys.version_info[1] < 1:
#    print("This library requires at least Python-requests version 1.1.x")
#    sys.exit(1)

import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

from requests import auth
from requests import HTTPError

from copy import copy

import urllib

try:
    import json
except ImportError:
    import simplejson as json

from _conf import _conf


class SSLAdapter(HTTPAdapter):
    '''An HTTPS Transport Adapter that uses an arbitrary SSL version.'''
    def __init__(self, ssl_version=None, **kwargs):
        self.ssl_version = ssl_version

        super(SSLAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=self.ssl_version)


class IDODSClient(object):
    '''
    IDODSClient provides a client connection object to perform
    save, retrieve, and update operations for NSLS II insertion device online data service.
    '''

    def __init__(self, BaseURL=None, username=None, password=None):
        '''
        BaseURL = the url of the insertion device online data service
        username =
        password =
        '''
        # self.__jsonheader = {'content-type': 'application/json', 'accept': 'application/json'}
        self.__jsonheader = {'content-type': 'application/x-www-form-urlencoded', 'accept': 'application/json'}
        self.__resource = 'test/'

        try:
            self.__baseURL = self.__getdefaultconfig('BaseURL', BaseURL)
            self.__userName = self.__getdefaultconfig('username', username)
            self.__password = self.__getdefaultconfig('password', password)

            if self.__userName and self.__password:
                # self.__auth = (self.__userName, self.__password)
                self.__auth = auth.HTTPBasicAuth(self.__userName, self.__password)

            else:
                self.__auth = None

            self.__session = requests.Session()

            # specify ssl version. Use SSL v3 for secure connection, https.
            self.__session.mount('https://', SSLAdapter(ssl_version=ssl.PROTOCOL_SSLv3))

            requests.post(self.__baseURL + self.__resource, headers=copy(self.__jsonheader), auth=self.__auth).raise_for_status()
            # requests.get(self.__baseURL + self.__resource, headers=copy(self.__jsonheader), auth=self.__auth).raise_for_status()

        except Exception as e:
            raise Exception('Failed to create client.')

    def __getdefaultconfig(self, arg, value):
        if value is None and _conf.has_option('DEFAULT', arg):
            return _conf.get('DEFAULT', arg)
        else:
            return value

    def retrieveVendor(self, name, description=None):
        '''
        Retrieve vendor by its name and description
        Wildcast matching are supported for both name and description.

        :param name: vendor name
        :type name: str

        :param description: description for a vendor
        :type description: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': {
                    'id': ,
                    'name': ,
                    'description':
                    }
                 ...
                }

        :Raises: HTTPError
        '''

        # Try to retrieve vendor
        url = 'vendor/'

        # Set parameters
        params = {
            'name': name
        }

        # Add description
        if description:
            params['description'] = description

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveVendor(self, name, description=None):
        '''Save vendor and its description into database

        :param name: vendor name
        :type name: str

        :param dtype: device type

        :param description: a brief description which could have up to 255 characters
        :type description: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': vendor_id}

        :Raises: HTTPError
        '''

        # Set URL
        url = 'savevendor/'

        # Set parameters
        params = {
            'name': name
        }

        # Add description
        if description:
            params['description'] = description

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateVendor(self, old_name, name, **kws):
        '''
        Update vendor and its description

        :param name: vendor name
        :type name: str

        :param old_name: update vendor by its old name
        :type old_name: str

        :param description: a brief description which could have up to 255 characters
        :type description: str

        :return: True or HTTPError

        :Raises: HTTPError
        '''

        # Set URL
        url = 'updatevendor/'

        # Set parameters
        params = {
            'vendor_id': None,
            'old_name': old_name,
            'name': name
        }

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def retrieveComponentType(self, name, description=None):
        '''Retrieve a component type using the key words:

        - name
        - description

        :param name: component type type name
        :type name: str

        :param description: description for this device
        :type desctiprion: str

        :return: a map with structure like:

            .. code-block: python

                {'id1':
                    {'id': device type id,
                    'name': device type name,
                    'description': device type description,
                    'prop1key': prop1value
                    ...
                    'propNkey': propNvalue
                    },
                 ...
                }

        :Raises: HTTPError
        '''

        # Set URL
        url = 'cmpnttype/'

        # Set parameters
        params = {
            'name': name
        }

        # Add description
        if description:
            params['description'] = description

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveComponentType(self, name, description=None, props=None):
        '''Save a component type using the key words:

        - name
        - description
        - props

        :param name: component type name
        :type name: str

        :param description: description for this device
        :type desctiprion: str

        :param props: component type properties
        :type props: python dict

        :return: a map with structure like:

            .. code-block: python

                {'id': device type id}

        :Raises: HTTPError

        '''

        # Set URL
        url = 'savecmpnttype/'

        # Set parameters
        params = {
            'name': name
        }

        # Add description
        if description:
            params['description'] = description

        # Add props
        if props:
            params['props'] = json.dumps(props)

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateComponentType(self, old_name, name, **kws):
        '''
        Update description of a device type.
        Once a device type is saved, it is not allowed to change it again since it will cause potential colflict.

        - old_name
        - name
        - description
        - props

        :param old_name: component type name we want to update by
        :type old_name: str

        :param name: device type name
        :type name: str

        :param description: description for this device
        :type desctiprion: str

        :param props: component type properties
        :type props: python dict

        :return: True if everything is ok

        :Raises: HTTPError
        '''

        # Set URL
        url = 'updatecmpnttype/'

        # Set parameters
        params = {
            'component_type_id': None,
            'old_name': old_name,
            'name': name
        }

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add props
        if 'props' in kws:
            params['props'] = json.dumps(kws['props'])

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def retrieveComponentTypePropertyType(self, name):
        '''
        Retrieve component type property type by its name

        - name: property type name

        :return: a map with structure like:

            .. code-block:: python

                {
                    'id': {
                        'id': ,              # int
                        'name': ,           # string
                        'description': ,    # string
                    }
                }

        :Raises: HTTPError
        '''

        # Set URL
        url = 'cmpnttypeproptype/'

        # Set parameters
        params = {
            'name': name
        }

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveComponentTypePropertyType(self, name, description=None):
        '''
        Insert new component type property type into database

        - name: name of the component type property type M
        - description: description of the component type property tpye O

        :return: a map with structure like:

            .. code-block:: python

                {'id': propertytypeid}

        :Raises: HTTPError
        '''

        # Set URL
        url = 'savecmpnttypeproptype/'

        # Set parameters
        params = {
            'name': name
        }

        # Add description
        if description:
            params['description'] = description

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateComponentTypePropertyType(self, old_name, name, **kws):
        '''
        Insert new component type property type into database

        - old_name: name of the component type property type we want to update by M
        - name: name of the component type property type M
        - description: description of the component type property tpye O

        :return: True if everything is ok

        :Raises: HTTPError
        '''

        # Set URL
        url = 'updatecmpnttypeproptype/'

        # Set parameters
        params = {
            'property_type_id': None,
            'old_name': old_name,
            'name': name
        }

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def retrieveInventory(self, name):
        '''Retrieve an insertion device from inventory by device inventory name and type.
        Wildcard matching is supported for inventory name and device type. ::

            * for multiple characters matching
            ? for single character matching


        :param name: insertion device inventory name, which is usually different from its field name (the name after installation).
        :type name: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': { 'name':,                       # string
                         'serialno':,                   # string
                         'cmpnt_type':                   # string
                         'typeinto':                    # string
                         'vendor':,                     # string
                         'length': ,                    # float
                         'up_corrector_position': ,     # float
                         'middle_corrector_position': , # float
                         'down_corrector_position':,    # float
                         'gap_min': ,                   # float
                         'gap_max': ,                   # float
                         'gap_tolerance':,              # float
                         'phase1_min':,                 # float
                         'phase1_max':,                 # float
                         'phase2_min':,                 # float
                         'phase2_max':,                 # float
                         'phase3_min':,                 # float
                         'phase3_max':,                 # float
                         'phase4_min':,                 # float
                         'phase4_max':,                 # float
                         'phase_tolerance':,            # float
                         'k_max_linear':,               # float
                         'k_max_circular':,             # float
                         'phase_mode_p':,               # string
                         'phase_mode_a1':,              # string
                         'phase_mode_a2':               # string

                        }
                }

        :Raises: HTTPError
        '''

        # Set URL
        url = 'inventory/'

        # Set parameters
        params = {
            'name': name
        }

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveInventory(self, name, **kws):
        '''
        save insertion device into inventory using any of the acceptable key words:

        - name:  name to identify that device from vendor
        - cmpnt_type: device type name
        - alias: alias name if it has
        - serialno: serial number
        - vendor: vendor name
        - props: properties with structure as below

        .. code-block:: python

            {
                'length': ,                    # float
                'up_corrector_position': ,     # float
                'middle_corrector_position': , # float
                'down_corrector_position':,    # float
                'gap_min': ,                   # float
                'gap_max': ,                   # float
                'gap_tolerance':,              # float
                'phase1_min':,                 # float
                'phase1_max':,                 # float
                'phase2_min':,                 # float
                'phase2_max':,                 # float
                'phase3_min':,                 # float
                'phase3_max':,                 # float
                'phase4_min':,                 # float
                'phase4_max':,                 # float
                'phase_tolerance':,            # float
                'k_max_linear':,               # float
                'k_max_circular':,             # float
                'phase_mode_p':,               # string
                'phase_mode_a1':,              # string
                'phase_mode_a2':               # string
            }

        :param name: insertion device name, which is usually different from its field name (the name after installation).
        :type name: str

        :param dtype: device type
        :type dtype: str

        :param alias: alias name if it has
        :type alias: str

        :param serialno: serial number
        :type serialno: str

        :param vendor: name of vendor
        :type vendor: str

        :param props: a map to describe the property of an insertion device as described above
        :type props: object

        :return: a map with structure like:

            .. code-block:: python

                {'id': inventory_id}

        :Raises: HTTPError
        '''

        # Set URL
        url = 'saveinventory/'

        # Set parameters
        params = {
            'name': name
        }

        # Add component type
        if 'cmpnt_type' in kws:
            params['cmpnt_type'] = kws['cmpnt_type']

        # Add alias
        if 'alias' in kws:
            params['alias'] = kws['alias']

        # Add serialno
        if 'serialno' in kws:
            params['serialno'] = kws['serialno']

        # Add vendor
        if 'vendor' in kws:

            # Check vendor value
            if kws['vendor'] is None:
                self.__raise_for_status(400, 'If vendor is passed it should not be None!')

            params['vendor'] = kws['vendor']

        # Add props
        if 'props' in kws:
            params['props'] = json.dumps(kws['props'])

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateInventory(self, old_name, name, **kws):
        '''
        Update inventory using any of the acceptable key words:

        - old_name:  name of the inventory we want to update by
        - name:  name to identify that device from vendor
        - cmpnt_type: device type name
        - alias: alias name if it has
        - serialno: serial number
        - vendor: vendor name
        - props: properties with structure as below

        .. code-block:: python

            {
                'length': ,                    # float
                'up_corrector_position': ,     # float
                'middle_corrector_position': , # float
                'down_corrector_position':,    # float
                'gap_min': ,                   # float
                'gap_max': ,                   # float
                'gap_tolerance':,              # float
                'phase1_min':,                 # float
                'phase1_max':,                 # float
                'phase2_min':,                 # float
                'phase2_max':,                 # float
                'phase3_min':,                 # float
                'phase3_max':,                 # float
                'phase4_min':,                 # float
                'phase4_max':,                 # float
                'phase_tolerance':,            # float
                'k_max_linear':,               # float
                'k_max_circular':,             # float
                'phase_mode_p':,               # string
                'phase_mode_a1':,              # string
                'phase_mode_a2':               # string
            }

        :param name: insertion device name, which is usually different from its field name (the name after installation).
        :type name: str

        :param dtype: device type
        :type dtype: str

        :param alias: alias name if it has
        :type alias: str

        :param serialno: serial number
        :type serialno: str

        :param vendor: name of vendor
        :type vendor: str

        :param props: a map to describe the property of an insertion device as described above
        :type props: object

        :return: True if everything is ok

        :Raises: HTTPError
        '''

        # Set URL
        url = 'updateinventory/'

        # Set parameters
        params = {
            'inventory_id': None,
            'old_name': old_name,
            'name': name
        }

        # Add component type
        if 'cmpnt_type' in kws:
            params['cmpnt_type'] = kws['cmpnt_type']

        # Add alias
        if 'alias' in kws:
            params['alias'] = kws['alias']

        # Add serialno
        if 'serialno' in kws:
            params['serialno'] = kws['serialno']

        # Add vendor
        if 'vendor' in kws:

            # Check vendor value
            if kws['vendor'] is None:
                self.__raise_for_status(400, 'If vendor is passed it should not be None!')

            params['vendor'] = kws['vendor']

        # Add props
        if 'props' in kws:
            params['props'] = json.dumps(kws['props'])

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def retrieveInventoryPropertyTemplate(self, name):
        '''
        Retrieve inventory property template by its name

        - name: Inventory property name

        :return: a map with structure like:

            .. code-block:: python

                {
                    'id': {
                        'id': ,              # int
                        'cmpnt_type': ,      # int
                        'name': ,           # string
                        'description': ,    # string
                        'default': ,        # string
                        'unit':             # string
                    }
                }

        :Raises: HTTPError
        '''

        # Set URL
        url = 'inventoryproptmplt/'

        # Set parameters
        params = {
            'name': name
        }

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveInventoryPropertyTemplate(self, cmpnt_type, name, description=None, default=None, unit=None):
        '''
        Insert new inventory property template into database

        - cmpnt_type: component type name M
        - name: property template name M
        - description: property template description O
        - default: property template default value O
        - unit: property template unit O

        :return: a map with structure like:

            .. code-block:: python

                {'id': propertytemplateid}

        :Raises: HTTPError
        '''

        # Set URL
        url = 'saveinventoryproptmplt/'

        # Set parameters
        params = {
            'cmpnt_type': cmpnt_type,
            'name': name
        }

        # Add description
        if description:
            params['description'] = description

        # Add default
        if default:
            params['default'] = default

        # Add unit
        if unit:
            params['unit'] = unit

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateInventoryPropertyTemplate(self, tmplt_id, cmpnt_type, name, **kws):
        '''
        Update inventory property template in a database

        - tmplt_id: property template id M
        - cmpnt_type: component type name M
        - name: property template name M
        - description: property template description O
        - default: property template default value O
        - unit: property template unit O

        :return: True if update succeeded

        :Raises: HTTPError
        '''

        # Set URL
        url = 'updateinventoryproptmplt/'

        # Set parameters
        params = {
            'tmplt_id': tmplt_id,
            'cmpnt_type': cmpnt_type,
            'name': name
        }

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add default
        if 'default' in kws:
            params['default'] = kws['default']

        # Add unit
        if 'unit' in kws:
            params['unit'] = kws['unit']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def retrieveInstall(self, name, **kws):
        '''Retrieve insertion device installation using any of the acceptable key words:

        :param name: installation name, which is its label on field
        :type name: str

        :param description: installation description
        :type description: str

        :param cmpnt_type: component type name of the device
        :type cmpnt_type: str

        :param coordinatecenter: coordinate center number
        :type coordinatecenter: str

        :param all_install: retrieve also system installs
        :type all_install: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': {
                        'id':                     #int,
                        'name':                   #string,
                        'description':            #string,
                        'cmpnt_type':             #string,
                        'cmpnt_type_description': #string,
                        'coordinatecenter':       #float
                    }
                }

        :Raises: ValueError, MySQLError
        '''

        # Set URL
        url = 'install/'

        # Set parameters
        params = {
            'name': name
        }

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add component type
        if 'cmpnt_type' in kws:
            params['cmpnt_type'] = kws['cmpnt_type']

        # Add coordinate center
        if 'coordinatecenter' in kws:
            params['coordinatecenter'] = kws['coordinatecenter']

        # Add all install
        if 'all_install' in kws:
            params['all_install'] = kws['all_install']

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveInsertionDevice(
            self, install_name, coordinate_center, project, beamline, beamline_desc,
            install_desc, inventory_name, down_corrector, up_corrector, length, gap_max,
            gap_min, gap_tolerance, phase1_max, phase1_min, phase2_max, phase2_min,
            phase3_max, phase3_min, phase4_max, phase4_min, phase_tolerance,
            k_max_circular, k_max_linear, phase_mode_a1, phase_mode_a2, phase_mode_p,
            type_name, type_desc
            ):
        '''
        Save insertion device

        :param install_name: installation name
        :type install_name: str

        :param coordinate_center: coordinate center
        :type coordinate_center: float

        :param project: project name
        :type project: str

        :param beamline: beamline name
        :type beamline: str

        :param beamline_desc: beamline description
        :type beamline_desc: str

        :param install_desc: install description
        :type install_desc: str

        :param inventory_name: inventory name
        :type inventory_name: str

        :param down_corrector: inventory property down corrector
        :type down_corrector: str

        :param up_corrector: inventory property up corrector
        :type up_corrector: str

        :param length: inventory property length
        :type length: str

        :param gap_max: invnetory property gap maximum
        :type gap_max: str

        :param gap_min: inventory property gap minimum
        :type gap_min: str

        :param gap_tolerance: inventory property gap tolerance
        :type gap_tolerance: str

        :param phase1_max: inventory property phase1 maximum
        :type phase1_max: str

        :param phase1_min: inventory property phase1 minimum
        :type phase1_min: str

        :param phase2_max: inventory prperty phase2 maximum
        :type phase2_max: str

        :param phase2_min: inventory property phase2 minimum
        :type phase2_min: str

        :param phase3_max: inventory property phase3 maximum
        :type phase3_max: str

        :param phase3_min: inventory property phase3 minimum
        :type phase3_min: str

        :param phase4_max: inventory property phase4 maximum
        :type phase4_max: str

        :param phase4_min: inventory property phase4 minimum
        :type phase4_min: str

        :param phase_tolerance: inventory property phase tolerance
        :type phase_tolerance: str

        :param k_max_circular: inventory property k maximum circular
        :type k_max_circular: str

        :param k_max_linear: inventory property k maximum linear
        :type k_max_linear: str

        :param phase_mode_a1: inventory property phase mode a1
        :type phase_mode_a1: str

        :param phase_mode_a2: inventory property phase mode a2
        :type phase_mode_a2: str

        :param phase_mode_p: inventory property phase mode p
        :type phase_mode_p: str

        :param type_name: component type name
        :type type_name: str

        :param type_desc: component type description
        :type type_desc: str

        :return: True if everything went ok

        :raise: HTTPError
        '''

        # Set URL
        url = 'saveinsertiondevice/'

        # Set parameters
        params = {
            'install_name': install_name,
            'coordinate_center': coordinate_center,
            'project': project,
            'beamline': beamline,
            'beamline_desc': beamline_desc,
            'install_desc': install_desc,
            'inventory_name': inventory_name,
            'down_corrector': down_corrector,
            'up_corrector': up_corrector,
            'length': length,
            'gap_max': gap_max,
            'gap_min': gap_min,
            'gap_tolerance': gap_tolerance,
            'phase1_max': phase1_max,
            'phase1_min': phase1_min,
            'phase2_max': phase2_max,
            'phase2_min': phase2_min,
            'phase3_max': phase3_max,
            'phase3_min': phase3_min,
            'phase4_max': phase4_max,
            'phase4_min': phase4_min,
            'phase_tolerance': phase_tolerance,
            'k_max_circular': k_max_circular,
            'k_max_linear': k_max_linear,
            'phase_mode_a1': phase_mode_a1,
            'phase_mode_a2': phase_mode_a2,
            'phase_mode_p': phase_mode_p,
            'type_name': type_name,
            'type_desc': type_desc
        }

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveInstall(self, name, **kws):
        '''Save insertion device installation using any of the acceptable key words:

        - name: installation name, which is its label on field
        - description: installation description
        - cmpnt_type: component type of the device
        - coordinatecenter: coordinate center number

        raises:
            HTTPError

        returns:
            {'id': new install id}
        '''

        # Set URL
        url = 'saveinstall/'

        # Set parameters
        params = {
            'name': name
        }

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add component type
        if 'cmpnt_type' in kws:
            params['cmpnt_type'] = kws['cmpnt_type']

        # Add coordinate center
        if 'coordinatecenter' in kws:
            params['coordinatecenter'] = kws['coordinatecenter']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateInstall(self, old_name, name, **kws):
        '''Update insertion device installation using any of the acceptable key words:

        - old_name: installation name, we want ot update by
        - name: installation name, which is its label on field
        - description: installation description
        - cmpnt_type: component type of the device
        - coordinatecenter: coordinate center number

        raises:
            HTTPError

        returns:
            True if everything is ok
        '''

        # Set URL
        url = 'updateinstall/'

        # Set parameters
        params = {
            'old_name': old_name,
            'name': name
        }

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add component type
        if 'cmpnt_type' in kws:

            # Check for none
            if kws['cmpnt_type'] is None:
                self.__raise_for_status(400, 'If component type parameter is present it should not be set to None!')

            params['cmpnt_type'] = kws['cmpnt_type']

        # Add coordinate center
        if 'coordinatecenter' in kws:
            params['coordinatecenter'] = kws['coordinatecenter']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveInstallRelProperty(self, install_rel_parent, install_rel_child, install_rel_property_type_name, install_rel_property_value):
        '''
        Save install rel property into database

        :param install_rel_parent: name of the parent in the install rel
        :type install_rel_parent: str

        :param install_rel_child: name of the child in the install rel
        :type install_rel_child: str

        :param install_rel_property_type_name: name of the install rel property type
        :type install_rel_property_type_name: str

        :param install_rel_property_value: value of the install rel property
        :type install_rel_property_value: str

        :raises: HTTPError

        :returns: {'id': new install rel property id}
        '''

        # Set URL
        url = 'saveinstallrelprop/'

        # Set parameters
        params = {
            'install_rel_parent': install_rel_parent,
            'install_rel_child': install_rel_child,
            'install_rel_property_type_name': install_rel_property_type_name,
            'install_rel_property_value': install_rel_property_value
        }

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateInstallRelProperty(self, install_rel_parent, install_rel_child, install_rel_property_type_name, install_rel_property_value):
        '''
        Update install rel property in the database

        :param install_rel_parent: name of the parent in the install rel
        :type install_rel_parent: str

        :param install_rel_child: name of the child in the install rel
        :type install_rel_child: str

        :param install_rel_property_type_name: name of the install rel property type
        :type install_rel_property_type_name: str

        :param install_rel_property_value: value of the install rel property
        :type install_rel_property_value: str

        :raises: HTTPError

        :returns: True if everything was OK
        '''

        # Set URL
        url = 'updateinstallrelprop/'

        # Set parameters
        params = {
            'install_rel_parent': install_rel_parent,
            'install_rel_child': install_rel_child,
            'install_rel_property_type_name': install_rel_property_type_name,
            'install_rel_property_value': install_rel_property_value
        }

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def retrieveInstallRel(self, install_rel_id=None, parent_install=None, child_install=None, description=None, order=None, date=None, expected_property=None):
        '''
        Retrieve install rel from the database. Specific relation can be retrieved or all the children of specific parent or
        all the parents of specific child.

        :param install_rel_id: id of the install_rel table
        :type install_rel_id: int

        :param parent_install: name of the parent install element
        :type parent_install: str

        :param child_install: name of the child install element
        :type child_install: str

        :param description: description of a relationship
        :type description: str

        :param order: order number of child element in the parent element; accepts a range in a tuple
        :type order: order number of child element in the parent element; accepts a range in a tuple

        :param date: date of the device installation; accepts a range in a tuple
        :type date: str

        :param expected_property: if we want to search for relationships with specific property set to a specific value, we
              can prepare a dict and pass it to the function e.g. {'beamline': 'xh*'} will return all of the
              beamlines with names starting with xh or {'beamline': None} will return all of the beamlines

        :type expected_property: dict

        :return: a map with structure like:

            .. code-block: python

                {
                    'id': {
                        'id':           #int,
                        'parentid':     #int,
                        'parentname':   #string,
                        'childid':      #int,
                        'childname':    #string,
                        'description':  #string,
                        'order':        #int,
                        'date':         #string,
                        'prop1key':     #string,
                        ...
                        'propNkey':     #string
                    }
                }

        :raises: HTTPError
        '''

        # Set URL
        url = 'installrel/'

        # Set parameters
        params = {
            'install_rel_id': install_rel_id,
            'parent_install': parent_install,
            'child_install': child_install,
            'description': description,
            'order': order,
            'date': date
        }

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveInstallRel(self, parent_install, child_install, description=None, order=None, props=None):
        '''
        Save install relationship in the database.

        :param parent_install: id of the parent element
        :type parent_install: int

        :param child_install: id of the child element
        :type child_install: int

        :param description: description of the relationship
        :type description: str

        :param order: order of the child in the relationship
        :type order: int

        :param props: dict structure:

            .. code-block: python

                {
                    'key1': 'value1',
                    ...
                    'keyN': 'valueN'
                }

        :type props: dict

        :return: a map with structure like:

            .. code-block: python

                {'id': id of the saved install rel}

        :raises: HTTPError
        '''

        # Set URL
        url = 'saveinstallrel/'

        # Set parameters
        params = {
            'parent_install': parent_install,
            'child_install': child_install
        }

        # Add description
        if description:
            params['description'] = description

        # Add order
        if order:
            params['order'] = order

        # Add props
        if props:
            params['props'] = json.dumps(props)

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateInstallRel(self, parent_install, child_install, **kws):
        '''
        Update install relationship.

        :param parent_install: name of the parent element we want ot update by
        :type parent_install: str

        :param child_install: name of the child element we want ot update by
        :type child_install: str

        :param description: description of the relationship
        :type description: str

        :param order: order of the child in the relationship
        :type order: int

        :param props: dict structure

            .. code-block:: python

                {
                    'key1': 'value1',
                    ...
                    'keyN': 'valueN'
                }

        :type props: dict

        returns:
            True if everything is ok

        raises:
            HTTPError
        '''

        # Set URL
        url = 'updateinstallrel/'

        # Set parameters
        params = {
            'parent_install': parent_install,
            'child_install': child_install
        }

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add order
        if 'order' in kws:
            params['order'] = kws['order']

        # Add props
        if 'props' in kws:
            params['props'] = json.dumps(kws['props'])

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def retrieveInstallRelPropertyType(self, name):
        '''
        Retrieve install relationship property type by its name

        - name: property type name

        :return: a map with structure like:

            .. code-block:: python

                {
                    'id': {
                        'id': ,             # int
                        'name': ,           # string
                        'description': ,    # string
                        'unit': ,          # string
                    }
                }

        :Raises: HTTPError
        '''

        # Set URL
        url = 'installrelproptype/'

        # Set parameters
        params = {
            'name': name
        }

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveInstallRelPropertyType(self, name, description=None, unit=None):
        '''
        Insert new install relationship property type into database

        - name: name of the install relationship property type M
        - description: description of the install relationship property type O
        - unit: unit used for this property type O

        :return: a map with structure like:

            .. code-block:: python

                {'id': propertytypeid}

        :Raises: HTTPError
        '''

        # Set URL
        url = 'saveinstallrelproptype/'

        # Set parameters
        params = {
            'name': name
        }

        # Add description
        if description:
            params['description'] = description

        # Add unit
        if unit:
            params['unit'] = unit

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateInstallRelPropertyType(self, old_name, name, **kws):
        '''
        Update install relationship property type

        - old_name: name of the install relationship property type we want to update by O
        - name: name of the install relationship property type M
        - description: description of the install relationship property type O
        - unit: units used for this property type O

        :return: True if everything is ok

        :Raises: HTTPError
        '''

        # Set URL
        url = 'updateinstallrelproptype/'

        # Set parameters
        params = {
            'old_name': old_name,
            'name': name
        }

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add unit
        if 'unit' in kws:
            params['unit'] = kws['unit']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def retrieveInventoryToInstall(self, inventory_to_install_id, install_name, inv_name):
        '''
        Return installed devices or psecific map

        params:
            - inventory_to_install_id
            - install_name
            - inv_name

        :param inventory_to_install_id: id of the inventory to install map
        :type inventory_to_install_id: int

        :param install_name: label name after installation
        :type install_name: str

        :param inv_name: name in its inventory
        :type inv_name: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': {
                        'id': #int,
                        'installid': #int,
                        'installname': #string,
                        'inventoryid': #int,
                        'inventoryname': #string
                    }
                }

        :Raises: HTTPError
        '''

        # Set URL
        url = 'inventorytoinstall/'

        # Set parameters
        params = {
            'inventory_to_install_id': inventory_to_install_id,
            'install_name': install_name,
            'inv_name': inv_name
        }

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveInventoryToInstall(self, install_name, inv_name):
        '''Link a device as installed once it is installed into field using the key words:
        - install_name
        - inv_name

        :param install_name: label name after installation
        :type install_name: str

        :param inv_name: name in its inventory
        :type inv_name: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': id of new inventorytoinstall record}

        :Raises: HTTPError
        '''

        # Set URL
        url = 'saveinventorytoinstall/'

        # Set parameters
        params = {
            'install_name': install_name,
            'inv_name': inv_name
        }

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateInventoryToInstall(self, inventory_to_install_id, install_name, inv_name):
        '''Update a device as installed when its installation has been changed using the key words:

        - inventory_to_install_id
        - install_name
        - inv_name

        :param install_name: label name after installation
        :type install_name: str

        :param inv_name: name in its inventory
        :type inv_name: str

        :return: True if everything was ok

        :Raises: HTTPError
        '''

        # Set URL
        url = 'updateinventorytoinstall/'

        # Set parameters
        params = {
            'inventory_to_install_id': inventory_to_install_id,
            'install_name': install_name,
            'inv_name': inv_name
        }

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def retrieveDataMethod(self, name, description=None):
        '''Retrieve a method name and its description which is used when producing data set for an insertion device.

        :param name: name of the method
        :type name: str

        :param description: description of this method
        :type description: str

        :return: a map with structure like:

            .. code-block:: python

                {'id':
                    {'id': data method id,
                     'name': method name,
                     'description': description of this method
                    }
                }

        :Raises: HTTPError
        '''

        # Try to retrieve data method
        url = 'datamethod/'

        # Set parameters
        params = {
            'name': name
        }

        # Add description
        if description:
            params['description'] = description

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveDataMethod(self, name, description=None):
        '''Save a method with its description which is used when producing data set for an insertion device.

        :param name: name of the method
        :type name: str

        :param description: description of this method
        :type description: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': method_id}

        :Raises: HTTPError
        '''

        # Set URL
        url = 'savedatamethod/'

        # Set parameters
        params = {
            'name': name
        }

        # Add description
        if description:
            params['description'] = description

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateDataMethod(self, old_name, name, **kws):
        '''Update data method by id or name.

        :param datamethod_id id of the data method we want to update by
        :type datamethod_id: int

        :param old_name: name of the method we want to update by
        :type old_name: str

        :param name: name of the method
        :type name: str

        :param description: description of this method
        :type description: str

        :return: True if everything was ok

        :Raises: HTTPError
        '''

        # Set URL
        url = 'updatedatamethod/'

        # Set parameters
        params = {
            'datamethod_id': None,
            'old_name': old_name,
            'name': name
        }

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def retrieveOfflineData(self, **kws):
        '''Retrieve insertion device offline data using any of the acceptable key words:

        - offlineid
        - description
        - gap
        - phase1
        - phase2
        - phase3
        - phase4
        - phasemode
        - polarmode
        - status
        - method_name
        - inventory_name
        - with_data

        :param offlineid: id of the offline data we want to retrieve
        :type offlineid: int

        :param description: a brief description for this data entry
        :type description: str

        :param gap: gap when this data set is produced
        :type gap: float

        :param phase1: phase 1 when this data set is produced
        :type phase1: float

        :param phase2: phase 2 when this data set is produced
        :type phase2: float

        :param phase3: phase 3 when this data set is produced
        :type phase3: float

        :param phase4: phase 4 when this data set is produced
        :type phase4: float

        :param phasemode: description for the mode of phase, which is determined by gap/phase
        :type phasemode: str

        :param polarmode: description for the mode of polar, which is determined by gap/phase
        :type polarmode: str

        :param status: status of this data set
        :type status: int

        :param method_name: name of method used to produce the data
        :type method_name: str

        :param inventory_name: name of inventory used to produce the data
        :type inventory_name: str

        :param with_data: do we want data is returned together with the result?
        :type with_data: True/False

        :return: a map with structure like:

            .. code-block:: python

                {'offlinedata_id': {
                        'username': ,      # string
                        'description': ,   # string
                        'date': ,          # timestamp
                        'gap':,            # float
                        'phase1': ,        # float
                        'phase2': ,        # float
                        'phase3':,         # float
                        'phase4':,         # float
                        'phasemode':,      # string
                        'polarmode':,      # string
                        'status':,         # int
                        'data_file_name':, # string
                        'data_file_ts':,   # string
                        'data_id':,        # int
                        'script_name':,    # string
                        'script':,         # string
                        'method_name':,    # string
                        'methoddesc':,     # string
                        'inventory_name':, # string
                        'data':            # string, base64 encoded file content
                    }
                }

        :Raises: HTTPError
        '''

        # Set URL
        url = 'offlinedata/'

        # Set parameters
        params = {}

        # Add offline id
        if 'offlineid' in kws:
            params['offlineid'] = kws['offlineid']

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add gap
        if 'gap' in kws:
            params['gap'] = kws['gap']

        # Add phase1
        if 'phase1' in kws:
            params['phase1'] = kws['phase1']

        # Add phase2
        if 'phase2' in kws:
            params['phase2'] = kws['phase2']

        # Add phase3
        if 'phase3' in kws:
            params['phase3'] = kws['phase3']

        # Add phase4
        if 'phase4' in kws:
            params['phase4'] = kws['phase4']

        # Add phasemode
        if 'phasemode' in kws:
            params['phasemode'] = kws['phasemode']

        # Add polarmode
        if 'polarmode' in kws:
            params['polarmode'] = kws['polarmode']

        # Add status
        if 'status' in kws:
            params['status'] = kws['status']

        # Add method name
        if 'method_name' in kws:
            params['method_name'] = kws['method_name']

        # Add inventory name
        if 'inventory_name' in kws:
            params['inventory_name'] = kws['inventory_name']

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        returnData = r.json()

        # Append data if with_data is set
        if 'with_data' in kws and kws['with_data'] is True:

            # Set URL
            url = 'rawdata/'

            # Go through all returned offline data and append data
            offlineDataKeys = returnData.keys()

            for key in offlineDataKeys:
                offlineData = returnData[key]

                # Set parameters
                params = {
                    'raw_data_id': offlineData['data_id']
                }

                result = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
                self.__raise_for_status(r.status_code, r.text)
                resultData = result.json()

                resultKeys = resultData.keys()
                resultObject = resultData[resultKeys[0]]
                returnData[key]['data'] = resultObject['data']

        return returnData

    def retrieveInstallOfflineData(self, **kws):
        '''Retrieve insertion device offline data using any of the acceptable key words:

        - install_name
        - description
        - date
        - gap
        - phase1
        - phase2
        - phase3
        - phase4
        - phasemode
        - polarmode
        - status
        - method_name
        - with_data

        :param description: a brief description for this data entry
        :type description: str

        :param date: offline data date
        :type date: str

        :param gap: gap when this data set is produced
        :type gap: float

        :param phase1: phase 1 when this data set is produced
        :type phase1: float

        :param phase2: phase 2 when this data set is produced
        :type phase2: float

        :param phase3: phase 3 when this data set is produced
        :type phase3: float

        :param phase4: phase 4 when this data set is produced
        :type phase4: float

        :param phasemode: description for the mode of phase, which is determined by gap/phase
        :type phasemode: str

        :param polarmode: description for the mode of polar, which is determined by gap/phase
        :type polarmode: str

        :param status: status of this data set
        :type status: int

        :param method_name: name of method used to produce the data
        :type method_name: str

        :param install_name: name of install item
        :type install_name: str

        :param with_data: do we want data is returned together with the result?
        :type with_data: True/False

        :return: a map with structure like:

            .. code-block:: python

                {'offlinedata_id': {
                        'install_name': ,  # string
                        'username': ,      # string
                        'description': ,   # string
                        'date': ,          # timestamp
                        'gap':,            # float
                        'phase1': ,        # float
                        'phase2': ,        # float
                        'phase3':,         # float
                        'phase4':,         # float
                        'phasemode':,      # string
                        'polarmode':,      # string
                        'status':,         # int
                        'data_file_name':, # string
                        'data_file_ts':,   # string
                        'data_id':,        # int
                        'script_name':,    # string
                        'script':,         # string
                        'method_name':,    # string
                        'methoddesc':,     # string
                        'inventory_name':, # string
                        'data':            # string, base64 encoded file content
                    }
                }

        :Raises: HTTPError
        '''

        # Set URL
        url = 'offlinedatainstall/'

        # Set parameters
        params = {}

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add date
        if 'date' in kws:
            params['date'] = kws['date']

        # Add gap
        if 'gap' in kws:
            params['gap'] = kws['gap']

        # Add phase1
        if 'phase1' in kws:
            params['phase1'] = kws['phase1']

        # Add phase2
        if 'phase2' in kws:
            params['phase2'] = kws['phase2']

        # Add phase3
        if 'phase3' in kws:
            params['phase3'] = kws['phase3']

        # Add phase4
        if 'phase4' in kws:
            params['phase4'] = kws['phase4']

        # Add phasemode
        if 'phasemode' in kws:
            params['phasemode'] = kws['phasemode']

        # Add polarmode
        if 'polarmode' in kws:
            params['polarmode'] = kws['polarmode']

        # Add status
        if 'status' in kws:
            params['status'] = kws['status']

        # Add method name
        if 'method_name' in kws:
            params['method_name'] = kws['method_name']

        # Add install name
        if 'install_name' in kws:
            params['install_name'] = kws['install_name']

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        returnData = r.json()

        # Append data if with_data is set
        if 'with_data' in kws and kws['with_data'] is True:

            # Set URL
            url = 'rawdata/'

            # Go through all returned offline data and append data
            offlineDataKeys = returnData.keys()

            for key in offlineDataKeys:
                offlineData = returnData[key]

                # Set parameters
                params = {
                    'raw_data_id': offlineData['data_id']
                }

                result = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
                self.__raise_for_status(r.status_code, r.text)
                resultData = result.json()

                resultKeys = resultData.keys()
                resultObject = resultData[resultKeys[0]]
                returnData[key]['data'] = resultObject['data']

        return returnData

    def saveMethodAndOfflineData(self, inventory_name, method, method_desc, data_desc, data_file_name, data_file_path, status, gap, phase1, phase2, phase3, phase4, phase_mode, polar_mode):
        '''
        Save data method and offline data into the database

        :param inventory_name: inventory name
        :type inventory_name: str

        :param username: username of the user who saved the offline data
        :type username: str

        :param method: data method name
        :type method: str

        :param method_desc: data method description
        :type method_desc: str

        :param data_desc: offline data description
        :type data_desc: str

        :param data_file_name: data file name
        :type data_file_name: str

        :param data_id: id of the saved raw data
        :type data_id: int

        :param status: is offline data Active = 1 or Obsolete - 0
        :type status: int

        :param gap: gap
        :type gap: float

        :param phase1: phase1
        :type phase1: float

        :param phase2: phase2
        :type phase2: float

        :param phase3: phase3
        :type phase3: float

        :param phase4: phase4
        :type phase4: float

        :param phase_mode: phase mode
        :type phase_mode: str

        :param polar_mode: polar mode
        :type polar_mode: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': offline_data_id}

        :raise: HTTPError
        '''

        # Set URL
        url = 'savemethodofflinedata/'

        # Set parameters
        params = {
            'inventory_name': inventory_name,
            'method': method,
            'method_desc': method_desc,
            'data_desc': data_desc,
            'data_file_name': data_file_name,
            'status': status,
            'gap': gap,
            'phase1': phase1,
            'phase2': phase2,
            'phase3': phase3,
            'phase4': phase4,
            'phase_mode': phase_mode,
            'polar_mode': polar_mode
        }

        fileName = data_file_path

        with open(fileName, 'rb') as f:
            ur = self.__session.post(self.__baseURL+'saverawdata/', files={'file': f}, auth=self.__auth)
            self.__raise_for_status(ur.status_code, ur.text)

        params['data_id'] = ur.json()['id']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def saveOfflineData(self, **kws):
        '''
        save insertion device offline data using any of the acceptable key words:

        - inventory_name
        - username
        - description
        - gap
        - phase1
        - phase2
        - phase3
        - phase4
        - phasemode
        - polarmode
        - status
        - data_file_name
        - data_file_ts
        - data
        - script_name
        - script
        - method_name

        :param inventory_name: name of the inventory offline data is connected to
        :type inventory_name: str

        :param username: author who created this data entry originally
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param gap: gap when this data set is produced
        :type gap: float

        :param phase1: phase 1 when this data set is produced
        :type phase1: float

        :param phase2: phase 2 when this data set is produced
        :type phase2: float

        :param phase3: phase 3 when this data set is produced
        :type phase3: float

        :param phase4: phase 4 when this data set is produced
        :type phase4: float

        :param phasemode: description for the mode of phase, which is determined by gap/phase
        :type phasemode: str

        :param polarmode: description for the mode of polar, which is determined by gap/phase
        :type polarmode: str

        :param status: status of this data set
        :type status: int

        :param data_file_name: file name of the data
        :type data_file_name: str

        :param data_file_ts: time stamp of data file with format like "YYYY-MM-DD HH:MM:SS"
        :type data_file_ts: str

        :param data: real data dumped into JSON string
        :type data: str

        :param script_name: name of script to produce the data
        :type script_name: str

        :param script: script to produce the data
        :type script: str

        :param method_name: name of method used to produce the data
        :type method_name: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': offline_data_id}

        :Raises: HTTPError
        '''

        # Set URL
        url = 'saveofflinedata/'

        # Set parameters
        params = {}

        # Add inventory name
        if 'inventory_name' in kws:

            # Check inventory name
            if kws['inventory_name'] is None:
                self.__raise_for_status(400, 'If inventory name is passed it should not be None!')

            params['inventory_name'] = kws['inventory_name']

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add username
        if 'username' in kws:
            params['username'] = kws['username']

        # Add gap
        if 'gap' in kws:
            params['gap'] = kws['gap']

        # Add phase1
        if 'phase1' in kws:
            params['phase1'] = kws['phase1']

        # Add phase2
        if 'phase2' in kws:
            params['phase2'] = kws['phase2']

        # Add phase3
        if 'phase3' in kws:
            params['phase3'] = kws['phase3']

        # Add phase4
        if 'phase4' in kws:
            params['phase4'] = kws['phase4']

        # Add phasemode
        if 'phasemode' in kws:
            params['phasemode'] = kws['phasemode']

        # Add polarmode
        if 'polarmode' in kws:
            params['polarmode'] = kws['polarmode']

        # Add status
        if 'status' in kws:
            params['status'] = kws['status']

        # Add data file name
        if 'data_file_name' in kws:
            params['data_file_name'] = kws['data_file_name']

        # Add data file timestamp
        if 'data_file_ts' in kws:
            params['data_file_ts'] = kws['data_file_ts']

        # Add data
        if 'data' in kws:
            fileName = kws['data']

            with open(fileName, 'rb') as f:
                ur = self.__session.post(self.__baseURL+'saverawdata/', files={'file': f}, auth=self.__auth)
                self.__raise_for_status(ur.status_code, ur.text)

            params['data_id'] = ur.json()['id']

        # Add script_name
        if 'script_name' in kws:
            params['script_name'] = kws['script_name']

        # Add script
        if 'script' in kws:
            params['script'] = kws['script']

        # Add method name
        if 'method_name' in kws:
            params['method_name'] = kws['method_name']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateOfflineData(self, offline_data_id, **kws):
        '''
        Update insertion device offline data by its id

        parameters:
        - inventory_name
        - username
        - description
        - gap
        - phase1
        - phase2
        - phase3
        - phase4
        - phasemode
        - polarmode
        - status
        - data_file_name
        - data_file_ts
        - data
        - script_name
        - script
        - method_name

        :param inventory_name: name of the inventory offline data is connected to
        :type inventory_name: str

        :param username: author who created this data entry originally
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param gap: gap when this data set is produced
        :type gap: float

        :param phase1: phase 1 when this data set is produced
        :type phase1: float

        :param phase2: phase 2 when this data set is produced
        :type phase2: float

        :param phase3: phase 3 when this data set is produced
        :type phase3: float

        :param phase4: phase 4 when this data set is produced
        :type phase4: float

        :param phasemode: description for the mode of phase, which is determined by gap/phase
        :type phasemode: str

        :param polarmode: description for the mode of polar, which is determined by gap/phase
        :type polarmode: str

        :param status: status of this data set
        :type status: int

        :param data_file_name: file name of the data
        :type data_file_name: str

        :param data_file_ts: time stamp of data file with format like "YYYY-MM-DD HH:MM:SS"
        :type data_file_ts: str

        :param data: real data dumped into JSON string
        :type data: str

        :param script_name: name of script to produce the data
        :type script_name: str

        :param script: script to produce the data
        :type script: str

        :param method_name: name of method used to produce the data
        :type method_name: str

        :return: True if everything is ok

        :Raises: HTTPError
        '''
        # Set URL
        url = 'updateofflinedata/'

        # Set parameters
        params = {
            'offline_data_id': offline_data_id
        }

        # Add inventory name
        if 'inventory_name' in kws:

            # Check inventory name
            if kws['inventory_name'] is None:
                self.__raise_for_status(400, 'If inventory name is passed it should not be None!')

            params['inventory_name'] = kws['inventory_name']

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add username
        if 'username' in kws:
            params['username'] = kws['username']

        # Add gap
        if 'gap' in kws:
            params['gap'] = kws['gap']

        # Add phase1
        if 'phase1' in kws:
            params['phase1'] = kws['phase1']

        # Add phase2
        if 'phase2' in kws:
            params['phase2'] = kws['phase2']

        # Add phase3
        if 'phase3' in kws:
            params['phase3'] = kws['phase3']

        # Add phase4
        if 'phase4' in kws:
            params['phase4'] = kws['phase4']

        # Add phasemode
        if 'phasemode' in kws:
            params['phasemode'] = kws['phasemode']

        # Add polarmode
        if 'polarmode' in kws:
            params['polarmode'] = kws['polarmode']

        # Add status
        if 'status' in kws:
            params['status'] = kws['status']

        # Add data file name
        if 'data_file_name' in kws:
            params['data_file_name'] = kws['data_file_name']

        # Add data file timestamp
        if 'data_file_ts' in kws:
            params['data_file_ts'] = kws['data_file_ts']

        # Add data
        if 'data' in kws:
            fileName = kws['data']

            with open(fileName, 'rb') as f:
                ur = self.__session.post(self.__baseURL+'saverawdata/', files={'file': f}, auth=self.__auth)
                self.__raise_for_status(ur.status_code, ur.text)

            params['data_id'] = ur.json()['id']

        # Add script_name
        if 'script_name' in kws:
            params['script_name'] = kws['script_name']

        # Add script
        if 'script' in kws:
            params['script'] = kws['script']

        # Add method name
        if 'method_name' in kws:

            # Check method name
            if kws['method_name'] is None:
                self.__raise_for_status(400, 'If method name is passed it should not be None!')

            params['method_name'] = kws['method_name']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def deleteOfflineData(self, offline_data_id):
        '''
        Delete offline data

        :param offline_data_id: offline data id
        :type offline_data_id: int

        :return: True if everything was ok

        :Raises: HTTPError
        '''
        # Set URL
        url = 'deleteofflinedata/'

        # Set parameters
        params = {
            'offline_data_id': offline_data_id
        }

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def retrieveOnlineData(self, **kws):
        '''Retrieve insertion device online data using any of the acceptable key words:

        - onlineid
        - install_name
        - username
        - description
        - url
        - status
        - with_data
        - data_path
        - callback

        :param onlineid: id of the online data we want to update by
        :type onlineid: int

        :param install_name: device name that the data belongs to
        :type install_name: str

        :param username: author who updated this data entry
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param url: external url of the data file is stored
        :type url: str

        :param status: status of this data set
        :type status: int

        :param with_data: should data be downloaded from the server or not
        :type with_data: boolean

        :param data_path: path to the local file in which downloaded file will be put to
        :type data_path: string

        :param callback: reference to a local method that will receive info about a file that is being downloaded. This parameter, if present, is a hook function that will be called once on establishment of the network connection and once after each
                        block read thereafter. The hook will be passed three arguments; a count of blocks transferred so far, a block size in bytes, and the total size of the file. The third argument may be -1 in some cases.

            Example of the callback method

            def callback(block_number, block_size, total_size):
                print block_number, block_size, total_size

        :type callback: function

        :return: a map with structure like:

            .. code-block:: python

                {'id': {
                        'id':,            #int
                        'installid':,     #int
                        'install_name':,  #string
                        'username':,      #string
                        'description':,   #string
                        'url':,           #string
                        'date':,          #date
                        'status':,        #int
                    }
                }

        :Raises: HTTPError
        '''

        # Set URL
        url = 'onlinedata/'

        # Set parameters
        params = {}

        # Add online id
        if 'onlineid' in kws:
            params['onlineid'] = kws['onlineid']

        # Add install name
        if 'install_name' in kws:
            params['install_name'] = kws['install_name']

        # Add username
        if 'username' in kws:
            params['username'] = kws['username']

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add url
        if 'url' in kws:
            params['url'] = kws['url']

        # Add status
        if 'status' in kws:
            params['status'] = kws['status']

        r = self.__session.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        returnData = r.json()

        # Set data path
        data_path = None

        if 'data_path' in kws:
            data_path = kws['data_path']

        # Set callback
        callback = None

        if 'callback' in kws:
            callback = kws['callback']

        # Append data if with_data is set
        if 'with_data' in kws and kws['with_data'] is True:

            # Go through all returned online data and append data
            onlineDataKeys = returnData.keys()

            for key in onlineDataKeys:
                onlineData = returnData[key]
                urlParts = self.__baseURL.split('/')
                downloadUrl = urlParts[:-3]

                urllib.urlretrieve('/'.join(downloadUrl) + '/' + onlineData['url'], filename=data_path, reporthook=callback)

        return returnData

    def saveOnlineData(self, install_name, **kws):
        '''Save insertion device online data using any of the acceptable key words:

        - install_name
        - username
        - description
        - data
        - data_file_name
        - status

        The data itself is stored on server's harddisk because its size might blow up to GB level.
        Ths file url is stored in the database.

        :param install_name: device name that the data belongs to
        :type install_name: str

        :param username: author who updated this data entry
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param data: path to the file we want to upload
        :type data: str

        :param data_file_name: name of the file we want to upload
        :type data_file_name: str

        :param status: status of this data set
        :type status: int

        :return: a map with structure like:

            .. code-block:: python

                {'id': data id}

        :Raises: HTTPError
        '''

        # Set URL
        url = 'saveonlinedata/'

        # Set parameters
        params = {
            'install_name': install_name
        }

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add username
        if 'username' in kws:
            params['username'] = kws['username']

        # Add url
        if 'data' in kws and 'data_file_name' in kws:

            # Upload a file
            uploadedFile = self.uploadFile(kws['data'], kws['data_file_name'])

            params['url'] = uploadedFile['path']

        # Add status
        if 'status' in kws:
            params['status'] = kws['status']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def updateOnlineData(self, online_data_id, **kws):
        '''
        Update insertion device online data using any of the acceptable key words:

        - install_name
        - username
        - description
        - data
        - data_file_name
        - status

        The data itself is stored on server's harddisk because its size might blow up to GB level.
        Ths file url is stored in the database.

        :param install_name: device name that the data belongs to
        :type install_name: str

        :param username: author who updated this data entry
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param data: path to the file we want to upload
        :type data: str

        :param data_file_name: name of the file we want to upload
        :type data_file_name: str

        :param status: status of this data set
        :type status: int

        :return: True if everything is ok

        :Raises: HTTPError
        '''
        # Set URL
        url = 'updateonlinedata/'

        # Set parameters
        params = {
            'online_data_id': online_data_id
        }

        # Add install name
        if 'install_name' in kws:

            # Check install name
            if kws['install_name'] is None:
                self.__raise_for_status(400, 'If install name is passed it should not be None!')

            params['install_name'] = kws['install_name']

        # Add description
        if 'description' in kws:
            params['description'] = kws['description']

        # Add username
        if 'username' in kws:
            params['username'] = kws['username']

        # Add url
        if 'data' in kws and 'data_file_name' in kws:

            # Upload a file
            uploadedFile = self.uploadFile(kws['data'], kws['data_file_name'])

            params['url'] = uploadedFile['path']

        # Add status
        if 'status' in kws:
            params['status'] = kws['status']

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def deleteOnlineData(self, online_data_id):
        '''
        Delete online data

        :param online_data_id: online data id
        :type online_data_id: int

        :return: True if everything was ok

        :Raises: HTTPError
        '''
        # Set URL
        url = 'deleteonlinedata/'

        # Set parameters
        params = {
            'online_data_id': online_data_id
        }

        r = self.__session.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def uploadFile(self, data, file_name):
        '''
        Upload a file

        params:
            - data path to the file
            - file_name name of the file
        '''

        with open(data, 'rb') as f:

            # Set parameters
            params = {
                'file_name': file_name
            }

            r = self.__session.post(self.__baseURL+'file/', files={'file': f}, data=params, auth=self.__auth)
            self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def idodsInstall(self):
        '''
        Save common data into the database

        :return: True if everything is ok

        :Raises: HTTPError
        '''

        # Try to retrieve data method
        url = 'idods_install/'

        r = self.__session.post(self.__baseURL+url, verify=False, headers=self.__jsonheader, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def testAuth(self):
        '''
        Test auth

        :Raises: HTTPError
        '''

        url = 'test/'

        r = self.__session.post(self.__baseURL+url, verify=False, headers=self.__jsonheader, auth=self.__auth)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    def testCall(self):
        '''
        Test call without auth

        :Raises: HTTPError
        '''

        url = 'testcall/'

        r = self.__session.post(self.__baseURL+url, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)

        return r.json()

    @classmethod
    def __raise_for_status(self, status_code, reason):
        http_error_msg = ''

        if 400 <= status_code < 500:
            http_error_msg = '%s Client Error: %s' % (status_code, reason)

        elif 500 <= status_code < 600:
            http_error_msg = '%s Server Error: %s' % (status_code, reason)

        if http_error_msg:
            http_error = HTTPError(http_error_msg)
            http_error.response = self
            raise http_error
