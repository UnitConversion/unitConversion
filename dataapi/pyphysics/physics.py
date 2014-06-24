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
