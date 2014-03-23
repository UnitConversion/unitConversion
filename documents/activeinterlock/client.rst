Client API Library
==============================================

Client is implemented in Python and is accessing active interlock service through a RESTful interface. For now, there is only one method in library and it allows us to download/retrieve approved dataset from the database. It there is no approved dataset in the database, *no dataset available message* is returned instead.

Authentication
--------------------

Downloading active interlock requires user to posses special permissions. To check if user has appropriate permissions, user needs to be authenticated when requesting the data.

To authenticate requests, user must create an *activeinterlock.conf* file in the */etc/* directory with the following contents: ::

 [DEFAULT]
 username=username
 password=password

Client API Library
---------------------

This library is to access active interlock service.

.. automodule:: activeinterlockpy.activeinterlockclient
    :members: 

