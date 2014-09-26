Service Implementation
==============================================

This service is implemented as a RESTful web service using the Django framework. 

RESTful Interface
--------------------
A RESTful-style service is implemented for saving and retrieving data.
It currently supports 2 REST methods, which are GET and POST respectively. 
If the server receives another http method request, apart from GET and POST, it returns as a bad http request (status code: 400) with a message, which is "Unsupported HTTP method", to show that method is not supported.

There are some POST and GET methods that are called through a specific URL. The possible URLs and methods are summarized:
  
+--------------------------------+---------------------------+---------+----------+
|    URL                         |             Method        |   GET   |   POST   |
+================================+===========================+=========+==========+
| ai/statuses/                   | retrieveStatusesWS        |    x    |          |
+--------------------------------+---------------------------+---------+----------+
| ai/activeinterlockheader/      | retrieveAiHeaderWS        |    x    |          |
+--------------------------------+---------------------------+---------+----------+
| ai/saveactiveinterlockheader/  | saveAiHeaderWS            |         |    x     |
+--------------------------------+---------------------------+---------+----------+
| ai/device/                     | retrieveDeviceWS          |    x    |          |
+--------------------------------+---------------------------+---------+----------+
| ai/savedevice/                 | saveDeviceWS              |         |    x     |
+--------------------------------+---------------------------+---------+----------+
| ai/updatedevice/               | updateDeviceWS            |         |    x     |
+--------------------------------+---------------------------+---------+----------+
| ai/updatestatus/               | updateStatusWS            |         |    x     |
+--------------------------------+---------------------------+---------+----------+
| ai/updateprop/                 | updatePropWS              |         |    x     |
+--------------------------------+---------------------------+---------+----------+
| ai/approve/                    | approveCellsWS            |         |    x     |
+--------------------------------+---------------------------+---------+----------+
| ai/logic/                      | retrieveLogicWS           |    x    |          |
+--------------------------------+---------------------------+---------+----------+
| ai/savelogic/                  | saveLogicWS               |         |    x     |
+--------------------------------+---------------------------+---------+----------+
| ai/updatelogic/                | updateLogicWS             |         |    x     |
+--------------------------------+---------------------------+---------+----------+
| ai/download/                   | downloadActiveInterlockWS |         |    x     |
+--------------------------------+---------------------------+---------+----------+
| user/login/                    | user_login                |    x    |    x     |
+--------------------------------+---------------------------+---------+----------+
| user/logout/                   | user_logout               |    x    |    x     |
+--------------------------------+---------------------------+---------+----------+

The server verifies each method, and performs a client request. There are also two methods that are not a part of the active interlock service but are necessary for managing the user session.
    
A JSON encoding/decoding is adopted to transfer data over the network. All data has to be encoded into a JSON string before sending over the network. An JSON header could be for example: ::

    {'content-type':'application/json', 'accept':'application/json'}

When a RESTful method is called, its parameters are checked and then then the dataapi method with the same name is called.
    
Authentication
----------------

The user must to be authenticated before proceeding with all POST methods.