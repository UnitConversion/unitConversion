Introduction
==============================================
revised: Feb 9, 2014


General
--------------
This system is dedicated for NSLS II (National Synchrotron Light Source II) project, which is constructed
at BNL (Brookhaven National Laboratory). All requirements are driven by NSLS II project at BNL, especially its storage ring.

This system is a sub-system of EPS (Equipment Protection System). Its purpose is to protect machine from an electron beam loss, 
and operate the charged particle beam safely. When the beam conditions are out of range, it is needed to dump electron beam within 1 milli-seconds.

The data service is to capture all static data which are needed to operate an active interlock system, save data in RDB (relational database), 
and keep all history data. Each data set has a status, and details of status will be discussed later. 

Currently, MySQL is adopted as back-end RDBMS.

**Terminology**:

	The terminology defined here is a subset of whole fast active interlock system which are related the data management service. 
	
    - AI: Active Interlock system for storage ring equipment protection
    - AI-BM: Active Interlock system for equipment protection from bending magnet radiation
    - AI-ID: Active Interlock system for equipment protection from insertion device radiation
    - AIE: Active Interlock Envelope
    - AIE-BM: Active Interlock Envelope for Bending Magnets
    - AIE-ID: Active Interlock Envelope for Insertion Devices
    - AIE: Active Interlock Envelope
    - AIOL:  active interlock offset limit, which applies for both horizontal & vertical
        - AIOLH: active interlock offset limit in horizontal plane
        - AIOLV: active interlock offset limit in vertical  plane
    - AIAL:  active interlock angle limit, which applies for both horizontal & vertical
        - AIALH: active interlock horizontal angle limit in horizontal plane
        - AIALV: active interlock vertical angle limit in vertical plane
    - BMPS: Bending Magnet Photon Shutter
    - BPM-ID: RF Beam Position Monitors installed in the Straight Section of the Storage Ring and dedicated to Insertion Device
    - BPM-SR: RF Beam Position Monitors installed in the the Storage Ring except BPM-IDs
    - cUcd: Canted ID configuration and settings at upstream
    - cucD: Canted ID configuration and settings at downstream
    - PSH: ID Photon Shutter
    - SCBM: Safe Current for Bending Magnets
    - SCID: Safe Current for IDs

**Data for active interlock**: 

There are 2 types of interlock, which are AI-BM and AI-ID respectively.
For AI-BM, 2 data are captured at each given BPM, which is threshold for horizontal plane, and for vertical plane. 

For AI-ID, each active interlock unit consists of three (3) logical devices, which are usually two (2) BPMs 
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
      10       |x|<AIOL & |y|<AIOL                Slit                  AI-BM
    ------  ----------------------------------  --------------------  ----------------------
      20       |x1|<AIOL & |x2|<AIOL              Diamond               AIE-ID-B
    ------  ----------------------------------  --------------------  ----------------------
      21       |(x2-x1)*(s3-s1)/(s2-s1)|<AIOL     Rectangular           AIE-ID-A
             & |(x2-x1)/(s2-s1)|<AIAL
    ------  ----------------------------------  --------------------  ----------------------
      22       |x1|<AIOL & |x2|<AIOL              Rectangular           AIE-ID-C
             & |(x2-x1)/(s2-s1)|<AIAL            + optimal offset
    ------  ----------------------------------  --------------------  ----------------------
      23       |x1|<AIOL & |x2|<AIOL 
             & |(x2-x1)*(s3-s1)/(s2-s1)|<AIOL     Rectangular           AIE-ID-D
             & |(x2-x1)/(s2-s1)|<AIAL            + small offset
    ======  ==================================  ====================  ======================

The tens digit identifies a major AIE (active interlock envelope) shape, and the unit digit is for a derivation.
If there is a new shape, a new code could be extended.

:NOTE: An assumption here is that there is no more than 10 different shapes, and each shape has less than 10 derivations.

Status transaction
--------------------

One data set consists of the data of all AI-ID and AI-BM if it is given with the logic applying to those units.

Each data set has a status, and there are 5 status during the life time of a status as below:

    - editable: only data with this status could be changed, and there is only up to one data set for this status 
    - approved: all data and logic has been approved, and ready to be used, and there is only up to one data set for this status 
    - active: data set is using, and there is only up to one data set for this status
    - backup: previous active data set, and there is only up to one data set for this status
    - history: history data which can be viewable only, and all data are here.

There is up to one editable data-set (could be 0 or 1);
There is up to one approved data-set (could be 0 or 1);
There is up to one active data-set (could be 0 or 1);
There is up to one backup data-set (could be 0 or 1);
There are many data set history data-set;

An editable data set could be turned into approved status manually. If there is another data set with approved status, a warning should be given.
If any data in approved data set is modified, its status turns into edit mode, and overwrite current editable data set with a warning.
A approved data set could be turned into active status when downloading by a Python client library. Once that happens, it turns into active data set, 
and current data set in active turns into backup, and current data set in backup goes into history.
Data set in active or backup could be copied into editable. If there is an editable data set, it overwrites existing once with a warning.  
During copying data from active or backup, each data status is kept as approved except the whole data set as unapproved. 

Only after all data in editable data set and its logic are approved, its status could be turned into approved status.
Data in editable data set could be approved separately.

Unapproved data shows as red, and approved data is green.
  

Implementation
----------------
A particular implementation of this data service is described in this section, which is as a REST web service under Django framework. This service consists of 3 layers: ::
    
    1. client layer, which provides an interface to end user of service; 
    2. service layer, which (1) provides an interface to a client, response request from 
       client and send/receive data overnetwork thru http/REST interface to/from client, 
       and (2) interfaces with underneath rdb thru a data api; 
    3. relational database layer, which stores all data.

Together with the Django service, a web UI and Python client library should be provided.
An authorized user could be able to modify the data, approve the data, and change the data status.

 
