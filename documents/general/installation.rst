Run a Local Server
=====================

This section briefly describes how to run services locally for test purposes. Instructions on how to deploy the server
to, e.g., an Apache server is not included.

There are 2 services included in this package, i.e., the MUNICONV service and the Lattice/Model service.
This is an installation guide to install these services.


Package Dependency
-------------------

Packages needed by all services:

- Python (=2.7.x)
- Django (>= 1.4.x)
- MySQL-python (>= 1.2.x)
- MySQL server (>=5.1.0)
- Django-nose (>=0.1.3, optional)
- python-sphinx (>=1.1.x, needed for generating documents)

Packages needed for the MUNICONV service:

- numpy (>=1.6.0)
- scipy (>=0.11.0)

Packages needed for the Lattice/Model service:
 - a command line tool related to, e.g., tracy3, tracy4
 - elegant/sdds if an online simulation is desired.

Checkout the Source Code
--------------------------
The source code is managed with git, and hosted on github. All source code can be checked out from:

.. code-block:: bash
    
    $ git clone http://github.com/UnitConversion/unitConversion.git

Don't worry about the name of the repository. This is historical because the repository was named after the first service, which happened to be the unit conversion service. This respository contains all the files that you need.

If you experience any errors with checking out the repository, e.g. refused connection, please confirm that your network settings, e.g. proxy settings, are correct. 

Relational Database Configuration
-----------------------------------
A python file called ``credentials.py`` has to be created and put into the ``physics_dev/physics_django`` directory.  This file must contain the following:

.. code-block:: python

    DATABASES = {
        'default': {
            'ENGINE':  'django.db.backends.mysql',  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME':    'your database name',        # Or path to database file if using sqlite3.
            'USER':    'your rdb user name',        # Not used with sqlite3.
            'PASSWORD':'your password',             # Not used with sqlite3.
            'HOST':    'your rdb server',           # Set to empty string for localhost. Not used with sqlite3.
            'PORT':    '3306'                       # Set to empty string for default. Not used with sqlite3.
            }
    }
    SECRET_KEY = 'whatever your security key such as q23rans.jcfkh34hpr89hvbdcjkbv%^*()P{Ludihsbkjln/aerg'

Here we assume that you are using MySQL as the back-end database server. For an RDB server accessed over the network, enter the server name or IP address, or a empty string for localhost as the 'HOST', but, if the server is open to socket access, enter its socket link such as ::

    /var/run/mysql5/mysqld.sock

Running the Service
-------------------
A local copy of the service can be run from the command line or from an IDE.

To run the service from a command line, use the working example, ``start_server``, which can be found in the ``demo`` directory.  ``start_server`` contains:

.. code-block:: bash

    #!/bin/sh -X
    export DJANGO_MANAGE_LOCATION=physics_dev/physics_django/manage.py
    export PYTHONPATH=${PWD}/../dataapi:$PYTHONPATH
    cd ../physics_dev/physics_django
    python manage.py runserver

This example reloads the server each time that there is any change that affects the server. If you do not want to reload the server, simple add the ``--noreload`` parameter to the ``runserver`` as follows:

.. code-block:: bash

    python manage.py runserver --noreload

If the server runs successfully, a message similar to what appears below will be printed out:

.. code-block:: bash

    $ sh start_server
    Validating models...
    
    0 errors found
    Django version 1.4.2, using settings 'physics_django.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

If there is an error, e.g. like:

.. code-block:: bash

    Error: Can't find the file 'settings.py' in the directory containing 'manage.py'. It appears you've customized things.
    You'll have to run django-admin.py, passing it your settings module.
    (If the file settings.py does indeed exist, it's causing an ImportError somehow.)

then the most likely problem is that the ``credentials.py`` file cannot be found, or the content of the ``credentials.py`` file is not correct.

To demonstrate running the service from from an IDE, we use Eclipse as our IDE. Let's say that the project has been checked out in the workspace, and all the proper Eclipse plug-ins have been installed. Here we assume that an Eclipse plug-in, ``pydev``, has been installed and that Eclipse is able to recognize a Django project. You can follow the steps here to run the server from Eclipse: ::

    1. Set project as a PyDev project. [First time only]
       Right-click on the project -> PyDev sub-menu; 
    2. Set project as a Django project. [First time only]
       Right-click on the project -> PyDev sub-menu; 
    3. Run Django tests. [First time only]
       Right-click on the project -> Django sub-menu.
       This will prompt you to select the ``manage.py`` file if DJANGO_MANAGE_LOCATION is not set yet.
    4. DJANGO_MANAGE_LOCATION should be set correctly. Double-check it,
       [First time only, or if there is anything wrong with this setting].
       Right-click on project -> Properties -> PyDev - PYTHONPATH -> String Substitution Variables. 
    5. Run it as a Django project to start the server from Eclipse.
    
You should see an output in the Eclipse console that is similar to: ::
    
    Validating models...

    0 errors found
    Django version 1.4.2, using settings 'physics_django.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    
By default, Eclipse runs the server in the ``--noreload`` mode. You can change this if you want to load the server automatically when there are changes.

Generating Documentation
--------------------------
The documentation is written using Python Sphinx, and can be found in the ``documents`` directory. A ``Make`` file script is created to generate the  latest documentation in various formats, e.g. html, pickle, JSON, etc. Check whatever is available on your platform, for example on a \*nix system, simply type ``make`` from a terminal: 

.. code-block:: bash

    $ make

This shows available options: ::

    Please use `make <target>' where <target> is one of
      html       to make standalone HTML files
      dirhtml    to make HTML files named index.html in directories
      singlehtml to make a single large HTML file
      pickle     to make pickle files
      json       to make JSON files
      htmlhelp   to make HTML files and a HTML help project
      qthelp     to make HTML files and a qthelp project
      devhelp    to make HTML files and a Devhelp project
      epub       to make an epub
      latex      to make LaTeX files, you can set PAPER=a4 or PAPER=letter
      latexpdf   to make LaTeX files and run them through pdflatex
      text       to make text files
      man        to make manual pages
      texinfo    to make Texinfo files
      info       to make Texinfo files and run them through makeinfo
      gettext    to make PO message catalogs
      changes    to make an overview of all changed/added/deprecated items
      linkcheck  to check all external links for integrity
      doctest    to run all doctests embedded in the documentation (if enabled)

The two most popular document formats, html and PDF, can be generated. To create html files, simply use the command (e.g. on a \*nix system terminal):

.. code-block:: bash

    $ cd documents
    $ make html

The generated html files can be found in the ``build/html`` directory.

To generate a PDF document:

.. code-block:: bash

    $ make latexpdf

The PDF file, ``physicsServices.pdf``, can be found in the ``build/latexpdf`` directory.

The following packages are needed for document generation and should be installed: ::

    latex2rtf
    texlive
    texlive-latex-extra