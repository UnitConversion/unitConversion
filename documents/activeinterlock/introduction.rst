Introduction
==============================================

General
--------------
This system is dedicated for NSLS II (National Synchrotron Light Source II) project, which is constructed
at BNL (Brookhaven National Laboratory). All requirements are driven by NSLS II project at BNL, especially its storage ring.

This system is a sub-system of EPS (Equipment Protection System). Its purpose is to protect machine from an electron beam loss, operate the beam safely. When the beam conditions are out of range, it is needed to dump electron beam within 1 milli-seconds.

The data service is to capture all static data which are needed by active interlock system, saves data in RDB (relational database) server, and keep all data history data. Once data is saved into RDB database, except its status (active or inactive), it is not allowed to change the data anymore to prevent any undesired behavior. Currently, MySQL is adopted as back-end RDBMS.

**Terminology**:

   - AIOL:  active interlock offset limit, which applies for both horizontal & vertical
       - AIHOL: active interlock horizontal offset limit
       - AIVOL: active interlock vertical offset limit
   - AIAL:  active interlock angle limit, which applies for both horizontal & vertical
       - AIHAL: active interlock horizontal angle limit
       - AIVAL: active interlock vertical angle limit


**Active interlock unit**: 

Each active interlock unit consists of three (3) logical devices, which are usually two (2) BPMs 
and one virtual device located in between of 2 BPMs with a sequence as below: ::

    Device 1 (BPM) ---> Device 3 (Active Interlock Envelop) ---> Device 2 (BPM)

As mentioned above, AIOL/AIAL applies both horizontal and vertical axes. According the device location, 
some detailed parameters are defined as below:
    
     - ``x1``: horizontal and vertical (x & y) beam position at device 1;
     - ``x2``: horizontal and vertical (x & y) beam position at device 2;
     - ``s1``: location offset of device 1 relative a position, center of a straight section usually;
     - ``s2``: location offset of device 2 relative a position, center of a straight section usually;
     - ``s3``: location offset of device 3 relative a position, center of a straight section usually;
  
**Active interlock logic**: 

An active interlock logic is defined to keep electron beam within allowed phase space in above 3 locations.
The logic presented in source data are encoded with an algorithm as below: ::
    
    ======  ==================================  ====================  ======================
     code               logic                       shape               AIE type
    ------  ----------------------------------  --------------------  ----------------------
      10       |x1|<AIOL & |x2|<AIOL              Diamond               AIE-ID-B & AIE-BM
    ------  ----------------------------------  --------------------  ----------------------
      20       |(x2-x1)*(s3-s1)/(s2-s1)|<AIOL     Rectangular           AIE-ID-A
             & |(x2-x1)/(s2-s1)|<AIAL
    ------  ----------------------------------  --------------------  ----------------------
      21       |x1|<AIOL & |x2|<AIOL              Rectangular           AIE-ID-C
             & |(x2-x1)/(s2-s1)|<AIAL            + optimal offset
    ------  ----------------------------------  --------------------  ----------------------
      22       |x1|<AIOL & |x2|<AIOL 
             & |(x2-x1)*(s3-s1)/(s2-s1)|<AIOL     Rectangular           AIE-ID-D
             & |(x2-x1)/(s2-s1)|<AIAL            + small offset
    ======  ==================================  ====================  ======================

The tens digit identifies a major AIE (active interlock envelope) shape, and the unit digit is for a derivation.
If there is a new shape, a new code could be extended.

:NOTE: An assumption here is that there is no more than 10 different shapes, and each shape has less than 10 derivations.

Implementation
----------------
A particular implementation of this data service is described in this section, which is as a REST web service under Django framework. This service consists of 3 layers: ::
    
    1. client layer, which provides an interface to end user of service; 
    2. service layer, which (1) provides an interface to a client, response request from 
       client and send/receive data overnetwork thru http/REST interface to/from client, 
       and (2) interfaces with underneath rdb thru a data api; 
    3. relational database layer, which stores all data.

In current implementation, 2 http methods, which are GET and POST respectively, are adopted. After the server is running, the data service is available from url like for example: ::

    http://localhost:8000/activeinterlock

A JSON encoding/decoding is adopted to transfer data over network. All data has to be encoded into a JSON string format before sending over network. For binary data, a BASE64 algorithm is supported to encode/decode the data into/from a string to enable data transferring with JSON string. An JSON header could be for example as below: ::

    {'content-type':'application/json', 'accept':'application/json'}
    
