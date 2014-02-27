Service Implementation
==============================================

This service is implemented as a RESTful web service using Django framework. 

RESTful Interface
--------------------
A RESTful style service is implemented for data saving and retrieving.
It currently supports 2 REST methods, which are GET and POST respectively. 
Other than those 2 methods, if server receives another http method request, it returns as a bad http request (status code: 400) with a message, which is "Unsupported HTTP method", to show that method is not supported.

For each GET and POST method, there are set of functions associated with each, which are summarized as below: ::

(This is old version, and new implementation should be revised according the requirement.)

  ==========  ==================================   =============================
    Method                   GET                              POST
  ----------  ----------------------------------   -----------------------------
   Function    retrieveActiveInterlock              saveActiveInterlock
              ----------------------------------   -----------------------------
                                                    updateActiveInterlockStatus
              ----------------------------------   -----------------------------
               retrieveActiveInterlockPropType      saveActiveInterlockPropType
              ----------------------------------   -----------------------------
               retrieveActiveInterlockLogic         saveActiveInterlockLogic
  ==========  ==================================   =============================


The server verifies each function of a method, and performs a client request if the function is supported by that method. Otherwise, it returns as a bad http request (status code: 400) with a message,
which is "Wrong HTTP method for function ...", to show that function is not supported by requested method.
    
A JSON encoding/decoding is adopted to transfer data over network. All data has to be encoded into a JSON string format before sending over network. An JSON header could be for example as below: ::

    {'content-type':'application/json', 'accept':'application/json'}

For binary data, a BASE64 algorithm is supported to encode/decode the data into/from a string to enable data transferring using JSON string. A typical use case is to save original raw data, which is usually published with for example excel spreadsheet format.

Data Process Functions
-----------------------

.. automodule:: activeinterlock.dataprocess
    :members: 
    
    
    