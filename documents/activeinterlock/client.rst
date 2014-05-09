Client API Library
==============================================

Client is implemented in Python and is accessing active interlock service through a RESTful interface. For now, there is only one method in library and it allows us to download/retrieve datasets from the database. If there is no dataset with specific status in the database, **no dataset available message** is returned instead. If dataset exists in the database it is returned as a json object with the following structure: ::

 {
  'bm': {   # Bending Magnet part of the returned object
    'id': {
      'id':                   , #int, id of the device in the database
      'ai_id':                , #int, id of the active interlock
      'name':                 , #str, name of the device
      'definition':           , #str, definition of the device
      'logic':                , #str, name of the logic
      'shape':                , #str, shape of the logic
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
      'name':                 , #str, name of the device and also s3 name
      'definition':           , #str, definition of the device
      'logic':                , #str, name of the logic
      'shape':                , #str, shape of the logic
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
      'label':                , # str, column's name
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

Response comprises of three parts. Part for the BPM data, part for the ID data and Logic part.

Examples of use
---------------------

To download active interlock dataset firstly we have to initialize a client::

  client = ActiveInterlockClient(BaseURL="http://localhost:8000/ai/")

Client accepts three input parameters that can also be omitted if they are defined in **activeinterlock.conf** file. These parameters are:
 * BaseURL
 * username
 * password

In the example above we passed in **BaseURL** parameter do define server access URL. After client is initialized, we can download active interlock by calling::

  client.downloadActiveInterlock()

Another way of calling download is by passing a status parameter::

  client.downloadActiveInterlock("approved")

We can only download active interlock datasets that have the following statuses:
 * approved
 * active

In case status parameter is omitted it defaults to **approved**. Returned value of download method is explained in the following section.

If active interlock with **approved** status is downloaded, its status is changed to **active**.

Authentication
--------------------

Downloading active interlock requires user to have special permissions. To check if user has appropriate permissions, user needs to be authenticated when requesting the data.

To authenticate requests, user must create an **activeinterlock.conf** file in the **/etc/** directory with the following contents: ::

 [DEFAULT]
 username=username
 password=password

After client is initialized it will check for this file, parse it and authenticate all POST requests with given username and password. If username and/or password are not correct or if file is not found in the directory mentioned above, server will respond with **401 Unauthorized** error message.

Client API Library
---------------------

This library is to access active interlock service.

.. automodule:: activeinterlockpy.activeinterlockclient
    :members: 

