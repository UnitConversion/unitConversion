Web client
==============================================

Web client is implemented using *Angular.js* and *jquery*. It connects to the server through RESTful Interface and is served from the django server.

Description and usage of the user interface
--------------------------------------------

Description of the layout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Web user interface comprises of navigation bar on the top and the body below it. Navigation bar has menu items that represent all of the available statuses of the dataset. On the right there is a dropdown element that allows user to log in and log out. By clicking on the status menu item, dataset is displayed in the body.

In body part of the user interface the whole dataset is displayed. Dataset has three parts/tables and they can be viewed by selecting appropriate tab in the tab navigation bar. On the right there are buttons that enable user to move dataset from one status to another.

Every dataset part (BM, ID, logic) is displayed in its own table. Every row represents a device or a logic and every cell a property of the device that must be captured. Table can be editable or not depending on user permissions. When table is editable, data in most of the cells can be changes and thus updated. After updating, some of the cell also need approval. Data in the cell can be approved by clicking on the button that appears after updating the value below the changed value. To speed up things, the whole row can be approved by clicking on the approve button which is positioned at the end of every row. New device and logic can be added by pressing the *Add new device* or *Add new logic* buttons.

.. figure:: img/ui.png
   :scale: 50%
   
   Home screen is displaying BM device.

Log in / log out
~~~~~~~~~~~~~~~~~~

Datasets are read-only by default. Adding a modifying existing data requires user to be logged in and have needed permissions. When user gen an account he can log in by clicking on the Log in button that is positioned in the top right corner.

.. figure:: img/log_in.png
   :scale: 50%
   
   Log in button.

When user is finished with adding and modifying data he can log out by clicking on the log out menu item.

.. figure:: img/log_out.png
   :scale: 50%
   
   Log out menu.

Adding, modifying and approving data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To add, modify and approve data, user has to be logged in and it has to have special permissions. To add a new device or logic, user must click on the **Add new device** or **Add new logic** button. New row is displayed with user inputs in every cell. After values are entered into user input, user can click on **Add** button to save new device/logic or **Cancel** to cancel this action.

.. figure:: img/add.png
   :scale: 50%
   
   Add a new device into BM table.

After adding a new device/logic some of the cells get red background and approve button shows up. Data in this cells need to be approved before the whole dataset can be approved and thus used. After clicking on a button, pop up is shown with a warning message and user has to click on **Yes** button to approve the value in a cell.

.. figure:: img/approve_cell.png
   :scale: 50%
   
   Approve value in a cell.

To approve the whole row, user has to click on **Approve** button that is positioned at the end of each row. After clicking on it, pop up is shown with warning message. User has to click on **Yes** button to approve the whole row.

.. figure:: img/approve_row.png
   :scale: 50%
   
   Approve the whole row.

Adding, approving the datasets and moving through statuses
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In the navigation bar there are five button which represent possible statuses of the dataset. Next to the name of the status there is a badge with the number of datasets that have that status. All of the statuses except history are taken only by one dataset. All of the datasets that were active end up in history when they are replaced with the new datasets.

When new datasets are added they have status set to editable. Consequentially in web client new datasets can be added by first selecting editable status from menu and then clicking **Create new dataset** button. Pop up shows up and user can enter description for a new dataset and then click **Create**.

.. figure:: img/create.png
   :scale: 50%
   
   Create dataset.
   
.. figure:: img/create_popup.png
   :scale: 50%
   
   Enter description and click Create.

After logic and devices are entered and approved, the whole dataset can be approved by pressing the **Approve** button that is places in the same line with tabs.

.. figure:: img/approve_dataset.png
   :scale: 50%
   
   Approve dataset.

After dataset is approved web client is refreshed and dataset is accessible by clicking on **Approved** menu item. **Editable** status is now again empty and new dataset can be created.

Dataset history
~~~~~~~~~~~~~~~~

When data is downloaded it gets the active status. If there was a dataset with active status it gets backup status and if there was a dataset with backup status it is moved to history. Therefore all active datasets are moved to history when they are replaced with new ones. When clicking on the **History** menu item, table with all datasets with status history are displayed. In the table there are important information like data created, dataset author, description etc.

.. figure:: img/history.png
   :scale: 50%
   
   History view.

Every row in history table has a **Show** button at the end of the row and by clicking on it dataset is displayed as in any other status with a difference that the data is in read-only mode.