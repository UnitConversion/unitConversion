Introduction
============

General
-----------

The Physics Service is a collection of services that are motivated by physics application development for particle beam commissioning and beam operation of large particle accelerators. The services in the collection share the same architecture, and technologies. The foundation is a relational database (RDB) which uses the schemas derived from the `IRMIS project <http://irmis.sourceforge.net//>`_.


There are currently 2 services that have been developed are are described below:

* MUNICONV (Multiple purpose unit conversion service). The first iteration targets the NSLS II magnet unit conversion between engineering units (e.g. Ampere), physics units (e.g. Tesla), and model units (e.g. K1, K2). It uses the IRMIS 3 schema as its RDB backend, and MySQL as the RDBMS.

* Lattice/Model. This service tries to capture element geometric information (layout with misalignment), and magnetic strength in its lattice domain, and beam parameters like TWISS parameters, transfer matrix, closed orbit, etc. in the model domain. The data could come from the design, a test senario, and/or a real measurement.

The source code is managed using Git, and hosted on GitHub :: 

  https://github.com/UnitConversion/unitConversion

The code can be checked out from github :: 

  git clone http://github.com/UnitConversion/unitConversion.git


Project Structure
------------------------

The project directory is structured as follows: ::

    dataapi                    - Python library to access relational database
    database                   - MySQL database 
    physics_dev/physics_django - REST web service implemented under the Django framework
    documents                  - Documentation written with sphinx
    utest                      - unit test
    demo                       - an example of how to launch server from the command line
    example                    - some use cases showing how to use the service from the client side
    library                    - a collection of 3rd party libraries which might be needed

