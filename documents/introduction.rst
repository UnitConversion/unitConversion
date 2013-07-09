Introduction
============

General
-----------

Physics service is a collection of services that are motivated by large particle accelerator
physics application development for particle beam commissioning and beam operation. The services
under the collection shares the same architecture, and technologies. It is a relational database 
related project, which uses the schemas derived from IRMIS project.


Currently, there are 2 services have been developed described as below:

* MUNICONV (Multiple purpose unit conversion service). The first targeting is for NSLS II magnet unit conversion between engineering unit (Ampere for example), physics unit (Tesla for example), and model unit (K1, K2 for example). It uses IRMIS 3 schema as its RDB backend, and MySQL as the RDBMS.

* Lattice/Model. In this service, it tries to capture element geometric information (layout with misalignment), and magnetic strength in its lattice domain, and beam parameters like TWISS parameters, transfer matrix, closed orbit and so on in the model domain. The data could be from design, a test senario, and/or a real measurement.

The source code is managed using Git, and hosted on GitHub as below :: 

  https://github.com/UnitConversion/unitConversion

The code could be check out from github as below :: 

  git clone http://github.com/UnitConversion/unitConversion.git


Project structure
------------------------

Project directory structure is as below: ::

    dataapi                    - Python library to access relational database
    database                   - MySQL database 
    physics_dev/physics_django - REST web service implemented under Django framework
    documents                  - Documentation written with sphinx
    utest                      - unit test
    demo                       - an example how to launch server from command line
    example                    - some use cases showing how to use service from client side
    library                    - collection of 3rd party libraries which might be needed

