'''
Created on Jun 4, 2014

@author dejan.dezman@cosylab.com
'''

import MySQLdb
import os
import base64
import time

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

            raise MySQLError('Error when saving vendor:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveComponentTypePropertyType(self, name, description=None):
        '''
        Retrieve component type property type by its name

        :param name: property type name
        :type name: str

        :param description: property type description
        :type description: str

        :return: a tuple::

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
            raise MySQLError('Error when fetching component type property type:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveComponentTypePropertyType(self, name, description=None):
        '''
        Insert new component type property type into database

        - name: name of the component type property type M
        - description: description of the component type property type O

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