Client API Library
==============================================

Client is implemented in Python and is accessing active interlock service through a RESTful interface. For now, there is only one method in library and it allows us to download/retrieve approved dataset from the database. If there is no approved dataset in the database, **no dataset available message** is returned instead. If dataset exists in the database it is returned as a json object with the following structure: ::

 {
  'bm': {
    bm data
  },
  'id': {
    id data
  },
  'logic': {
    logic data
  }
 }

After dataset is downloaded status of the dataset is set to **active**.

Authentication
--------------------

Downloading active interlock requires user to have special permissions. To check if user has appropriate permissions, user needs to be authenticated when requesting the data.

To authenticate requests, user must create an *activeinterlock.conf* file in the */etc/* directory with the following contents: ::

 [DEFAULT]
 username=username
 password=password

Client API Library
---------------------

This library is to access active interlock service.

.. automodule:: activeinterlockpy.activeinterlockclient
    :members: 

