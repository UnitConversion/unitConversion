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

The data is returned from the server with a JSON encoding. An json header from client could be for example as below: ::

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

GET Methods
^^^^^^^^^^^^^^^^^^^^^^

A GET method is to get data back from service, and a get command could be formalized into a URL simply.
Available commands for get operation are listed as below.

Rules for wildcasting matching:

    - \* for multiple characters matching;
    - ? for single character matching.

It raises a **HTTP/404** error if an invalid keyword is given.

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
    
    Typically, the map file name is original file name of map file, and map file value is from a file read-in. If a map file is a plain text file, it is read directly as a list with each line as one value of the list. For a binary map, a SDDS kick-map for example, the whole file is read as a string and encoded with **Base64** algorithm as specified in RFC 3548. The advantage using Base64 algorithm is that encoded text strings can be safely used as parts of URLs, or included as part of an HTTP POST request.

    Example command (a request sent to server as below) is similar with that in command retrieveLatticeInfo: ::
    
    /lattice/?function=retrieveLattice&name=*&version=*&branch=*
    
    this returns exact the same result with retrieveLatticeInfo. Or to get lattice data: ::
    
    /lattice/?function=retrieveLattice&name=*&version=*&branch=*&withdata=true
    
    Or get raw lattice: ::
        
    /lattice/?function=retrieveLattice&name=*&version=*&branch=*&rawdata=true
    
    or get lattice and raw lattice: ::
    
    /lattice/?function=retrieveLattice&name=*&version=*&branch=*&withdata=true&rawdata=true
    

* **retrieveLatticeStatus**

* **retrieveModelCodeInfo**

* **retrieveModelStatus**

* **retrieveModel**

* **retrieveModelList**

* **retrieveTransferMatrix**

* **retrieveClosedOrbit**

* **retrieveTwiss**

* **retrieveBeamParameters**


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



