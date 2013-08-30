Run a local server
=====================

This section is a brief instruction how to run services locally for test purpose. How to deploy the server
to for example an apache server is not included in this section.

There are 2 services included in this packages, which are municonv services and lattice/model service.
This is a installation guide how to install the service.


Package Dependency
-------------------

Packages needed by all services:

- Python (=2.7.x)
- Django (>= 1.4.x)
- MySQL-python (>= 1.2.x)
- MySQL server (>=5.1.0)
- Django-nose (>=0.1.3, optional)
- python-sphinx (>=1.1.x, needed for generating documents)

for unit conversion, it needs

- numpy (>=1.6.0)
- scipy (>=0.11.0)

for lattice/model, it needs command line tool related to for example tracy3, tracy4, and elegant/sdds if an online simulation is desired.

Checkout the source code
--------------------------
The source code is managed with git, and hosted on github. All source code can be checkout as below:

.. code-block:: bash
    
    $ git clone http://github.com/UnitConversion/unitConversion.git

Don't be bothered by its name of the repository, which was named because the first service was unit conversion service.

Check the network setting, proxy for example, if there is any error such as refused connection.

Relational database configuration
-----------------------------------
A python file so-called credentials.py has to be created and put under physics_dev/physics_django. Its content is as below:

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

Here we assume using MySQL as the back-end database server. For a RDB server accessing over network, put the server name or IP address, or a empty string for localhost as the 'HOST', but, if the server is open to socket access, put its socket link such as ::

    /var/run/mysql5/mysqld.sock

Running service
-----------------
There are few ways to run a local copy locally for example from an IDE, or from command line.
For command line, a running example, start_server, could be found under demo directory with contents as below:

.. code-block:: bash

    #!/bin/sh -X
    export DJANGO_MANAGE_LOCATION=physics_dev/physics_django/manage.py
    export PYTHONPATH=${PWD}/../dataapi:$PYTHONPATH
    cd ../physics_dev/physics_django
    python manage.py runserver

this example will reload server each time when there is any change affecting server. If you do not want to reload the server, simple add
a parameter to the runserver for example:

.. code-block:: bash

    python manage.py runserver --noreload

if the server runs successfully, a message will be printed out as below:

.. code-block:: bash

    $ sh start_server
    Validating models...
    
    0 errors found
    Django version 1.4.2, using settings 'physics_django.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.

if it reports an error like:

.. code-block:: bash

    Error: Can't find the file 'settings.py' in the directory containing 'manage.py'. It appears you've customized things.
    You'll have to run django-admin.py, passing it your settings module.
    (If the file settings.py does indeed exist, it's causing an ImportError somehow.)

most likely, it can not find credentials.py file, or the content in credentials.py is not correct.

From an IDE, here we use eclipse IDE as an example, let's say the project has been checked out in the workspace, and all the proper eclipse plug-ins have been installed. Here we assume an eclipse plug-in, pydev, has been installed, and eclipse is able to recognize
a django project. You can follow the steps here to run the server from eclipse: ::

    1. set project as a PyDev project. [First time only]
       right-clicking the project -> PyDev sub-menu; 
    2. set project as a Django project. [First time only]
       right-clicking the project -> PyDev sub-menu; 
    3. run django tests. [First time only]
       right-clicking the project -> django sub-menu.
       This will prompt you to select manage.py file if DJANGO_MANAGE_LOCATION is not set yet.
    4. DJANGO_MANAGE_LOCATION should be set correctly. Double check it,
       [First time only, or there is anything wrong with this setting].
       right click project -> properties -> PyDev - PYTHONPATH -> String Substitution Variables. 
    5. run it as a Django project to start the server from eclipse.
    
You should see an output from eclipse console as below: ::
    
    Validating models...

    0 errors found
    Django version 1.4.2, using settings 'physics_django.settings'
    Development server is running at http://127.0.0.1:8000/
    Quit the server with CONTROL-C.
    
By default, eclipse runs it with noreload mode. Change it if you want to load change automatically.

Generating documentation
--------------------------
The documentation is written using python sphinx, which is under documents directory. Make files script is created to generate latest documentation, and documents could be generated in various format. Check whatever is available on your platform, for example on a \*nix system, simply type 'make' from a terminal: 

.. code-block:: bash

    $ make

it shows available options, and an example is shown as below: ::

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

Most popularly, 2 kinds of document format, which are html and PDF respectively, are generated. To create html files, simply use command like for example on \*nix system terminal

.. code-block:: bash

    $ cd documents
    $ make html

the html files can be found under _build/html.

Or use follow command to generate a PDF document:

.. code-block:: bash

    $ make latexpdf

a PDF file, phynsicsServices.pdf, can be found under _build/latexpdf directory.

some extra packages are needed listed as below if they are not installed yet: ::

    latex2rtf
    texlive
    texlive-latex-extra

