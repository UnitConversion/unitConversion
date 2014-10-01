The Client API
==============================================

The client is implemented in Python and accesses the active interlock service through a RESTful interface. Currently, there is only a single method in the library and it allows downloading/retrieval of datasets from the database. If there is no dataset with the specific status in the database, a **no dataset available** message is returned instead. If the dataset exists in the database, then it is returned as a JSON object with the following structure: ::

 {
  'bm': {   # Bending Magnet part of the returned object
    'id': {
      'id':                   , #int, id of the device in the database
      'ai_id':                , #int, id of the active interlock
      'name':                 , #str, name of the device
      'definition':           , #str, definition of the device
      'logic':                , #str, name of the logic
      'shape':                , #str, shape of the logic
      'logic_code':           , #int, logic code
      'bm_cell':              , #str, cell
      'bm_sequence':          , #str, sequence
      'bm_type':              , #str, type
      'bm_s':                 , #str, s
      'bm_aiolh':             , #str, horizontal offset limit
      'bm_aiorh':             , #str, horizontal offset origin
      'bm_aiolv':             , #str, vertical offset limit
      'bm_aiorv':             , #str, vertical offset origin
      'bm_safe_current':      , #str, safe current
      'bm_in_use':            , #str, is element in use
      'prop_statuses': {
        'prop1key':           , #int, status of the property,
        ...
        'propNkey':           , #int, status of the property
      },
      'prop_units': {
        'prop1key':           , #string, property unit,
        ...
        'propNkey':           , #string, property unit
      }
    }
  },
  'id': {
    'id': {   # Insertion Device part of the returned object
      'id':                   , #int, id of the device in the database
      'ai_id':                , #int, id of the active interlock
      'name':                 , #str, name of the device and also the s3 name
      'definition':           , #str, definition of the device
      'logic':                , #str, name of the logic
      'shape':                , #str, shape of the logic
      'logic_code':           , #int, logic code
      'cell':                 , #str, cell
      'type':                 , #str, type
      'set':                  , #str, set
      'str_sect':             , #str, straight section
      'defined_by':           , #str, defined by
      's1_name':              , #str, s1 name
      's1_pos':               , #str, s1 position
      's1_pos_from':          , #str, s1 position from AIE-ID location
      's2_name':              , #str, s2 name
      's2_pos':               , #str, s2 position
      's2_pos_from':          , #str, s2 position from AIE-ID location
      's3_pos':               , #str, s3 position
      's3_pos_from':          , #str, s3 position from center of straight section
      'max_offset':           , #str, maximum offset
      'max_angle':            , #str, maximum angle
      'extra_offset':         , #str, extra offset
      'x_offset_s1':          , #str, horizontal s1 offset
      'x_offset_origin_s1':   , #str, horizontal s1 offset origin
      'x_offset_s2':          , #str, horizontal s2 offset
      'x_offset_origin_s2':   , #str, horizontal s2 offset origin
      'x_offset_s3':          , #str, horizontal s3 offset
      'x_angle':              , #str, horizontal angle
      'y_offset_s1':          , #str, vertical s1 offset
      'y_offset_origin_s1':   , #str, vertical s1 offset origin
      'y_offset_s2':          , #str, vertical s2 offset
      'y_offset_origin_s2':   , #str, vertical s2 offset origin
      'y_offset_s3':          , #str, vertical s3 offset
      'y_angle':              , #str, vertical angle
      'safe_current':         , #str, safe current
      'in_use':               , #str, is element in use
      'prop_statuses': {
        'prop1key':           , #int, status of the property,
        ...
        'propNkey':           , #int, status of the property
      },
      'prop_units': {
        'prop1key':           , #string, property unit,
        ...
        'propNkey':           , #string, property unit
      }
    }
  },
  'logic': {   # Logic part of the returned object
    'id': {
      'label':                , # str, name of column
      'id':                   , # int, internal id of active interlock logic
      'name':                 , # str, name of active interlock envelop 
      'shape':                , # str, allowed envelop shape in phase space
      'logic':                , # str, logic expression
      'code':                 , # int, logic code for hardware convenience
      'status':               , # int, satus of the logic
      'created_by':           , # str, who created this entry
      'created_date':         , # datetime, when this entry was created
      'num':                  , # int, usage count of this logic
    }
  }
 }

The response is made up of three parts:
    - BPM data
    - ID data 
    - logic.

Examples of Use
---------------------

To download the active interlock dataset, the client must first be initialized::

  client = ActiveInterlockClient(BaseURL="http://localhost:8000/ai/")

The client accepts three input parameters that can be omitted if they have been defined in the **activeinterlock.conf** file. These parameters are:
 * BaseURL
 * username
 * password
where the **BaseURL** parameter defines the server access URL. After the client is initialized, the active interlock dataset can be downloaded by calling::

  client.downloadActiveInterlock()

Another method of downloading the dataset is by passing a status parameter::

  client.downloadActiveInterlock("approved")

Only active interlock datasets that have the following statuses can be downloaded:
 * approved
 * active

If the status parameter is omitted, it defaults to **approved**. The returned value of the download method is explained in the  :ref:`activeInterlockDownloadResponse` section. 

If an active interlock dataset with an **approved** status is downloaded, its status is changed to **active**.

.. _activeInterlockDownloadResponse:

Authentication
--------------------

Downloading an active interlock dataset requires the user to have special permissions, which means that the user must be authenticated when requesting the data.

To authenticate requests, the user must create an **activeinterlock.conf** file in the **/etc/** directory with the following content: ::

 [DEFAULT]
 username=username
 password=password

After the client has been initialized, it will look for this file, parse it and authenticate all POST requests with the provided username and password. If the file is not found in the directory, or if the username and/or password are not correct, then the server will respond with a **401 Unauthorized** error message.

The Client API Library
---------------------

This library accesses the active interlock service.

.. automodule:: activeinterlockpy.activeinterlockclient
    :members: 

