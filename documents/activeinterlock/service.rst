Service Implementation
==============================================

This service is implemented as a RESTful web service using Django framework. 

RESTful Interface
--------------------
A RESTful style service is implemented for data saving and retrieving.
It currently supports 2 REST methods, which are GET and POST respectively. 
Other than those 2 methods, if server receives another http method request, it returns as a bad http request (status code: 400) with a message, which is "Unsupported HTTP method", to show that method is not supported.

There are a couple of POST and GET methods that are called through a specific URL. List of URLs and methods is summarized below:
  
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

The server verifies each method, and performs a client request. There are also two methods that are not a part of active interlock but are necessary for managing user session.
    
A JSON encoding/decoding is adopted to transfer data over network. All data has to be encoded into a JSON string format before sending over network. An JSON header could be for example as below: ::

    {'content-type':'application/json', 'accept':'application/json'}

When RESTful method is called its parameters are checked and then dataapi method with the same name is called.
    
Authentication
----------------

For all POST methods user needs to be authenticated before proceeding.