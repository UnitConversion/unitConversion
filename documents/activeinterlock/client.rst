Client API Library
==============================================

Client is implemented in Python and is accessing active interlock service through a RESTful interface. For now, there is only one method in library and it allows us to download/retrieve datasets from the database. If there is no dataset with specific status in the database, **no dataset available message** is returned instead. If dataset exists in the database it is returned as a json object with the following structure: ::

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

