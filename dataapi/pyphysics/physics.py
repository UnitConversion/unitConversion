'''
Created on Jun 4, 2014

@author dejan.dezman@cosylab.com
'''

import MySQLdb
import os
import base64
import time
import logging

from utils import (_generateFilePath, _checkParameter, _checkWildcardAndAppend, _generateUpdateQuery, _checkRangeAndAppend)
from _mysql_exceptions import MySQLError

try:
    from django.utils import simplejson as json
except ImportError:
    import json


class physics(object):
    '''
    Data API for common data storage.

    All data have to be either all saved, or none is saved.
    '''
    def __init__(self, conn, transaction=None):
        '''
        Initialize physics class.

        :param conn: MySQL connection object
        :type conn: object

        :param transaction: Django MySQL transaction object. If this is set, it uses Django's transaction manager to manage each transaction.
        :type transaction: object

        :returns: physics -- class object
        '''

        self.conn = conn

        # Use django transaction manager
        self.transaction = transaction

        # Init logger
        self.logger = logging.getLogger('physics')
        hdlr = logging.FileHandler('/var/tmp/physics.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

    def retrieveVendor(self, name, description=None):
        '''
        Retrieve vendor by its name and description
        Wildcast matching are supported for both name and description.

        :param name: vendor name
        :type name: str

        :param description: description for a vendor
        :type description: str

        :return: a tuple::

                (
                    (
                        id,
                        name,
                        description
                    ),
                    ...
                }

        :Raises: ValueError, Exception
        '''

        # Check for vendor name parameter
        _checkParameter('name', name)

        # Generate SQL statement
        vals = []
        sql = '''
        SELECT vendor_id, vendor_name, vendor_description FROM vendor WHERE
        '''

        # Append name
        sqlVals = _checkWildcardAndAppend('vendor_name', name, sql, vals)

        # Append description
        if description is not None:
            sqlVals = _checkWildcardAndAppend('vendor_description', description, sqlVals[0], sqlVals[1], 'AND')

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Get any one since it should be unique
            res = cur.fetchall()
            return res

        except Exception as e:
            self.logger.info('Error when fetching vendor:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching vendor:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveVendor(self, name, description=None):
        '''Save vendor and its description into database

        :param name: vendor name
        :type name: str

        :param dtype: device type

        :param description: a brief description which could have up to 255 characters
        :type description: str

        :return: vendor_id

        :Raises: ValueError, MySQLError
        '''

        # Check for vendor name parameter
        _checkParameter('name', name)

        # Try to retrieve vendor by its name
        existingVendor = self.retrieveVendor(name, description=description)

        if len(existingVendor):
            raise ValueError("Vendor (%s) already exists in the database!" % name)

        # Generate SQL statement
        sql = '''
        INSERT INTO vendor (vendor_name, vendor_description) VALUES (%s, %s)
        '''
        vals = [name, description]

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sql, vals)

            # Get last row id
            vendorid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return vendorid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving vendor:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving vendor:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveComponentType(self, name, description=None):
        '''
        Retrieve a component type

        :param name: component type type name
        :type name: str

        :param description: description for this device
        :type desctiprion: str

        :return: a map with structure like:

            .. code-block: python

                (
                    (
                        component_type_id,
                        component_type_name,
                        description
                    ),
                    ...
                )

        :Raises: MySQLError
        '''

        # Start SQL
        sql = '''
        SELECT cmpnt_type_id, cmpnt_type_name, description FROM cmpnt_type WHERE
        '''

        vals = []

        # Append component type
        sqlAndVals = _checkWildcardAndAppend("cmpnt_type_name", name, sql, vals)

        # Append description if it exist
        if description is not None:
            sqlAndVals = _checkWildcardAndAppend("description", description, sqlAndVals[0], sqlAndVals[1], "AND")

        # Execute SQL
        try:
            cur = self.conn.cursor()
            cur.execute(sqlAndVals[0], sqlAndVals[1])
            res = cur.fetchall()

            return res

        except Exception as e:
            self.logger.info('Error when fetching component type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching component type:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveComponentType(self, component_type_name, description=None):
        '''
        Save a component type

        :param component_type_name: component type name
        :type component_type_name: str

        :param description: description for this device
        :type desctiprion: str

        :return: id of a new component type

        :Raises: MySQLError
        '''

        # Save it into database and return its new id
        sql = ''' INSERT into cmpnt_type (cmpnt_type_name, description) VALUES (%s, %s) '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (component_type_name, description))
            componenttypeid = cur.lastrowid

            # Commit transaction
            if self.transaction is None:
                self.conn.commit()

            return componenttypeid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving component type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving component type:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveComponentTypeVendor(self, component_type_id, vendor_id):
        '''
        Retrieve component type - vendor map

        :param component_type_id: component type id
        :type component_type_id: int

        :param vendor_id: vendor id
        :type vendor_id: int

        :return: a tuple::

                (
                    (
                        id,
                        component_type_id,
                        component_type_name,
                        vendor_id,
                        vendor_name
                    ),
                    ...
                }

        :Raises: ValueError, Exception
        '''

        # Generate SQL statement
        vals = []
        sql = '''
        SELECT
            cv.cmpnttype__vendor_id,
            cv.cmpnt_type_id,
            ct.cmpnt_type_name,
            cv.vendor_id,
            v.vendor_name
        FROM cmpnttype__vendor cv
        LEFT JOIN vendor v ON(cv.vendor_id = v.vendor_id)
        LEFT JOIN cmpnt_type ct ON(cv.cmpnt_type_id = ct.cmpnt_type_id)
        WHERE
        '''

        # Append component type id
        sqlVals = _checkWildcardAndAppend('ct.cmpnt_type_id', component_type_id, sql, vals)

        # Append vendor id
        if vendor_id:
            sqlVals = _checkWildcardAndAppend('v.vendor_id', vendor_id, sqlVals[0], sqlVals[1], 'AND')

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Get all
            res = cur.fetchall()
            return res

        except Exception as e:
            self.logger.info('Error when fetching component type - vendor map:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching component type - vendor map:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveComponentTypeVendor(self, component_type_id, vendor_id):
        '''
        Save component type - vendor map

        :param component_type_id: component type id
        :type component_type_id: int

        :param vendor_id: vendor id
        :type vendor_id: int

        :return: id of the map

        :Raises: ValueError, MySQLError
        '''

        # Try to retrieve existing map
        existingMap = self.retrieveComponentTypeVendor(component_type_id, vendor_id)

        if len(existingMap):
            raise ValueError("Map already exists in the database!")

        # Generate SQL statement
        sql = '''
        INSERT INTO cmpnttype__vendor (cmpnt_type_id, vendor_id) VALUES (%s, %s)
        '''
        vals = [component_type_id, vendor_id]

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sql, vals)

            # Get last row id
            mapid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return mapid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving component type - vendor map:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving component type - vendor map:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveComponentTypePropertyType(self, name, description=None):
        '''
        Retrieve component type property type by its name

        :param name: property type name
        :type name: str

        :param description: property type description
        :type description: str

        :return: a tuple:

            .. code-block:: python

                (
                    (
                        id,
                        name,
                        description
                    ),
                    ...
                )

        :Raises: ValueError, MySQLError
        '''

        # Check name
        _checkParameter("name", name)

        # Construct SQL
        sql = '''
        SELECT
            cmpnt_type_prop_type_id, cmpnt_type_prop_type_name, cmpnt_type_prop_type_desc
        FROM
            cmpnt_type_prop_type
        WHERE
        '''
        vals = []

        # Append name
        sqlAndVals = _checkWildcardAndAppend("cmpnt_type_prop_type_name", name, sql, vals)

        # Append description
        if description is not None:
            sqlAndVals = _checkWildcardAndAppend("cmpnt_type_prop_type_desc", description, sqlAndVals[0], sqlAndVals[1], 'AND')

        try:
            cur = self.conn.cursor()
            cur.execute(sqlAndVals[0], sqlAndVals[1])

            # Get any one since it should be unique
            res = cur.fetchall()
            return res

        except Exception as e:
            self.logger.info('Error when fetching component type property type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching component type property type:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveComponentTypePropertyType(self, name, description=None):
        '''
        Insert new component type property type into database

        :param name: name of the component type property type M
        :type name: str

        :param description: description of the component type property type O
        :type description: str

        :return: id of the newly inserted item

        :Raises: ValueError, MySQLError
        '''

        # Raise an error if component type property type exists
        existingComponentTypePropertyType = self.retrieveComponentTypePropertyType(name)

        if len(existingComponentTypePropertyType):
            raise ValueError("Component type property type (%s) already exists in the database!" % name)

        # Check name
        _checkParameter("name", name)

        # Generate SQL
        sql = '''
        INSERT INTO cmpnt_type_prop_type
            (cmpnt_type_prop_type_name, cmpnt_type_prop_type_desc)
        VALUES
            (%s, %s)
        '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (name, description))

            # Get last row id
            typeid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return typeid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving new component type property type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving new component type property type:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveComponentTypeProperty(self, component_type_id, component_type_property_type_id=None, value=None):
        '''
        Retrieve component type property from the database

        :param component_type_id: id of the component type entry
        :type component_type_id: int

        :param component_type_property_type_id: id of the property type
        :type component_type_property_type_id: int

        :param value: value of the property
        :type value: str

        :returns: a tuble:

            .. code-block:: python

                (
                    (
                        id,
                        value,
                        cmpnt_type_id,
                        cmpnt_prop_type_id,
                        cmpnt_prop_type_name,
                        cmpnt_type_name
                    ),
                    ...
                )

        :raises: Exception
        '''

        # Generate SQL
        sql = '''
        SELECT
            cp.cmpnt_type_prop_id,
            cp.cmpnt_type_prop_value,
            cp.cmpnt_type_id,
            cp.cmpnt_type_prop_type_id,
            cpt.cmpnt_type_prop_type_name,
            ct.cmpnt_type_name
        FROM cmpnt_type_prop cp
        LEFT JOIN cmpnt_type_prop_type cpt ON (cp.cmpnt_type_prop_type_id = cpt.cmpnt_type_prop_type_id)
        LEFT JOIN cmpnt_type ct ON (cp.cmpnt_type_id = ct.cmpnt_type_id)
        WHERE
        '''

        # Add component type id parameter
        sql += ' cp.cmpnt_type_id = %s '
        vals = [component_type_id]

        # Add component type property type parameter
        if component_type_property_type_id:
            sql += ' AND cp.cmpnt_type_prop_type_id = %s '
            vals.append(component_type_property_type_id)

        sqlVals = (sql, vals)

        # Add value parameter if exists
        if value:
            sqlVals = _checkWildcardAndAppend('cmpnt_type_prop_value', value, sqlVals[0], sqlVals[1], 'AND')

        try:
            # Retrieve objects from the database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            return cur.fetchall()

        except Exception as e:
            self.logger.info('Error when retrieving component type property from the table:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when retrieving component type property from the table:\n%s (%s)' % (e.args[1], e.args[0]))

    def saveComponentTypeProperty(self, component_type_id, component_type_property_type_id, value):
        '''
        Save inventory property into database

        :param component_type_id: id of the component type
        :type component_type_id: int

        :param component_type_property_type_id: id of the component type property type
        :type component_type_property_type_id: int

        :param value: value of the component type property
        :type value: str

        :return: new component type property id

        :raise: MySQLError
        '''

        # Generate SQL
        sql = '''
        INSERT INTO cmpnt_type_prop
            (cmpnt_type_id, cmpnt_type_prop_type_id, cmpnt_type_prop_value)
        VALUES
            (%s, %s, %s)
        '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (component_type_id, component_type_property_type_id, value))

            # Get last row id
            propid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return propid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving component type property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving component type property:\n%s (%d)' % (e.args[1], e.args[0]))

    def updateComponentTypeProperty(self, component_type_id, component_type_property_type_id, value):
        '''
        Save inventory property into database

        :param component_type_id: id of the component type
        :type component_type_id: int

        :param component_type_property_type_id: id of the component type property type
        :type component_type_property_type_id: int

        :param value: value of the component type property
        :type value: str

        :returns: True if everything is ok

        :raises: MySQLError
        '''

        # Define query dict
        queryDict = {}
        whereDict = {}

        # Where component type id equals
        whereDict['cmpnt_type_id'] = component_type_id

        # Where component type property type id equals
        whereDict['cmpnt_type_prop_type_id'] = component_type_property_type_id

        # Set value parameter
        queryDict['cmpnt_type_prop_value'] = value

        # Generate SQL
        sqlVals = _generateUpdateQuery('cmpnt_type_prop', queryDict, None, None, whereDict)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating component type property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating component type property:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveInventoryPropertyTemplate(self, name, cmpnt_type_id=None, description=None):
        '''
        Retrieve inventory property template by its name

        :param name: Inventory property name
        :type name: str

        :param cmpnt_type_id: component type name
        :type cmpnt_type_id: str

        :param description: inventory property template description
        :type description: str

        :return: a map with structure like:

            .. code-block:: python

                (
                    (
                        id,
                        name,
                        description,
                        default,
                        unit,
                        cmpnt_type,
                        cmpnt_type_id
                    ),
                    ...
                )

        :Raises: MySQLError
        '''

        # Construct SQL
        sql = '''
        SELECT
            tmp.inventory_prop_tmplt_id,
            tmp.inventory_prop_tmplt_name,
            tmp.inventory_prop_tmplt_desc,
            tmp.inventory_prop_tmplt_default,
            tmp.inventory_prop_tmplt_units,
            cmpnt.cmpnt_type_name,
            tmp.cmpnt_type_id
        FROM inventory_prop_tmplt tmp
        LEFT JOIN cmpnt_type cmpnt ON tmp.cmpnt_type_id = cmpnt.cmpnt_type_id
        WHERE
        '''
        vals = []

        # Append name
        sqlAndVals = _checkWildcardAndAppend("tmp.inventory_prop_tmplt_name", name, sql, vals)

        # Append component type id
        if cmpnt_type_id:
            sqlAndVals = _checkWildcardAndAppend("tmp.cmpnt_type_id", cmpnt_type_id, sqlAndVals[0], sqlAndVals[1], 'AND')

        if description:
            sqlAndVals = _checkWildcardAndAppend("tmp.inventory_prop_tmplt_desc", description, sqlAndVals[0], sqlAndVals[1], 'AND')

        try:
            cur = self.conn.cursor()
            cur.execute(sqlAndVals[0], sqlAndVals[1])

            # get any one since it should be unique
            res = cur.fetchall()

            return res

        except Exception as e:
            self.logger.info('Error when fetching inventory property template:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching inventory property template:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveInventoryPropertyTemplate(self, name, cmpnt_type_id, description=None, default=None, unit=None):
        '''
        Insert new inventory property template into database

        :param name: property template name M
        :type name: str

        :param cmpnt_type_id: component type id M
        :type cmpnt_type_id: int

        :param description: property template description O
        :type description: str

        :param default: property template default value O
        :type default: str

        :param unit: property template unit O
        :type unit: str

        :return: new property template id

        :Raises: MySQLError
        '''

        # Generate SQL
        sql = '''
        INSERT INTO inventory_prop_tmplt
        (cmpnt_type_id, inventory_prop_tmplt_name, inventory_prop_tmplt_desc, inventory_prop_tmplt_default, inventory_prop_tmplt_units)
        VALUES
        (%s, %s, %s, %s, %s)
        '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (cmpnt_type_id, name, description, default, unit))

            # Get last row id
            templateid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return templateid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving new inventory property template:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving new inventory property template:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveInventoryProperty(self, inventory_id, inventory_property_template_id=None, value=None):
        '''
        Retrieve id and value from inventory property table

        :param inventory_id: id of the inventory entry
        :type inventory_id: int

        :param inventory_property_template_id: id of the inventory property template
        :type inventory_property_template_id: int

        :param value: value of the property template
        :type value: str

        :returns: Python tuple

            (
                (
                    inventory_prop_id,
                    inventory_prop_value,
                    inventory_prop_tmplt_id,
                    inventory_id,
                    inventory_prop_tmplt_name,
                    invnetory_name
                ),
                ...
            )

        :raises: MySQLError
        '''

        # Generate SQL
        sql = '''
        SELECT
            ip.inventory_prop_id,
            ip.inventory_prop_value,
            ip.inventory_prop_tmplt_id,
            ip.inventory_id,
            ipt.inventory_prop_tmplt_name,
            inv.name
        FROM inventory_prop ip
        LEFT JOIN inventory_prop_tmplt ipt ON (ip.inventory_prop_tmplt_id = ipt.inventory_prop_tmplt_id)
        LEFT JOIN inventory inv ON (ip.inventory_id = inv.inventory_id)
        WHERE
        '''

        # Add inventory_id parameter
        sql += ' ip.inventory_id = %s '
        vals = [inventory_id]

        # Add inventory_prop_tmplt_id parameter
        if inventory_property_template_id:
            sql += ' AND ip.inventory_prop_tmplt_id = %s '
            vals.append(inventory_property_template_id)

        sqlVals = (sql, vals)

        # Add value parameter if exists
        if value:
            sqlVals = _checkWildcardAndAppend('inventory_prop_value', value, sqlVals[0], sqlVals[1], 'AND')

        try:
            # Retrieve objects from the database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            res = cur.fetchall()
            return res

        except Exception as e:
            self.logger.info('Error when retrieve id and vale from inventory property table:\n%s (%s)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when retrieve id and vale from inventory property table:\n%s (%s)' % (e.args[1], e.args[0]))

    def saveInventoryProperty(self, inventory_id, inventory_property_template_id, value):
        '''
        Save inventory property into database

        :param inventory_id: id of the inventory we are saving property for
        :type inventory_id: int

        :param inventory_property_template_id: id of the property template/inventory property key name
        :type inventory_property_template_id: int

        :param value: value of the property template/property key name
        :type value: str

        :returns: id of the new property

        :raises: MySQLError
        '''

        # Generate SQL
        sql = '''
        INSERT INTO inventory_prop
        (inventory_id, inventory_prop_tmplt_id, inventory_prop_value)
        VALUES
        (%s, %s, %s)
        '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (inventory_id, inventory_property_template_id, value))

            # Get last row id
            propid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return propid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving inventory property value:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving inventory property value:\n%s (%d)' % (e.args[1], e.args[0]))

    def updateInventoryProperty(self, inventory_id, inventory_property_template_id, value):
        '''
        Update inventory property in a database

        :prop inventory_id: name of the inventory we are saving property for
        :type inventory_id: str

        :prop inventory_property_template_id: name of the property template/inventory property key name
        :type inventory_property_template_id: str

        :prop value: value of the property template/property key name
        :type value: str

        :returns: True if everything is ok

        :raises: ValueError, MySQLError
        '''

        # Define query dict
        queryDict = {}
        whereDict = {}

        # Set inventory
        whereDict['inventory_id'] = inventory_id

        # Set property template
        whereDict['inventory_prop_tmplt_id'] = inventory_property_template_id

        # Set value parameter
        queryDict['inventory_prop_value'] = value

        # Generate SQL
        sqlVals = _generateUpdateQuery('inventory_prop', queryDict, None, None, whereDict)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating inventory property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating inventory property:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveInventory(self, name, serial_number, component_type_name, vendor, inventory_id=None):
        '''
        Retrieve an insertion device from inventory.
        Wildcard matching is supported for inventory name, device type and vendor. ::

            * for multiple characters matching
            ? for single character matching


        :param name: insertion device inventory name, which is usually different from its field name (the name after installation).
        :type name: str

        :param serial_number: device serial number
        :type serial_number: str

        :param component_type_name: name of the component type
        :type component_type_name: str

        :param vendor: name of the vendor name
        :type vendor: str

        :param inventory_id: inventory id
        :type inventory_id: int

        :return: a tuple with structure like:

            .. code-block:: python

                (
                    (
                        inventory_id,
                        inventory_name,
                        alias,
                        serial_no,
                        cmpnt_type_name,
                        cmpnt_type_description,
                        vendor_name
                    ),
                    ...
                )

        :Raises: MySQLError
        '''

        # Generate SQL
        sql = '''
        SELECT inv.inventory_id, inv.name, inv.alias, inv.serial_no,
            ctype.cmpnt_type_name, ctype.description,
            vendor.vendor_name
        FROM inventory inv
        LEFT JOIN vendor on vendor.vendor_id = inv.vendor_id
        LEFT JOIN cmpnt_type ctype on ctype.cmpnt_type_id = inv.cmpnt_type_id
        WHERE 1=1
        '''

        vals = []
        sqlVals = (sql, vals)

        # Append inventory id
        if inventory_id:
            sqlVals = _checkWildcardAndAppend('inv.inventory_id', inventory_id, sqlVals[0], sqlVals[1], 'AND')

        # Append inv.name parameter
        if name:
            sqlVals = _checkWildcardAndAppend('inv.name', name, sql, vals, 'AND')

        # Append serial number
        if serial_number:
            sqlVals = _checkWildcardAndAppend('inv.serial_no', serial_number, sqlVals[0], sqlVals[1], 'AND')

        # Append component type name
        if component_type_name:
            sqlVals = _checkWildcardAndAppend('ctype.cmpnt_type_name', component_type_name, sqlVals[0], sqlVals[1], 'AND')

        # Append vendor
        if vendor:
            sqlVals = _checkWildcardAndAppend('vendor.vendor_name', vendor, sqlVals[0], sqlVals[1], 'AND')

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Get any one since it should be unique
            res = cur.fetchall()

            return res

        except Exception as e:
            self.logger.info('Error when fetching insertion device inventory:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching insertion device inventory:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveInventory(self, name, component_type_id, alias, serial_number, vendor_id):
        '''
        Save device into inventory

        :param name: device name, which is usually different from its field name (the name after installation).
        :type name: str

        :param component_type_id: component type id
        :type component_type_id: int

        :param alias: alias name if it exists
        :type alias: str

        :param serial_number: serial number
        :type serial_number: str

        :param vendor_id: name of vendor id
        :type vendor_id: str

        :return: id of the new device in the inventory

        :Raises: MySQLError

        '''

        # Generate SQL
        sql = '''
        INSERT INTO inventory (cmpnt_type_id, vendor_id, name, alias, serial_no) VALUES
        (%s, %s, %s, %s, %s)
        '''

        try:
            # Insert inventory into database
            cur = self.conn.cursor()
            cur.execute(sql, (component_type_id, vendor_id, name, alias, serial_number))

            # Get last row id
            invid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return invid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving new inventory:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving new inventory:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveInstall(self, name, component_type_name, description):
        '''Retrieve insertion device installation using any of the acceptable key words:

        :param name: installation name, which is its label on field
        :type name: str

        :param description: installation description
        :type description: str

        :param component_type_name: component type name of the device
        :type component_type_name: str

        :return: a tuple with structure like:

            .. code-block:: python

                (
                    (
                        install_id,
                        name,
                        location,
                        cmpnt_type_name,
                        cmpnt_type_description,
                        cmpnt_type_id,
                        coordinatecenter
                    ),
                    ...
                )

        :Raises: MySQLError
        '''

        # Generate SQL
        sql = '''
        SELECT
            inst.install_id,
            inst.field_name,
            inst.location,
            ct.cmpnt_type_name,
            ct.description,
            inst.cmpnt_type_id,
            inst.coordinate_center
        FROM install inst
        LEFT JOIN cmpnt_type ct ON(inst.cmpnt_type_id = ct.cmpnt_type_id)
        WHERE
        '''

        vals = []

        # Append name parameter
        sqlVals = _checkWildcardAndAppend('inst.field_name', name, sql, vals)

        # Append description parameter
        if description:
            sqlVals = _checkWildcardAndAppend('inst.location', description, sqlVals[0], sqlVals[1], 'AND')

        # Append component type parameter
        if component_type_name:
            sqlVals = _checkWildcardAndAppend('ct.cmpnt_type_name', component_type_name, sqlVals[0], sqlVals[1], 'AND')

        try:
            # Execute SQL
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Get last id
            res = cur.fetchall()
            return res

        except Exception as e:
            self.logger.info('Error when fetching installation:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching installation:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveInstall(self, name, description, cmpnt_type_id, coordinate_center):
        '''
        Install a device

        :param name: installation name, which is its label on field
        :type name: str

        :param description: installation description
        :type description: str

        :param cmpnt_type_id: id of the component type
        :type cmpnt_type_id: int

        :param coordinate_center: coordinate center number
        :type coordinate_center: float

        :return: new install id

        :raises: MySQLError
        '''

        # Generate SQL
        sql = '''
        INSERT INTO install
            (cmpnt_type_id, field_name, location, coordinate_center)
        VALUES
            (%s, %s, %s, %s)
        '''

        try:
            # Insert record into database
            cur = self.conn.cursor()
            cur.execute(sql, (cmpnt_type_id, name, description, coordinate_center))

            # Get last row id
            invid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return invid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving new inventory:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving new inventory:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveInstallRel(self, parent_install_id, child_install_id, description=None, order=None):
        '''
        Save install relationship into a database.

        :param parent_install_id: id of the parent element
        :type parent_install_id: int

        :param child_install_id: id of the child element
        :type child_install_id: int

        :param description: description of the relationship
        :type description: str

        :param order: order of the child in the relationship
        :type order: int

        :return:  new install rel id

        :raises: MySQLError
        '''

        # Generate SQL
        sql = '''
        INSERT INTO install_rel (
            parent_install_id,
            child_install_id,
            logical_desc,
            logical_order,
            install_date
        ) VALUES (%s, %s, %s, %s, NOW())
        '''

        try:
            # Insert entity
            cur = self.conn.cursor()
            cur.execute(sql, (parent_install_id, child_install_id, description, order))

            # Get last row id
            idrel = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return idrel

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving new install rel:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving new install rel:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveInventoryToInstall(self, inventory__install_id, install_id, inventory_id):
        '''
        Return installed devices or psecific map

        :param inventory__install_id: id of the inventory to install map
        :type inventory__install_id: int

        :param install_id: id of the instaleld device
        :type install_id: int

        :param inventory_id: id of the device in the inventory
        :type inventory_id: int

        :return: a tuple with a structure like:

            .. code-block:: python

                (
                    (
                        id,
                        install_id,
                        inventory_id,
                        install_name,
                        inventory_name,
                        install_location
                    ),
                    ...
                )

        :Raises: MySQLError
        '''

        # Generate SQL
        sql = '''
        SELECT
            ii.inventory__install_id,
            ii.install_id,
            ii.inventory_id,
            inst.field_name,
            inv.name,
            inst.location
        FROM inventory__install ii
        LEFT JOIN install inst ON(ii.install_id = inst.install_id)
        LEFT JOIN inventory inv ON(ii.inventory_id = inv.inventory_id)
        WHERE 1=1
        '''

        vals = []

        # Check primary key
        if inventory__install_id:
            sql += ' AND ii.inventory__install_id = %s '
            vals.append(inventory__install_id)

        # Check inventory name
        if inventory_id:
            sqlVals = _checkWildcardAndAppend('ii.inventory_id', inventory_id, sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]

        # Check install name
        if install_id:
            sqlVals = _checkWildcardAndAppend('ii.install_id', install_id, sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]

        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
            return res

        except Exception as e:
            self.logger.info('Error when fetching installed devices:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching installed devices:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveInventoryToInstall(self, install_id, inventory_id):
        '''
        Link a device as installed once it is installed into field

        :param install_id: id of the install entity
        :type install_id: int

        :param inventory_id: id of the inventory
        :type inventory_id: int

        :return: id of a map entry

        :Raises: MySQLError
        '''

        # Generate SQL
        sql = '''
        INSERT INTO inventory__install (install_id, inventory_id)
        VALUES (%s, %s)
        '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (install_id, inventory_id))

            # Get last id
            lastid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return lastid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving inventory to install:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving inventory to install:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveRotCoilData(self, inventory_id):
        '''
        Return rotation coil data

        :param inventory_id: id of the device in the inventory
        :type inventory_id: int

        :return: a tuple with a structure like:

            .. code-block:: python

                (
                    (
                        rot_coil_data_id,
                        inventory_id,
                        alias,
                        meas_coil_id,
                        ref_radius,
                        magnet_notes,
                        login_name,
                        cond_curr,
                        meas_loc,
                        run_number,
                        sub_device,
                        current_1,
                        current_2,
                        current_3,
                        up_dn_1,
                        up_dn_2,
                        up_dn_3,
                        analysis_number,
                        integral_xfer_function,
                        orig_offset_x,
                        orig_offset_y,
                        B_ref_int,
                        Roll_angle,
                        meas_notes,
                        meas_date,
                        author,
                        a1,
                        a2,
                        a3,
                        b1,
                        b2,
                        b3,
                        a4_21,
                        b4_21,
                        data_issues,
                        data_usage,
                        name
                    ),
                    ...
                )

        :Raises: MySQLError
        '''

        # Generate SQL
        sql = '''
        SELECT
            rcd.rot_coil_data_id,
            rcd.inventory_id,
            rcd.alias,
            rcd.meas_coil_id,
            rcd.ref_radius,
            rcd.magnet_notes,
            rcd.login_name,
            rcd.cond_curr,
            rcd.meas_loc,
            rcd.run_number,
            rcd.sub_device,
            rcd.current_1,
            rcd.current_2,
            rcd.current_3,
            rcd.up_dn_1,
            rcd.up_dn_2,
            rcd.up_dn_3,
            rcd.analysis_number,
            rcd.integral_xfer_function,
            rcd.orig_offset_x,
            rcd.orig_offset_y,
            rcd.B_ref_int,
            rcd.Roll_angle,
            rcd.meas_notes,
            rcd.meas_date,
            rcd.author,
            rcd.a1,
            rcd.a2,
            rcd.a3,
            rcd.b1,
            rcd.b2,
            rcd.b3,
            rcd.a4_21,
            rcd.b4_21,
            rcd.data_issues,
            rcd.data_usage,
            inv.name
        FROM rot_coil_data rcd
        LEFT JOIN inventory inv ON (rcd.inventory_id = inv.inventory_id)
        WHERE
        '''

        vals = []

        # Check primary key
        sql += ' rcd.inventory_id = %s '
        vals.append(inventory_id)

        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
            return res

        except Exception as e:
            self.logger.info('Error when fetching rot coil data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching rot coil data:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveRotCoilData(
            self, inventory_id, alias=None, meas_coil_id=None, ref_radius=None, magnet_notes=None, login_name=None, cond_curr=None,
            meas_loc=None, run_number=None, sub_device=None, current_1=None, current_2=None, current_3=None, up_dn_1=None, up_dn_2=None, up_dn_3=None,
            analysis_number=None, integral_xfer_function=None, orig_offset_x=None, orig_offset_y=None, b_ref_int=None, roll_angle=None,
            meas_notes=None, author=None, a1=None, a2=None, a3=None, b1=None, b2=None, b3=None, a4_21=None, b4_21=None, data_issues=None, data_usage=None):
        '''
        Save rotation coil data

        :param inventory_id:
        :type inventory_id: int

        :param alias:
        :type alias: str

        :param meas_coil_id:
        :type meas_coil_id: str

        :param ref_radius:
        :type ref_radius: double

        :param magnet_notes:
        :type magnet_notes: str

        :param login_name:
        :type login_name: str

        :param cond_curr:
        :type cond_curr: double

        :param meas_loc:
        :type meas_loc: str

        :param run_number:
        :type run_number: str

        :param sub_device:
        :type sub_device: str

        :param current_1:
        :type current_1: double

        :param current_2:
        :type current_2: double

        :param current_3:
        :type current_3: double

        :param up_dn_1:
        :type up_dn_1: str

        :param up_dn_2:
        :type up_dn_2: str

        :param up_dn_3:
        :type up_dn_3: str

        :param analysis_number:
        :type analysis_number: str

        :param integral_xfer_function:
        :type integral_xfer_function: double

        :param orig_offset_x:
        :type orig_offset_x: double

        :param orig_offset_y:
        :type orig_offset_y: double

        :param b_ref_int:
        :type b_ref_int: double

        :param roll_angle:
        :type roll_angle: double

        :param meas_notes:
        :type meas_notes: str

        :param author:
        :type author: str

        :param a1:
        :type a1: double

        :param a2:
        :type a2: double

        :param a3:
        :type a3: double

        :param b1:
        :type b1: double

        :param b2:
        :type b2: double

        :param b3:
        :type b3: double

        :param a4_21:
        :type a4_21: str

        :param b4_21:
        :type b4_21: str

        :param data_issues:
        :type data_issues: str

        :param data_usage:
        :type data_usage: int

        :return: new rot coil data id

        :raise: MySQLError
        '''

        # Generate SQL
        sql = '''
        INSERT INTO rot_coil_data
            (inventory_id, alias, meas_coil_id, ref_radius, magnet_notes, login_name, cond_curr,
            meas_loc, run_number, sub_device, current_1, current_2, current_3, up_dn_1, up_dn_2, up_dn_3,
            analysis_number, integral_xfer_function, orig_offset_x, orig_offset_y, B_ref_int, Roll_angle,
            meas_notes, meas_date, author, a1, a2, a3, b1, b2, b3, a4_21, b4_21, data_issues, data_usage)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (
                inventory_id, alias, meas_coil_id, ref_radius, magnet_notes, login_name, cond_curr,
                meas_loc, run_number, sub_device, current_1, current_2, current_3, up_dn_1, up_dn_2, up_dn_3,
                analysis_number, integral_xfer_function, orig_offset_x, orig_offset_y, b_ref_int, roll_angle,
                meas_notes, author, a1, a2, a3, b1, b2, b3, a4_21, b4_21, data_issues, data_usage
            ))

            # Get last row id
            rotid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return rotid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving rot coil data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving rot coil data:\n%s (%d)' % (e.args[1], e.args[0]))

    def updateRotCoilData(
            self, rot_coil_data_id, inventory_id=None, alias=None, meas_coil_id=None, ref_radius=None, magnet_notes=None, login_name=None, cond_curr=None,
            meas_loc=None, run_number=None, sub_device=None, current_1=None, current_2=None, current_3=None, up_dn_1=None, up_dn_2=None, up_dn_3=None,
            analysis_number=None, integral_xfer_function=None, orig_offset_x=None, orig_offset_y=None, b_ref_int=None, roll_angle=None,
            meas_notes=None, author=None, a1=None, a2=None, a3=None, b1=None, b2=None, b3=None, a4_21=None, b4_21=None, data_issues=None, data_usage=None):
        '''
        Update rotation coil data

        :param rot_coil_data_id:
        :type rot_coil_data_id:

        :param inventory_id:
        :type inventory_id:

        :param alias:
        :type alias:

        :param meas_coil_id:
        :type meas_coil_id:

        :param ref_radius:
        :type ref_radius:

        :param magnet_notes:
        :type magnet_notes:

        :param login_name:
        :type login_name:

        :param cond_curr:
        :type cond_curr:

        :param meas_loc:
        :type meas_loc:

        :param run_number:
        :type run_number:

        :param sub_device:
        :type sub_device:

        :param current_1:
        :type current_1:

        :param current_2:
        :type current_2:

        :param current_3:
        :type current_3:

        :param up_dn_1:
        :type up_dn_1:

        :param up_dn_2:
        :type up_dn_2:

        :param up_dn_3:
        :type up_dn_3:

        :param analysis_number:
        :type analysis_number:

        :param integral_xfer_function:
        :type integral_xfer_function:

        :param orig_offset_x:
        :type orig_offset_x:

        :param orig_offset_y:
        :type orig_offset_y:

        :param b_ref_int:
        :type b_ref_int:

        :param roll_angle:
        :type roll_angle:

        :param meas_notes:
        :type meas_notes:

        :param author:
        :type author:

        :param a1:
        :type a1:

        :param a2:
        :type a2:

        :param a3:
        :type a3:

        :param b1:
        :type b1:

        :param b2:
        :type b2:

        :param b3:
        :type b3:

        :param a4_21:
        :type a4_21:

        :param b4_21:
        :type b4_21:

        :param data_issues:
        :type data_issues:

        :param data_usage:
        :type data_usage:

        :return: True if everything was ok

        :raise: MySQLError
        '''

        # Define query dict
        queryDict = {}
        whereDict = {}

        # Set inventory
        whereDict['rot_coil_data_id'] = rot_coil_data_id

        # Set parameters
        if inventory_id:
            queryDict['inventory_id'] = inventory_id

        if alias:
            queryDict['alias'] = alias

        if meas_coil_id:
            queryDict['meas_coil_id'] = meas_coil_id

        if ref_radius:
            queryDict['ref_radius'] = ref_radius

        if magnet_notes:
            queryDict['magnet_notes'] = magnet_notes

        if login_name:
            queryDict['login_name'] = login_name

        if cond_curr:
            queryDict['cond_curr'] = cond_curr

        if meas_loc:
            queryDict['meas_loc'] = meas_loc

        if run_number:
            queryDict['run_number'] = run_number

        if sub_device:
            queryDict['sub_device'] = sub_device

        if current_1:
            queryDict['current_1'] = current_1

        if current_2:
            queryDict['current_2'] = current_2

        if current_3:
            queryDict['current_3'] = current_3

        if up_dn_1:
            queryDict['up_dn_1'] = up_dn_1

        if up_dn_2:
            queryDict['up_dn_2'] = up_dn_2

        if up_dn_3:
            queryDict['up_dn_3'] = up_dn_3

        if analysis_number:
            queryDict['analysis_number'] = analysis_number

        if integral_xfer_function:
            queryDict['integral_xfer_function'] = integral_xfer_function

        if orig_offset_x:
            queryDict['orig_offset_x'] = orig_offset_x

        if orig_offset_y:
            queryDict['orig_offset_y'] = orig_offset_y

        if b_ref_int:
            queryDict['b_ref_int'] = b_ref_int

        if roll_angle:
            queryDict['roll_angle'] = roll_angle

        if meas_notes:
            queryDict['meas_notes'] = meas_notes

        queryDict['meas_date'] = 'now'

        if author:
            queryDict['author'] = author

        if a1:
            queryDict['a1'] = a1

        if a2:
            queryDict['a2'] = a2

        if a3:
            queryDict['a3'] = a3

        if b1:
            queryDict['b1'] = b1

        if b2:
            queryDict['b2'] = b2

        if b3:
            queryDict['b3'] = b3

        if a4_21:
            queryDict['a4_21'] = a4_21

        if b4_21:
            queryDict['b4_21'] = b4_21

        if data_issues:
            queryDict['data_issues'] = data_issues

        if data_usage:
            queryDict['data_usage'] = data_usage

        # Generate SQL
        sqlVals = _generateUpdateQuery('rot_coil_data', queryDict, None, None, whereDict)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating rot coil data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating rot coil data:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveHallProbeData(self, inventory_id):
        '''
        Return hall probe data

        :param inventory_id: id of the device in the inventory
        :type inventory_id: int

        :return: a tuple with a structure like:

            .. code-block:: python

                (
                    (
                        hall_probe_id,
                        inventory_id,
                        alias,
                        meas_date,
                        measured_at_location,
                        sub_device,
                        run_identifier,
                        login_name,
                        conditioning_current,
                        current_1,
                        current_2,
                        current_3,
                        up_dn1,
                        up_dn2,
                        up_dn3,
                        mag_volt_1,
                        mag_volt_2,
                        mag_volt_3,
                        x,
                        y,
                        z,
                        bx_t,
                        by_t,
                        bz_t,
                        meas_notes,
                        data_issues,
                        data_usage,
                        name
                    ),
                    ...
                )

        :Raises: MySQLError
        '''

        # Generate SQL
        sql = '''
        SELECT
            hpd.hall_probe_id,
            hpd.inventory_id,
            hpd.alias,
            hpd.meas_date,
            hpd.measured_at_location,
            hpd.sub_device,
            hpd.run_identifier,
            hpd.login_name,
            hpd.conditioning_current,
            hpd.current_1,
            hpd.current_2,
            hpd.current_3,
            hpd.up_dn1,
            hpd.up_dn2,
            hpd.up_dn3,
            hpd.mag_volt_1,
            hpd.mag_volt_2,
            hpd.mag_volt_3,
            hpd.x,
            hpd.y,
            hpd.z,
            hpd.bx_t,
            hpd.by_t,
            hpd.bz_t,
            hpd.meas_notes,
            hpd.data_issues,
            hpd.data_usage,
            inv.name
        FROM hall_probe_data hpd
        LEFT JOIN inventory inv ON (hpd.inventory_id = inv.inventory_id)
        WHERE
        '''

        vals = []

        # Check primary key
        sql += ' hpd.inventory_id = %s '
        vals.append(inventory_id)

        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
            return res

        except Exception as e:
            self.logger.info('Error when fetching hall probe data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching hall probe data:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveHallProbeData(
            self, inventory_id, sub_device, alias=None, measured_at_location=None,
            run_identifier=None, login_name=None, conditioning_current=None, current_1=None, current_2=None,
            current_3=None, up_dn1=None, up_dn2=None, up_dn3=None, mag_volt_1=None, mag_volt_2=None, mag_volt_3=None,
            x=None, y=None, z=None, bx_t=None, by_t=None, bz_t=None, meas_notes=None, data_issues=None, data_usage=None):
        '''
        Save hall probe data

        :param inventory_id: id of the device in the inventory
        :type inventory_id: int

        :param alias:
        :type alias: str

        :param sub_device:
        :type sub_device: str

        :param measured_at_location:
        :type measured_at_location: str

        :param run_identifier:
        :type run_identifier: str

        :param login_name:
        :type login_name: str

        :param conditioning_current:
        :type conditioning_current: double

        :param current_1:
        :type current_1: double

        :param current_2:
        :type current_2: double

        :param current_3:
        :type current_3: double

        :param up_dn1:
        :type up_dn1: str

        :param up_dn2:
        :type up_dn2: str

        :param up_dn3:
        :type up_dn3: str

        :param mag_volt_1:
        :type mag_volt_1: double

        :param mag_volt_2:
        :type mag_volt_2: double

        :param mag_volt_3:
        :type mag_volt_3: double

        :param x:
        :type x: double

        :param y:
        :type y: double

        :param z:
        :type z: double

        :param bx_t:
        :type bx_t: double

        :param by_t:
        :type by_t: double

        :param bz_t:
        :type bz_t: double

        :param meas_notes:
        :type meas_notes: str

        :param data_issues:
        :type data_issues: str

        :param data_usage:
        :type data_usage: int

        :return: new rot coil data id

        :raise: MySQLError
        '''

        # Generate SQL
        sql = '''
        INSERT INTO hall_probe_data(
            inventory_id, alias, meas_date, measured_at_location, sub_device,
            run_identifier, login_name, conditioning_current, current_1, current_2,
            current_3, up_dn1, up_dn2, up_dn3, mag_volt_1, mag_volt_2, mag_volt_3,
            x, y, z, bx_t, by_t, bz_t, meas_notes, data_issues, data_usage
            )
        VALUES
            (%s, %s, NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (
                inventory_id, alias, measured_at_location, sub_device,
                run_identifier, login_name, conditioning_current, current_1, current_2,
                current_3, up_dn1, up_dn2, up_dn3, mag_volt_1, mag_volt_2, mag_volt_3,
                x, y, z, bx_t, by_t, bz_t, meas_notes, data_issues, data_usage
            ))

            # Get last row id
            halid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return halid

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving hall probe data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving hall probe data:\n%s (%d)' % (e.args[1], e.args[0]))

    def updateHallProbeData(
            self, hall_probe_id, inventory_id=None, sub_device=None, alias=None, measured_at_location=None,
            run_identifier=None, login_name=None, conditioning_current=None, current_1=None, current_2=None,
            current_3=None, up_dn1=None, up_dn2=None, up_dn3=None, mag_volt_1=None, mag_volt_2=None, mag_volt_3=None,
            x=None, y=None, z=None, bx_t=None, by_t=None, bz_t=None, meas_notes=None, data_issues=None, data_usage=None):
        '''
        Update hall probe data

        :param hall_probe_id: id hall probe
        :type hall_probe_id: int

        :param inventory_id: id of the device in the inventory
        :type inventory_id: int

        :param alias:
        :type alias: str

        :param sub_device:
        :type sub_device: str

        :param measured_at_location:
        :type measured_at_location: str

        :param run_identifier:
        :type run_identifier: str

        :param login_name:
        :type login_name: str

        :param conditioning_current:
        :type conditioning_current: double

        :param current_1:
        :type current_1: double

        :param current_2:
        :type current_2: double

        :param current_3:
        :type current_3: double

        :param up_dn1:
        :type up_dn1: str

        :param up_dn2:
        :type up_dn2: str

        :param up_dn3:
        :type up_dn3: str

        :param mag_volt_1:
        :type mag_volt_1: double

        :param mag_volt_2:
        :type mag_volt_2: double

        :param mag_volt_3:
        :type mag_volt_3: double

        :param x:
        :type x: double

        :param y:
        :type y: double

        :param z:
        :type z: double

        :param bx_t:
        :type bx_t: double

        :param by_t:
        :type by_t: double

        :param bz_t:
        :type bz_t: double

        :param meas_notes:
        :type meas_notes: str

        :param data_issues:
        :type data_issues: str

        :param data_usage:
        :type data_usage: int

        :return: True if everything was ok

        :raise: MySQLError
        '''

        # Define query dict
        queryDict = {}
        whereDict = {}

        # Set id
        whereDict['hall_probe_id'] = hall_probe_id

        # Set parameters
        if inventory_id:
            queryDict['inventory_id'] = inventory_id

        if sub_device:
            queryDict['sub_device'] = sub_device

        if alias:
            queryDict['alias'] = alias

        if measured_at_location:
            queryDict['measured_at_location'] = measured_at_location

        if run_identifier:
            queryDict['run_identifier'] = run_identifier

        if login_name:
            queryDict['login_name'] = login_name

        if conditioning_current:
            queryDict['conditioning_current'] = conditioning_current

        if current_1:
            queryDict['current_1'] = current_1

        if current_2:
            queryDict['current_2'] = current_2

        if current_3:
            queryDict['current_3'] = current_3

        if up_dn1:
            queryDict['up_dn1'] = up_dn1

        if up_dn2:
            queryDict['up_dn2'] = up_dn2

        if up_dn3:
            queryDict['up_dn3'] = up_dn3

        if mag_volt_1:
            queryDict['mag_volt_1'] = mag_volt_1

        if mag_volt_2:
            queryDict['mag_volt_2'] = mag_volt_2

        if mag_volt_3:
            queryDict['mag_volt_3'] = mag_volt_3

        if x:
            queryDict['x'] = x

        if y:
            queryDict['y'] = y

        if z:
            queryDict['z'] = z

        if bx_t:
            queryDict['bx_t'] = bx_t

        if by_t:
            queryDict['by_t'] = by_t

        if bz_t:
            queryDict['bz_t'] = bz_t

        if meas_notes:
            queryDict['meas_notes'] = meas_notes

        if data_issues:
            queryDict['data_issues'] = data_issues

        if data_usage:
            queryDict['data_usage'] = data_usage

        # Generate SQL
        sqlVals = _generateUpdateQuery('hall_probe_data', queryDict, None, None, whereDict)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating hall probe data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating hall probe data:\n%s (%d)' % (e.args[1], e.args[0]))
