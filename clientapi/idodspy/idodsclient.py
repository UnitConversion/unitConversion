'''
Copyright (c) 2013 Brookhaven National Laboratory

All rights reserved. Use is subject to license terms and conditions.

Created on Feb 17, 2014
@author: dejan.dezman@cosylab.com

'''

import sys
if sys.version_info[0] != 2 or sys.version_info[1] < 6:
    print("This library requires at least Python version 2.6")
    sys.exit(1)

import requests
_requests_version=[int(x) for x in requests.__version__.split('.')]
if _requests_version[0] < 1 or sys.version_info[1] < 1:
    print("This library requires at least Python-requests version 1.1.x")
    sys.exit(1)

from requests import auth
from requests import HTTPError

from copy import copy

import base64
try: 
    import json
except ImportError: 
    import simplejson as json

from _conf import _conf

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
        self.__jsonheader = {'content-type':'application/json', 'accept':'application/json'}    
        self.__resource = 'test/'
        
        try:
            self.__baseURL = self.__getdefaultconfig('BaseURL', BaseURL)
            self.__userName = self.__getdefaultconfig('username', username)
            self.__password = self.__getdefaultconfig('password', password)
            
            if self.__userName and self.__password:
                #self.__auth = (self.__userName, self.__password)
                self.__auth = auth.HTTPBasicAuth(self.__userName, self.__password)
            
            else:
                self.__auth = None
            
            requests.post(self.__baseURL + self.__resource, headers=copy(self.__jsonheader), auth=self.__auth).raise_for_status()
            self.client = requests.session()
        
        except:
            raise Exception, 'Failed to create client to ' + self.__baseURL + self.__resource
        
    def __getdefaultconfig(self, arg, value):
        if value == None and _conf.has_option('DEFAULT', arg):
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
        params={
            'name': name
        }
        
        # Add description
        if description:
            params['description'] = description
        
        r=self.client.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)
        
        return r.json()

    def saveVendor(self, name, description = None):
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
        params={
            'name': name
        }
        
        # Add description
        if description:
            params['description'] = description
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
            'vendor_id': None,
            'old_name': old_name,
            'name': name
        }
        
        # Add description
        if 'description' in kws:
            params['description'] = kws['description']
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
        self.__raise_for_status(r.status_code, r.text)
        
        return r.json()

    def retrieveComponentType(self, name, description = None):
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
        params={
            'name': name
        }
        
        # Add description
        if description:
            params['description'] = description
        
        r=self.client.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
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
        params={
            'name': name
        }
        
        # Add description
        if description:
            params['description'] = description
        
        # Add props
        if props:
            params['props'] = json.dumps(props)
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
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
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
            'name': name
        }
        
        r=self.client.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)
        
        return r.json()

    def saveComponentTypePropertyType(self, name, description = None):
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
        params={
            'name': name
        }
        
        # Add description
        if description:
            params['description'] = description
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
            'property_type_id': None,
            'old_name': old_name,
            'name': name
        }
        
        # Add description
        if 'description' in kws:
            params['description'] = kws['description']
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
            'name': name
        }
        
        r=self.client.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
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
        params={
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
            if kws['vendor'] == None:
                self.__raise_for_status(400, 'If vendor is passed it should not be None!')
            
            params['vendor'] = kws['vendor']
        
        # Add props
        if 'props' in kws:
            params['props'] = json.dumps(kws['props'])
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
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
            if kws['vendor'] == None:
                self.__raise_for_status(400, 'If vendor is passed it should not be None!')
            
            params['vendor'] = kws['vendor']
        
        # Add props
        if 'props' in kws:
            params['props'] = json.dumps(kws['props'])
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
            'name': name
        }
        
        r=self.client.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)
        
        return r.json()

    def saveInventoryPropertyTemplate(self, cmpnt_type, name, description = None, default = None, unit = None):
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
        params={
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
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
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
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
        self.__raise_for_status(r.status_code, r.text)
        
        return r.json()

    def retrieveInstall(self, name, **kws):
        '''Retrieve insertion device installation using any of the acceptable key words:

        - name: installation name, which is its label on field
        - description: installation description
        - cmpnt_type: component type name of the device
        - coordinatecenter: coordinate center number
        
        raises:
            HTTPError
            
        returns:
            {'id': {
                    'id':                #int,
                    'name':              #string,
                    'description':       #string,
                    'cmpnt_type':         #string,
                    'coordinatecenter':  #float
                }
            }
        '''
        
        # Set URL
        url = 'install/'
        
        # Set parameters
        params={
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
        
        r=self.client.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
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
        params={
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
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
            'old_name': old_name,
            'name': name
        }
        
        # Add description
        if 'description' in kws:
            params['description'] = kws['description']
        
        # Add component type
        if 'cmpnt_type' in kws:
            
            # Check for none
            if kws['cmpnt_type'] == None:
                self.__raise_for_status(400, 'If component type parameter is present it should not be set to None!')
            
            params['cmpnt_type'] = kws['cmpnt_type']
        
        # Add coordinate center
        if 'coordinatecenter' in kws:
            params['coordinatecenter'] = kws['coordinatecenter']
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
        self.__raise_for_status(r.status_code, r.text)
        
        return r.json()

    def retrieveInstallRel(self, install_rel_id = None, parent_install = None, child_install = None, description = None, order = None, date = None, expected_property = None):
        '''
        Retrieve install rel from the database. Specific relation can be retrieved or all the children of specific parent or
        all the parents of specific child.
        
        params:
            - install_rel_id: id of the install_rel table
            - parent_install: name of the parent install element
            - child_install: name of the child install element
            - description: description of a relationship
            - order: order number of child element in the parent element; accepts a range in a tuple
            - date: date of the device installation; accepts a range in a tuple
            - expected_property: if we want to search for relationships with specific property set to a specific value, we
              can prepare a dict and pass it to the function e.g. {'beamline': 'xh*'} will return all of the
              beamlines with names starting with xh or {'beamline': None} will return all of the beamlines
            
        returns:
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
            
        raises:
            HTTPError
        '''
        
        # Set URL
        url = 'installrel/'
        
        # Set parameters
        params={
            'install_rel_id': install_rel_id,
            'parent_install': parent_install,
            'child_install': child_install,
            'description': description,
            'order': order,
            'date': date
        }
        
        r=self.client.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)
        
        return r.json()

    def saveInstallRel(self, parent_install, child_install, description = None, order = None, props = None):
        '''
        Save install relationship in the database.
        
        params:
            - parent_install: id of the parent element
            - child_install: id of the child element
            - description: description of the relationship
            - order: order of the child in the relationship
            - props :
                {
                    'key1': 'value1',
                    ...
                    'keyN': 'valueN'
                }
        returns:
            {'id': id of the saved install rel}
            
        raises:
            HTTPError
        '''
        
        # Set URL
        url = 'saveinstallrel/'
        
        # Set parameters
        params={
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
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
        self.__raise_for_status(r.status_code, r.text)
        
        return r.json()

    def updateInstallRel(self, parent_install, child_install, **kws):
        '''
        Update install relationship.
        
        params:
            - parent_install: name of the parent element we want ot update by
            - child_install: name of the child element we want ot update by
            - description: description of the relationship
            - order: order of the child in the relationship
            - props :
                {
                    'key1': 'value1',
                    ...
                    'keyN': 'valueN'
                }
        
        returns:
            True if everything is ok
            
        raises:
            HTTPError
        '''
        
        # Set URL
        url = 'updateinstallrel/'
        
        # Set parameters
        params={
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
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
            'name': name
        }
        
        r=self.client.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
        self.__raise_for_status(r.status_code, r.text)
        
        return r.json()

    def saveInstallRelPropertyType(self, name, description = None, unit = None):
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
        params={
            'name': name
        }
        
        # Add description
        if description:
            params['description'] = description
        
        # Add unit
        if unit:
            params['unit'] = unit
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
            'old_name': old_name,
            'name': name
        }
        
        # Add description
        if 'description' in kws:
            params['description'] = kws['description']
        
        # Add unit
        if 'unit' in kws:
            params['unit'] = kws['unit']
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
            'inventory_to_install_id': inventory_to_install_id,
            'install_name': install_name,
            'inv_name': inv_name
        }
        
        r=self.client.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
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
        params={
            'install_name': install_name,
            'inv_name': inv_name
        }
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
            'inventory_to_install_id': inventory_to_install_id,
            'install_name': install_name,
            'inv_name': inv_name
        }
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
        self.__raise_for_status(r.status_code, r.text)
        
        return r.json()

    def retrieveDataMethod(self, name, description = None):
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
        params={
            'name': name
        }
        
        # Add description
        if description:
            params['description'] = description
        
        r=self.client.get(self.__baseURL+url, params=params, verify=False, headers=self.__jsonheader)
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
        params={
            'name': name
        }
        
        # Add description
        if description:
            params['description'] = description
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
        params={
            'datamethod_id': None,
            'old_name': old_name,
            'name': name
        }
        
        # Add description
        if 'description' in kws:
            params['description'] = kws['description']
        
        r=self.client.post(self.__baseURL+url, data=params, headers=self.__jsonheader, verify=False)
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
    