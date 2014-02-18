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
            
            if username and password:
                self.__auth = auth.HTTPBasicAuth(username, password)
            
            else:
                self.__auth = None
            
            requests.post(self.__baseURL + self.__resource, headers=copy(self.__jsonheader), auth=(self.__userName, self.__password)).raise_for_status()
            self.client = requests.session()
        
        except:
            raise Exception, 'Failed to create client to ' + self.__baseURL + self.__resource
        
    def __getdefaultconfig(self, arg, value):
        if value == None and _conf.has_option('DEFAULT', arg):
            return _conf.get('DEFAULT', arg)
        else:
            return value

    def retrieveactiveinterlock(self, status, datefrom=None, dateto=None, withdata=True, rawdata=False):
        '''Retrieve a data set according its saved time, and status.
        One data set should have same properties for all device although its value could be empty.
        
        data structure:
        
        .. code-block:: python
        
            {id: {
                  'status': ,
                  'rawdata': {'name':, 'data': },
                  'description': , 
                  'author': ,
                  'initialdate': ,
                  'lastmodified': ,
                  'modifieddate': ,
                  'data':{'label':       [], # str, column's name, also property type collections for one active interlock unit.
                          'units':       [], # str, units for each columns. Empty string if it does not have one.
                         
                          # the following are those columns appeared in ``label`` field.
                          'name':        [], # str, active interlock device name 
                          'definition':  [], # str, definition for that device
                          'logicname':   [], # str, active interlock envelop name
                          'shape':       [], # str, allowed shape in phase space
                          's':           [], # double, s position in a lattice, particularly in a installation lattice
                          'offset':      [], # double, offset relative to the center of a straight section
                          'safecurent':  [], # double, allowed beam current for safe operation.  
                                             # no need for active interlock if beam current is lower than this value.
                          'aihol':       [], # double, allowed horizontal offset limit
                          'aivol':       [], # double, allowed vertical offset limit
                          'aihal':       [], # double, allowed horizontal angle limit
                          'aival':       [], # double, allowed vertical angle limit
                          'up_name':     [], # str, upstream BPM name involved in this active interlock unit
                          'up_definition': [], #str, upstream device definition
                          'up_offset':   [], # double, offset of upstream BPM relative to the center of a straight section
                          'up_aihol':    [], # double, allowed horizontal offset limit of upstream BPM
                          'up_aivol':    [], # double, allowed vertical offset limit of upstream BPM
                          'down_name':   [], # str, downstream BPM name involved in this active interlock unit
                          'down_definition': [], #str, downstream device definition
                          'down_offset': [], # double, offset of downstream BPM relative to the center of a straight section
                          'down_aihol':  [], # double, allowed horizontal offset limit of downstream BPM
                          'down_aivol':  [], # double, allowed vertical offset limit of downstream BPM
                          'logiccode':   [], # logic algorithm encoding code
                         }
                 },
                 ...
            }
            
        label is now defined as below:
         
        .. code-block:: python
         
            ['name', 'definition', 'logicname', 'shape', 'logic', 'logiccode'
             's', 'offset', 'safecurent', 'aihol', 'aivol', 'aihal', 'aival',
             'up_name', 'up_definition', 'up_offset', 'up_aihol', 'up_aivol',
             'down_name', 'down_definition', 'down_offset', 'down_aihol', 'down_aivol',
            ]
        
        units is for each columns contained in ``label``, therefore, it should have exact sequence as it appears in label
        except ``units`` itself which should be the last one.
        is most like as below:
        
        .. code-block:: python
         
            ['', '', '', '', '', '', 
             'm', 'm', 'mA', 'mm', 'mm', 'mrad', 'mrad',
             '', '', 'm', 'mm', 'mm',
             '', '', 'm', 'mm', 'mm'
            ]
        
        :param status: Current status.
        :type status: int
        
        :param datefrom: data saved after this time. Default is None, which means data from very beginning. It has format as **yyyy-MM-dd hh:mm:ss**.
        :type datafrom: datetime
        
        :param dateto: data saved before this time. Default is None, which means data till current. It has format as **yyyy-MM-dd hh:mm:ss**.
        :type datato: datetime
        
        :param withdata: get data set. Default is true, which means always gets data by default. Otherwise, only device names are retrieved for desired data set.
        :type withdata: boolean
        
        :param rawdata: get raw data back also. Default is false, which means no raw data.
        :type rawdata: boolean
        
        :Returns: dict
            
        :Raises: HTTPError
        
        '''
        params = {'function': 'retrieveActiveInterlock',
                  'status': status
                  }
        if datefrom != None:
            params['datefrom'] = datefrom
        if dateto != None:
            params['dateto'] = dateto
        if withdata != None:
            params['withdata'] = withdata
        if rawdata != None:
            params['rawdata'] = rawdata

        resp=self.client.get(self.__baseURL+self.__resource, 
                             params=params,
                             headers=copy(self.__jsonheader),
                             verify=False,
                             auth=self.__auth)
        self.__raise_for_status(resp.status_code, resp.text)
        return resp.json()
    
    def saveactiveinterlock(self, data, description=None, datafile=None, active=True, author=None):
        '''Save a new data set of active interlock.
        By default, it deactivates existing active data set, and active this new data set.
        Only one active data is allowed.
        
        A logic of active interlock has to be saved first, otherwise, an AttributeError might raise if logic can not be found.
        
        data structure:
        
        .. code-block:: python
        
            {'label':       [], # str, column's name, also property type collections for one active interlock unit.
             'units':       [], # str, units for each columns. Empty string if it does not have one.
             
             # the following are those columns appeared in ``label`` field.
             'name':        [], # str, active interlock device name 
             'definition':  [], # str, definition for that device
             'logicname':   [], # str, active interlock envelop name
             'shape':       [], # str, allowed shape in phase space
             's':           [], # double, s position in a lattice, particularly in a installation lattice
             'offset':      [], # double, offset relative to the center of a straight section
             'safecurent':  [], # double, allowed beam current for safe operation.  
                                # no need for active interlock if beam current is lower than this value.
             'aihol':       [], # double, allowed horizontal offset limit
             'aivol':       [], # double, allowed vertical offset limit
             'aihal':       [], # double, allowed horizontal angle limit
             'aival':       [], # double, allowed vertical angle limit
             'up_name':     [], # str, upstream BPM name involved in this active interlock unit
             'up_definition': [], #str, upstream device definition
             'up_offset':   [], # double, offset of upstream BPM relative to the center of a straight section
             'up_aihol':    [], # double, allowed horizontal offset limit of upstream BPM
             'up_aivol':    [], # double, allowed vertical offset limit of upstream BPM
             'down_name':   [], # str, downstream BPM name involved in this active interlock unit
             'down_definition': [], #str, downstream device definition
             'down_offset': [], # double, offset of downstream BPM relative to the center of a straight section
             'down_aihol':  [], # double, allowed horizontal offset limit of downstream BPM
             'down_aivol':  [], # double, allowed vertical offset limit of downstream BPM
            }
            
        label is now defined as below:
         
        .. code-block:: python
         
            ['name', 'definition', 'logicname', 'shape',
             's', 'offset', 'safecurent', 'aihol', 'aivol', 'aihal', 'aival',
             'up_name', 'up_definition', 'up_offset', 'up_aihol', 'up_aivol',
             'down_name', 'down_definition', 'down_offset', 'down_aihol', 'down_aivol',
            ]
            
        units is for each columns contained in ``label``, therefore, it should have exact sequence as it appears in label
        except ``units`` itself which should be the last one.
        is most like as below:
        
        .. code-block:: python
         
            ['', '', '', '',
             'm', 'm', 'mA', 'mm', 'mm', 'mrad', 'mrad',
             '', '', 'm', 'mm', 'mm',
             '', '', 'm', 'mm', 'mm'
            ]
            
        :param data: original data structure is described as above.
        :type data: dict
            
        :param description: comments or any other notes for this data set.
        :type description: str
        
        :param datafile: raw data file with full path.
        :type datafile: str
        
        :param active: set current data set active. It sets new data set as active by default unless it is explicitly set to keep old active data set.
        :type active: boolean
        
        :param author: the person who set this data set.
        :type author: str
        
        :Returns: active interlock internal id if saved successfully.
            
        :Raises: HTTPError 

        '''
        payload = {'function': 'saveActiveInterlock',
                   'data':    json.dumps(data),
                   'active':  active, 
                   }
        if description != None:
            payload['description'] = description
        if datafile != None:
            with file(datafile, 'r') as f:
                bindata = base64.b64encode(f.read())
                payload['rawdata'] = json.dumps({'name': datafile,
                                                 'data': bindata})
        if author != None:
            payload['author'] = author

        resp=self.client.post(self.__baseURL+self.__resource, 
                              data=payload,
                              headers=copy(self.__jsonheader),
                              verify=False,
                              auth=self.__auth)
        self.__raise_for_status(resp.status_code, resp.text)
        return resp.json()['id']

    def updateactiveinterlockstatus(self, aiid, status, author=None):
        '''Update status of a data set.
        Once data is saved into database, only its status is allowed to be updated between active & inactive.
        Only up to one (1) data set is allowed to be active. When the status is to active a particular data set,
        it deactivates current active data set.
        
        Currently, the status is either active and inactive as defined as below: ::
        
            0: inactive
            1: active 
        
        However, the definition could be extended when there is other requirement.
        
        :param aiid: internal id of an active interlock data set
        :type aiid: int
        
        :param status: new status code
        :type status: int
        
        :param author: name who requests this update
        :type author: str
            
        :Returns: boolean
            
            The return code: ::
                
                True -- when the status is changed.
                False -- when the status is not changed.
        
        :Raises: HTTPError
        
        '''    
        payload={'function': 'updateActiveInterlockStatus',
                 'id': aiid,
                 'status': status, 
         }
        if author != None:
            payload['author']=author
        resp=self.client.post(self.__baseURL+self.__resource, 
                              data=payload,
                              headers=copy(self.__jsonheader),
                              verify=False,
                              auth=self.__auth)
        self.__raise_for_status(resp.status_code, resp.text)
        return resp.json()['status']
    
    def retrieveactiveinterlockproptype(self, name, unit=None, description=None):
        '''Each involved in active interlock system has some properties like offset, AIHOL/AIVOL, AIHAL/AIVAL, safe current, and so on.
        This method is to retrieve active interlock property type information with given name, unit, and/or description.
        
        Wildcast matching is supported with:
        
            - ``*`` for multiple characters match, 
            - ``?`` for single character match.

        :param name: property type name.
        :type name: str
        
        :param unit: unit of given property type.
        :type unit: str
        
        :param description: description of given property type.
        :type description: str
        
        :returns: dict
            
            A python dictionary is return with each field as an list which could be converted into a table. Its structure is as below:
            
            .. code-block:: python
            
                {'label':       [], # str, columns's name
                 'id':          [], # int, internal id of property type
                 'name':        [], # str, active interlock property type name 
                 'unit':        [], # str, active interlock property type unit
                 'description': [], # str, property type description
                 'date':        [], # datetime, when this entry was created
                }
        
        :raises: HTTPError
        
        '''
        params={'function': 'retrieveActiveInterlockPropType',
                'name': name, 
         }
        if unit != None:
            params['unit']=unit
        if description != None:
            params['description']=description
        resp=self.client.get(self.__baseURL+self.__resource, 
                             params=params,
                             headers=copy(self.__jsonheader),
                             verify=False,
                             auth=self.__auth)
        self.__raise_for_status(resp.status_code, resp.text)
        return resp.json()

    def saveactiveinterlockproptype(self, name, unit=None, description=None):
        '''Each involved in active interlock system has some properties like offset, AIHOL/AIVOL, AIHAL/AIVAL, safe current, and so on.
        This method is to save active interlock property type information with given name, unit, and/or description.
        
        The property name with given unit is unique in the database. It allows user to reuse a property type name, but given it 
        a different unit.
        
        :param name: property type name.
        :type name: str
        
        :param unit: unit of given property type.
        :type unit: str
        
        :param description: description of given property type.
        :type description: str
        
        :returns: internal property type id
            
        :raises: HTTPError
        
        '''
        payload={'function': 'saveActiveInterlockPropType',
                 'name': name, 
         }
        if unit != None:
            payload['unit']=unit
        if description != None:
            payload['description']=description
        resp=self.client.post(self.__baseURL+self.__resource, 
                              data=payload,
                              headers=copy(self.__jsonheader),
                              verify=False,
                              auth=self.__auth)
        self.__raise_for_status(resp.status_code, resp.text)
        return resp.json()['id']
        
    def retrieveactiveinterlocklogic(self, name, shape=None, logic=None):
        '''Retrieve logic information according given search constrains.
        Active interlock envelop name has to be provided as a minimum requirement for this function.
        
        Wildcast matching is supported for name and shape with:
        
            - ``*`` for multiple characters match, 
            - ``?`` for single character match.

        Wildcast is not supported for logic since the * is a math symbol.

        :param name: active interlock envelop name.
        :type name: str
        
        :param shape: active interlock shape name in phase space.
        :type shape: str
        
        :param logic: active interlock logic.
        :type logic: str
        
        :returns: dict 
            
            A python dictionary is return with each field as an list which could be converted into a table. Its structure is as below:
            
            .. code-block:: python
            
                {'label':  [], # str, column's name
                 'id':     [], # int, internal id of active interlock logic
                 'name':   [], # str, name of active interlock envelop 
                 'shape':  [], # str, allowed envelop shape in phase space
                 'logic':  [], # str, logic expression
                 'code':   [], # int, logic code for hardware convenience
                 'author': [], # str, who created this entry
                 'date':   [], # datetime, when this entry was created
                }
        
        :raises: HTTPError
        
        '''
        params={'function': 'retrieveActiveInterlockLogic',
                'name': name}
        if shape != None:
            params['shape']=shape
        if logic != None:
            params['logic']=logic
        resp=self.client.get(self.__baseURL+self.__resource, 
                             params=params,
                             headers=copy(self.__jsonheader),
                             verify=False,
                             auth=self.__auth)
        self.__raise_for_status(resp.status_code, resp.text)
        return resp.json()
    
    def saveactiveinterlocklogic(self, name, shape, logic, logiccode, author=None):
        '''Save logic information for active interlock system.
        It calls REST POST, and performs saveActiveInterlockLogic function.
        
        :param name: active interlock envelop name
        :type name: str
        
        :param shape: active interlock shape name in phase space
        :type shape: str
        
        :param logic: active interlock logic expression
        :type logic: str
        
        :param logiccode: logic algorithm encoding code for hardware convenience
        :type logiccode: int

        :param author: who creates this data set
        :type author: str
            
        :returns: internal id of active interlock logic
                
        :Raises: ValueError, HTTPError
        
        '''
        payload={'function': 'saveActiveInterlockLogic',
                 'name': name, 
                 'shape': shape, 
                 'logic': logic, 
                 'logiccode': logiccode, 
         }
        if author != None:
            payload['author']=author
        resp=self.client.post(self.__baseURL+self.__resource, 
                              data=payload,
                              headers=copy(self.__jsonheader),
                              verify=False,
                              auth=self.__auth)
        self.__raise_for_status(resp.status_code, resp.text)
        return resp.json()['id']

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
    