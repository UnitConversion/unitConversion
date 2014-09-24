Client API
=============================

The client is implemented in Python and accesses the service through a RESTful interface.

Client API Library
---------------------

.. automodule:: idodspy.idodsclient
    :members:

Examples of Use
-------------------

The process of saving data into the database can be quite tricky and sometimes difficult. This is because the database schema is fixed and the data to be saved in the database can be quite complex. In the following sections, we list some examples of how to use the data API to save, retrieve, update and delete data.

Basic
~~~~~~~~~~

Connect to Client
+++++++++++++++++++

Before we can call any methods from the Python API, we must initialize the client. We do this by first importing the module:

.. code-block:: python

	from idodspy.idodsclient import IDODSClient

and then by executing the initialization call:

.. code-block:: python

	client = IDODSClient(BaseURL='http://localhost:8000').

When calling the constructor, we should provide the base server URL.

Inventory
+++++++++++++

In the inventory, there are devices that are not yet installed.

To save an inventory item, we call the **saveInventory** method. Input parameters and returned objects are displayed in the `Client API Library`_. Mandatory parameters are: **name** and **cmpnt_type**. There is also a predefined list of properties that should be saved together with the inventory. Some of the items in the list can be set to **None**. The component type with a given name should already exist in the database or **saveInventory** will return an exception.

**Example**

In this example we save an inventory with inventory name **IVU22**, component type **IVU** and prop length set to **1**. All other properties are set to **None**.

.. code-block:: python

    client.saveInventory('IVU22', cmpnt_type='IVU', props={
        'length': 1,
        'up_corrector_position': None,
        'middle_corrector_position': None,
        'down_corrector_position': None,
        'gap_min': None,
        'gap_max': None,
        'gap_tolerance': None,
        'phase1_min': None,
        'phase1_max': None,
        'phase2_min': None,
        'phase2_max': None,
        'phase3_min': None,
        'phase3_max': None,
        'phase4_min': None,
        'phase4_max': None,
        'phase_tolerance': None,
        'k_max_linear': None,
        'k_max_circular': None,
        'phase_mode_p': None,
        'phase_mode_a1': None,
        'phase_mode_a2': None
    })

To retrieve a saved inventory item, we call the **retrieveInventory** method. This method has only one parameter **name** which is mandatory. When providing the **name** parameter we can also make use of wildcards. Refer to the documentation for this method for details.

**Example**

In this example we retrieve all inventory items with names starting with **IVU**. The retrieved data has a JSON structure as explained in the `Client API Library`_.

.. code-block:: python

	inventory = client.retrieveInventory('IVU*')


Inventory items cannot be deleted but they can be updated. To update existing items, we should provide the name of the item through the **old_name** parameter and then all parameters we want to update. 

**Example**
In this example we update the name of the existing inventory item.

.. code-block:: python

	client.updateInventory('IVU22', 'IVU23')

Install
+++++++++++++

When a device is installed, all information about position and type should be saved into the install table.

To install a device we call the **saveInstall** method. It has two mandatory parameters **name** and **cmpnt_type**. Example below describes how item can be saved into install.

**Example**

.. code-block:: python

	client.saveInstall('ivu22g1c10c', cmpnt_type='IVU', coordinatecenter = 2.2)

To retrieve information about installed device, we call the **retrieveInstall** method. Mandatory parameter is **name** but Wildcard characters can also be used to e.g. asterisk to retrieve information about all installed devices. 

**Example**

In this example, information about all devices is retrieved.

.. code-block:: python

	installed_devices = client.retrieveInstall('*')

Information about installed devices cannot be deleted but it can be updated. We update installed device information by calling the **updateInstall** method. We should provide the **old_name** and then set all parameters that need to be changed.

**Example**

In this example, we update the coordinate center property.

.. code-block:: python

	client.updateInstall('ivu22g1c10c', coordinatecenter = 0.0)

Inventory <=> Install Map
++++++++++++++++++++++++++

To link an installed device to a physical device in the database, we call **saveInventoryToInstall**. To save a link, we should provide the install name (**install_name**) and inventory name (**inventory_name**).

**Example**

.. code-block:: python

	client.saveInventoryToInstall('ivu22g1c10c', 'IVU22')

To retrieve a link, we execute **retrieveInventoryToInstall** and provide the id of the link (**inventory_to_install_id**), install name or inventory name. 

**Example**

In this example, we retrieve a link by providing the inventory name.

.. code-block:: python

	client.retrieveInventoryToInstall(None, None, 'IVU22')

When updating a link, we call **updateInventoryToInstall**, provide the link id (**inventory_to_install_id**) and then new install name or inventory name.

**Example**

.. code-block:: python

	client.updateInventoryToInstall(3, 'ivu22g1c10d', 'IVU23')

:Note: It is important to remember that one install item can be linked to only one inventory item and vice versa.

A Shortcut
+++++++++++++

The described process is quite complex so there is a shortcut in the API. The method, **saveInsertionDevice**, can do all of the above and a few more things (described below) in just one call. Essentially, this method:
 - saves inventory
 - saves install
 - saved inventory <=> install map

We can use this method to also mimic basic methods to save the inventory or the install item. By setting the inventory part of the parameters to **None**, the method will only save the install item, and by setting the install part of the parameters to **None**, the method will only save the inventory item. So at least one of **install_name** or **inventory_name** must be present. If both are present, the method will then create a link between inventory and install.

Offline Data
+++++++++++++

Offline data is the data source of the insertion device which is measured without a beam and is attached to a device in the inventory.

To save offline data, use **saveOfflineData**. At least **inventory_name**, **status**, **data** and **data_file_name** should be provided to successfully save offline data into a database. The **data_file_name** parameter is a new file name of the file found at **data** path on a local filesystem.

**Example**

.. code-block:: python

    client.saveOfflineData(inventory_name='EPU57', status=1, data='../dataapi/download_128', data_file_name='datafile', gap=3.4, description='desc')
When saving offline data we can also provide a **method_name** parameter but the method with that name must already exist in the database. To handle that, we can save the method with **saveDataMethod**. Another option is to use the **saveMethodAndOfflineData** method instead of the **saveOfflineData** method. Both methods are used similarly but the **saveMethodAndOfflineData** method checks if the method already exists in the database and if it does not exist it automatically saves it first and only then does it save the offline data.

We can retrieve saved offline data by calling **retrieveOfflineData** and providing one or more of the following parameters: **offlineid**, **description**, **gap**, **phase1**, **phase2**, **phase3**, **phase4**, **phasemode**, **polarmode**, **status**, **method_name**, **inventory_name**. There is also one special parameter named **with_data**. By providing this parameters and setting it to **True**, offline data will be returned together with the uploaded file. The uploaded file will be **Base64** encoded.

**Example**

.. code-block:: python

    client.retrieveOfflineData(offlineid=345, with_data=True)

Example of the returned object:

.. code-block:: python

    {'offlinedata_id': {
            'username': ,      # string
            'description': ,   # string
            'date': ,          # timestamp
            'gap':,            # float
            'phase1': ,        # float
            'phase2': ,        # float
            'phase3':,         # float
            'phase4':,         # float
            'phasemode':,      # string
            'polarmode':,      # string
            'status':,         # int
            'data_file_name':, # string
            'data_file_ts':,   # string
            'data_id':,        # int
            'script_name':,    # string
            'script':,         # string
            'method_name':,    # string
            'methoddesc':,     # string
            'inventory_name':, # string
            'data':            # string, base64 encoded file content
        },
        ...
    }

For now, the API also allows us to update offline data so we can correct possible typos. A mandatory parameter is **offline_data_id**, all other parameters are optional.

**Example**

.. code-block:: python

    client.updateOfflineData(345, status=0)

Offline data can also be deleted. All we need to do is provide the **offline_data_id** to the **deleteOfflineData** method.

**Example**

.. code-block:: python

    client.deleteOfflineData(345)

Online Data
+++++++++++++

Online data is insertion device data source measured with beam. A device is only available online after it has been installed and online data has been attached to this installed device.

To save online data we call **saveOnlineData**. We should provide at least the **install_name**, **data**, **data_file_name** and **status** parameters. The **data_file_name** parameter is the name of the new file we are uploading and the **data** parameter is a path to a file we want to upload.

**Example**

.. code-block:: python

    client.saveOnlineData('epu57g1c02c', data='../dataapi/download_128', data_file_name='datafile', status=1)

We can retrieve online data by calling the **retrieveOnlineData** method. We can provide one or more of the following parameters: **onlineid**, **install_name**, **username**, **description**, **url**, **status**. To retrieve the uploaded file together with other data, we should provide the  **with_data** parameter and set it to **True**. Since this is an actual file saved on a server, we also need to provide the path to where the file will be saved on our local drive. We can do this by providing the **data_path** parameter with valid local path to a file where the file will be downloaded to. Downloading of the uploaded file can take quite some time and we can track download progress. To track download progress we should provide the **callback** parameter by which we provide a callback method that will be called at the start of the download process and after each file block is downloaded.

**Example of the Callback Method Definition**

.. code-block:: python

    def callbackMethod(self, count, block_size, total_size):
        '''
        Track downloading of the file

        :param count: count of block transfered so far
        :type count: int

        :param block_size: block site in bytes
        :type block_size: long

        :param total_size: total size of the file
        :type total_size: long
        '''
        print count, block_size, total_size

**Example of Retrieving Online Data together with Uploaded File**

.. code-block:: python

    client.retrieveOnlineData(onlineid=123, with_data=True, data_path="downloadedfile", callback=self.callbackMethod)

To update online data we call the **updateOnlineData** method and provide the **onlineid** parameter.

**Example**

.. code-block:: python

    client.updateOnlineData(123, description='New description')

Online data can also be deleted. All we need to do is provide **online_data_id** to the **deleteOnlineData** method.

**Example**

.. code-block:: python

    client.deleteOnlineData(123)

Advanced
~~~~~~~~~~

To save all the data we mentioned in the previous section, we also need support data to be present in the database, e.g. information about the vendor, data method, component type property types, etc. The client API allows us to save and update all of these. Most answers on how to do this can be found by reading the automatically generated documentation that can be found in `Client API Library`_. In this section we will provide some examples of some tricky things are sometimes necessary so that data in the database is correctly structured and consistent.

Device Hierarchies / Install IDODS
+++++++++++++++++++++++++++++++++++

Devices can be placed into two hierarchical trees. The first tree represents the device in a financial structure. The device can be assigned to a project and to a beamline. This tree is named **Beamline project**. The second tree represents device's geometric layout. The device can be found in a cell and and in a girder. The second tree is named **Device geometric layout**. To create this hierarchy, some system component types and install items have to be saved into a database. The purpose of system component types and system install items is to separate those items from real devices when retrieving component types and install items.

The client API provides a method, **idodsInstall**, that saves the first two levels of the hierarchy and also creates connections between nodes. It creates a few system component types: **root**, **branch**, **beamline**, **project**, **cell** and **girder**. Each element of a tree that is not a device / leaf element has to be of one of those types. The install method also creates a few system install items: **Trees (root)**, **Device geometric layout (branch)** and **Beamline project (branch)**. Then it connects the root item to both branch items by calling **saveInstallRel**.

After running the **idodsInstall** method we get the following result::

 +-- Trees
      +-- Device geometric layout
      +-- Beamline project

When the starting tree structure is present in the database, we can start adding beamlines, projects, cells and girders.

We can add a new project to a hierarchy by calling **saveInstall** and setting **cmpnt_type** to **project**. When an install item is created we should also take care of that it is connected to the right place in a tree. We call **saveInstallRel** and provide the first parameter which is a child we just created and the second parameter which is a parent already present in a tree.

**Example of Adding an Install Item and Connecting it to a Tree

.. code-block:: python

    client.saveInstall('NSLS-II', cmpnt_type='project')
    client.saveInstallRel('NSLS-II', 'Beamline project')

Saving a Custom Property to a Hierarchical Tree Node
+++++++++++++++++++++++++++++++++++++++++++++++++++

To add a custom location- or project-specific property to a device, we can attach it to a tree node. Firstly, the property type must be created.

**Example of a Creating Tree Node Property Type**

.. code-block:: python

    client.saveInstallRelPropertyType('straight section')

After the property type is created we can add or update the tree node and set a value to a property.

**Example**

.. code-block:: python

    client.saveInstallRel('IXS', 'ivu22g1c10c', props={'straight section': 'asd'})