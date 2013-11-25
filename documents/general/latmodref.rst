Lattice/Model Web Service Reference Manual
==========================================

Introduction
--------------
A particular implementation of lattice/model service is described in this section, which is as a REST web service under Django framework.
As shown in Figure 2 in Lattice/Model basic section, this service consists of 3 layers: ::
    
    1. client layer, which provides an interface to end user of service; 
    2. service layer, which (1) provides an interface to a client, response request from 
       client and send/receive data overnetwork thru http/REST interface to/from client, 
       and (2) interfaces with underneath rdb thru a data api; 
    3. relational database layer, which stores all data.

In current implementation, 2 http methods, which are GET and POST respectively, are adopted. After the server is running, the lattice/model service is available from url like for example: ::

    http://localhost:8000/lattice

A JSON encoding/decoding is adopted to transfer data over network. All data has to be encoded into a JSON string format before sending over network. For binary data, a BASE64 algorithm is supported to encode/decode the data into/from a string to enable data transferring with JSON string. An JSON header could be for example as below: ::

    {'content-type':'application/json', 'accept':'application/json'}
    

Client
---------------------
The client layer provides an interface to end user in 2 kinds of format: (1) API library, which can be used by a client application, for example Python scripting or Matlab application; (2) graphic user interface, which could be a graphic interface from browser, or CSS (Control System Studio) application.

The implementation is under going, and documentation will come soon.

Service
---------------------
As described above, the service layer responses to answer the request from client, serves data back to or receives data from client thru REST/HTTP, and save into and retrieve data from underneath relational database thru data api. An online simulation can be carried out by request with proper configuration, and currently, it supports 2 simulation codes, which are tracy3 and elegant respectively. Since the lattice grammar is the only different between tracy3 and tracy4, the support for tracy4 is under development, and could be done easily.

Service API
~~~~~~~~~~~~~
The GET and POST methods implemented for lattice and model are described here.

:NOTE: As described above, all raw data are carried as a JSON string, therefore, the data is suggested to be decoded into native format, a dictionary in Python for example, before consuming it, or encoded into a JSON string before shipping over network.

A summary for service API is listed as below: 

==========================   =====================
   GET                          POST
--------------------------   ---------------------
  retrieveLatticeType          saveLatticeType
--------------------------   ---------------------
  retrieveLatticeInfo          saveLatticeInfo
  
                               updateLatticeInfo
--------------------------   ---------------------
  retrieveLattice              saveLattice
  
                               updateLattice
--------------------------   ---------------------
  retrieveLatticeStatus        saveLatticeStatus
--------------------------   ---------------------
  retrieveModelCodeInfo        saveModelCodeInfo
--------------------------   ---------------------
  retrieveModel                saveModel
  
                               updateModel
--------------------------   ---------------------
  retrieveModelList
--------------------------   ---------------------
  retrieveModelStatus          saveModelStatus
--------------------------   ---------------------
  retrieveTransferMatrix
--------------------------   ---------------------
  retrieveClosedOrbit
--------------------------   ---------------------
  retrieveTwiss
--------------------------   ---------------------
  retrieveBeamParameters
==========================   =====================


For status of a lattice or model, there is no updating method provided since the status history is not recorded.
Each status is treated as a brand new except the original info when the entry is created first time.

GET Methods
^^^^^^^^^^^^^^^^^^^^^^

A GET method is to get data back from service, and a get command could be formalized into a URL simply.
Available commands for get operation are listed as below.

Rules for wildcasting matching:

    - \* for multiple characters matching;
    - ? for single character matching.

It raises a **HTTP/404** error if an invalid keyword is given.

    :NOTE: Since the data is saved as it is, and server does not do any manipulation, client has to be careful with the data returned from server and the convention when the data is produced, especially the unit. For example, Elegant uses :math:`\beta*\gamma` as beam energy output. Another example is in Tracy, phase advance is defined in the units of 2π, which means there is a factor of 2π comparing with values from other code like elegant.


* **retrieveLatticeType**

    This command is to get lattice type information according given lattice type ``name`` and ``format``.
    The purpose to have lattice type with its format is to capture the original lattice information, which will
    help when retrieve the original lattice, and convert a lattice to another format.
 
    **keywords** for searching: ::
    
        function: retrieveLatticeType
        name:     lattice type name
        format:   lattice type format  

    Both ``name`` and ``format`` are needed to search available lattice type, otherwise, it will return a **HTTP/404** error with a message to say "Parameters is missing for function retrieveLatticeType". Wildcast is supported for ``name`` and ``format`` as mentioned above.
    
    :NOTE: the ``name`` with ``format`` is global unique. A format could be empty/None, but lattice type name has to be given. No duplicated entry is allowed for a given lattice name with specific format. 
    
    **Result data structure**: ::
    
        {lattice type id: {
                           'name': , 
                           'format': 
                          }, 
         ...
        }
        or {} if no existing entry.

    A lattice type is site-specific. Typical lattice types could be , but not limited to: ::   

    {'name': 'plain', 'format': 'txt'}
    {'name': 'tracy3',  'format': 'lat'}
    {'name': 'tracy4',  'format': 'lat'}
    {'name': 'elegant', 'format': 'lte'}


    Example command (a request sent to server as below): ::
    
    /lattice/?function=retrieveLatticeType&name=*&format=*
    
    it tries to get all available lattice types, and a returning result could be as: ::
    
        {u'1': {u'format': u'lat', u'name': u'tracy3'},
         u'2': {u'format': u'lte', u'name': u'elegant'}
        }

* **retrieveLatticeInfo**
  
    This command is to retrieve lattice header information. It gives lattice name, description, version, branch, 
    creation info (by who and when) when it was created first time, and updating info (by who and when) when it was modified/updated last time.

    **keywords** for searching: ::
    
        function:    retrieveLatticeInfo
        name:        lattice name
        version:     lattice version, which is a numeric number [optional]
        branch:      lattice branch [optional]
        description: a short description [optional]
        creator:     who created it first time [optional]
        

    The lattice ``name`` is needed to search available lattice, otherwise, it will return a **HTTP/404** error with a message to say "Parameters is missing for function retrieveLatticeInfo". Wildcast is supported for ``name``, ``branch``, ``description``, and ``creator`` as mentioned above.
    
    :NOTE: the ``name`` for ``branch`` at ``version`` is global unique. 
    
    **Result data structure**: ::
    
                {'id': {                             # identifier of this lattice
                        'lattice name': ,            # name of this lattice
                        'version': ,                 # version of this lattice
                        'branch': ,                  # branch this lattice belongs to
                        'description':  [optional],  # lattice description
                        'creator':      [optional],  # who created this lattice first time
                        'originalDate': [optional],  # when this lattice was create first time
                        'updated':      [optional],  # who updated last time
                        'lastModified': [optional],  # when this lattice was updated last time
                        'latticeType':  [optional],  # lattice type name
                        'latticeFormat':[optional],  # lattice type format
                        }
                 ...
                } 

    Example command (a request sent to server as below): ::
    
    /lattice/?function=retrieveLatticeInfo&name=*&version=*&branch=*
    
    it tries to get all available lattice headers, and a returning result could be as: ::
    
        {'1': {'branch': 'Design',
               'creator': 'NSLS II',
               'description': 'This is a design lattice released on Oct 3rd, 2012',
               'latticeFormat': 'lat',
               'latticeType': 'tracy3',
               'name': 'CD3-Oct3-12-30Cell-addID-par',
               'originalDate': '2013-06-20T13:51:02',
               'version': 20121003},
         '2': {'branch': 'Design',
               'creator': 'NSLS II',
               'description': 'This is a design lattice released on Apr 7th, 2010',
               'latticeFormat': 'lat',
               'latticeType': 'tracy3',
               'name': 'CD3-Apr07-10-30cell-par',
               'originalDate': '2013-06-20T13:51:05',
               'version': 20100407}}


* **retrieveLattice**

    Retrieve lattice geometric layout with magnetic strength. A proper lattice deck could be able to be generated from the retrieved data.
    All information are provided here, which is able to construct a desired lattice deck.

    **keywords** for searching: ::
    
        function:    retrieveLattice
        name:        lattice name
        version:     lattice version
        branch:      lattice branch
        description: [optional] lattice description 
        latticetype: [optional] a name-value pair to identify lattice type 
                        {'name': , 'format': } 
        withdata:    [optional] flag to identify to get real lattice data with head.
                     True  -- get the lattice geometric and strength
                     False -- default value, get lattice header description only.
        rawdata:     [optional] flag to identify whether to get raw file back.
                     This flag will try to get the raw data received.
        
    The lattice ``name``, ``version``, and ``branch`` are needed to search available lattice, otherwise, it will return a **HTTP/404** error with a message to say "Parameters is missing for function retrieveLattice". Wildcast is supported for ``name``, ``branch``, ``description``, and ``creator`` as mentioned above.
    
    :NOTE: the ``name`` for ``branch`` at ``version`` is global unique. 

        
    **Result data structure**: ::

            {'id':  # identifier of this lattice
                    {'lattice name':              # lattice name
                     'version': ,                 # version of this lattice
                     'branch': ,                  # branch this lattice belongs to
                     'description':  [optional],  # lattice description
                     'creator':      [optional],  # who created this lattice first time
                     'originalDate': [optional],  # when this lattice was create first time
                     'updated':      [optional],  # who updated last time
                     'lastModified': [optional],  # when this lattice was updated last time
                     'latticeType':  [optional],  # lattice type name
                     'latticeFormat':[optional],  # lattice type format
                     'lattice':      [optional],  # real lattice data
                     'rawlattice':   [optional],  # raw lattice data the server received
                     'map':          [optional]   # field map. A dictionary with name-value 
                                                  # pair. Place for kick map for example.
                    } ,
                ...
             }

    Other than **retrieveLatticeInfo**, this function returns up to 3 more data when ``withdata``, and/or ``rawdata`` is set.

    **lattice**:
    
    This returns a flatten lattice when ``withdata`` keyword is set, which consists of element geometric layout, type, and strength setting with associated helper information such as unit if it applies. The flatten lattice has a structure like below: ::
    
        {
          'element index':  {'id': ,          # internal element id
                             'name': ,        # element name
                             'length': ,      # element length
                             'position': ,    # s position along beam trajectory
                             'type': ,        # element type
                             'typeprops': [], # collection of property names belonging 
                                              # to this element type in this particular 
                                              # lattice
                             'typeprop':      # value of each property with its unit 
                                              #if it has different unit other than default
                            },
          ...
          'columns':             []   # full list of all properties for all elements 
                                      # in this particular lattice
          'typeunit': [optional] {},  # unit name-value pair for each type property 
                                      # if it applies
        }
    
    ``typeprop`` is a list like ``[value, unit]``. If the ``unit`` is differ with default, its unit could be carried here. In most case, the ``unit`` could be omitted, which means ``typeprop`` has structure ``[value]``, if it is same with default.
    
    element index is the order that each element appears in this lattice. It starts from zero ('0'), which usually belongs to a hidden element, referes to a starting point, and does not appear in a lattice deck, for example "BEGIN" for tracy and "_BEG_" for elegant. Its value is another map or dictionary in python, that its keys relies on the original lattice when it is imported. Some common keys are as shown above.
    
    Here is an example of lattice structure: ::

        {
         '0': {'position':0.0,'length':0.0,'type':'MARK','name':'_BEG_', id':6903},
         '1': {'typeprops':['ON_PASS'], 'name': 'MA1', 'length': 0.0, 'ON_PASS': ['1'], 
               'position':0.0,'type': 'MALIGN','id': 6904},
         '2': {'position':0.0,'length':0.0,'type':'MARK','name':'MK4G1C30A','id':6905},
         '3': {'position':4.65,'length':4.65,'type':'DRIF','name':'DH0G1A','id':6906},
         ...
         '6': {'typeprops':['K2'],'name':'SH1G2C30A','K2':['31.83577810453853'],
               'length':0.2,'position':4.85,'type':'KSEXT','id':6909},
         ...
         '10': {'typeprops':['K1'],'name':'QH1G2C30A','K1':['-0.683259469066921'],
                'length':0.25,'position':5.275,'type':'KQUAD','id':6913},
         ...
         '37': {'typeprops':['ANGLE','E1','E2'],'ANGLE':['0.10472'],'name':'B1G3C30A',
                'type':'CSBEND','length':2.62,'position':10.95,'E1':['0.05236'],
                'id':6940,'E2':['0.05236']},
         ...
         '214': {'typeprops':['INPUT_FILE','N_KICKS','PERIODS','KREF','FIELD_FACTOR'],
                 'name':'DWKM','INPUT_FILE':['"W90v5_pole80mm_finemesh_7m.sdds"'],
                 'N_KICKS':['39'],'length':3.51,'PERIODS':['39'],
                 'KREF':['21.38006225118012'],'position':52.7972,
                 'FIELD_FACTOR':['0.707106781186548'],'type':'UKICKMAP','id':7117},
         ...
         3194': {'typeprops':['VOLT','PHASE','PHASE_REFERENCE','FREQ'],'name':'RF',
                 'VOLT':['2500000'],'length':0.0,'PHASE_REFERENCE':['9223372036854775807'],
                 'position':791.958,'FREQ':['499461995.8990133'],'type':'RFCA','id':10097,
                 'PHASE':['173.523251376']},
         ...
         'columns': ['ON_PASS','K2','K1','ANGLE','E1','E2','INPUT_FILE','N_KICKS','PERIODS',
                     'KREF','FIELD_FACTOR','VOLT','PHASE','PHASE_REFERENCE','FREQ','MODE',
                     'FILENAME'],
        }


    **rawlattice**
    
    This returns the original raw lattice when ``rawlattice`` is set as a name-value pair map, or dictionary in python, with structure as below: ::
        
        { 'name': '',
          'data': []
        }
    
    The 'name' here is typically the lattice deck file name, and 'data' is list which is from a file read-in with each line as a value of the list.
    An original lattice deck could be simply created from the raw lattice data.
    
    **map**
    
    When either ``rawlattice`` and/or ``withdata`` is set, and the original lattice has an external map file, it returns here as a name-value pair map, or dictionary in python, with structure as below: ::
    
        { map_file_name_1: map_file_value_1,
          map_file_name_2: map_file_value_2,
          ...
        }
    
    Typically, the map file name is original file name of map file, and map file value is from a file read-in.
    
    encoding/decoding map data:
        A file could be a plain ASCII text file like most .txt file, or a binary file like a SDDS file. Data encoding/decoding algorithm supported by this service is as below:

        - ASCII data. If a map file is a plain text file, the data is read directly as a list with each line as one value of the list since a list can be easily serialized into a JSON string.
        
        - Binary data. Since the data is transfered over network as JSON string, which doesn't support binary data natively, the binary data has to be encoded so that it can be places into a string element in JSON. An algorithm, **Base64** as specified in RFC 3548, is used to encode/decode the binary data into/from a JSON string. The reason to choose Base64 is (1) it is a build-in module in Python which means server has no 3rd party library dependency; (2) ability to fit binary data into a strictly text-based and very limited format; (3) overhead is minimal compared to the convenience to maintain with JSON; (4) simple, commonly used standard, and unlikely to find something better specifically to use with JSON; (5) encoded text strings can be safely used as parts of URLs, or included as part of an HTTP POST request.

    Example command (a request sent to server as below) is similar with that in command retrieveLatticeInfo: ::
    
    /lattice/?function=retrieveLattice&name=*&version=*&branch=*
    
    this returns exact the same result with retrieveLatticeInfo. Or to get lattice data: ::
    
    /lattice/?function=retrieveLattice&name=*&version=*&branch=*&withdata=true
    
    or raw lattice: ::
        
    /lattice/?function=retrieveLattice&name=*&version=*&branch=*&rawdata=true
    
    or lattice and raw data: ::
    
    /lattice/?function=retrieveLattice&name=*&version=*&branch=*&withdata=true&rawdata=true
    

* **retrieveLatticeStatus**

    This retrieves a status of lattice, which is indicated by an integer. Each site could have its own convention how to use the status integer.
    A typical use of the lattice status is to identify a golden lattice, and a reference definition could be as below:
    
    +-----+-----------------------------------------------+
    | id  |   statement                                   |
    +=====+===============================================+
    |  0  |  current golden lattice                       |  
    +-----+-----------------------------------------------+
    |  1  |  alternative golden lattice                   |  
    +-----+-----------------------------------------------+
    |  2  |  lattice from live machine                    |  
    +-----+-----------------------------------------------+
    |  3  |  previous golden lattice                      |  
    +-----+-----------------------------------------------+

    **keywords** for searching: ::
    
        function:   retrieveLatticeStatus
        name:       lattice name
        version:    lattice version
        branch:     lattice branch
        status:     [optional]    lattice status

            
    if status is not specified, it gets all lattices having status no matter whatever its status is.
        
    **Result data structure**: ::
    
            {'id':  # identifier of this lattice
                    {'lattice name':              # lattice name
                     'version': ,                 # version of this lattice
                     'branch': ,                  # branch this lattice belongs to
                     'status': ,                  # lattice description
                     'creator':      [optional],  # who set status first time
                     'originalDate': [optional],  # when this status was set first time
                     'updated':      [optional],  # who updated last time
                     'lastModified': [optional],  # when it was updated last time
                    } ,
                ...
             }


    Example command (a request sent to server as below) could be as below: ::
    
    /lattice/?function=retrieveLatticeStatus&name=*&version=*&branch=*&status=*
    
    it gets all lattices those have status


Up to here, the commands for GET to interactive with lattice related data have been explained. Next paragraph focus on the GET commands related to model data.

As the definition in this service, a model is an output from either a simulation code, or from a measurement for a given lattice. A model data could be re-produced within acceptable error tolerance when all initial parameters are in place.

* **retrieveModelCodeInfo**
    
    Since model data is an output from for example simulation, it is necessary to capture some brief information like data was generated by which simulation code with which algorithm. This commands is to get the simulation code name with the algorithm back. The code name could be a name of a particular simulation code, or whatever the name fit the site naming convention if it is from a measurement. It is suggested to given a brief name for the algorithm, but not mandatory. 
    
    :NOTE: the code name with algorithm has to be unique, and empty algorithm is also treated as one value.

    **keywords** for searching: ::
    
        function:   retrieveModelCodeInfo
        name:       [optional] code name to generate a model
        algorithm:  [optional] algorithm to generate a model

    Client can search by either name, and/or algorithm. But if both name and algorithm are not given, it raises an exception, and returns client a 404 error.

    **Result data structure**: ::
    
            {'id':  # model code internal id
                  {'name':         # simulation code name
                   'algorithm': ,  # algorithm, None if not specified.
                  } ,
                ...
             }

    Example command (a request sent to server as below) could be as below: ::
    
    /lattice/?function=retrieveModelCodeInfo&name=*&algorithm=*
    
    This command is particular useful since it returns all existing entries. Client is able to check what the service has already, and is able to reuse existing entry.

* **retrieveModelList**

    Retrieve model header information that satisfies given constrains. 
    
    **keywords** for searching: ::
        
        function:       retrieveModelList
        latticename:    lattice name that this model belongs to
        latticeversion: the version of lattice
        latticebranch:  the branch of lattice
    
    **Result data structure**: ::    
    
        {'model name':                  # model name
            {'id': ,                    # internal model id number
             'latticeId': ,             # internal lattice id to identify
                                        # which this particular model belongs to
             'description':, [optional] # description of this model
             'creator': ,    [optional] # name who create this model first time
             'originalDate':,[optional] # date when this model was created
             'updated': ,    [optional] # name who modified last time
             'lastModified':,[optional] # the date this model was modified last time
            }
            ...
        }

    Example command could be as below: ::
    
        /lattice/?function=retrieveModelList&latticename=*&latticeversion=*&latticebranch=*
    
    This command gets informations for all existing models for all lattices. Be careful to use this command since it might contain too many information.
    
* **retrieveModel**

    Retrieve a model list that satisfies given constrains with global beam parameters.

    **keywords** for searching: ::
    
        function:    retrieveModelList
        name:        name of a model to be retrieved
        id:          id of a model to be retrieved
    
    Client can search and retrieve a model by either a name of a model, or its internal id. When an ID is given, it retrieves exact that model which has given ID number. 
    
    :NOTE: if both ID and name are given, it tries to match both. It sometime is useful.
    
    **Result data structure**: ::    
    
        {'model name':                    # model name
                {'id': ,                  # model id number
                 'latticeId': ,           # id of the lattice which given model belongs to
                 'description': ,         # description of this model
                 'creator': ,             # name who create this model first time
                 'originalDate': ,        # date when this model was created
                 'updated': ,             # name who modified last time
                 'lastModified': ,        # the date this model was modified last time
                 'tunex': ,               # horizontal tune
                 'tuney': ,               # vertical tune
                 'alphac': ,              # momentum compaction
                 'chromX0': ,            # linear horizontal chromaticity
                 'chromX1': ,            # non-linear horizontal chromaticity
                 'chromX2': ,            # high order non-linear horizontal chromaticity
                 'chromY0': ,            # linear vertical chromaticity
                 'chromY1': ,            # non-linear vertical chromaticity
                 'chromY2': ,            # high order non-linear vertical chromaticity
                 'finalEnergy': ,         # the final beam energy in GeV
                 'simulationCode': ,      # name of simulation code, 
                                          # Elegant and Tracy for example
                 'sumulationAlgorithm': , # algorithm used by simulation code, 
                                          # for example serial or parallel, 
                                          # or in case of tracy, SI, or SI/PTC
                 'simulationControl': ,   # various control constrains such as 
                                          # initial condition, beam distribution, 
                                          # and output controls
                 'simulationControlFile': # file name to control a simulation conditions, 
                                          # like a .ele file for elegant
                }
         ...
        }
                                
                               }


    :NOTE: for data generated from Elegant, ``finalEnergy`` usually is :math:`\beta*\gamma` unless the client converted it before saving it.

    Example command could be as below: ::
    
        /lattice/?function=retrieveModel&name=*
        
    This command gets informations for all existing models. Be careful to use this command since it might contain too many information.

    or can search by id as below: ::    
    
        /lattice/?function=retrieveModel&id=1
        
    This command gets informations for existing model with id = 1.

    or can search by both id and name as below: ::    
    
        /lattice/?function=retrieveModel&id=1&name=whatever
        
    This command gets informations for existing model ``whatever`` that its id = 1. A wildcast is supported in the name matching; in this case, a model has given name matching pattern with given id will be returned by server.
    
    
* **retrieveModelStatus**

    Like a lattice, a model could have a status also, which is indicated by an integer. This API is to retrieve the status number if it has one.
    
    Each site could have own convention how to define the status. A typical use of the model status is to identify a golden model, and a reference definition could be as below:
    
    +-----+-----------------------------------------------+
    | id  |   statement                                   |
    +=====+===============================================+
    |  0  |  current golden model                         |  
    +-----+-----------------------------------------------+
    |  1  |  alternative golden model                     |  
    +-----+-----------------------------------------------+
    |  2  |  model from live machine                      |  
    +-----+-----------------------------------------------+
    |  3  |  previous golden model                        |  
    +-----+-----------------------------------------------+

    **keywords** for searching: ::
    
        function:  retrieveModelStatus
        name:      model name
        status:    id number of that status.

    if status is not specified, it gets all models having a status, no matter whatever its status is.
        
    **Result data structure**: ::
        
        {'id':  # identifier of this lattice
            {'lattice name':              # lattice name
             'version': ,                 # version of this lattice
             'branch': ,                  # branch this lattice belongs to
             'status': ,                  # lattice description
             'creator':      [optional],  # who set status first time
             'originalDate': [optional],  # when this status was set first time
             'updated':      [optional],  # who updated last time
             'lastModified': [optional],  # when it was updated last time
            },
            ...
        }
    
    
    Example command (a request sent to server as below) could be as below: ::
        
        /lattice/?function=retrieveModelStatus&name=*&status=*
        
    it gets all models those have status.
    
    
* **retrieveTransferMatrix**

    Retrieve transfer matrix if the it is available from a given model.
        
    **keywords** for searching: ::
    
        modelname:   the name shows that which model this API will deal with
        from:        floating number, s position of starting element, default 0
        to:          floating number, s position of ending element, 
                        default the max of element in a lattice

    **Result data structure**: ::
    
        {'model name':  # model name
            {
                'name':          [element name],
                'index':         [element index],
                'position':      [s position],
                'transferMatrix':[[transfer matrix],],
            }
            ...
        }
    
    It returns a map, or dictionary in Python, results for each model shows as one entry in this map, with a sub-map/sub-dictionary. The sub-map has 4 keys which are described as below, and the value of each key is a collection/list/array:
    
    - name. Element ``'name'`` appears in its lattice.
    - index. ``'index'`` is an sequence number to identify element appeared in its lattice.
    - position. ``'position'`` is s position at the end of each element along beam direction, which is typically generated with a simulation code.
    - transferMatrix. ``'transferMatrix'`` is 6-dimension beam linear transfer matrix from starting point, which means the valued is propagated from s=0. Transfer matrix of each element is a sub-array of the transfer matrix with a structure like:
        
        [M00 M01 M01 M03 M04 M05 M06 M07 M08 .. M55]
        
        :NOTE: the value heavily relies on the simulation environment such as code, algorithm, and others. 

    Example command (a request sent to server as below) could be as below: ::
        
        /lattice/?function=retrieveTransferMatrix&name=whateverthename&from=12.3456&to=34.5678
        
    it intendes to get transfer matrix from model ``whateverthename``, that element s position is (12.3456, 34.5678). If there is no element in that range, it return an empty value.

* **retrieveClosedOrbit**

    Retrieve closed orbit distortion if the it is available from a given model.
        
    **keywords** for searching: ::
    
        modelname:   the name shows that which model this API will deal with
        from:        floating number, s position of starting element, default 0
        to:          floating number, s position of ending element, 
                        default the max of element in a lattice

    **Result data structure**: ::
    
        {'model name':  # model name
            {
                'name':     [element name],
                'index':    [element index],
                'position': [s position],
                'codx':     [codx],
                'cody':     [cody]
            }
            ...
        }
    
    It returns a map, or dictionary in Python, results for each model shows as one entry in this map, with a sub-map/sub-dictionary. The sub-map has 5 keys which are described as below, and the value of each key is a collection/list/array:
    
    - name. Element ``'name'`` appears in its lattice.
    - index. ``'index'`` is an sequence number to identify element appeared in its lattice.
    - position. ``'position'`` is s position at the end of each element along beam direction, which is typically generated with a simulation code.
    - codx. ``'codx'`` is horizontal closed orbit distortion.
    - cody. ``'cody'`` is vertical closed orbit distortion.
    
    Example command (a request sent to server as below) could be as below: ::
        
        /lattice/?function=retrieveClosedOrbit&name=whateverthename&from=12.3456&to=34.5678
        
    it intendes to get closed orbit for model ``whateverthename``, that element s position is (12.3456, 34.5678). If there is no element in that range, it return an empty value.

* **retrieveTwiss**

    Retrieve twiss parameters if the it is available from a given model.
        
    **keywords** for searching: ::
    
        modelname:   the name shows that which model this API will deal with
        from:        floating number, s position of starting element, default 0
        to:          floating number, s position of ending element, 
                        default the max of element in a lattice

    **Result data structure**: ::
    
        {'model name':  # model name
            {
                'name':     [element name],
                'index':    [element index],
                'position': [s position],
                'alphax':   [],
                'alphay':   [],
                'betax':    [],
                'betay':    [],
                'etax':     [],
                'etay':     [],
                'etapx':    [],
                'etapy':    [],
                'phasex':   [],
                'phasey':   [],
            }
            ...
        }
    
    It returns a map, or dictionary in Python, results for each model shows as one entry in this map, with a sub-map/sub-dictionary. The sub-map has 4 keys which are described as below, and the value of each key is a collection/list/array:
    
    - name. Element ``'name'`` appears in its lattice.
    - index. ``'index'`` is an sequence number to identify element appeared in its lattice.
    - position. ``'position'`` is s position at the end of each element along beam direction, which is typically generated with a simulation code.
    - alphax. ``alphax`` is horizontal :math:`\alpha` twiss function
    - alphay. ``alphay`` is vertical :math:`\alpha` twiss function
    - betax. ``betax`` is horizontal :math:`\beta` twiss function
    - betay. ``betay`` is vertical :math:`\beta` twiss function
    - etax. ``etax`` is horizontal dispersion
    - etay. ``etay`` is vertical dispersion
    - etapx. ``etapx`` is slope of horizontal dispersion
    - etapy. ``etapy`` is slope of vertical dispersion
    - phasex. ``phasex`` is horizontal phase advance
    - phasey. ``phasey`` is vertical phase advance

    :NOTE: Be careful about the value, especially the unit of value. Usually, the value is stored as it is. It is suggested that client does not manipulate the value and uses code convention when it is stored. 

    Example command (a request sent to server as below) could be as below: ::
        
        /lattice/?function=retrieveTwiss&name=whateverthename&from=12.3456&to=34.5678
        
    it intendes to get twiss parameter for model ``whateverthename``, that element s position is (12.3456, 34.5678). If there is no element in that range, it return an empty value.

* **retrieveBeamParameters**

    Retrieve all beam parameters of each element that satisfies given constrains.
        
    **keywords** for searching: ::
    
        modelname:   the name shows that which model this API will deal with
        from:        floating number, s position of starting element, default 0
        to:          floating number, s position of ending element, 
                        default the max of element in a lattice

        {'model name':  # model name
            {
                'name':          [element name],
                'index':         [element index],
                'position':      [s position],
                'alphax':        [],
                'alphay':        [],
                'betax':         [],
                'betay':         [],
                'etax':          [],
                'etay':          [],
                'etapx':         [],
                'etapy':         [],
                'phasex':        [],
                'phasey':        [],
                'codx',          [],
                'cody',          [],
                'transferMatrix':[[transfer matrix],],
            }
            ...
        }
    
    The returned result is a collection of 3 APIs: which are ``retrieveTransferMatrix``, ``retrieveClosedOrbit``, and ``retrieveTwiss``.    

    Example command (a request sent to server as below) could be as below: ::
        
        /lattice/?function=retrieveBeamParameters&name=whateverthename&from=12.3456&to=34.5678
        
    it intendes to get all beam parameters from model ``whateverthename``, that element s position is (12.3456, 34.5678). If there is no element in that range, it return an empty value.


POST Methods
^^^^^^^^^^^^^^^^^^^^^^

A POST method is to save data into service, and API for post operation is list as below:

* **saveLatticeType**

    This command is to save lattice type information using given lattice type name and format. The purpose to have lattice type with its format is to capture the original lattice information, which will help when retrieve the original lattice, and convert a lattice to another format. If the lattice type with its format is there already, it returns an error.

    **keywords** to carry data:

    The data is shipped to server using a map, or dictionary in Python, with following format: ::

        {'function': 'saveLatticeType',
         'name':     lattice type name,
         'format':   lattice type format
        }

    As described above, a lattice type is site-specific. Typical lattice types could be , but not limited to: ::

        {'name': 'plain', 'format': 'txt'}
        {'name': 'tracy3',  'format': 'lat'}
        {'name': 'tracy4',  'format': 'lat'}
        {'name': 'elegant', 'format': 'lte'}

    If this operation is finished successfully, it returns a map as below: ::
        
        {'result': internal id}
    
    otherwise, raise an error.

    A Python client example is shown as below:
    
    .. code-block:: python
        :linenos:

        import httplib
        import urllib

        params = urllib.urlencode({'function': 'saveLatticeType', 
                                   'name': 'tracy3', 
                                   'format': 'lat'})
        headers = {'content-type':'application/json', 
                   'accept':'application/json'}
        conn = httplib.HTTPConnection('localhost', 8000)
        conn.request("POST", "/lattice/", params, headers)
        response = conn.getresponse()
        conn.close()

    in this case, if lattice ``tracy3`` with ``lat`` format is not in server yet, client gets a result like for example: ::
    
        {"result": 9}
        
    if it exists already, server returns an error with message like : ::

        Lattice type (tracy3) with given format (lat) exists already.


* **saveLatticeInfo**

    This command is to save lattice description information. Lattice data, geometric layout and strength setting respectively, are not included here. A lattice has a name, version, and branch, and those 3 make a lattice unique globally. A time stamp is added automatically by the underneath database, which is transparent to the client. If a lattice info exists already, the server returns an error.

    **keywords** to carry data:

    The data is shipped to server using a map, or dictionary in Python, with following format: ::

        {'function':    'saveLatticeInfo',
         'name':        lattice name
         'version':     version number
         'branch':      branch name
         'latticetype': [optional] a dictionary which consists of {'name': , 'format': }
                         example lattice type is as described above.
         'description': [optional] description for this lattice, 
                            allow user put any info here (< 255 characters)
         'creator':     [optional] original creator
         }

    If this operation is finished successfully, it returns id of the new lattice as a map as below: ::
    
        {'id': internal id}
    
    otherwise, raise an error.

    A Python client example is shown as below:
    
    .. code-block:: python
        :linenos:

        import httplib
        import urllib
        import json

        paramsdata = {'function': 'saveLatticeInfo', 
                      'name': 'lattice info demo',
                      'version': 20131001,
                      'branch': 'design',
                      'latticetype': json.dumps({'name': 'elegant', 'format': 'lte'}),
                      'description': 'demo example how to insert a lattice information',
                      'creator': 'Examiner'}
        params = urllib.urlencode(paramsdata)
        headers = {'content-type':'application/json', 
                   'accept':'application/json'}
        conn = httplib.HTTPConnection('localhost', 8000)
        conn.request("POST", "/lattice/", params, headers)
        response = conn.getresponse()
        conn.close()

    in this case, if lattice does not exist yet, and is saved successfully, client gets a result like for example: ::
    
        {"id": 9}
        
    if it exists already, server returns an error with message like : ::

        lattice (name: lattice info demo, version: 20131001, branch: design) exists already.


* **updateLatticeInfo**

    Updating an existing lattice description information. Once a lattice is saved, it is not allowed to delete it anymore since it might be used by many other sources. However, it is always able to update it. If lattice does exist yet, it returns an error.
    
    **keywords** to carry data: 

    The data is shipped to server using a map, or dictionary in Python, with following format: ::

        {'function':    'saveLatticeInfo',
         'name':        lattice name
         'version':     version number
         'branch':      branch name
         'latticetype': [optional] a dictionary which consists of {'name': , 'format': }
                          example lattice type is as described above.
         'description': [optional] description for this lattice, 
                            allow user put any info here (< 255 characters)
         'creator':     [optional] name who update this lattice head
         }

    If this operation is finished successfully, it returns new of the new lattice as a map as below: ::
    
        {'id': true}
    
    otherwise, raise an error.

    
    A Python client example is shown as below:
    
    .. code-block:: python
        :linenos:

        import httplib
        import urllib
        import json

        paramsdata = {'function': 'updateLatticeInfo', 
                      'name': 'lattice info demo',
                      'version': 20131001,
                      'branch': 'design',
                      'latticetype': json.dumps({'name': 'elegant', 'format': 'lte'}),
                      'description': 'demo example how to insert a lattice information',
                      'creator': 'Examiner'}
        params = urllib.urlencode(paramsdata)
        headers = {'content-type':'application/json', 
                   'accept':'application/json'}
        conn = httplib.HTTPConnection('localhost', 8000)
        conn.request("POST", "/lattice/", params, headers)
        response = conn.getresponse()
        conn.close()

    in this case, if lattice is there and updated successfully, client gets a result like for example: ::
    
        {"result": true}

    If lattice does not exist yet, it get an error as: ::

        Did not find lattice (name: lattice info demo, version: 20131001, branch: design).
    

* **saveLattice**

    This command is to save lattice data. It creates a new entry with given lattice description information, or raises an error if lattice description exists already. 
    
    **keywords** to carry data: 
    
    The data is shipped to server using a map, or dictionary in Python, with following format: ::
    
        {'function':    'saveLattice',
         'name':        lattice name
         'version':     version number
         'branch':      branch name
         'latticetype': a dictionary which consists of {'name': , 'format': }
         'description': description for this lattice,
                            allow user put any info here (< 255 characters)
         'creator':     original creator
         'lattice':     lattice data, a dictionary:
                        {'name': ,
                         'data': ,
                         'raw': ,
                         'map': {'name': 'value'},
                         'alignment': ,
                         'control': {'name': ,
                                     'data': }, # control info for a simulation run, 
                                                # ele file for elegant for example
                         'init_twiss':, # initial twiss condition
                         }
                         name: file to be saved into, same with lattice name by default
                         data: lattice geometric and strength with predefined format
                         raw:  raw data, same with data but in original lattice format
                         map:  name-value pair dictionary
                         alignment: mis-alignment information
         'dosimulation': Flag to identify whether to perform a simulation. 
                            False by default.
         }
    
    The structure is similar with command ``saveLatticeInfo`` except 2 additional keywords added in this function, which are ``lattice`` and ``dosimulation`` respectively. The data structure is described as below: ::
    
        - lattice. Place to carry all lattice information, and transfer data  
                    from client to server. Its structure is described as below.
        - dosimulation. A Flag to identify whether to perform a simulation. 
                    False by default, which means a simulation will not be carried out. 
    
    **lattice sub-structure**
    
    Real lattice information is included in lattice sub-structure. Here is some details about the keywords used by this structure:
    
    - name: lattice file name which the lattice raw data will be saved into on the server side.
    - data: lattice data from lattice file. the real data is in this structure, and different lattice format has different requirement. Details will be explained below.
    - raw: original lattice which might be carried in different format.
    - map: place to contain for example field map. A typical use of this is to carry kick map over network. As described in section ``retrieveLattice``, plain text map are read in as list/array with each line as one value of the array. For binary map, the whole file has to be read and encoded with **Base64** algorithm.
    - control: data to serve simulation on the server side. Since there are many simulation codes having separated file, an .ele of elegant for example, this information is carried here. It has ``name``, which is control file name, and ``data`` which is content of the control file. If a header is contained inside a lattice deck, tracy3/tracy4 for example, its header information other than element layout could be saved here also.
    - alignment: place to hold misalignment data. It is currently a place holder, and not implemented yet. An integration with real misalignment data from survey could be hold here, and integrate on the server side.
    - init_twiss: place to send server initial twiss parameters if it applies. It is currently a place holder, and not implemented yet.
    
    
    **data** sub-structure of lattice sub-structure
    
    Current implementation of lattice service supports 3 different formats, which are (1) plain text format with tab-formatting, (2) tracy3, and (3) elegant respectively. To separate server from parsing all kinds of different lattice, it only accepts lattice from client with dedicated format.

    (1) Tab-formatted plain lattice
    
    Suggested lattice type for this lattice: ``{'name': 'plain', 'format': 'txt'}``. 
    
    For plain text file, it is carried as an array, which is with each line as one value of the array. A header is needed and should have the following format: ::
    
             ElementName ElementType  L  s   K1    K2   Angle [dx dy dz pitch yaw roll map]
                                      m  m  1/m2  1/m3  rad   [m  m  m  rad   rad rad     ]
             ------------------------------------------------------------------------------
    
    The 1\ :sup:`st` line is name for each column to identify what the property value is for. Most likely the first 7 columns are common to a lattice, but user also be able to add extra information like alignment errors and map such as kick map file name of insertion device. The map is suggested to appear as the last column. The 2\ :sup:`nd` column is the place to carry unit information if one column has, and 3\ :sup:`rd` column is divider between body and head. 
    
    It also needs that the ``s`` position starting from zero(0), which means the starting point to matching is suggested to include the starting point, which usually appears as for example ``_BEG_`` in elegant or ``begin`` in tracy3/tracy4, but might not be in its lattice deck.

    The misalignment could be displacement (:math:`\delta_x, \delta_y, \delta_x`) and/or rotating (:math:`\theta_x, \theta_y, \theta_z`, or pitch, yaw, roll) along ``x``, ``y``, and ``z`` axes.

    :NOTE: currently, all properties of an element have to be on one line, and multiple lines is not supported yet.

    (2) Tracy3, and elegant lattice

    Suggested lattice type as below: ::
    
        ===========   ==========================================
          lattice         type
        -----------   ------------------------------------------
          tracy3        {'name': 'tracy3',  'format': 'lat'}
        -----------   ------------------------------------------
          tracy4        {'name': 'tracy4',  'format': 'lat'}
        -----------   ------------------------------------------
          elegant       {'name': 'elegant', 'format': 'lte'}
        ===========   ==========================================

    

    for a lattice used by a particular simulation code like tracy3, tracy4, or elegant, it has its own grammar, and most likely differs pretty much from each other. To avoid the trouble to parse each particular lattice by server, a data structure is designed as below: ::
    
        {sequence #: { 'name':     ,
                       'length':   , 
                       'position': , 
                       'type':     , 
                       ...         [other properties such as K1, K2, or others]
                     }
        }
    
    for example, a tracy lattice could be carried like: ::
    
  		'data': {
		0: {'position': '0.00000', 'length': '0.0', 
		    'type': 'Marker', 'name': 'BEGIN'},
		1: {'position': '4.29379', 'length': '4.29379', 
		    'type': 'Drift', 'name': 'DH05G1C30A'},
		2: {'position': '4.31579', 'length': '0.022', 
		    'type': 'Drift', 'name': 'DFH2G1C30A'},
		3: {'position': '4.31579', 'type': 'Corrector,Horizontal', 
		    'name': 'FXH2G1C30A', 'Method': 'Meth'},
		4: {'position': '4.31579', 'type': 'Corrector,Vertical', 
		    'name': 'FYH2G1C30A', 'Method': 'Meth'},
		5: {'position': '4.33779', 'length': '0.022', 
		    'type': 'Drift', 'name': 'DFH2G1C30A'},
		6: {'position': '4.65000', 'length': '0.31221', 
		    'type': 'Drift', 'name': 'DH1G1A'},
		7: {'position': '4.65000', 'type': 'Marker', 'name': 'GEG1C30A'},
		8: {'position': '4.65000', 'type': 'Marker', 'name': 'GSG2C30A'},
		9: {'name': 'SH1G2C30A', 'K': '12.098850', 'N': 'Nsext', 
		    'length': '0.2', 
		    'position': '4.85000', 'type': 'Sextupole', 'Method': 'Meth'},
		10: {'position':'4.93500', 'length':'0.085', 'type':'Drift', 'name':'DH1AG2A'},
		11: {'position': '4.93500', 'type': 'Beam Position Monitor', 
		    'name': 'PH1G2C30A'},
		12: {'position': '5.01250', 'length': '0.0775', 'type': 'Drift', 
		    'name': 'DBPM01'},
		13: {'name': 'QH1G2C30A', 'K': '-0.633004', 'N': 'Nquad', 
		    'length': '0.275', 'position': '5.28750', 'type': 'Quadrupole', 
		    'Method': 'Meth'},
		14: {'position': '5.43250', 'length': '0.145', 'type': 'Drift', 
		    'name': 'DH2AG2A'},
		15: {'name': 'SQHHG2C30A', 'K': '0', 'N': 'Nquad', 'length': '0.1', 
		    'position': '5.53250', 'type': 'Quadrupole', 'Method': 'Meth'},
		16: {'position': '5.53250', 'type': 'Corrector,Horizontal', 
		    'name': 'CXH1G2C30A', 'Method': 'Meth'},
		17: {'position': '5.53250', 'type': 'Corrector,Vertical', 
		    'name': 'CYH1G2C30A', 'Method': 'Meth'},
		18: {'name': 'SQHHG2C30A', 'K': '0', 'N': 'Nquad', 'length': '0.1', 
		    'position': '5.63250', 'type': 'Quadrupole', 'Method': 'Meth'},
		....
		}
				
    **online simulation**

    Currently, the server supports simulation using tracy-3 or elegant. If the lattice sent from client is in correctly format, either tracy3 or elegant, client can flag ``dosimulation`` to be true to trig server to carry out a quick simulation, and save simulation results. However, if the lattice format is not in tracy3 or elegant, even ``dosimulation`` is set to be true, the  server does not perform a simulation. Also server leaves client to check the lattice whether a simulation can be done correctly, which means that client is responsible to check the lattice to ensure a simulation could be executed successfully. Commands needed by server is listed as below: ::
      
      ===========   =====================
        code         needed commands
      -----------   ---------------------
        tracy3          tracy3
      -----------   ---------------------
        elegant        elegant
                       sddsprocess
                       sddsxref
                       sddsconvert
                       sddsprintout
      ===========   =====================
    
    
    :NOTE: Above commands have to be locatable by server. If they are not in searching PATH, some environment variables, ``TRACY3_CMD`` for tracy3 and ``ELEGANT_CMD`` for elegant respectively, have to be set. 

    Simulation results are saved associated with given lattice automatically if simulation is carried out successfully. The data is saved in 2 parts, which are global beam parameters like final beam energy, and beam parameters for each elements. Data from different simulation code are slightly different. Detailed data is described as below for tracy3 and elegant:
    
    for tracy global parameters for a ring are: ::
    
        'tunex': horizontal tune
        'tuney':  vertical tune
        'chromX0': horizontal linear chromaticity
        'chromY0': vertical linear chromaticity
        'finalEnergy': beam energy in GeV
        'alphac': momentum compaction factor
        'simulationCode':  which is ``tracy3``
        'sumulationAlgorithm': ,  which is ``SI``

    for linear machine, only the ``finalEnergy`` is saved as global parameters.
    
    parameters for each element are as: ::
        
        'alphax': ,
        'alphay': ,
        'betax': ,
        'betay': ,
        'etax': ,
        'etay': ,
        'etapx': ,
        'etapy': ,
        'phasex': ,
        'phasey': ,
        'codx': ,
        'cody': ,
        'transferMatrix': which is linear matrix ordered M00, M01, M02, ..., M55
        's': ,
        'energy': energy at each element
    
    for elegant, global parameters are: ::
    
        'tunex': , horizontal tune
        'tuney': , vertical tune
        'chromX0': , horizontal linear chromaticity
        'chromX1': , non-linear horizontal chromaticity
        'chromX2': , high order non-linear horizontal chromaticity
        'chromY0': , vertical linear chromaticity
        'chromY1': , non-linear vertical chromaticity
        'chromY2': , high order non-linear vertical chromaticity
        'finalEnergy': beam energy in GeV, this value is recorded as beta*gamma
        'alphac': , momentum compaction factor
        'simulationCode': , which is ``elegant``
        'sumulationAlgorithm': ,  which is ``matrix``

    parameters for each element are as: ::
        
        'alphax': ,
        'alphay': ,
        'betax': ,
        'betay': ,
        'etax': ,
        'etay': ,
        'etapx': ,
        'etapy': ,
        'phasex': ,
        'phasey': ,
        'codx': ,
        'cody': ,
        'transferMatrix': which is linear matrix ordered M00, M01, M02, ..., M55
        's': ,
        'energy': energy at each element, this value is recorded as beta*gamma
    
    If a lattice does not exist yet, and saves successfully, client gets a result like for example: ::
    
        {"result": true}

    If lattice does not exist yet, it get an error as: ::

        Did not find lattice (name: lattice info demo, version: 20131001, branch: design).

* **updateLattice**

    This function is similar with ``saveLattice``, but updating an existing lattice information. The data structure is same with ``saveLattice`` function.
    If lattice data is in place already, it returns an error, otherwise, if lattice is there and updated successfully, client gets a result like for example: ::
    
        {"result": true}

    If lattice does not exist yet, it get an error.
    
    In this function, same with ``saveLattice``, user can request server to perform a simulation. 

* **saveLatticeStatus**

    Each lattice could be assigned a status, which is an integer with site-specific convention. It captures who assigns a status for a specific lattice, and by when. Also who updates its status, and by when.
    
    **keywords** to carry data: 
    
    The data is shipped to server using a map, or dictionary in Python, with following format: ::
    
        {'function':    'saveLatticeStatus',
         'name':        lattice name
         'version':     version number
         'branch':      branch name
         'creator':     original creator
         'status':      who commands this function
        }
    
    How to utilize the ``status`` is entirely up to each site, and could vary differently. A suggested convention could be as below: ::

        0: current golden lattice [by default]
        1: current live lattice
        2: alternative golden lattice
        3: previous golden lattice, but not any more
        
        (The number is flexible to be changed or extended.)
    
    It returns a structure as below if command is performed successfully: ::
        
        {'result': true}
    
    otherwise, raise an exception
    
    :NOTE: The status is not captured in this version, therefore, there is no distinguish between command ``save*`` and ``update*``.  All are treated as saving a new status.

* **saveModelCodeInfo**

    In this service, a model is defined as an output from either simulation, or measurement. To help understanding each particular model, its environment, particularly the name of simulation code and a brief description for the algorithm used, is captured.

    **keywords** to carry data: 
    
    The data is shipped to server using a map, or dictionary in Python, with following format: ::
    
        {'function':    'saveModelCodeInfo',
         'name':        simulation code name
         'algorithm':   algorithm to be use to generate the beam parameters
        }

    Example could be as below (user could have its own): ::

      ===========   =====================
        name           algorithm
      -----------   ---------------------
        tracy3          SI
      -----------   ---------------------
        tracy3          PTC
      -----------   ---------------------
        tracy4          SI
      -----------   ---------------------
        tracy4          PTC
      -----------   ---------------------
        elegant         serial
      -----------   ---------------------
        elegant         parallel
      ===========   =====================    
    
    One exception here is to deal with model data from measurement, which could be determined by each site, for example using ``measurement`` as name.

    It returns a structure as below if command is performed successfully: ::
        
        {'result': true}
    
    otherwise, raise an exception

* **saveModelStatus**
    
    Similar with lattice, each model could be assigned a status, which is an integer with site-specific convention. It captures who assigns a status for a specific model, and by when. Also who updates its status, and by when.
    
    **keywords** to carry data: 
    
    The data is shipped to server using a map, or dictionary in Python, with following format: ::
    
        {'function':    'saveModelStatus',
         'name':        model name
         'status':      who commands this function
        }
    
    How to utilize the ``status`` is entirely up to each site, and could vary differently. A suggested convention could be as below: ::

        0: current golden model [by default]
        1: alternative golden model
        2: previous golden model, but not any more
        
        (The number is flexible to be changed or extended.)
    
    It returns a structure as below if command is performed successfully: ::
        
        {'result': true}
    
    otherwise, raise an exception
    
    :NOTE: The status is not captured in this version, therefore, there is no distinguish between command ``save*`` and ``update*``.  All are treated as saving a new status.
    
* **saveModel**
    
    This command is to save a model result for a given lattice. It requires a lattice exists first.

    **keywords** to carry data:

    The data is shipped to server using a map, or dictionary in Python, with following format: ::
    
        {'function':      'saveModel',
         'latticename':   lattice name that this model belongs to
         'latticeversion: the version of lattice
         'latticebranch:  the branch of lattice
         'model':         a dictionary which holds all data 
        }        
    
    Details data is carried by ``model`` structure, which is ``model`` sub-structure section. 
    
    **model** sub-structure is described as below: ::
    
        {'model name':               # model name
           { # header information
            'description': ,         # description of this model
            'creator': ,             # who requested this function
            'tunex': ,               # horizontal tune
            'tuney': ,               # vertical tune
            'alphac':                # momentum compaction factor
            'chromX0': ,            # linear horizontal chromaticity
            'chromX1': ,            # non-linear horizontal chromaticity
            'chromX2': ,            # high order non-linear horizontal chromaticity
            'chromY0': ,            # linear vertical chromaticity
            'chromY1': ,            # non-linear vertical chromaticity
            'chromY2': ,            # high order non-linear vertical chromaticity
            'finalEnergy': ,         # the final beam energy in GeV
            'simulationCode': ,      # name of simulation code, Elegant and Tracy for example
            'sumulationAlgorithm': , # algorithm used by simulation code, for example serial 
                                     # or parallel for elegant, and SI or PTC for Tracy 
            'simulationControl': ,   # various control constrains such as initial condition, 
                                     # beam distribution, and output controls
            'simulationControlFile': # file name that control the simulation conditions, 
                                     # like a .ele file for elegant simulation data
            'beamParameter':         # a map/dictionary consists of twiss, close orbit, 
                                     # transfer matrix and others
           }
           ...
        }
    
    This sub-structure allows a client to carry multiple results to server at the same time. All those values are for whole model except ``beamParameter`` structure, which is for each element.
    
    For the ``simulationControl``, it is a readin from a file as a list with each line of the file as one value of the list; its file name is captured with ``simulationControlFile``.
    
    **beamParameter** sub-structure
    
    Beam parameters at each element is carried in the ``beamParameter`` sub-structure as below: ::
    
        { element_order: #element_order starts with 0.
            { 'name': ,     # element name
              'position': , # element position
              'alphax': ,
              'alphay': ,
              'betax': ,
              'betay': ,
              'etax': ,
              'etay': ,
              'etapx': ,
              'etapy': ,
              'phasex': ,
              'phasey': ,
              'codx': ,
              'cody': ,
              'transferMatrix': ,
              'indexSliceCheck': ,
              'energy': ,
              'particleSpecies': ,
              'particleMass': ,
              'particleCharge': ,
              'beamChargeDensity': ,
              'beamCurrent': ,
              'x': ,
              'xp': ,
              'y': ,
              'yp': ,
              'z': ,
              'zp': ,
              'emittancex': ,
              'emittancey': ,
              'emittancexz':  
            }
         }

    Most values here are primitive data such as double, or string, except the transferMatrix which is a 2-D array with a structure as below.
    
    **transferMatrix** sub-structure is as below: ::
    
        [[M00, M01, M02, ..., M05], [M10, M11, ..., M15], ..., [M50, M51, ..., M55]]
        
    :NOTE: 
        - In principle, server is capable to capture any type of transfer matrix. However, current implementation supports linear transfer matrix only.
        - The element layout/sequence carried in this structure has to match with the one in lattice.
    
    It returns ids of the new model with a structure as below if command is performed successfully: ::
        
        {'result': [ids]}
    
    otherwise, raise an exception
    
* **updateModel**

    If given model exists already, it is suggested to use ``updateModel`` command instead of ``saveModel``. The data structure is same with that in ``saveModel``.

    It returns operation status with a structure as below if command is performed successfully: ::
        
        {'result': true}

    otherwise, raise an exception
    
