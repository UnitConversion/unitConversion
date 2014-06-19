Client API
=============================

Client is implemented in Python and is accessing service through a RESTful interface.

Client API Library
---------------------

.. automodule:: idodspy.idodsclient
    :members:

Examples of use
-------------------

Because database schema is as it is and data we want to save in the database can be quite complex, saving this data or part of this data can be very hard. In the following subsections there are some examples of use of data API to save, retrieve, update and delete data.

Basic
~~~~~~~~~~

Connect to client
+++++++++++++++++++

Before we can call methods from Python API, we should initialize the client. We can initialize it by first importing the module:

.. code-block:: python

	from idodspy.idodsclient import IDODSClient

and then by executing the initialize call:

.. code-block:: python

	client = IDODSClient(BaseURL='http://localhost:8000')

When calling the constructor we should provide base server URL to it.

Inventory
+++++++++++++

In inventory there are devices that are not yet installed.

To save inventory item we should call **saveInventory** method. Input parameters and returned object is displayed in the `Client API Library`_. Mandatory parameters are: **name** and **cmpnt_type**. There is also a predefined list of properties that should be saved together with the inventory. Some of the items in the list can be set to **None**. When providing those parameters, entities with provided names should already exist in the database or **saveInventory** will return an exception.

Example:

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

In the above example we saved inventory with inventory name **IVU22**, component type **IVU** and prop length set to **1**. All other properties are set to **None**.

To retrieve saved inventory item, we should call **retrieveInventory**. Method has only one parameter **name** which is mandatory. When providing **name** parameter we can also make use of Wildcard characters as described in the method documentation.

Example:

.. code-block:: python

	inventory = client.retrieveInventory('IVU*')

In the above example we retrieve all inventory items with names starting with **IVU**. Retrieved data is JSON structure and is explained in the `Client API Library`_.

Inventory item cannot be deleted but it can be updated. To update existing item we should provide name of the saved item through the **old_name** parameter and then all parameters we want to update. In the example below we will update the name of the existing inventory item.

Example:

.. code-block:: python

	client.updateInventory('IVU22', 'IVU23')

Install
+++++++++++++

When device is installed, all information about position and type should be saved into install table.

To install a device we should call **saveInstall** method. It has two mandatory parameters **name** and **cmpnt_type**. Example below describes how item can be saved into install.

Example:

.. code-block:: python

	client.saveInstall('ivu22g1c10c', cmpnt_type='IVU', coordinatecenter = 2.2)

To retrieve information about installed device, we should call **retrieveInstall** method. Mandatory parameter is **name** but Wildcard characters can also be used to e.g. retrieve information about all installed devices. In the following example information about all devices is retrieved.

Example:

.. code-block:: python

	installed_devices = client.retrieveInstall('*')

Information about install cannot be deleted but it can be updated. We can update installed device information by calling **updateInstall** method. We should provide **old_name** parameter and then set all parameters that need to be changed.

Example:

.. code-block:: python

	client.updateInstall('ivu22g1c10c', coordinatecenter = 0.0)

In the example above we updated the coordinate center property.

Inventory <=> Install map
++++++++++++++++++++++++++

To link install device to physical device in the database, we can call **saveInventoryToInstall**. To save a link we should provide install name (**install_name**) and inventory name (**inventory_name**).

Example:

.. code-block:: python

	client.saveInventoryToInstall('ivu22g1c10c', 'IVU22')

To retrieve a link, we can execute **retrieveInventoryToInstall** and provide id of the link (**inventory_to_install_id**), install name or inventory name. In the following example we are going to retrieve a link by providing inventory name.

Example:

.. code-block:: python

	client.retrieveInventoryToInstall(None, None, 'IVU22')

When updating a link, we should call **updateInventoryToInstall**, provide link id (**inventory_to_install_id**) and then new install name or inventory name.

Example:

.. code-block:: python

	client.updateInventoryToInstall(3, 'ivu22g1c10d', 'IVU23')

We should have in mind a rule that one install item can be linked to only one inventory items and vice versa.

A shortcut
+++++++++++++

Described process is quite complex so there is a shortcut in the API. Method **saveInsertionDevice** can do all of the above and a couple of other stuff (described in following sections) in just one call. It:
 - saves inventory
 - saves install
 - saved inventory <=> install map

We can use this method to also mimic basic methods to save inventory or install item. By setting inventory part of the parameters to **None** method will only save install item, by setting install part of the parameters to **None**, method will only save inventory item. So at least **install_name** or **inventory_name** parameter should be present. If both are present, method will also make a link between inventory and install.

Offline data
+++++++++++++

Offline data is the data source of the insertion device which is measured without a beam and is attached to device in inventory.

To save offline data we should use **saveOfflineData**. At least **inventory_name**, **status**, **data** and **data_file_name** should be provided to successfully save offline data into a database. **data_file_name** parameter is a new file name of the file found at **data** path on a local filesystem.

Example:

.. code-block:: python

    client.saveOfflineData(inventory_name='EPU57', status=1, data='../dataapi/download_128', data_file_name='datafile', gap=3.4, description='desc')

When saving offline data we can also provide **method_name** parameter but method with that name should already exist in the database. To deal with that we can save method with **saveDataMethod** method. Second option is to use **saveMethodAndOfflineData** method instead of **saveOfflineData** method. Both methods are used similarly but **saveMethodAndOfflineData** method checks if method exist in the database and if it does not exist it automatically saves it and after that it saves offline data.

We can retrieve saved offline data by calling **retrieveOfflineData** and providing one or more of the following parameters: **offlineid**, **description**, **gap**, **phase1**, **phase2**, **phase3**, **phase4**, **phasemode**, **polarmode**, **status**, **method_name**, **inventory_name**. There is also one special parameter named **with_data**. By providing this parameters and setting it to **True**, offline data will be returned together with uploaded file. Uploaded file will be **base64** encoded.

Example:

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

For now, API also allows us to update offline data so we can repair possible mistypings. Mandatory parameter is **offline_data_id**, all other parameters are optional.

Example:

.. code-block:: python

    client.updateOfflineData(345, status=0)

Offline data can also be deleted. All we need to do is provide **offline_data_id** to **deleteOfflineData** method.

Example:

.. code-block:: python

    client.deleteOfflineData(345)

Online data
+++++++++++++

Online data is insertion device data source measured with beam. A device is only available online after it is installed and online data is attached to this installed device.

To save online data we should call **saveOnlineData** data. We should provide at least **install_name**, **data**, **data_file_name** and **status** parameters. **data_file_name** parameter is the new name of the file we are uploading and **data** parameter is a path to a file we want to upload.

Example:

.. code-block:: python

    client.saveOnlineData('epu57g1c02c', data='../dataapi/download_128', data_file_name='datafile', status=1)

We can retrieve online data by calling **retrieveOnlineData** method. We can provide one or more of the following parameters: **onlineid**, **install_name**, **username**, **description**, **url**, **status**. To retrieve uploaded file together with other data, we should provide **with_data** parameter and set it to **True**. Because this is actual file saved on a server, we also need to provide path to where file will be saved on our local drive. We can do this by providing **data_path** parameter with valid local path to a file where file will be downloaded to. Downloading of uploaded file can take some time and we have a possibility to track download progress. To track download progress we should provide **callback** parameter by which we provide a callback method that will be called at the start of the download process and after each file block is downloaded.

Example of the callback method definition:

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

Example of retrieving online data together with uploaded file:

.. code-block:: python

    client.retrieveOnlineData(onlineid=123, with_data=True, data_path="downloadedfile", callback=self.callbackMethod)

To update online data we should call **updateOnlineData** method and provide **onlineid** parameter.

Example:

.. code-block:: python

    client.updateOnlineData(123, description='New description')

Online data can also be deleted. All we need to do is provide **online_data_id** to **deleteOnlineData** method.

Example:

.. code-block:: python

    client.deleteOnlineData(123)

Advanced
~~~~~~~~~~

To save all the data we mentioned in the previous section we also need support data to be present in the database like: information about vendor, data method, component type property types etc. Client API allows us to save and update all of them. Most answers on how to do this can be found by reading auto generated documentation that can be found at `Client API Library`_. In this section we will provide a couple of examples of some tricky stuff we sometimes have to do so data in the database is correctly structured and consistent.