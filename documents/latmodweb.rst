Lattice/Model web service
==========================================

Introduction
------------
A particular implementation of lattice/model service is described in this section, which is as a REST web service under Django framework.
As shown in Figure 2 in Lattice/Model basic, this service consists of 3 layers, (1) client layer, which provides an interface to end user of service; (2) service layer, which provides an interface to a client, response request from client and ship/receive data overnetwork thru http/REST interface; (3) relational database layer, which stores all data.

In current implementation, it supports 2 types of http method, which are GET and POST respectively. The details of each is described as below.

Lattice/Model Client
---------------------
The client layer provides an interface to end user in 2 kinds of format: (1) API library, which can be used by a client application, for example Python scripting or Matlab application; (2) user interface, a graphic interface from browser, or CSS (Control System Studio) application.

The implementation is under going, and documentation will come soon.

Lattice/Model Service
---------------------
The service layer responses to answer the request from client, and server data back from or save data into database. The database access is thru a data API (application programming interface), which isolates the RDB access details and business logic from RDB client. Advantage with the data API is that is makes inner schema changes transparent to RDB client, which give both the RDB schema expert and service developer more flexibility. Two major functions are provided in this layer. (1) As a data storage center, receiving all data from client, and storing into the RDB, and serving data back. (2) Providing a quick online simulation when a proper lattice deck with required model control information is provided.



Lattice/Model Database
------------------------
All data are stored inside this layer. The data could be a real data, element name, magnetic strength for example, or a link to point to an external file on file system. The RDB schema is derived from IRMIS schema, which was originally developed by Don Dohan at Brookhaven National Laboratory. It uses MySQL RDBMS (relational database management system) as backend data storage engine. 




Running online simulation
---------------------------




