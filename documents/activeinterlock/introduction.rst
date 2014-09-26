Introduction
==============================================
Revised: Sep 26, 2014


General
--------------
This Active Interlock Data service is dedicated for the NSLS II (National Synchrotron Light Source II) project, being constructed
at Brookhaven National Laboratory (BNL). All requirements are driven by the NSLS II project, especially its storage ring.

This system is a sub-system of the Equipment Protection System (EPS). Its purpose is to protect machine from an electron beam loss, 
and operate the charged particle beam safely. When the beam conditions are out of range, the electron beam must be dumped within 1 ms.

The purpose of the Active Interlock Data service is to capture all static data which is needed to operate an active interlock system, save data into a relational database (RDB), and keep all historical data. Each data set has a status, the details of which will be discussed later. 

Currently, MySQL is adopted as the back-end RDBMS.

**Terminology**

The terminology defined here is a subset of whole fast active interlock system which is related to the data management service. 

    - AI: Active Interlock system for storage ring equipment protection
    - AI-BM: Active Interlock system for equipment protection from bending magnet radiation
    - AI-ID: Active Interlock system for equipment protection from insertion device radiation
    - AIE: Active Interlock Envelope
    - AIE-BM: Active Interlock Envelope for Bending Magnets
    - AIE-ID: Active Interlock Envelope for Insertion Devices
    - AIOL:  active interlock offset limit, which applies to both horizontal & vertical
        - AIOLH: active interlock offset limit in horizontal plane
        - AIOLV: active interlock offset limit in vertical  plane
    - AIAL:  active interlock angle limit, which applies for to horizontal & vertical
        - AIALH: active interlock horizontal angle limit in horizontal plane
        - AIALV: active interlock vertical angle limit in vertical plane
    - BMPS: Bending Magnet Photon Shutter
    - BPM-ID: RF Beam Position Monitors installed in the Straight Section of the Storage Ring and dedicated to Insertion Device
    - BPM-SR: RF Beam Position Monitors installed in the the Storage Ring except BPM-IDs
    - cUcd: Canted ID configuration and settings, upstream
    - cucD: Canted ID configuration and settings, downstream
    - PSH: ID Photon Shutter
    - SCBM: Safe Current for Bending Magnets
    - SCID: Safe Current for IDs

**Data for Active Interlock** 

There are 2 types of interlock, which are AI-BM and AI-ID respectively.
For AI-BM, 2 data sets are captured at each given BPM, which is the threshold for the horizontal and vertical planes. 

For AI-ID, each active interlock unit consists of three (3) logical devices, which are usually two (2) BPMs 
and one virtual device located between 2 BPMs with the sequence: ::

    Device 1 (BPM) ---> Device 3 (Active Interlock Envelop) ---> Device 2 (BPM)

AIOL and AIAL applies to the horizontal and vertical axes, respectively. According to the device location, some detailed parameters are defined:
    
     - ``x1``: horizontal and vertical (x & y) beam position at device 1;
     - ``x2``: horizontal and vertical (x & y) beam position at device 2;
     - ``s1``: location offset of device 1 relative a position, center of a straight section usually;
     - ``s2``: location offset of device 2 relative a position, center of a straight section usually;
     - ``s3``: location offset of device 3 relative a position, center of a straight section usually;
     
**Active Interlock Logic** 

Active interlock logic is defined to keep the electron beam within an allowed phase space in the 3 locations above.
The logic presented in the source data are encoded with according to the following algorithm: ::
    
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

:NOTE: The assumption here is that there is no more than 10 different shapes, and each shape has less than 10 derivations.

Status Transaction
--------------------

One data set consists of the data from all AI-IDs and AI-BMs if it is given with the logic applying to those units.

Each data set has a status, and there are 5 possibilies for the status:

    - editable: only data with this status can be changed
		- There is up to one editable data-set (could be 0 or 1).
    - approved: all data and logic has been approved, and ready to be used
		- There is up to one approved data-set (could be 0 or 1).
    - active: data set currently being used
		- There is up to one active data-set (could be 0 or 1).
    - backup: previous active data set
		- There is up to one backup data-set (could be 0 or 1)
    - history: historical data which can only be viewed.
		- There are many data sets with a status of history.

An editable data set can be turned into approved data set manually. If there is another data set with an approved status, a warning will be given.
If data in an approved data set is modified, its status turns into "editable", and the current editable data set is overwritten, with a warning.
A approved data set can be turned into an active data set when downloaded by a Python client library. When that happens, it becomes an active data set, and the current active data set becomes a backup data set, while the current backup data set becomes a history data set.

Data in an editable data set can be approved individually. Unapproved data is shown in red, and approved data is shown in green.

Active or backup data sets can be copied into an editable data set. If there is an existing editable data set, it is overwritten, with a warning.  
When data is copied from an active or backup data set, the status of each piece of data is kept as approved, but the status of the whole data set is changed to unapproved. 

Only after all data in an editable data set and its logic are approved, can the status of the data set be changed to approved.

Implementation
----------------
The implementation of the data service that is described in this section is as a REST web service under the Django framework. This service consists of 3 layers: ::
    
    1. client layer, which provides an interface to the end user of the service; 
    2. service layer, which 
		a. provides an interface to a client, responds to requests the from client and sends/receives data over the network through an http/REST interface to/from the client, and 
		b. interfaces with the underlying RDB throught a data api; 
    3. relational database layer, which stores all data.

Together with the Django service, a web UI and Python client library will also provided.

An authorized user will be able to modify the data, approve the data, and change the data status.