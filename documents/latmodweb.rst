Lattice/Model web service
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

+--------------------------+----------------------------------------+
| GET                      |   POST                                 |
+==========================+========================================+
|   retrieveLatticeType    |  saveLatticeType                       |  
+--------------------------+----------------------------------------+
|                          |  saveLatticeInfo                       |  
|   retrieveLatticeInfo    +----------------------------------------+
|                          |  updateLatticeInfo                     |  
+--------------------------+----------------------------------------+
|                          |  saveLattice                           |  
|   retrieveLattice        +----------------------------------------+
|                          |  updateLattice                         |  
+--------------------------+----------------------------------------+
|   retrieveLatticeStatus  |  saveLatticeStatus                     |  
+--------------------------+----------------------------------------+
|   retrieveModelCodeInfo  |  saveModelCodeInfo                     |  
+--------------------------+----------------------------------------+
|                          |  saveModel                             |  
|   retrieveModel          +----------------------------------------+
|                          |  updateModel                           |  
+--------------------------+----------------------------------------+
|   retrieveModelList      |                                        |  
+--------------------------+----------------------------------------+
|   retrieveModelStatus    |  saveModelStatus                       |  
+--------------------------+----------------------------------------+
|   retrieveTransferMatrix |                                        |  
+--------------------------+----------------------------------------+
|   retrieveClosedOrbit    |                                        |  
+--------------------------+----------------------------------------+
|   retrieveTwiss          |                                        |  
+--------------------------+----------------------------------------+
|   retrieveBeamParameters |                                        |  
+--------------------------+----------------------------------------+

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
        latticetype: [optional] a name-value pair to identify lattice type {'name': , 'format': } 
        withdata:    [optional] flag to identify to get real lattice data with head or not.
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
                     'map':          [optional]   # file map. A dictionary which has name-value pair
                    } ,
                ...
             }

    Other than **retrieveLatticeInfo**, this function returns up to 3 more data when ``withdata``, and/or ``rawdata`` is set.

    **lattice**:
    
    This returns a flatten lattice when ``withdata`` keyword is set, which consists of element geometric layout, type, and strength setting with associated helper information such as unit if it applies. The flatten lattice has a structure like below: ::
    
        {
          'element index':  {'id': ,                    # internal element id
                             'name': ,                  # element name
                             'length': ,                # element length
                             'position': ,              # s position along beam trajectory
                             'type': ,                  # element type
                             'typeprops': [],           # collection of property names belonging 
                                                        # to this element type in this particular 
                                                        # lattice
                             'typeprop': [value, unit]},# value of each property with its unit 
                                                        #if it has different unit other than default
          ...
          'columns':             []   # full list of all properties for all elements 
                                      # in this particular lattice
          'typeunit': [optional] {},  # unit name-value pair for each type property if it applies
        }
    
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
             'latticeId': ,             # internal lattice id which this particular model belongs to
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
                 'chromex0': ,            # linear horizontal chromaticity
                 'chromex1': ,            # non-linear horizontal chromaticity
                 'chromex2': ,            # high order non-linear horizontal chromaticity
                 'chromey0': ,            # linear vertical chromaticity
                 'chromey1': ,            # non-linear vertical chromaticity
                 'chromey2': ,            # high order non-linear vertical chromaticity
                 'finalEnergy': ,         # the final beam energy in GeV
                 'simulationCode': ,      # name of simulation code, Elegant and Tracy for example
                 'sumulationAlgorithm': , # algorithm used by simulation code, for example serial or parallel,
                                          # and SI, or SI/PTC for Tracy code
                 'simulationControl': ,   # various control constrains such as initial condition, beam distribution, 
                                          # and output controls
                 'simulationControlFile': # file name that control the simulation conditions, like a .ele file for elegant
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
        to:          floating number, s position of ending element, default the max of element in a lattice

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
        to:          floating number, s position of ending element, default the max of element in a lattice

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
        to:          floating number, s position of ending element, default the max of element in a lattice

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
        to:          floating number, s position of ending element, default the max of element in a lattice

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

* **saveLatticeInfo**

* **updateLatticeInfo**

* **saveLattice**

* **updateLattice**

* **saveLatticeStatus**

* **saveModelCodeInfo**

* **saveModelStatus**

* **saveModel**

* **updateModel**



Data API
~~~~~~~~~~~
Coming soon

The idea to have a data
The database access is thru a data API (application programming interface), which isolates the RDB access details and business logic from RDB client. Advantage with the data API is that is makes inner schema changes transparent to RDB client, which give both the RDB schema expert and service developer more flexibility. Two major functions are provided in this layer. (1) As a data storage center, receiving all data from client, and storing into the RDB, and serving data back. (2) Providing a quick online simulation when a proper lattice deck with required model control information is provided.




MySQL Database
------------------------
All data are stored inside this layer. The data could be a real data, element name, magnetic strength for example, or a link to point to an external file on file system. The RDB schema is derived from IRMIS schema, which was originally developed by Don Dohan at Brookhaven National Laboratory. It uses MySQL RDBMS (relational database management system) as backend data storage engine. 




Online simulation
---------------------------
environment variable settings



