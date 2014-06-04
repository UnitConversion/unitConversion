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

To save offline data we should use **saveOfflineData**. At least **inventory_name**, **data_file_name** and **status** should be provided to successfully save offline data into a database. **data_file_name** parameter is a file path that points to an existing file on a filesystem.

Advanced
~~~~~~~~~~