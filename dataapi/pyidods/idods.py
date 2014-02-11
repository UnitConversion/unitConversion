import logging
import MySQLdb

from utils import (_wildcardformat)
from _mysql_exceptions import MySQLError

try:
    from django.utils import simplejson as json
except ImportError:
    import json

__all__ = []
__version__ = [1, 0, 0]

class idods(object):
    '''
    Data API for insertion device online data storage.

    All data have to be either all saved, or none is saved.
    '''
    def __init__(self, conn, transaction=None):
        '''initialize idods class.

        :param conn: MySQL connection object
        :type conn: object

        :param transaction: Django MySQL transaction object. If this is set, it uses Django's transaction manager to manage each transaction.
        :type transaction: object

        :returns:  idods -- class object

        '''
        self.logger = logging.getLogger('idods')
        hdlr = logging.FileHandler('/var/tmp/idods.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.DEBUG)

        self.conn = conn

        # Use django transaction manager
        self.transaction = transaction

    def _checkRangeAndAppend(self, parameterKey, parameterValue, sqlString, valsList, prependedOperator = None):
        '''
        Check for ranges in a parameter value and append appropriate sql
        
        parameters:
            - parameterKey: name of the parameter in the DB table
            - parameterValue: value of this parameter, it can be a tuple
            - sqlString: existing sql string that was generated outside of this function
            - valsList: list of formated values that should be inserted into sql statement
            - prepandedOperator: sql operator that will be prepended before the new condition
            
        return:
            tuple of new sql string and new list of values
        '''
        
        # Prepend operator if it exists
        if prependedOperator != None:
            sqlString += " " + prependedOperator + " "
        
        # Check if value equals tuple
        if isinstance(parameterValue, (list, tuple)):
                
            # Check tuple length. It should be 2.
            if len(parameterValue) != 2:
                raise ValueError("Range tuple for attribute %s should contain two values!" % parameterKey)
            
            # If everything is ok, append conditions to sql statement
            else:
                sqlString += ' ' + parameterKey + ' IS NOT NULL AND ' + parameterKey + ' >= %s AND ' + parameterKey + ' <= %s '
                valsList.append(parameterValue[0])
                valsList.append(parameterValue[1])
        
        # There is not tuple so just append equals
        else:
            sqlString += ' ' + parameterKey + ' = %s'
            valsList.append(parameterValue)
            
        return (sqlString, valsList)

    def _checkWildcardAndAppend(self, parameterKey, parameterValue, sqlString, valsList, prependedOperator = None):
        '''
        Check for wildcard characters in a parameter value and append appropriate sql
        
        parameters:
            - parameterKey: name of the parameter in the DB table
            - parameterValue: value of this parameter
            - sqlString: existing sql string that was generated outside of this function
            - valsList: list of formated values that should be inserted into sql statement
            - prepandedOperator: sql operator that will be prepended before the new condition
            
        return:
            tuple of new sql string and new list of values
        '''
        
        # Prepend operator if it exists
        if prependedOperator != None:
            sqlString += " " + prependedOperator + " "
            
        # Do not check for wildcard parameters if we have a number
        if isinstance(parameterValue, (int, float, long, complex)):
            sqlString += " " + parameterKey + " = %s "
            valsList.append(parameterValue)
            return (sqlString, valsList)
        
        # Check if user wants all objects
        if parameterValue == "*":
            sqlString += " 1=1 "
        
        # Check for wildcard characters
        elif "*" in parameterValue or "?" in parameterValue:
            sqlString += " " + parameterKey + " like %s "
            valsList.append(_wildcardformat(parameterValue))
            
        # All of the other options
        else:
            sqlString += " " + parameterKey + " = %s "
            valsList.append(parameterValue)
            
        return (sqlString, valsList)
    
    def _checkParameter(self, parameterKey, paramaterValue, parameterTypeWeAreCheckingFor = "string"):
        '''
        Check different types of input parameters. Parameter should match agreed criteria or exception will be thrown
        
        parameters:
            - parameterKey: name of the parameter
            - parameterValue: value of the parameter
            - parameterTypeWeAreCheckingFor: which type are we chacking
                * string: if we are checking string value
                * prim: if we are checking primary key value
            
        raise:
            ValueError if parameter don'r match agreed criteria
        '''
        
        # Check string
        if parameterTypeWeAreCheckingFor == "string":
            
            if not isinstance(paramaterValue, (str, unicode)):
                raise ValueError("Parameter %s is missing!" % parameterKey)
            
        # Check primary key
        elif parameterTypeWeAreCheckingFor == "prim":
            
            try:
                paramaterValue = int(paramaterValue)
                
            except ValueError as e:
                raise ValueError("Parameter %s cannot be None. %s." % (parameterKey, e.args[0]))

    def _generateUpdateQuery(self, tableName, queryDict, whereKey, whereValue, whereDict = None):
        '''
        Check number of parameters that are set and generate update SQL
        
        params:
            - tableName: name of the table we are updating
            - queryDict: dictionary where every key is an attribute name and every value new attribute value
            - whereKey: attribute by which we are updating
            - whereValue: attribute value by which we are updating
            - whereDict: dictionary of where keys and values
        
        raises:
            ValueError if no attributes are set
        '''
        
        # Create value list
        vals = []
        
        # Check the number of attributes that are set
        if len(queryDict) < 1:
            raise ValueError("At least one attribute has to be set to a new value!")
        
        # Generate SQL
        sql = 'UPDATE ' + tableName + ' SET '
        sqlList = []
        
        # Go through parameters
        for attr in queryDict.keys():
            value = queryDict[attr]
            sqlList.append(' ' + attr + ' = %s ')
            vals.append(value)
        
        sql += ','.join(sqlList)
        
        if whereDict == None:
            # Append where condition
            sql += ' WHERE ' + whereKey + ' = %s '
            vals.append(whereValue)
            
        else:
            sql += ' WHERE '
            sqlList = []
            
            # Go through where keys
            for whereKey in whereDict.keys():
                whereValue = whereDict[whereKey]
                sqlList.append(' ' + whereKey + ' = %s ')
                vals.append(whereValue)
                
            sql += " AND ".join(sqlList)
        
        return (sql, vals)

    def retrieveVendor(self, name, description=None):
        '''
        Retrieve vendor by its name and description
        Wildcast matching are supported for both name and description.

        :param name: vendor name
        :type name: str
        
        :param description: description for a vendor
        :type description: str
        
        :return: a map with structure like:

            .. code-block:: python

                {'id': {
                    'id': ,
                    'name': ,
                    'description': 
                    }
                 ...
                }

        :Raises: ValueError, exception
        '''

        # Check for vendor name parameter
        self._checkParameter('name', name)

        # Generate SQL statement
        vals = []
        sql = '''
        SELECT vendor_id, vendor_name, vendor_description FROM vendor WHERE
        '''

        # Append name
        sqlVals = self._checkWildcardAndAppend('vendor_name', name, sql, vals)

        # Append description
        if description != None:
            sqlVals = self._checkWildcardAndAppend('vendor_description', description, sqlVals[0], sqlVals[1], 'AND')

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Get any one since it should be unique
            res = cur.fetchall()
            resdict = {}

            # Generate return dictionary
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'name': r[1],
                    'description': r[2]
                }

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching vendor:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching vendor:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveVendor(self, name, description = None):
        '''Save vendor and its description into database

        :param name: vendor name
        :type name: str
        
        :param dtype: device type

        :param description: a brief description which could have up to 255 characters
        :type description: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': vendor_id}

        :Raises: ValueError, MySQLError
        '''
        
        # Check for vendor name parameter
        self._checkParameter('name', name)

        # Try to retrieve vendor by its name
        existingVendor = self.retrieveVendor(name, description=description)

        if len(existingVendor):
            raise ValueError("Vendor (%s) already exists in the database!" % name);

        # Generate SQL statement
        if description != None:
            sql = '''
            INSERT INTO vendor (vendor_name, vendor_description) VALUES (%s, %s)
            '''
            vals=[name, description]
        
        else:
            sql = '''
            INSERT INTO vendor (vendor_name) VALUES (%s)
            '''
            vals=[name]

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sql, vals)

            # Get last row id
            vendorid = cur.lastrowid

            # Create transaction
            if self.transaction == None:
                self.conn.commit()

            return {'id': vendorid}

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving vendor:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving vendor:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateVendor(self, vendor_id, old_name, name, **kws):
        '''Update vendor and its description

        :param vendor_id: vendor id needed for updating
        :type vendor_id: id

        :param name: vendor name
        :type name: str

        :param old_name: update vendor by its old name
        :type old_name: str

        :param description: a brief description which could have up to 255 characters
        :type description: str

        :return: True or MySQLError

        :Raises: ValueError, MySQLError
        '''
        
        # Set properties
        queryDict = {}
        whereKey = None
        whereValue = None
        
        # Check id
        if vendor_id:
            self._checkParameter('id', vendor_id, 'prim')
            whereKey = 'vendor_id'
            whereValue = vendor_id
            
        # Check old name
        if old_name:
            self._checkParameter('name', old_name)
            whereKey = 'vendor_name'
            whereValue = old_name
            
        # Check where condition
        if whereKey == None:
            raise ValueError("Vendor id or old vendor name should be present to execute an update!")
        
        # Check for vendor name parameter
        self._checkParameter('name', name)
        queryDict['vendor_name'] = name

        
        # Append description
        if 'description' in kws:
            queryDict['vendor_description'] = kws['description']

        # Generate SQL
        sqlVals = self._generateUpdateQuery('vendor', queryDict, whereKey, whereValue)

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction == None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when updating vendor:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating vendor:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveInventoryPropertyTemplate(self, name):
        '''
        Retrieve inventory property template by its name

        - name: Inventory property name

        :return: a map with structure like:

            .. code-block:: python

                {
                    'id': {
                        'id': ,              # int
                        'cmpnttype': ,      # int
                        'name': ,           # string
                        'description': ,    # string
                        'default': ,        # string
                        'unit':             # string
                    }
                }

        :Raises: ValueError, MySQLError
        '''

        # Check name
        self._checkParameter("name", name)

        # Construct SQL
        sql = '''
        SELECT
            tmp.inventory_prop_tmplt_id, cmpnt.cmpnt_type_name,
            tmp.inventory_prop_tmplt_name, tmp.inventory_prop_tmplt_desc,
            tmp.inventory_prop_tmplt_default, tmp.inventory_prop_tmplt_units
        FROM inventory_prop_tmplt tmp
        LEFT JOIN cmpnt_type cmpnt ON tmp.cmpnt_type_id = cmpnt.cmpnt_type_id
        WHERE
        '''
        vals = []
        
        # Append name
        sqlAndVals = self._checkWildcardAndAppend("inventory_prop_tmplt_name", name, sql, vals)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlAndVals[0], sqlAndVals[1])

            # get any one since it should be unique
            res = cur.fetchall()
            resdict = {}

            # Construct return dict
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'cmpnttype': r[1],
                    'name': r[2],
                    'description': r[3],
                    'default': r[4],
                    'unit': r[5]
                }
            
            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching inventory property template:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching inventory property template:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveInventoryPropertyTemplate(self, cmpnt_type, name, description = None, default = None, unit = None):
        '''
        Insert new inventory property template into database

        - cmpnt_type: component type name M
        - name: property template name M
        - description: property template description O
        - default: property template default value O
        - unit: property template unit O

        :return: a map with structure like:

            .. code-block:: python

                {'id': propertytemplateid}

        :Raises: ValueError, MySQLError
        '''

        # Raise an error if inventory property template exists
        existingInventoryPropertyTemplate = self.retrieveInventoryPropertyTemplate(name)
        
        if len(existingInventoryPropertyTemplate):
            raise ValueError("Inventory property template (%s) already exists in the database!" % name)

        # Check component type
        result = self.retrieveComponentType(cmpnt_type);

        if len(result) == 0:
            raise ValueError("Component type (%s) does not exist in the database." % (cmpnt_type))

        cmpnttypeid = result.keys()[0]

        # Check name
        self._checkParameter("name", name)

        # Generate SQL
        sql = '''
        INSERT INTO inventory_prop_tmplt
        (cmpnt_type_id, inventory_prop_tmplt_name, inventory_prop_tmplt_desc, inventory_prop_tmplt_default, inventory_prop_tmplt_units)
        VALUES
        (%s, %s, %s, %s, %s)
        '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (cmpnttypeid, name, description, default, unit))

            # Get last row id
            templateid = cur.lastrowid

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': templateid}

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving new inventory property template:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving new inventory property template:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateInventoryPropertyTemplate(self, tmplt_id, cmpnt_type, name, **kws):
        '''
        Update inventory property template in a database

        - tmplt_id: property template id M
        - cmpnt_type: component type name M
        - name: property template name M
        - description: property template description O
        - default: property template default value O
        - unit: property template unit O

        :return: True if update succeeded

        :Raises: ValueError, MySQLError
        '''

        # Set query dict
        queryDict = {}
        whereKey = 'inventory_prop_tmplt_id'

        self.logger.info(tmplt_id)

        # Check id
        self._checkParameter('id', tmplt_id, 'prim')
        whereValue = tmplt_id

        # Check component type
        result = self.retrieveComponentType(cmpnt_type);

        if len(result) == 0:
            raise ValueError("Component type (%s) does not exist in the database." % (cmpnt_type))

        cmpnttypeid = result.keys()[0]
        queryDict['cmpnt_type_id'] = cmpnttypeid

        # Check name
        self._checkParameter("name", name)
        queryDict['inventory_prop_tmplt_name'] = name

        # Check description parameter
        if 'description' in kws:
            queryDict['inventory_prop_tmplt_desc'] = kws['description']

        # Check default parameter
        if 'default' in kws:
            queryDict['inventory_prop_tmplt_default'] = kws['default']

        # Check unit parameter
        if 'unit' in kws:
            queryDict['inventory_prop_tmplt_units'] = kws['unit']

        # Generate SQL
        sqlVals = self._generateUpdateQuery('inventory_prop_tmplt', queryDict, whereKey, whereValue)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when updating inventory property template:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating inventory property template:\n%s (%d)' %(e.args[1], e.args[0]))

    def _retrieveInventoryProperty(self, inventoryId, inventoryPropertyTemplateId = None, value = None):
        '''
        Retrieve id and value from inventory property table
        
        parameters:
            - inventoryId: id of the inventory entry
            - inventoryPropertyTemplateId: id of the inventory property template
            - value: value of the property template
            
        returns:
            { 'id': {
                    'id': #int,
                    'value': #string,
                    'inventoryname': #string,
                    'templatename': #string
                }
            }
            
        raises:
            ValueError, MySQLError
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
        vals = [inventoryId]

        # Add inventory_prop_tmplt_id parameter
        if inventoryPropertyTemplateId:
            sql += ' AND ip.inventory_prop_tmplt_id = %s '
            vals.append(inventoryPropertyTemplateId)
        
        sqlVals = (sql, vals)

        # Add value parameter if exists
        if value:
            sqlVals = self._checkWildcardAndAppend('inventory_prop_value', value, sqlVals[0], sqlVals[1], 'AND')

        try:
            # Retrieve objects from the database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            res = cur.fetchall()
            resdict = {}
            
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'value': r[1],
                    'inventoryname': r[5],
                    'templatename': r[4]
                }
                
            return resdict
            
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieve id and vale from inventory property table:\n%s (%s)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when retrieve id and vale from inventory property table:\n%s (%s)' %(e.args[1], e.args[0]))

    def retrieveInventoryProperty(self, inventoryName, inventoryPropertyTemplateName = None, value = None):
        '''
        Retrieve id and value from inventory property table
        
        parameters:
            - inventoryName: name of the inventory entry
            - inventoryPropertyTemplateName: name of the inventory property template
            - value: value of the property template
            
        returns:
            { 'id': {
                    'id': #int,
                    'value': #string,
                    'inventoryname': #string,
                    'templatename': #string
                }
            }
            
        '''
        
        # Check inventory
        retrieveInventory = self.retrieveInventory(inventoryName)
        
        if len(retrieveInventory) == 0:
            raise ValueError("Inventory (%s) doesn't exist in the database!" % inventoryName)

        retrieveInventoryKeys = retrieveInventory.keys()
        inventoryId = retrieveInventory[retrieveInventoryKeys[0]]['id']

        # Check inventory property template
        # of a specific inventory
        
        inventoryPropertyTemplateId = None
        
        if inventoryPropertyTemplateName:
            retrieveInventoryPropertyTemplate = self.retrieveInventoryPropertyTemplate(inventoryPropertyTemplateName)
            
            if len(retrieveInventoryPropertyTemplate) == 0:
                raise ValueError("Inventory property template (%s) doesn't exist in the database!" % inventoryPropertyTemplateName);
    
            retrieveInventoryPropertyTemplateKeys = retrieveInventoryPropertyTemplate.keys()
            inventoryPropertyTemplateId = retrieveInventoryPropertyTemplate[retrieveInventoryPropertyTemplateKeys[0]]['id']

        return self._retrieveInventoryProperty(inventoryId, inventoryPropertyTemplateId, value)

    def saveInventoryProperty(self, inventoryName, inventoryPropertyTemplateName, value):
        '''
        Save inventory property into database
        
        params:
            - inventoryName: name of the inventory we are saving property for
            - inventoryPropertyTemplateName: name of the property template/inventory property key name
            - value: value of the property template/property key name
            
        returns:
            {'id': new inventory property id}
            
        raises:
            ValueError, MySQLError
        '''
        
        # Check for previous inventory property
        retrieveInventoryProperty = self.retrieveInventoryProperty(inventoryName, inventoryPropertyTemplateName)
        
        if len(retrieveInventoryProperty) != 0:
            raise ValueError("Inventory property for inventory (%s) and template (%s) already exists in the database!" % (inventoryName, inventoryPropertyTemplateName));
        
        # Check inventory
        retrieveInventory = self.retrieveInventory(inventoryName)
        
        if len(retrieveInventory) == 0:
            raise ValueError("Inventory (%s) doesn't exist in the database!" % inventoryName)

        retrieveInventoryKeys = retrieveInventory.keys()
        inventoryId = retrieveInventory[retrieveInventoryKeys[0]]['id']

        # Check inventory property template
        retrieveInventoryPropertyTemplate = self.retrieveInventoryPropertyTemplate(inventoryPropertyTemplateName)
        
        if len(retrieveInventoryPropertyTemplate) == 0:
            raise ValueError("Inventory property template (%s) doesn't exist in the database!" % inventoryPropertyTemplateName);

        retrieveInventoryPropertyTemplateKeys = retrieveInventoryPropertyTemplate.keys()
        inventoryPropertyTemplateId = retrieveInventoryPropertyTemplate[retrieveInventoryPropertyTemplateKeys[0]]['id']

        # Generate SQL
        sql = '''
        INSERT INTO inventory_prop
        (inventory_id, inventory_prop_tmplt_id, inventory_prop_value)
        VALUES
        (%s, %s, %s)
        '''
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (inventoryId, inventoryPropertyTemplateId, value))
            
            # Get last row id
            propid = cur.lastrowid

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': propid}
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when saving inventory property value:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving inventory property value:\n%s (%d)' % (e.args[1], e.args[0]))

    def updateInventoryProperty(self, oldInventoryName, oldInventoryPropertyTemplateName, value):
        '''
        Update inventory property in a database
        
        params:
            - oldInventoryName: name of the inventory we are saving property for
            - oldInventoryPropertyTemplateName: name of the property template/inventory property key name
            - value: value of the property template/property key name
            
        returns:
            True if everything is ok
            
        raises:
            ValueError, MySQLError
        '''
        
        # Define query dict
        queryDict = {}
        whereDict = {}
        
        # Check inventory
        retrieveInventory = self.retrieveInventory(oldInventoryName)
        
        if len(retrieveInventory) == 0:
            raise ValueError("Inventory (%s) doesn't exist in the database!" % oldInventoryName)

        retrieveInventoryKeys = retrieveInventory.keys()
        inventoryId = retrieveInventory[retrieveInventoryKeys[0]]['id']
        whereDict['inventory_id'] = inventoryId

        # Check inventory property template
        retrieveInventoryPropertyTemplate = self.retrieveInventoryPropertyTemplate(oldInventoryPropertyTemplateName)
        
        if len(retrieveInventoryPropertyTemplate) == 0:
            raise ValueError("Inventory property template (%s) doesn't exist in the database!" % oldInventoryPropertyTemplateName);

        retrieveInventoryPropertyTemplateKeys = retrieveInventoryPropertyTemplate.keys()
        inventoryPropertyTemplateId = retrieveInventoryPropertyTemplate[retrieveInventoryPropertyTemplateKeys[0]]['id']
        whereDict['inventory_prop_tmplt_id'] = inventoryPropertyTemplateId

        # Set value parameter
        queryDict['inventory_prop_value'] = value

        # Generate SQL
        sqlVals = self._generateUpdateQuery('inventory_prop', queryDict, None, None, whereDict)
        
        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return True
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when updating inventory property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating inventory property:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveInventory(self, name, **kws):
        '''
        save insertion device into inventory using any of the acceptable key words:

        - name:  name to identify that device from vendor
        - cmpnt_type: device type name
        - alias: alias name if it has
        - serialno: serial number
        - vendor: vendor name
        - props: properties with structure as below

        .. code-block:: python

            {
                'length': ,                    # float
                'up_corrector_position': ,     # float
                'middle_corrector_position': , # float
                'down_corrector_position':,    # float
                'gap_min': ,                   # float
                'gap_max': ,                   # float
                'gap_tolerance':,              # float
                'phase1_min':,                 # float
                'phase1_max':,                 # float
                'phase2_min':,                 # float
                'phase2_max':,                 # float
                'phase3_min':,                 # float
                'phase3_max':,                 # float
                'phase4_min':,                 # float
                'phase4_max':,                 # float
                'phase_tolerance':,            # float
                'k_max_linear':,               # float
                'k_max_circular':,             # float
                'phase_mode_p':,               # string
                'phase_mode_a1':,              # string
                'phase_mode_a2':               # string
            }

        :param name: insertion device name, which is usually different from its field name (the name after installation).
        :type name: str

        :param dtype: device type
        :type dtype: str

        :param alias: alias name if it has
        :type alias: str

        :param serialno: serial number
        :type serialno: str

        :param vendor: name of vendor
        :type vendor: str

        :param props: a map to describe the property of an insertion device as described above
        :type props: object

        :return: a map with structure like:

            .. code-block:: python

                {'id': inventory_id}

        :Raises: ValueError, MySQLError

        '''

        # Check name parameter
        res = self.retrieveInventory(name)
        
        if len(res) != 0:
            raise ValueError("Inventory (%s) already exists in inventory." % (name))

        # Check device type parameter
        compnttypeid=None

        if kws.has_key('cmpnt_type') and kws['cmpnt_type'] != None:
            
            # Check component type parameter
            self._checkParameter("component type", kws['cmpnt_type'])
            
            res = self.retrieveComponentType(kws['cmpnt_type'])
            reskeys = res.keys()

            if len(res) != 1:
                raise ValueError("Insertion device type (%s) does not exist."%(kws['dtype']))
            
            else:
                compnttypeid = res[reskeys[0]]['id']

        # Check alias parameter
        alias = None

        if kws.has_key('alias') and kws['alias'] != None:
            alias = kws['alias']

        # Check serial number parameter
        serialno = None

        if kws.has_key('serialno') and kws['serialno'] != None:
            serialno = kws['serialno']

        # Check vendor parameter
        vendor = None

        if kws.has_key('vendor') and kws['vendor'] != None:
            
            # Check parameter
            self._checkParameter("vendor name", kws['vendor'])
            
            res = self.retrieveVendor(kws['vendor'])

            if len(res) == 0:
                raise ValueError("Vendor with name (%s) doesn't exist." % kws['vendor'])
            
            resKeys = res.keys()
            vendor = res[resKeys[0]]['id']
            
        # Generate SQL
        sql = '''
        INSERT INTO inventory (cmpnt_type_id, vendor_id, name, alias, serial_no) VALUES
        (%s, %s, %s, %s, %s)
        '''
        
        try:
            # Insert inventory into database
            cur = self.conn.cursor()
            cur.execute(sql, (compnttypeid, vendor, name, alias, serialno))
            
            # Get last row id
            invid = cur.lastrowid

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            # Inventory is saved, now we can save properties into database
            if kws.has_key('props') and kws['props'] != None:
                props = kws['props']
                
                # Save all the properties
                for key in props:
                    value = props[key]
                    
                    # Save it into database
                    self.saveInventoryProperty(name, key, value)
                
            return {'id': invid}
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving new inventory:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving new inventory:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateInventory(self, inventory_id, old_name, name, **kws):
        '''
        Update inventory using any of the acceptable key words:

        - inventory_id:  inventory id from the database table
        - old_name:  name of the inventory we want to update by
        - name:  name to identify that device from vendor
        - cmpnt_type: device type name
        - alias: alias name if it has
        - serialno: serial number
        - vendor: vendor name
        - props: properties with structure as below

        .. code-block:: python

            {
                'length': ,                    # float
                'up_corrector_position': ,     # float
                'middle_corrector_position': , # float
                'down_corrector_position':,    # float
                'gap_min': ,                   # float
                'gap_max': ,                   # float
                'gap_tolerance':,              # float
                'phase1_min':,                 # float
                'phase1_max':,                 # float
                'phase2_min':,                 # float
                'phase2_max':,                 # float
                'phase3_min':,                 # float
                'phase3_max':,                 # float
                'phase4_min':,                 # float
                'phase4_max':,                 # float
                'phase_tolerance':,            # float
                'k_max_linear':,               # float
                'k_max_circular':,             # float
                'phase_mode_p':,               # string
                'phase_mode_a1':,              # string
                'phase_mode_a2':               # string
            }

        :param name: insertion device name, which is usually different from its field name (the name after installation).
        :type name: str

        :param dtype: device type
        :type dtype: str

        :param alias: alias name if it has
        :type alias: str

        :param serialno: serial number
        :type serialno: str

        :param vendor: name of vendor
        :type vendor: str

        :param props: a map to describe the property of an insertion device as described above
        :type props: object

        :return: True if everything is ok

        :Raises: ValueError, MySQLError

        '''

        # Set query dict
        queryDict = {}
        whereKey = None
        whereValue = None
        
        # Check id
        if inventory_id:
            self._checkParameter('id', inventory_id, 'prim')
            whereKey = 'inventory_id'
            whereValue = inventory_id
            
        # Check old name
        if old_name:
            self._checkParameter('name', old_name)
            whereKey = 'name'
            whereValue = old_name
        
        if whereKey == None:
            raise ValueError("Id or old name should be present to execute an update!")

        # Check name parameter
        self._checkParameter('name', name)
        queryDict['name'] = name

        # Check device type parameter
        if kws.has_key('cmpnt_type') and kws['cmpnt_type'] != None:
            
            # Check component type parameter
            self._checkParameter("component type", kws['cmpnt_type'])
            
            res = self.retrieveComponentType(kws['cmpnt_type'])
            reskeys = res.keys()

            if len(res) != 1:
                raise ValueError("Insertion device type (%s) does not exist."%(kws['dtype']))
            
            else:
                compnttypeid = res[reskeys[0]]['id']

            queryDict['cmpnt_type_id'] = compnttypeid

        # Check alias parameter
        if kws.has_key('alias'):
            queryDict['alias'] = kws['alias']

        # Check serial number parameter
        if kws.has_key('serialno'):
            queryDict['serial_no'] = kws['serialno']

        # Check vendor parameter
        if kws.has_key('vendor') and kws['vendor'] != None:
            
            # Check parameter
            self._checkParameter("vendor name", kws['vendor'])
            
            res = self.retrieveVendor(kws['vendor'])

            if len(res) == 0:
                raise ValueError("Vendor with name (%s) doesn't exist." % kws['vendor'])
            
            resKeys = res.keys()
            vendor = res[resKeys[0]]['id']
            queryDict['vendor_id'] = vendor
            
        sqlVals = self._generateUpdateQuery('inventory', queryDict, whereKey, whereValue)
        
        try:
            # Insert inventory into database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            # Inventory is updated, now we can update properties
            if kws.has_key('props') and kws['props'] != None:
                props = kws['props']
                
                # Update all properties
                for key in props:
                    value = props[key]
                    self.updateInventoryProperty(name, key, value)
                
            return True
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when updating inventory:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating inventory:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveInventory(self, name):
        '''Retrieve an insertion device from inventory by device inventory name and type.
        Wildcard matching is supported for inventory name and device type. ::

            * for multiple characters matching
            ? for single character matching


        :param name: insertion device inventory name, which is usually different from its field name (the name after installation).
        :type name: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': { 'name':,                       # string
                         'serialno':,                   # string
                         'cmpnttype':                   # string
                         'typeinto':                    # string
                         'vendor':,                     # string
                         'length': ,                    # float
                         'up_corrector_position': ,     # float
                         'middle_corrector_position': , # float
                         'down_corrector_position':,    # float
                         'gap_min': ,                   # float
                         'gap_max': ,                   # float
                         'gap_tolerance':,              # float
                         'phase1_min':,                 # float
                         'phase1_max':,                 # float
                         'phase2_min':,                 # float
                         'phase2_max':,                 # float
                         'phase3_min':,                 # float
                         'phase3_max':,                 # float
                         'phase4_min':,                 # float
                         'phase4_max':,                 # float
                         'phase_tolerance':,            # float
                         'k_max_linear':,               # float
                         'k_max_circular':,             # float
                         'phase_mode_p':,               # string
                         'phase_mode_a1':,              # string
                         'phase_mode_a2':               # string

                        }
                }

        :Raises: ValueError, MySQLError
        '''

        # Check name parameter
        self._checkParameter('name', name)
        
        # Generate SQL
        sql = '''
        SELECT inv.inventory_id, inv.name, inv.alias, inv.serial_no,
            ctype.cmpnt_type_name, ctype.description,
            vendor.vendor_name
        FROM inventory inv
        LEFT JOIN vendor on vendor.vendor_id = inv.vendor_id
        LEFT JOIN cmpnt_type ctype on ctype.cmpnt_type_id = inv.cmpnt_type_id
        WHERE
        '''
        
        vals = []
        
        # Append inv.name parameter
        sqlVals = self._checkWildcardAndAppend('inv.name', name, sql, vals)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            # Get any one since it should be unique
            res = cur.fetchall()
            resdict = {}
            
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'name': r[1],
                    'serialno': r[3],
                    'cmpnttype': r[4],
                    'vendor': r[6]
                }
                
                # Get the rest of the properties
                properties = self._retrieveInventoryProperty(r[0])
                
                # Append properties to existing object
                for prop in properties:
                    obj = properties[prop]
                    resdict[r[0]][obj['templatename']] = obj['value']
            
            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching insertion device inventory:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching insertion device inventory:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveRawData(self, data):
        '''
        Save raw data into database
        
        params:
            - data: data we want to save in a blob
        
        raises:
            MySQLError
            
        returns:
            {'id': new raw data id}
        
        '''
        
        # Generate SQL
        sql = '''
        INSERT INTO id_raw_data (data) VALUES (%s)
        '''
        
        try:
            # Insert data into database
            cur = self.conn.cursor()
            cur.execute(sql, data)
            
            # Get last id
            dataid = cur.lastrowid
            
            # Handle transaction
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': dataid}
            
        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving new raw data:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving new raw data:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateRawData(self, rawDataId, data):
        '''
        Update raw data
        
        params:
            - rawDataId: id of the raw data we want to update by
            - data: data we want to save in a blob
        
        raises:
            ValueError, MySQLError
            
        returns:
            True
        
        '''
        
        # Define properties
        queryDict = {}
        
        # Check id
        self._checkParameter('id', rawDataId, 'prim')
        whereKey = 'id_raw_data_id'
        whereValue = rawDataId
        
        # Set data parameter
        queryDict['data'] = data
        
        # Generate SQL
        sqlVals = self._generateUpdateQuery('id_raw_data', queryDict, whereKey, whereValue)
        
        try:
            # Insert data into database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            # Handle transaction
            if self.transaction == None:
                self.conn.commit()
                
            return True
            
        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when updating raw data:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating raw data:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveOfflineData(self, **kws):
        '''
        save insertion device offline data using any of the acceptable key words:

        - inventory_name
        - username
        - description
        - gap
        - phase1
        - phase2
        - phase3
        - phase4
        - phasemode
        - polarmode
        - status
        - data_file_name
        - data_file_ts
        - data
        - script_name
        - script
        - method_name

        :param inventory_name: name of the inventory offline data is connected to
        :type inventory_name: str

        :param username: author who created this data entry originally
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param gap: gap when this data set is produced
        :type gap: float

        :param phase1: phase 1 when this data set is produced
        :type phase1: float

        :param phase2: phase 2 when this data set is produced
        :type phase2: float

        :param phase3: phase 3 when this data set is produced
        :type phase3: float

        :param phase4: phase 4 when this data set is produced
        :type phase4: float

        :param phasemode: description for the mode of phase, which is determined by gap/phase
        :type phasemode: str

        :param polarmode: description for the mode of polar, which is determined by gap/phase
        :type polarmode: str

        :param status: status of this data set
        :type status: int

        :param data_file_name: file name of the data
        :type data_file_name: str

        :param data_file_ts: time stamp of data file with format like "YYYY-MM-DD HH:MM:SS"
        :type data_file_ts: str

        :param data: real data dumped into JSON string
        :type data: str

        :param script_name: name of script to produce the data
        :type script_name: str

        :param script: script to produce the data
        :type script: str

        :param method_name: name of method used to produce the data
        :type method_name: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': offline_data_id}

        :Raises: ValueError, exception
        '''
        
        # Check inventoryname
        inventoryname = None
        inventoryid = None
        
        if 'inventory_name' in kws and kws['inventory_name'] != None:
            inventoryname = kws['inventory_name']
            
            returnedInventory = self.retrieveInventory(inventoryname)
            
            if len(returnedInventory) == 0:
                raise ValueError("Invnetory (%s) does not exist in the database!" % inventoryname)
            
            returnedInventoryKeys = returnedInventory.keys()
            inventoryid = returnedInventory[returnedInventoryKeys[0]]['id']
        
        # Check username parameter
        username = None
        
        if 'username' in kws and kws['username'] != None:
            username = kws['username']
            self._checkParameter('username', username)
            
        # Check description
        description = None
        
        if 'description' in kws and kws['description'] != None:
            description = kws['description']
            
        # Check gap
        gap = None
        
        if 'gap' in kws and kws['gap'] != None:
            gap = kws['gap']
            
        # Check phase1
        phase1 = None
        
        if 'phase1' in kws and kws['phase1'] != None:
            phase1 = kws['phase1']
            
        # Check phase2
        phase2 = None
        
        if 'phase2' in kws and kws['phase2'] != None:
            phase2 = kws['phase2']
            
        # Check phase3
        phase3 = None
        
        if 'phase3' in kws and kws['phase3'] != None:
            phase3 = kws['phase3']
            
        # Check phase4
        phase4 = None
        
        if 'phase4' in kws and kws['phase4'] != None:
            phase4 = kws['phase4']
            
        # Check phasemode
        phasemode = None
        
        if 'phasemode' in kws and kws['phasemode'] != None:
            phasemode = kws['phasemode']
            
        # Check polarmode
        polarmode = None
        
        if 'polarmode' in kws and kws['polarmode'] != None:
            polarmode = kws['polarmode']
            
        # Check status
        status = None
        
        if 'status' in kws and kws['status'] != None:
            status = kws['status']
            
        # Check data_file_name
        datafilename = None
        
        if 'data_file_name' in kws and kws['data_file_name'] != None:
            datafilename = kws['data_file_name']
            
        # Check data_file_ts
        datafilets = None
        
        if 'data_file_ts' in kws and kws['data_file_ts'] != None:
            datafilets = kws['data_file_ts']
            
        # Check data
        data = None
        
        if 'data' in kws and kws['data'] != None:
            data = kws['data']
            
        # Check script_name
        scriptname = None
        
        if 'script_name' in kws and kws['script_name'] != None:
            scriptname = kws['scriptname']
            
        # Check script
        script = None
        
        if 'script' in kws and kws['script'] != None:
            script = kws['script']
            
        # Check method_name
        methodname = None
        methodid = None
        
        if 'method_name' in kws and kws['method_name'] != None:
            methodname = kws['method_name']
            
            retrievedMethod = self.retrieveDataMethod(methodname)
            
            if len(retrievedMethod) == 0:
                raise ValueError("Data method (%s) doesn't exist in the database!" % methodname)

            retrievedMethodKeys = retrievedMethod.keys()
            methodid = retrievedMethod[retrievedMethodKeys[0]]['id']

        # Genreate SQL
        sql = '''
        INSERT INTO id_offline_data (
            inventory_id,
            id_data_method_id,
            id_raw_data_id,
            login_name,
            description,
            date,
            gap,
            phase1,
            phase2,
            phase3,
            phase4,
            phase_mode,
            polar_mode,
            data_status,
            result_file_name,
            result_file_time,
            script_file_name,
            script_file_content
        ) VALUES (
            %s,%s,1,%s,%s,NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        '''
        
        try:
            vals = [
                inventoryid,
                methodid,
                username,
                description,
                gap,
                phase1,
                phase2,
                phase3,
                phase4,
                phasemode,
                polarmode,
                status,
                datafilename,
                datafilets,
                scriptname,
                script
            ]
            
            # Insert offline data into database
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            
            # Get last row id
            offlinedataid = cur.lastrowid
            
            # Create transactions
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': offlinedataid}
        
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving new offline data:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving new offline data:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateOfflineData(self, offline_data_id, **kws):
        '''
        Update insertion device offline data by its id

        parameters:
        - inventory_name
        - username
        - description
        - gap
        - phase1
        - phase2
        - phase3
        - phase4
        - phasemode
        - polarmode
        - status
        - data_file_name
        - data_file_ts
        - data
        - script_name
        - script
        - method_name

        :param inventory_name: name of the inventory offline data is connected to
        :type inventory_name: str

        :param username: author who created this data entry originally
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param gap: gap when this data set is produced
        :type gap: float

        :param phase1: phase 1 when this data set is produced
        :type phase1: float

        :param phase2: phase 2 when this data set is produced
        :type phase2: float

        :param phase3: phase 3 when this data set is produced
        :type phase3: float

        :param phase4: phase 4 when this data set is produced
        :type phase4: float

        :param phasemode: description for the mode of phase, which is determined by gap/phase
        :type phasemode: str

        :param polarmode: description for the mode of polar, which is determined by gap/phase
        :type polarmode: str

        :param status: status of this data set
        :type status: int

        :param data_file_name: file name of the data
        :type data_file_name: str

        :param data_file_ts: time stamp of data file with format like "YYYY-MM-DD HH:MM:SS"
        :type data_file_ts: str

        :param data: real data dumped into JSON string
        :type data: str

        :param script_name: name of script to produce the data
        :type script_name: str

        :param script: script to produce the data
        :type script: str

        :param method_name: name of method used to produce the data
        :type method_name: str

        :return: True if everything is ok

        :Raises: ValueError, MySQLError
        '''
        
        # Define query dict
        queryDict = {}
        
        # Check id
        self._checkParameter('id', offline_data_id, 'prim')
        whereKey = 'id_offline_data_id'
        whereValue = offline_data_id
        
        # Check inventoryname
        if 'inventory_name' in kws and kws['inventory_name'] != None:
            inventoryname = kws['inventory_name']
            
            returnedInventory = self.retrieveInventory(inventoryname)
            
            if len(returnedInventory) == 0:
                raise ValueError("Invnetory (%s) does not exist in the database!" % inventoryname)
            
            returnedInventoryKeys = returnedInventory.keys()
            inventoryid = returnedInventory[returnedInventoryKeys[0]]['id']
            queryDict['inventory_id'] = inventoryid
        
        # Check username parameter
        if 'username' in kws:
            queryDict['login_name'] = kws['username']
            
        # Check description
        if 'description' in kws:
            queryDict['description'] = kws['description']
            
        # Check gap
        if 'gap' in kws:
            queryDict['gap'] = kws['gap']
            
        # Check phase1
        if 'phase1' in kws:
            queryDict['phase1'] = kws['phase1']
            
        # Check phase2
        if 'phase2' in kws:
            queryDict['phase2'] = kws['phase2']
            
        # Check phase3
        if 'phase3' in kws:
            queryDict['phase3'] = kws['phase3']
            
        # Check phase4
        if 'phase4' in kws:
            queryDict['phase4'] = kws['phase4']
            
        # Check phasemode
        if 'phasemode' in kws:
            queryDict['phase_mode'] = kws['phasemode']
            
        # Check polarmode
        if 'polarmode' in kws:
            queryDict['polar_mode'] = kws['polarmode']
            
        # Check status
        if 'status' in kws:
            queryDict['data_status'] = kws['status']
            
        # Check data_file_name
        if 'data_file_name' in kws:
            queryDict['result_file_name'] = kws['data_file_name']
            
        # Check data_file_ts
        if 'data_file_ts' in kws and kws['data_file_ts'] != None:
            queryDict['result_file_time'] = kws['data_file_ts']
            
        # Check data
        if 'data' in kws and kws['data'] != None:
            data = kws['data']
            # !!! save data
            
        # Check script_name
        if 'script_name' in kws:
            queryDict['script_file_name'] = kws['scriptname']
            
        # Check script
        if 'script' in kws:
            queryDict['script_file_content'] = kws['script']
            
        # Check method_name
        if 'method_name' in kws and kws['method_name'] != None:
            methodname = kws['method_name']
            
            retrievedMethod = self.retrieveDataMethod(methodname)
            
            if len(retrievedMethod) == 0:
                raise ValueError("Data method (%s) doesn't exist in the database!" % methodname)

            retrievedMethodKeys = retrievedMethod.keys()
            methodid = retrievedMethod[retrievedMethodKeys[0]]['id']
            queryDict['id_data_method_id'] = methodid

        # Genreate SQL
        sqlVals = self._generateUpdateQuery('id_offline_data', queryDict, whereKey, whereValue)
        
        try:
            
            # Insert offline data into database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            # Create transactions
            if self.transaction == None:
                self.conn.commit()
                
            return True
        
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when updating offline data:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating offline data:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveOfflineData(self, **kws):
        '''Retrieve insertion device offline data using any of the acceptable key words:

        - offlineid
        - description
        - gap
        - phase1
        - phase2
        - phase3
        - phase4
        - phasemode
        - polarmode
        - status
        - method_name
        - inventory_name

        :param offlineid: id of the offline data we want to retrieve
        :type offlineid: int

        :param description: a brief description for this data entry
        :type description: str

        :param gap: gap when this data set is produced
        :type gap: float

        :param phase1: phase 1 when this data set is produced
        :type phase1: float

        :param phase2: phase 2 when this data set is produced
        :type phase2: float

        :param phase3: phase 3 when this data set is produced
        :type phase3: float

        :param phase4: phase 4 when this data set is produced
        :type phase4: float

        :param phasemode: description for the mode of phase, which is determined by gap/phase
        :type phasemode: str

        :param polarmode: description for the mode of polar, which is determined by gap/phase
        :type polarmode: str

        :param status: status of this data set
        :type status: int

        :param method_name: name of method used to produce the data
        :type method_name: str

        :param inventory_name: name of inventory used to produce the data
        :type inventory_name: str

        :return: a map with structure like:

            .. code-block:: python

                {'data_id': {
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
                        'data':,           # string
                        'script_name':,    # string
                        'script':,         # string
                        'method_name':,    # string
                        'methoddesc':,     # string
                        'inventory_name':, # string
                    }
                }

        :Raises: KeyError, AttributeError

        '''
        
        # Generate SQL
        sql = '''
        SELECT
            iod.id_offline_data_id,
            iod.inventory_id,
            iod.id_data_method_id,
            iod.id_raw_data_id,
            iod.login_name,
            iod.description,
            iod.date,
            iod.gap,
            iod.phase1,
            iod.phase2,
            iod.phase3,
            iod.phase4,
            iod.phase_mode,
            iod.polar_mode,
            iod.data_status,
            iod.result_file_name,
            iod.result_file_time,
            iod.script_file_name,
            iod.script_file_content,
            idm.method_name,
            idm.description,
            inv.name
        FROM id_offline_data iod
        LEFT JOIN id_data_method idm ON (iod.id_data_method_id = idm.id_data_method_id)
        LEFT JOIN inventory inv ON (iod.inventory_id = inv.inventory_id)
        WHERE 1=1
        '''
        
        vals = []
        
        # Append offline id
        if 'offlineid' in kws and kws['offlineid'] != None:
            self._checkParameter('id', kws['offlineid'], 'prim')
            sql += ' AND id_offline_data_id = %s '
            vals.append(kws['offlineid'])
        
        # Append description parameter
        if 'description' in kws and kws['description'] != None:
            sqlVal = self._checkWildcardAndAppend('iod.description', kws['description'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]
        
        # Append gap parameter
        if 'gap' in kws and kws['gap'] != None:
            sqlVal = self._checkRangeAndAppend('iod.gap', kws['gap'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]
        
        # Append phase1 parameter
        if 'phase1' in kws and kws['phase1'] != None:
            sqlVal = self._checkRangeAndAppend('iod.phase1', kws['phase1'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]
        
        # Append phase2 parameter
        if 'phase2' in kws and kws['phase2'] != None:
            sqlVal = self._checkRangeAndAppend('iod.phase2', kws['phase2'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]
        
        # Append phase3 parameter
        if 'phase3' in kws and kws['phase3'] != None:
            sqlVal = self._checkRangeAndAppend('iod.phase3', kws['phase3'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]
        
        # Append phase4 parameter
        if 'phase4' in kws and kws['phase4'] != None:
            sqlVal = self._checkRangeAndAppend('iod.phase4', kws['phase4'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]
            
        # Append phasemode parameter
        if 'phasemode' in kws and kws['phasemode'] != None:
            sqlVal = self._checkWildcardAndAppend('iod.phase_mode', kws['phasemode'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]
            
        # Append polarmode parameter
        if 'polarmode' in kws and kws['polarmode'] != None:
            sqlVal = self._checkWildcardAndAppend('iod.polar_mode', kws['polarmode'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]
            
        # Append status parameter
        if 'status' in kws and kws['status'] != None:
            sql += ' AND iod.status = %s '
            vals.append(kws['status'])
            
        # Append method name parameter
        if 'method_name' in kws and kws['method_name'] != None:
            sqlVal = self._checkWildcardAndAppend('idm.method_name', kws['method_name'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]
        
        # Append inventory name
        if 'inventory_name' in kws and kws['inventory_name'] != None:
            sqlVal = self._checkWildcardAndAppend('inv.name', kws['inventory_name'], sql, vals, 'AND')
            sql = sqlVal[0]
        
        try:
            # Execute SQL
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            
            # Get all records
            res = cur.fetchall()
            resdict = {}
            
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'username': r[4],
                    'description': r[5],
                    'date': r[6].strftime("%Y-%m-%d %H:%M:%S"),
                    'gap': r[7],
                    'phase1': r[8],
                    'phase2': r[9],
                    'phase3': r[10],
                    'phase4': r[11],
                    'phasemode': r[12],
                    'polarmode': r[13],
                    'status': r[14],
                    'data_file_name': r[15],
                    'data_file_ts': None,
                    'data': 0,
                    'script_name': r[17],
                    'script': r[18],
                    'method_name': r[19],
                    'methoddesc': r[20],
                    'inventory_name': r[21]
                }
                
                # Format time if it is not null
                if r[16] != None:
                    resdict[r[0]]['data_file_ts'] = r[16].strftime("%Y-%m-%d %H:%M:%S")

            return resdict
            
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching offline data:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching offline data:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveDataMethod(self, name, description=None):
        '''Save a method with its description which is used when producing data set for an insertion device.

        :param name: name of the method
        :type name: str

        :param description: description of this method
        :type description: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': method_id}

        :Raises: ValueError, MySQLError
        '''
        
        # Raise and error if data method with the same name already exists in the database
        existingDataMethod = self.retrieveDataMethod(name, description)
        
        if len(existingDataMethod):
            raise ValueError("Data method (%s) already exists in the database!" % name)

        # Check name parameter
        self._checkParameter('name', name)
        
        # Generate SQL
        sql = '''
        INSERT INTO id_data_method
            (method_name, description)
        VALUES
            (%s, %s)
        '''
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (name, description))
            
            # Get last id
            dataMethodId = cur.lastrowid
            
            # Create transaction
            if self.transaction == None:
                self.conn.commit()
            
            return {'id': dataMethodId}
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when saving new data method:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving new data method:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateDataMethod(self, dataMethodId, oldName, name, **kws):
        '''Update data method by id or name.

        :param dataMethodId id of the data method we want to update by
        :type dataMethodId: int

        :param oldName: name of the method we want to update by
        :type oldName: str

        :param name: name of the method
        :type name: str

        :param description: description of this method
        :type description: str

        :return: True if everything was ok

        :Raises: ValueError, MySQLError
        '''
        
        # Define query dictionary
        queryDict = {}
        whereKey = None
        whereValue = None
        
        # Check if
        if dataMethodId:
            self._checkParameter('id', dataMethodId, 'prim')
            whereKey = 'id_data_method_id'
            whereValue = dataMethodId
            
        # Check name
        if oldName:
            self._checkParameter('name', oldName)
            whereKey = 'method_name'
            whereValue = oldName
            
        # Check if id or name is present
        if whereKey == None:
            raise ValueError("Id or old name should be present to execute an update!")

        # Check name parameter
        self._checkParameter('name', name)
        queryDict['method_name'] = name
        
        # Check description parameter
        if 'description' in kws:
            queryDict['description'] = kws['description']
        
        # Generate SQL
        sqlVals = self._generateUpdateQuery('id_data_method', queryDict, whereKey, whereValue)
        
        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            # Create transaction
            if self.transaction == None:
                self.conn.commit()
            
            return True
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when updating data method:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating data method:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveDataMethod(self, name, description = None):
        '''Retrieve a method name and its description which is used when producing data set for an insertion device.

        :param name: name of the method
        :type name: str

        :param description: description of this method
        :type description: str

        :return: a map with structure like:

            .. code-block:: python
                {'id':
                    {'id': data method id,
                     'name': method name,
                     'description': description of this method
                    }
                }

        :Raises: ValueError, MySQLError
        '''
        
        # Check name
        self._checkParameter('name', name)
        
        # Contruct SQL
        sql = '''
        SELECT
            id_data_method_id,
            method_name,
            description
        FROM id_data_method
        WHERE
        '''
        
        vals = []
        
        # Append name
        sqlAndVals = self._checkWildcardAndAppend('method_name', name, sql, vals)
        
        # Check if description exists
        if description:
            sqlAndVals = self._checkWildcardAndAppend('description', description, sqlAndVals[0], sqlAndVals[1], 'AND')

        try:
            # Execute SQL
            cur = self.conn.cursor()
            cur.execute(sqlAndVals[0], sqlAndVals[1])
            
            res = cur.fetchall()
            resdict = {}
            
            # Construct return dict
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'name': r[1],
                    'description': r[2]
                }
                
            return resdict
            
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching data method:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching data method:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveInventoryToInstall(self, inventoryToInstallId, installName, invName):
        '''
        Return installed devices or psecific map
        
        params:
        - installName
        - invName

        :param installName: label name after installation
        :type installName: str

        :param invName: name in its inventory
        :type invName: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': {
                        'id': #int,
                        'installid': #int,
                        'installname': #string,
                        'inventoryid': #int,
                        'inventoryname': #string
                    }
                }

        :Raises: ValueError, MySQLError
        '''
        
        # Generate SQL
        sql = '''
        SELECT
            ii.inventory__install_id,
            ii.install_id,
            ii.inventory_id,
            inst.field_name,
            inv.name
        FROM inventory__install ii
        LEFT JOIN install inst ON(ii.install_id = inst.install_id)
        LEFT JOIN inventory inv ON(ii.inventory_id = inv.inventory_id)
        WHERE 1=1
        '''
        
        vals = []
        
        # Check primary key
        if inventoryToInstallId:
            sql += ' AND ii.inventory__install_id = %s '
            vals.append(inventoryToInstallId)
            
        # Check inventory name
        if invName:
            sql += ' AND inv.name = %s '
            vals.append(invName)
            
        # Check install name
        if installName:
            sql += ' AND inst.field_name = %s '
            vals.append(installName)
            
        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
            resdict = {}
            
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'installid': r[1],
                    'installname': r[3],
                    'inventoryid': r[2],
                    'inventoryname': r[4]
                }
                
            return resdict
            
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching installed devices:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching installed devices:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveInventoryToInstall(self, installName, invName):
        '''Link a device as installed once it is installed into field using the key words:
        - installName
        - invName

        :param installName: label name after installation
        :type installName: str

        :param invName: name in its inventory
        :type invName: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': id of new inventorytoinstall record}

        :Raises: ValueError, MySQLError
        '''
        
        # Check install name
        install = self.retrieveInstall(installName)
        
        if len(install) < 1:
            raise ValueError("Install with name (%s) doesn't exist in the database!" % installName)
        
        installKeys = install.keys()
        installObject = install[installKeys[0]]
        
        # Check inventory name
        inventory = self.retrieveInventory(invName)
        
        if len(inventory) < 1:
            raise ValueError("Inventory with name (%s) doesn't exist in the database!" % invName)
        
        inventoryKeys = inventory.keys()
        inventoryObject = inventory[inventoryKeys[0]]
        
        # Check if map already exists
        existing = self.retrieveInventoryToInstall(None, installName, invName)
        
        if len(existing):
            raise ValueError("Inventory already installed!")
        
        # Generate SQL
        sql = '''
        INSERT INTO inventory__install (install_id, inventory_id)
        VALUES (%s, %s)
        '''
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (installObject['id'], inventoryObject['id']))
            
            # Get last id
            lastid = cur.lastrowid
            
            # Create transaction
            if self.transaction == None:
                self.conn.commit()
            
            return {'id': lastid}
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when saving inventory to install:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving inventory to install:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateInventoryToInstall(self, inventoryToInstallId, installName, invName):
        '''Update a device as installed when its installation has been changed using the key words:

        - installName
        - invName

        :param installName: label name after installation
        :type installName: str

        :param invName: name in its inventory
        :type invName: str

        :return: True if everything was ok

        :Raises: ValueError, MySQLError
        '''
        
        # Define query dict
        queryDict = {}
        
        # Check id
        self._checkParameter('id', inventoryToInstallId, 'prim')
        whereKey = 'inventory__install_id'
        whereValue = inventoryToInstallId
        
        # Check install name
        install = self.retrieveInstall(installName)
        
        if len(install) < 1:
            raise ValueError("Install with name (%s) doesn't exist in the database!" % installName)
        
        installKeys = install.keys()
        installObject = install[installKeys[0]]
        queryDict['install_id'] = installObject['id']
        
        # Check inventory name
        inventory = self.retrieveInventory(invName)
        
        if len(inventory) < 1:
            raise ValueError("Inventory with name (%s) doesn't exist in the database!" % invName)
        
        inventoryKeys = inventory.keys()
        inventoryObject = inventory[inventoryKeys[0]]
        queryDict['inventory_id'] = inventoryObject['id']
        
        # Generate SQL
        sqlVals = self._generateUpdateQuery('inventory__install', queryDict, whereKey, whereValue)
        
        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            # Create transaction
            if self.transaction == None:
                self.conn.commit()
            
            return True
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when updating inventory to install:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating inventory to install:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveComponentTypePropertyType(self, name):
        '''
        Retrieve component type property type by its name

        - name: property type name

        :return: a map with structure like:

            .. code-block:: python

                {
                    'id': {
                        'id': ,              # int
                        'name': ,           # string
                        'description': ,    # string
                    }
                }

        :Raises: ValueError, MySQLError
        '''

        # Check name
        self._checkParameter("name", name)

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
        sqlAndVals = self._checkWildcardAndAppend("cmpnt_type_prop_type_name", name, sql, vals)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlAndVals[0], sqlAndVals[1])

            # Get any one since it should be unique
            res = cur.fetchall()
            resdict = {}

            # Construct return dict
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'name': r[1],
                    'description': r[2]
                }
            
            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching component type property type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching component type property type:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveComponentTypePropertyType(self, name, description = None):
        '''
        Insert new component type property type into database

        - name: name of the component type property type M
        - description: description of the component type property tpye O

        :return: a map with structure like:

            .. code-block:: python

                {'id': propertytypeid}

        :Raises: ValueError, MySQLError
        '''

        # Raise an error if component type property type exists
        existingComponentTypePropertyType = self.retrieveComponentTypePropertyType(name)
        
        if len(existingComponentTypePropertyType):
            raise ValueError("Component type property type (%s) already exists in the database!" % name)

        # Check name
        self._checkParameter("name", name)

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
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': typeid}

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving new component type property type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving new component type property type:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateComponentTypePropertyType(self, property_type_id, old_name, name, **kws):
        '''
        Insert new component type property type into database

        - property_type_id: id of the property type we want to update by M
        - old_name: name of the component type property type we want to update by M
        - name: name of the component type property type M
        - description: description of the component type property tpye O

        :return: True if everything is ok

        :Raises: ValueError, MySQLError
        '''

        # Define query dict
        queryDict = {}
        whereKey = None
        whereValue = None

        # Check id
        if property_type_id:
            self._checkParameter('id', property_type_id, 'prim')
            whereKey = 'cmpnt_type_prop_type_id'
            whereValue = property_type_id
            
        # Check old name
        if old_name:
            self._checkParameter('name', old_name)
            whereKey = 'cmpnt_type_prop_type_name'
            whereValue = old_name
        
        if whereKey == None:
            raise ValueError("Id or old name should be present to execute an update!")

        # Check name
        self._checkParameter("name", name)
        queryDict['cmpnt_type_prop_type_name'] = name
        
        # Append description
        if 'description' in kws:
            queryDict['cmpnt_type_prop_type_desc'] = kws['description']

        # Generate SQL
        sqlVals = self._generateUpdateQuery('cmpnt_type_prop_type', queryDict, whereKey, whereValue)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when updating component type property type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating component type property type:\n%s (%d)' %(e.args[1], e.args[0]))

    def _retrieveComponentTypeProperty(self, componentTypeId, componentTypePropertyTypeId = None, value = None):
        '''
        Retrieve component type property from the database
        
        parameters:
            - componentTypeId: id of the component type entry
            - componentTypePropertyTypeId: id of the property type
            - value: value of the property
            
        returns:
            { 'id': {
                    'id': #int,
                    'value': #string,
                    'cmpnttypename': #string,
                    'typename': #string
                }
            }
            
        raises:
            ValueError, MySQLError
        '''
        
        # Generate SQL
        sql = '''
        SELECT 
            cp.cmpnt_type_prop_id,
            cp.cmpnt_type_id,
            cp.cmpnt_type_prop_type_id,
            cp.cmpnt_type_prop_value,
            cpt.cmpnt_type_prop_type_name,
            ct.cmpnt_type_name
        FROM cmpnt_type_prop cp
        LEFT JOIN cmpnt_type_prop_type cpt ON (cp.cmpnt_type_prop_type_id = cpt.cmpnt_type_prop_type_id)
        LEFT JOIN cmpnt_type ct ON (cp.cmpnt_type_id = ct.cmpnt_type_id)
        WHERE
        '''
        
        # Add component type id parameter
        sql += ' cp.cmpnt_type_id = %s '
        vals = [componentTypeId]

        # Add component type property type parameter
        if componentTypePropertyTypeId:
            sql += ' AND cp.cmpnt_type_prop_type_id = %s '
            vals.append(componentTypePropertyTypeId)
        
        sqlVals = (sql, vals)

        # Add value parameter if exists
        if value:
            sqlVals = self._checkWildcardAndAppend('cmpnt_type_prop_value', value, sqlVals[0], sqlVals[1], 'AND')

        try:
            # Retrieve objects from the database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            res = cur.fetchall()
            resdict = {}
            
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'value': r[3],
                    'cmpnttypename': r[5],
                    'typename': r[4]
                }
                
            return resdict
            
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving component type property from the table:\n%s (%s)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when retrieving component type property from the table:\n%s (%s)' %(e.args[1], e.args[0]))

    def retrieveComponentTypeProperty(self, componentTypeName, componentTypePropertyTypeName = None, value = None):
        '''
        Retrieve component type property from the database by name
        
        parameters:
            - componentTypeName: name of the component type
            - componentTypePropertyTypeName: name of the component type property type
            - value: value of the component type property type
            
        returns:
            { 'id': {
                    'id': #int,
                    'value': #string,
                    'cmpnttypename': #string,
                    'typename': #string
                }
            }
        '''
        
        # Check component type
        retrieveComponentType = self.retrieveComponentType(componentTypeName)
        
        if len(retrieveComponentType) == 0:
            raise ValueError("Component type (%s) doesn't exist in the database!" % componentTypeName)

        retrieveComponentTypeKeys = retrieveComponentType.keys()
        componentTypeId = retrieveComponentType[retrieveComponentTypeKeys[0]]['id']

        # Check component type property type
        # of a specific component tpye
        
        componentTypePropertyTypeId = None
        
        if componentTypePropertyTypeName:
            retrieveComponentTypePropertyType = self.retrieveComponentTypePropertyType(componentTypePropertyTypeName)
            
            if len(retrieveComponentTypePropertyType) == 0:
                raise ValueError("Component type property type (%s) doesn't exist in the database!" % componentTypePropertyTypeName);
    
            retrieveComponentTypePropertyTypeKeys = retrieveComponentTypePropertyType.keys()
            componentTypePropertyTypeId = retrieveComponentTypePropertyType[retrieveComponentTypePropertyTypeKeys[0]]['id']

        return self._retrieveComponentTypeProperty(componentTypeId, componentTypePropertyTypeId, value)

    def saveComponentTypeProperty(self, componentTypeName, componentTypePropertyTypeName, value):
        '''
        Save inventory property into database
        
        params:
            - componentTypeName: name of the component type
            - componentTypePropertyTypeName: name of the component type property type
            - value: value of the component type property
            
        returns:
            {'id': new component type property id}
            
        raises:
            ValueError, MySQLError
        '''
        
        # Check for previous component type property
        retrieveComponentTypeProperty = self.retrieveComponentTypeProperty(componentTypeName, componentTypePropertyTypeName)
        
        if len(retrieveComponentTypeProperty) != 0:
            raise ValueError("Component type property for component type (%s) and property type (%s) already exists in the database!" % (componentTypeName, componentTypePropertyTypeName));
        
        # Check component type
        retrieveComponentType = self.retrieveComponentType(componentTypeName)
        
        if len(retrieveComponentType) == 0:
            raise ValueError("Component type (%s) doesn't exist in the database!" % componentTypeName)

        retrieveComponentTypeKeys = retrieveComponentType.keys()
        componentTypeId = retrieveComponentType[retrieveComponentTypeKeys[0]]['id']

        # Check component type property type
        retrieveComponentTypePropertyType = self.retrieveComponentTypePropertyType(componentTypePropertyTypeName)
        
        if len(retrieveComponentTypePropertyType) == 0:
            raise ValueError("Component type property type (%s) doesn't exist in the database!" % componentTypePropertyTypeName);

        retrieveComponentTypePropertyTypeKeys = retrieveComponentTypePropertyType.keys()
        componentTypePropertyTypeId = retrieveComponentTypePropertyType[retrieveComponentTypePropertyTypeKeys[0]]['id']

        # Generate SQL
        sql = '''
        INSERT INTO cmpnt_type_prop
            (cmpnt_type_id, cmpnt_type_prop_type_id, cmpnt_type_prop_value)
        VALUES
            (%s, %s, %s)
        '''
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (componentTypeId, componentTypePropertyTypeId, value))
            
            # Get last row id
            propid = cur.lastrowid

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': propid}
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when saving component type property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving component type property:\n%s (%d)' % (e.args[1], e.args[0]))
    
    def updateComponentTypeProperty(self, oldComponentTypeName, oldComponentTypePropertyTypeName, value):
        '''
        Save inventory property into database
        
        params:
            - oldComponentTypeName: name of the component type
            - oldComponentTypePropertyTypeName: name of the component type property type
            - value: value of the component type property
            
        returns:
            True if everything is ok
            
        raises:
            ValueError, MySQLError
        '''
        
        # Define query dict
        queryDict = {}
        whereDict = {}
        
        # Check component type
        retrieveComponentType = self.retrieveComponentType(oldComponentTypeName)
        
        if len(retrieveComponentType) == 0:
            raise ValueError("Component type (%s) doesn't exist in the database!" % oldComponentTypeName)

        retrieveComponentTypeKeys = retrieveComponentType.keys()
        componentTypeId = retrieveComponentType[retrieveComponentTypeKeys[0]]['id']
        whereDict['cmpnt_type_id'] = componentTypeId

        # Check component type property type
        retrieveComponentTypePropertyType = self.retrieveComponentTypePropertyType(oldComponentTypePropertyTypeName)
        
        if len(retrieveComponentTypePropertyType) == 0:
            raise ValueError("Component type property type (%s) doesn't exist in the database!" % oldComponentTypePropertyTypeName);

        retrieveComponentTypePropertyTypeKeys = retrieveComponentTypePropertyType.keys()
        componentTypePropertyTypeId = retrieveComponentTypePropertyType[retrieveComponentTypePropertyTypeKeys[0]]['id']
        whereDict['cmpnt_type_prop_type_id'] = componentTypePropertyTypeId

        # Set value parameter
        queryDict['cmpnt_type_prop_value'] = value

        # Generate SQL
        sqlVals = self._generateUpdateQuery('cmpnt_type_prop', queryDict, None, None, whereDict)
        
        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return True
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when updating component type property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating component type property:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveComponentType(self, name, description = None):
        '''Retrieve a component type using the key words:

        - name
        - description

        :param name: component type type name
        :type name: str

        :param description: description for this device
        :type desctiprion: str

        :return: a map with structure like:

            .. code-block: python

                {'id1':
                    {'id': device type id,
                    'name': device type name,
                    'description': device type description,
                    'prop1key': prop1value
                    ...
                    'propNkey': propNvalue
                    },
                 ...
                }

        :Raises: ValueError, MySQLError
        '''

        # Check component type parameter
        self._checkParameter("component type", name)

        # Start SQL
        sql = '''
        SELECT cmpnt_type_id, cmpnt_type_name, description FROM cmpnt_type WHERE
        '''

        vals = []

        # Append component type
        sqlAndVals = self._checkWildcardAndAppend("cmpnt_type_name", name, sql, vals)

        # Append desciprtion if exists
        if description != None:
            sqlAndVals = self._checkWildcardAndAppend("description", description, sqlAndVals[0], sqlAndVals[1], "AND")

        # Execute SQL
        try:
            cur = self.conn.cursor()
            cur.execute(sqlAndVals[0], sqlAndVals[1])
            res = cur.fetchall()

            # Create return dictionry
            resdict = {}

            for r in res:
                resdict[r[0]] = {}
                resdict[r[0]]['id'] = r[0]
                resdict[r[0]]['name'] = r[1]
                resdict[r[0]]['description'] = r[2]
                
                # Get the rest of the properties
                properties = self._retrieveComponentTypeProperty(r[0])
                
                # Append properties to existing object
                for prop in properties:
                    obj = properties[prop]
                    resdict[r[0]][obj['typename']] = obj['value']

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching component type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching component type:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveComponentType(self, name, description=None, props=None):
        '''Save a component type using the key words:

        - name
        - description
        - props

        :param name: component type name
        :type name: str

        :param description: description for this device
        :type desctiprion: str
        
        :param props: component type properties
        :type props: python dict

        :return: a map with structure like:

            .. code-block: python

                {'id': device type id}

        :Raises: ValueError, MySQLError

        '''

        # Check device type
        self._checkParameter("component type", name)

        # Check if component type already exists
        componenttype = self.retrieveComponentType(name);
        
        if len(componenttype):
            raise ValueError("Component type (%s) already exists in the database!" % name);

        # Save it into database and return its new id
        sql = ''' INSERT into cmpnt_type (cmpnt_type_name, description) VALUES (%s, %s) '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (name, description))
            componenttypeid = cur.lastrowid

            # Commit transaction
            if self.transaction == None:
                self.conn.commit()
                
            # Component type is saved, now we can save properties into database
            if props != None:
                
                # Convert to json
                if isinstance(props, (dict)) == False:
                    props = json.loads(props)
                
                # Save all the properties
                for key in props:
                    value = props[key]
                    
                    # Save it into database
                    self.saveComponentTypeProperty(name, key, value)
                
            return {'id': componenttypeid}

        except MySQLError as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
                
            self.logger.info('Error when saving component type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving component type:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateComponentType(self, component_type_id, old_name, name, **kws):
        '''Update description of a device type.
        Once a device type is saved, it is not allowed to change it again since it will cause potential colflict.

        - component_type_id
        - old_name
        - name
        - description
        - props

        :param component_type_id: component type id we want to update by
        :type component_type_id: int

        :param old_name: component type name we want to update by
        :type old_name: str

        :param name: device type name
        :type name: str

        :param description: description for this device
        :type desctiprion: str
        
        :param props: component type properties
        :type props: python dict

        :return: True if everything is ok

        :Raises: ValueError, MySQLError
        '''
        
        # Set query dictionary
        queryDict = {}
        whereKey = None
        whereValue = None
        
        # Check id
        if component_type_id:
            self._checkParameter('id', component_type_id, 'prim')
            whereKey = 'cmpnt_type_id'
            whereValue = component_type_id
            
        # Check old name
        if old_name:
            self._checkParameter('name', old_name)
            whereKey = 'cmpnt_type_name'
            whereValue = old_name
            
        # Check where condition
        if whereKey == None:
            raise ValueError("Vendor id or old vendor name should be present to execute an update!")
        
        # Check device type
        self._checkParameter("component type", name)
        queryDict['cmpnt_type_name']= name
        
        # Add description
        if 'description' in kws:
            queryDict['description'] = kws['description']

        # Save it into database and return its new id
        sqlVals = self._generateUpdateQuery('cmpnt_type', queryDict, whereKey, whereValue)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Commit transaction
            if self.transaction == None:
                self.conn.commit()
                
            # Component type is saved, now we can update properties
            if 'props' in kws and kws['props'] != None:
                props = kws['props']
                
                # Convert to json
                if isinstance(props, (dict)) == False:
                    props = json.loads(props)
                
                
                # Update all the properties
                for key in props:
                    value = props[key]
                    
                    # Save it into database
                    self.updateComponentTypeProperty(name, key, value)
                
            return True

        except MySQLError as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
                
            self.logger.info('Error when updating component type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating component type:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveInstallRelPropertyType(self, name):
        '''
        Retrieve install relationship property type by its name

        - name: property type name

        :return: a map with structure like:

            .. code-block:: python

                {
                    'id': {
                        'id': ,             # int
                        'name': ,           # string
                        'description': ,    # string
                        'units': ,          # string
                    }
                }

        :Raises: ValueError, MySQLError
        '''

        # Check name
        self._checkParameter("name", name)

        # Construct SQL
        sql = '''
        SELECT
            install_rel_prop_type_id, install_rel_prop_type_name, install_rel_prop_type_desc, install_rel_prop_type_units
        FROM
            install_rel_prop_type
        WHERE
        '''
        vals = []
        
        # Append name
        sqlAndVals = self._checkWildcardAndAppend("install_rel_prop_type_name", name, sql, vals)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlAndVals[0], sqlAndVals[1])

            # Get any one since it should be unique
            res = cur.fetchall()
            resdict = {}

            # Construct return dict
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'name': r[1],
                    'description': r[2],
                    'units': r[3]
                }
            
            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching installation relationship property type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching installation ralationship property type:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveInstallRelPropertyType(self, name, description = None, units = None):
        '''
        Insert new install relationship property type into database

        - name: name of the install relationship property type M
        - description: description of the install relationship property type O
        - units: units used for this property type O

        :return: a map with structure like:

            .. code-block:: python

                {'id': propertytypeid}

        :Raises: ValueError, MySQLError
        '''

        # Raise an error if install relationship property type exists
        existingInstallRelPropertyType = self.retrieveInstallRelPropertyType(name)
        
        if len(existingInstallRelPropertyType):
            raise ValueError("Install rel property type (%s) already exists in the database!" % name)

        # Check name
        self._checkParameter("name", name)

        # Generate SQL
        sql = '''
        INSERT INTO install_rel_prop_type
            (install_rel_prop_type_name, install_rel_prop_type_desc, install_rel_prop_type_units)
        VALUES
            (%s, %s, %s)
        '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (name, description, units))

            # Get last row id
            typeid = cur.lastrowid

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': typeid}

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving new install rel property type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving new install rel property type:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateInstallRelPropertyType(self, typeId, oldName, name, **kws):
        '''
        Update install relationship property type

        - typeId: id of the install rellationship property type we want to update by O
        - oldName: name of the install relationship property type we want to update by O
        - name: name of the install relationship property type M
        - description: description of the install relationship property type O
        - units: units used for this property type O

        :return: True if everything is ok

        :Raises: ValueError, MySQLError
        '''
        
        # Define query dictionary
        queryDict = {}
        whereKey = None
        whereValue = None
        
        # Check if
        if typeId:
            self._checkParameter('id', typeId, 'prim')
            whereKey = 'install_rel_prop_type_id'
            whereValue = typeId
            
        # Check name
        if oldName:
            self._checkParameter('name', oldName)
            whereKey = 'install_rel_prop_type_name'
            whereValue = oldName
            
        # Check if where key is set
        if whereKey == None:
            raise ValueError("Id or old name should be present to execute an update!")

        # Check name
        self._checkParameter("name", name)
        queryDict['install_rel_prop_type_name'] = name
        
        # Check description
        if 'description' in kws:
            queryDict['install_rel_prop_type_desc'] = kws['description']
            
        # Check units
        if 'units' in kws:
            queryDict['install_rel_prop_type_units'] = kws['units']

        # Generate SQL
        sqlVals = self._generateUpdateQuery('install_rel_prop_type', queryDict, whereKey, whereValue)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when updating install rel property type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating install rel property type:\n%s (%d)' %(e.args[1], e.args[0]))

    def _retrieveInstallRelProperty(self, installRelId, installRelPropertyTypeId = None, value = None):
        '''
        Retrieve install rel property from the database
        
        parameters:
            - installRelId: id of the install rel entry
            - installRelPropertyTypeId: id of the property type
            - value: value of the property
            
        returns:
            { 'id': {
                    'id': #int,
                    'value': #string,
                    'typename': #string
                }
            }
            
        raises:
            ValueError, MySQLError
        '''
        
        # Generate SQL
        sql = '''
        SELECT
            ip.install_rel__prop_id,
            ip.install_rel_id,
            ip.install_rel_prop_type_id,
            ip.install_rel_prop_value,
            ipt.install_rel_prop_type_name
        FROM install_rel_prop ip
        LEFT JOIN install_rel_prop_type ipt ON (ip.install_rel_prop_type_id = ipt.install_rel_prop_type_id)
        WHERE
        '''
        
        # Add install rel id parameter
        sql += ' ip.install_rel_id = %s '
        vals = [installRelId]

        # Add install rel property type parameter
        if installRelPropertyTypeId:
            sql += ' AND ip.install_rel_prop_type_id = %s '
            vals.append(installRelPropertyTypeId)
        
        sqlVals = (sql, vals)

        # Add value parameter if exists
        if value:
            sqlVals = self._checkWildcardAndAppend('install_rel_prop_value', value, sqlVals[0], sqlVals[1], 'AND')

        try:
            # Retrieve objects from the database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            res = cur.fetchall()
            resdict = {}
            
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'value': r[3],
                    'typename': r[4]
                }
                
            return resdict
            
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving install rel property from the table:\n%s (%s)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when retrieving install rel property from the table:\n%s (%s)' %(e.args[1], e.args[0]))

    def retrieveInstallRelProperty(self, installRelId, installRelPropertyTypeName = None, value = None):
        '''
        Retrieve component type property from the database by name
        
        parameters:
            - installRelId: id of the install rel
            - installRelPropertyTypeName: name of the install rel property type
            - value: value of the property type
            
        returns:
            { 'id': {
                    'id': #int,
                    'value': #string,
                    'typename': #string
                }
            }
            
        raises:
            ValueError
        '''
        
        # Check component type
        #retrieveInstallRel = self.retrieveInstallRel(installRelId)
        
        #if len(retrieveInstallRel) == 0:
        #    raise ValueError("Install rel (%s) doesn't exist in the database!" % installRelId)

        #retrieveInstallRelKeys = retrieveInstallRel.keys()
        #installRelId = retrieveInstallRel[retrieveInstallRelKeys[0]]['id']

        # Check install rel property type
        # of a specific component type
        
        installRelPropertyTypeId = None
        
        if installRelPropertyTypeName:
            retrieveInstallRelPropertyType = self.retrieveInstallRelPropertyType(installRelPropertyTypeName)
            
            if len(retrieveInstallRelPropertyType) == 0:
                raise ValueError("Install rel property type (%s) doesn't exist in the database!" % installRelPropertyTypeName);
    
            retrieveInstallRelPropertyTypeKeys = retrieveInstallRelPropertyType.keys()
            installRelPropertyTypeId = retrieveInstallRelPropertyType[retrieveInstallRelPropertyTypeKeys[0]]['id']

        return self._retrieveInstallRelProperty(installRelId, installRelPropertyTypeId, value)

    def saveInstallRelProperty(self, installRelId, installRelPropertyTypeName, value):
        '''
        Save install rel property into database
        
        params:
            - installRelId: id of the install rel
            - installRelPropertyTypeName: name of the install rel property type
            - value: value of the install rel property
            
        returns:
            {'id': new install rel property id}
            
        raises:
            ValueError, MySQLError
        '''
        
        # Check for previous install rel property
        retrieveInstallRelProperty = self.retrieveInstallRelProperty(installRelId, installRelPropertyTypeName)
        
        if len(retrieveInstallRelProperty) != 0:
            raise ValueError("Install rel property for component type (%s) and property type (%s) already exists in the database!" % (installRelId, installRelPropertyTypeName));
        
        # Check install rel
        retrieveInstallRel = self.retrieveInstallRel(installRelId)
        
        if len(retrieveInstallRel) == 0:
            raise ValueError("Install rel (%s) doesn't exist in the database!" % installRelId)

        #retrieveInstallRelKeys = retrieveInstallRel.keys()
        #installRelId = retrieveInstallRel[retrieveInstallRelKeys[0]]['id']

        # Check install rel property type
        retrieveInstallRelPropertyType = self.retrieveInstallRelPropertyType(installRelPropertyTypeName)
        
        if len(retrieveInstallRelPropertyType) == 0:
            raise ValueError("Install rel property type (%s) doesn't exist in the database!" % installRelPropertyTypeName);

        retrieveInstallRelPropertyTypeKeys = retrieveInstallRelPropertyType.keys()
        installRelPropertyTypeId = retrieveInstallRelPropertyType[retrieveInstallRelPropertyTypeKeys[0]]['id']

        # Generate SQL
        sql = '''
        INSERT INTO install_rel_prop
            (install_rel_id, install_rel_prop_type_id, install_rel_prop_value)
        VALUES
            (%s, %s, %s)
        '''
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (installRelId, installRelPropertyTypeId, value))
            
            # Get last row id
            propid = cur.lastrowid

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': propid}
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when saving install rel property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving install rel property:\n%s (%d)' % (e.args[1], e.args[0]))

    def updateInstallRelProperty(self, installRelParentId, installRelChildId, installRelPropertyTypeName, **kws):
        '''
        Update install rel property
        
        params:
            - installRelParentId: id of the parent in the install rel
            - installRelChildId: id of the child in the install rel
            - installRelPropertyTypeName: name of the install rel property type
            - value: value of the install rel property
            
        returns: True if everything was ok
            
        raises:
            ValueError, MySQLError
        '''
        
        # Define query dictionary
        queryDict = {}
        whereDict = {}
        
        # Check install rel
        retrieveInstallRel = self.retrieveInstallRel(None, installRelParentId, installRelChildId)
        
        if len(retrieveInstallRel) == 0:
            raise ValueError("Install rel doesn't exist in the database!")

        retrieveInstallRelKeys = retrieveInstallRel.keys()
        retrieveInstallRelObject = retrieveInstallRel[retrieveInstallRelKeys[0]]

        whereDict['install_rel_id'] = retrieveInstallRelObject['id']
        
        # Check install rel property type
        retrieveInstallRelPropertyType = self.retrieveInstallRelPropertyType(installRelPropertyTypeName)
        
        if len(retrieveInstallRelPropertyType) == 0:
            raise ValueError("Install rel property type (%s) doesn't exist in the database!" % installRelPropertyTypeName);

        retrieveInstallRelPropertyTypeKeys = retrieveInstallRelPropertyType.keys()
        installRelPropertyTypeId = retrieveInstallRelPropertyType[retrieveInstallRelPropertyTypeKeys[0]]['id']
        whereDict['install_rel_prop_type_id'] = installRelPropertyTypeId

        # Add value parameter into query
        if 'value' in kws:
            queryDict['install_rel_prop_value'] = kws['value']

        # Generate SQL
        sqlVals = self._generateUpdateQuery('install_rel_prop', queryDict, None, None, whereDict)
        
        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return True
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when updating install rel property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating install rel property:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveInstallRel(self, parentInstallId, childInstallId, description = None, order = None, props = None):
        '''
        Save isntall relationship in the database.
        
        params:
            - parentInstallId: id of the parent element
            - childInstallId: id of the child element
            - description: description of the relationship
            - order: order of the child in the relationship
            - props :
                {
                    'key1': 'value1',
                    ...
                    'keyN': 'valueN'
                }
        '''
        
        # Check if the same relationship already exists in the database
        existingRel = self.retrieveInstallRel(None, parentInstallId, childInstallId)
        
        if len(existingRel):
            raise ValueError("Same relationship already exists in the database!")
        
        # Check if parent exists in install
        existingParent = self._retrieveInstallById(parentInstallId)
        
        if len(existingParent) == 0:
            raise ValueError("Parent with id (%s) does not exist in the database!" % parentInstallId)
        
        # Check if child exists in install
        existingChild = self._retrieveInstallById(childInstallId)
        
        if len(existingChild) == 0:
            raise ValueError("Child with id (%s) does not exist in the database!" % childInstallId)
    
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
            cur.execute(sql, (parentInstallId, childInstallId, description, order))
            
            # Get last row id
            idrel = cur.lastrowid
            
            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            # Install rel is saved, now we can save properties
            if props:
                
                # Save each property
                for key in props:
                    value = props[key]
                    self.saveInstallRelProperty(idrel, key, value)
                
            return {'id': idrel}
           
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when saving new install rel:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving new install rel:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateInstallRel(self, parentInstallId, childInstallId, **kws):
        '''
        Update install relationship.
        
        params:
            - parentInstallId: id of the parent element we want ot update by
            - childInstallId: id of the child element we want ot update by
            - description: description of the relationship
            - order: order of the child in the relationship
            - props :
                {
                    'key1': 'value1',
                    ...
                    'keyN': 'valueN'
                }
        '''
        
        # Define query dictionary
        queryDict = {}
        whereDict = {}
        
        # Check if parent exists in install
        existingParent = self._retrieveInstallById(parentInstallId)
        
        if len(existingParent) == 0:
            raise ValueError("Parent with id (%s) does not exist in the database!" % parentInstallId)
        
        whereDict['parent_install_id'] = parentInstallId
        
        # Check if child exists in install
        existingChild = self._retrieveInstallById(childInstallId)
        
        if len(existingChild) == 0:
            raise ValueError("Child with id (%s) does not exist in the database!" % childInstallId)
        
        whereDict['child_install_id'] = childInstallId
        
        # Add description
        if 'description' in kws:
            queryDict['logical_desc'] = kws['description']
        
        # Add order
        if 'order' in kws:
            queryDict['logical_order'] = kws['order']
    
        # Generate SQL
        sqlVals = self._generateUpdateQuery('install_rel', queryDict, None, None, whereDict)
       
        try:
            # Insert entity
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            # Install rel is saved, now we can save properties
            if 'props' in kws and kws['props'] != None:
                props = kws['props']
                
                # Save each property
                for key in props:
                    value = props[key]
                    self.updateInstallRelProperty(parentInstallId, childInstallId, key, value=value)
                
            return True
           
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when updating install rel:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating install rel:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveInstallRel(self, installRelId = None, parentInstallId = None, childInstallId = None, description = None, order = None, date = None, expectedProperty = None):
        '''
        Retrieve install rel from the database. Specific relation can be retrieved or all the children of specific parent or
        all the parents of specific child.
        
        params:
            - installRelId: id of the install_rel table
            - parentInstallId: id of the parent element
            - childInstallId: id of the child element
            - description: description of a relationship
            - order: order number of child element in the parent element; accepts a range in a tuple
            - date: date of the device installation; accepts a range in a tuple
            - prop: if we want to search for relationships with specific property set to a specific value, we
              can prepare a dict and pass it to the function e.g. {'beamline': 'xh*'} will return all of the
              beamlines with names starting with xh or {'beamline': None} will return all of the beamlines
            
        returns:
            {
                'id': {
                    'id':           #int,
                    'parentid':     #int,
                    'childid':      #int,
                    'description':  #string,
                    'order':        #int,
                    'date':         #string,
                    'prop1key':     #string,
                    ...
                    'propNkey':     #string
                }
            }
            
        raises:
            ValueError, MySQLError
        '''
        
        # Create vals list
        vals = []
        
        # Generate SQL
        if expectedProperty == None:
            sql = '''
            SELECT * FROM install_rel ir WHERE 1=1
            '''
        else:
            
            # Check expected property parameter
            if len(expectedProperty) > 1:
                raise ValueError("Expected property dictionary can contain only one key. Current dictionary contains (%s) keys." % len(expectedProperty))
            
            expectedPropertyKeys = expectedProperty.keys()
            
            sql = '''
            SELECT
                ir.install_rel_id,
                ir.parent_install_id,
                ir.child_install_id,
                ir.logical_desc,
                ir.logical_order,
                ir.install_date
            FROM install_rel ir
            LEFT JOIN install_rel_prop irp ON(ir.install_rel_id = irp.install_rel_id)
            LEFT JOIN install_rel_prop_type irpt ON(irp.install_rel_prop_type_id = irpt.install_rel_prop_type_id)
            WHERE irpt.install_rel_prop_type_name = %s
            '''
            
            vals.append(expectedPropertyKeys[0])
            
            # Check if expected property value is not None and append it
            if expectedProperty[expectedPropertyKeys[0]] != None:
                sql = ' AND irp.install_rel_prop_value = %s '
                vals.append(expectedProperty[expectedPropertyKeys[0]])
            
        # Check installRelId parameter
        if installRelId:
            sql += ' AND ir.install_rel_id = %s '
            vals.append(installRelId)
            
        # Check parentInstallId
        if parentInstallId:
            sql += ' AND ir.parent_install_id = %s '
            vals.append(parentInstallId)
            
        # Check childInstallId
        if childInstallId:
            sql += ' AND ir.child_install_id = %s '
            vals.append(childInstallId)
            
        # Check description parameter
        if description:
            sqlVals = self._checkWildcardAndAppend('ir.logical_desc', description, sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]
            
        # Check order parameter
        if order:
            sqlVals = self._checkRangeAndAppend('ir.logical_order', order, sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]
            
        # Check date parameter
        if date:
            sqlVals = self._checkRangeAndAppend('ir.install_date', date, sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]

        try:
            # Execute SQL
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            
            # Get values from the database
            res = cur.fetchall()
            resdict = {}
            
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'parentid': r[1],
                    'childid': r[2],
                    'description': r[3],
                    'order': r[4],
                    'date': r[5].strftime("%Y-%m-%d %H:%M:%S")
                }
                
                # Get the rest of the properties
                properties = self._retrieveInstallRelProperty(r[0])
                
                # Append properties to existing object
                for prop in properties:
                    obj = properties[prop]
                    resdict[r[0]][obj['typename']] = obj['value']
                    
            return resdict
        
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching install rel:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching install rel:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveInsertionDevice(self, installName, **kws):
        '''Save insertion device installation using any of the acceptable key words:

        - installName: installation name, which is its label on field
        - beamline: name of beamline
        - beamlinedesc: description of beamline
        - beamlineproject: project name what this beamline belongs to
        - center: coordinate center
        - straight: straight section name
        - straightdesc: straight section description
        - straightoptics: beam optics for this straight section, for example high beta, low beta, dispersion
        
        1. insertion device name;
        2. girder;
        3. cell;
        4. straight section name;
        5. straight section description (long straight section, short straight section, or bending magnet);
        6. straight section charge particle optics description;
        7. install place (up, center, or down);
        '''

    def saveInstall(self, installname, **kws):
        '''Save insertion device installation using any of the acceptable key words:

        - installname: installation name, which is its label on field
        - description: installation description
        - cmpnttype: component type of the device
        - coordinatecenter: coordinate center number
        
        raises:
            ValueError, MySQLError
            
        returns:
            {'id': new install id}
        '''
        
        # Check name parameter
        self._checkParameter('name', installname)
        
        # Check component type
        if 'cmpnttype' in kws and kws['cmpnttype'] != None:
            componentType = self.retrieveComponentType(kws['cmpnttype'])
            componentTypeKeys = componentType.keys()
        
        else:
            raise ValueError("Cmpnttype attribute should be present when inserting new installation!")
        
        # Check install description
        description = None
        
        if 'description' in kws and kws['description'] != None:
            description = kws['description']
            
        # Check coordinate center
        coordinate = None
        
        if 'coordinatecenter' in kws and kws['coordinatecenter'] != None:
            coordinate = kws['coordinatecenter']
            
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
            cur.execute(sql, (componentType[componentTypeKeys[0]]['id'], installname, description, coordinate))
        
            # Get last row id
            invid = cur.lastrowid
            
            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': invid}
        
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving new inventory:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving new inventory:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateInstall(self, installId, oldInstallName, installName, **kws):
        '''Update insertion device installation using any of the acceptable key words:

        - installName: installation name, which is its label on field
        - description: installation description
        - cmpnttype: component type of the device
        - coordinatecenter: coordinate center number
        
        raises:
            ValueError, MySQLError
            
        returns:
            True if everything is ok
        '''
        
        # Define query dictionary
        queryDict = {}
        whereKey = None
        whereValue = None
        
        # Check id
        if installId:
            self._checkParameter('id', installId, 'prim')
            whereKey = 'install_id'
            whereValue = installId
        
        # Check name
        if oldInstallName:
            self._checkParameter('name', oldInstallName)
            whereKey = 'field_name'
            whereValue = oldInstallName
            
        # Check if where key is set
        if whereKey == None:
            raise ValueError("Id or old name should be present to execute an update!")
        
        # Check name parameter
        self._checkParameter('name', installName)
        queryDict['field_name'] = installName
        
        # Check component type
        if 'cmpnttype' in kws:
            componentType = self.retrieveComponentType(kws['cmpnttype'])
            componentTypeKeys = componentType.keys()
            queryDict['cmpnt_type_id'] = componentType[componentTypeKeys[0]]
        
        # Check install description
        if 'description' in kws:
            description = kws['description']
            queryDict['location'] = description
            
        # Check coordinate center
        if 'coordinatecenter' in kws:
            coordinate = kws['coordinatecenter']
            queryDict['coordinate_center'] = coordinate
            
        # Generate SQL
        sqlVals = self._generateUpdateQuery('install', queryDict, whereKey, whereValue)
        
        try:
            # Insert record into database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
        
            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return True
        
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when updating inventory:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating inventory:\n%s (%d)' %(e.args[1], e.args[0]))

    def _retrieveInstallById(self, installid):
        '''
        Retrieve install its id.
        
        params:
            - installid: id of the install entity
            
        raises:
            ValueError, MySQLError
            
        returns:
            {'id': {
                    'id':                  #int,
                    'cmpnttype':           #string,
                    'name':                #string,
                    'description':         #string,
                    'coordinationcenter':  #float
                }
            }
        '''
        
        # Check install id
        if installid == None:
            raise ValueError("Install id should be present!")
        
        # Get install name from the database
        sql = '''
        SELECT field_name FROM install WHERE install_id = %s
        '''
        
        # Define install name
        installname = None
        
        try:
            # Execute SQL
            cur = self.conn.cursor()
            cur.execute(sql, installid)
            res = cur.fetchall()
            
            if len(res) != 1:
                raise ValueError("Install with id (%s) doesn't exist in the database!" % installid)
            
            # Get install name
            installname = res[0][0]
            return self.retrieveInstall(installname)
            
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching install from the database:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching install from the database:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveInstall(self, install_name, **kws):
        '''Retrieve insertion device installation using any of the acceptable key words:

        - install_name: installation name, which is its label on field
        - description: installation description
        - cmpnttype: component type name of the device
        - coordinatecenter: coordinate center number
        
        raises:
            ValueError, MySQLError
            
        returns:
            {'id': {
                    'id':                #int,
                    'name':              #string,
                    'description':       #string,
                    'cmpnttype':         #string,
                    'coordinatecenter':  #float
                }
            }
        '''
        
        # Check name
        self._checkParameter('name', install_name)
        
        # Generate SQL
        sql = '''
        SELECT
            inst.install_id,
            inst.cmpnt_type_id,
            inst.field_name,
            inst.location,
            inst.coordinate_center,
            ct.cmpnt_type_name
        FROM install inst
        LEFT JOIN cmpnt_type ct ON(inst.cmpnt_type_id = ct.cmpnt_type_id)
        WHERE
        '''
        
        vals = []
        
        # Append name parameter
        sqlVals = self._checkWildcardAndAppend('inst.field_name', install_name, sql, vals)
        
        # Append description parameter
        if 'description' in kws and kws['description'] != None:
            sqlVals = self._checkWildcardAndAppend('inst.location', kws['description'], sqlVals[0], sqlVals[1], 'AND')
            
        # Append component type parameter
        if 'cmpnttype' in kws and kws['cmpnttype'] != None:
            sqlVals = self._checkWildcardAndAppend('ct.cmpnt_type_name', kws['cmpnttype'], sqlVals[0], sqlVals[1], 'AND')

        # Append coordination center parameter
        if 'coordinatecenter' in kws and kws['coordinatecenter'] != None:
            sqlVals = self._checkRangeAndAppend('inst.coordinate_center', kws['coordinatecenter'], sqlVals[0], sqlVals[1], 'AND')

        try:
            # Execute SQL
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            # Get last id
            res = cur.fetchall()
            resdict = {}
            
            # Construct return dict
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'name': r[2],
                    'description': r[3],
                    'cmpnttype': r[5],
                    'coordinatecenter': r[4]
                }
                
            return resdict
        
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching installation:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching installation:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveOnlineData(self, install_name, **kws):
        '''Save insertion device online data using any of the acceptable key words:

        - install_name
        - username
        - description
        - url
        - status

        The data itself is stored on server's harddisk because its size might blow up to GB level.
        Ths file url is stored in the database.

        :param install_name: device name that the data belongs to
        :type install_name: str

        :param username: author who updated this data entry
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param url: external url of the data file is stored
        :type url: str

        :param status: status of this data set
        :type status: int

        :return: a map with structure like:

            .. code-block:: python

                {'id': data id}

        :Raises: ValueError, MySQLError
        '''
        
        # Check install name
        self._checkParameter('name', install_name)
            
        returnedInstall = self.retrieveInstall(install_name)
        
        if len(returnedInstall) == 0:
            raise ValueError("Install (%s) does not exist in the database!" % install_name)
        
        returnedInstallKeys = returnedInstall.keys()
        installid = returnedInstall[returnedInstallKeys[0]]['id']
            
        # Check username
        username = None
        
        if 'username' in kws and kws['username'] != None:
            username = kws['username']
            
        # Check description
        description = None
        
        if 'description' in kws and kws['description'] != None:
            description = kws['description']
            
        # Check url
        url = None
        
        if 'url' in kws and kws['url'] != None:
            url = kws['url']
            
        # Check status
        status = None
        
        if 'status' in kws and kws['status'] != None:
            status = kws['status']
            
        # Generate SQL
        sql = '''
        INSERT INTO id_online_data (
            install_id,
            login_name,
            description,
            data_url,
            date,
            status
        ) VALUES (
            %s, %s, %s, %s, NOW(), %s
        )
        '''
        
        try:
            # Insert data into database
            cur = self.conn.cursor()
            cur.execute(sql, (installid, username, description, url, status))
            
            # Get last row id
            onlinedataid = cur.lastrowid
            
            # Create transactions
            if self.transaction == None:
                self.conn.commit()
            
            return {'id': onlinedataid}
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving new online data:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving new online data:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveOnlineData(self, **kws):
        '''Retrieve insertion device online data using any of the acceptable key words:

        - onlineid
        - install_name
        - username
        - description
        - url
        - status

        :param onlineid: id of the online data we want to update by
        :type onlineid: int

        :param install_name: device name that the data belongs to
        :type install_name: str

        :param username: author who updated this data entry
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param url: external url of the data file is stored
        :type url: str

        :param status: status of this data set
        :type status: int

        :return: a map with structure like:

            .. code-block:: python

                {'id': {
                        'id':,            #int
                        'installid':,     #int
                        'install_name':,  #string
                        'username':,      #string
                        'description':,   #string
                        'url':,           #url
                        'date':,          #date
                        'status':,        #int
                    }
                }

        :Raises: ValueError, MySQLError
        '''
        
        # Generate SQL
        sql = '''
        SELECT
            iod.id_online_data_id,
            iod.install_id,
            iod.login_name,
            iod.description,
            iod.data_url,
            iod.date,
            iod.status,
            inst.field_name
        FROM id_online_data iod
        LEFT JOIN install inst ON(iod.install_id = inst.install_id)
        WHERE 1=1
        '''
        
        vals = []
        
        # Append online id
        if 'onlineid' in kws and kws['onlineid'] != None:
            self._checkParameter('id', kws['onlineid'], 'prim')
            sql += ' AND id_online_data_id = %s '
            vals.append(kws['onlineid'])
            
        # Append username
        if 'username' in kws and kws['username'] != None:
            sqlVals = self._checkWildcardAndAppend('iod.login_name', kws['username'], sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]
            
        # Append description
        if 'description' in kws and kws['description'] != None:
            sqlVals = self._checkWildcardAndAppend('iod.description', kws['description'], sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]
            
        # Append url
        if 'url' in kws and kws['url'] != None:
            sqlVals = self._checkWildcardAndAppend('iod.data_url', kws['url'], sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]
            
        # Append status
        if 'status' in kws and kws['status'] != None:
            sqlVals = self._checkRangeAndAppend('iod.status', kws['status'], sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]
            
        # Append install name
        if 'install_name' in kws and kws['install_name'] != None:
            sqlVals = self._checkWildcardAndAppend('inst.field_name', kws['install_name'], sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]
            
        try:
            # Execute SQL
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            
            # Get all records
            res = cur.fetchall()
            resdict = {}
            
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'installid': r[1],
                    'install_name': r[7],
                    'username': r[2],
                    'description': r[3],
                    'url': r[4],
                    'date': r[5].strftime("%Y-%m-%d %H:%M:%S"),
                    'status': r[6]
                }
            
            return resdict
            
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching online data:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching online data:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateOnlineData(self, online_data_id, **kws):
        '''update insertion device online data using any of the acceptable key words:

        - install_name
        - username
        - description
        - url
        - status

        The data itself is stored on server's harddisk because its size might blow up to GB level.
        Ths file url is stored in the database.

        :param install_name: device name that the data belongs to
        :type install_name: str

        :param username: author who updated this data entry
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param url: external url of the data file is stored
        :type url: str

        :param status: status of this data set
        :type status: int

        :return: True if everything is ok

        :Raises: ValueError, MySQLError
        '''
        
        # Define query dict
        queryDict = {}
        
        # Check id
        self._checkParameter('id', online_data_id, 'prim')
        whereKey = 'id_online_data_id'
        whereValue = online_data_id
        
        # Check install name
        if 'install_name' in kws and kws['install_name'] != None:
            installname = kws['install_name']
            
            returnedInstall = self.retrieveInstall(installname)
            
            if len(returnedInstall) == 0:
                raise ValueError("Install (%s) does not exist in the database!" % installname)
            
            returnedInstallKeys = returnedInstall.keys()
            installid = returnedInstall[returnedInstallKeys[0]]['id']
            queryDict['install_id'] = installid
            
        # Check username
        if 'username' in kws:
            queryDict['login_name'] = kws['username']
            
        # Check description
        if 'description' in kws:
            queryDict['description'] = kws['description']
            
        # Check url
        if 'url' in kws:
            queryDict['url'] = kws['url']
            
        # Check status
        if 'status' in kws:
            queryDict['status'] = kws['status']
            
        # Generate SQL
        sqlVals = self._generateUpdateQuery('id_online_data', queryDict, whereKey, whereValue)
        
        try:
            # Insert offline data into database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            # Create transactions
            if self.transaction == None:
                self.conn.commit()
                
            return True
        
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when updating online data:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating online data:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveInstallOfflineData(self, install_name, **kws):
        '''Retrieve insertion device offline data using any of the acceptable key words:

        - install_name
        - description
        - gap
        - phase1
        - phase2
        - phase3
        - phase4
        - phasemode
        - polarmode
        - status

        :param install_name: name of installed device on field
        :type install_name: str

        :param description: a brief description for this data entry
        :type description: str

        :param gap: gap when this data set is produced
        :type gap: float

        :param phase1: phase 1 when this data set is produced
        :type phase1: float

        :param phase2: phase 2 when this data set is produced
        :type phase2: float

        :param phase3: phase 3 when this data set is produced
        :type phase3: float

        :param phase4: phase 4 when this data set is produced
        :type phase4: float

        :param phasemode: description for the mode of phase, which is determined by gap/phase
        :type phasemode: str

        :param polarmode: description for the mode of polar, which is determined by gap/phase
        :type polarmode: str

        :param status: status of this data set
        :type status: int

        :return: a map with structure like:

            .. code-block:: python

                {'data_id': {
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
                        'resultfile':,     # string
                        'resultfiletime':, # string
                        'scriptfile':,     # string
                        'script':,         # string
                        'data':,           # JSON string
                        'methodname':,     # string
                        'methoddesc':,     # string
                    }
                }

        :Raises: ValueError, MySQLError
        '''
        
        # Check name
        self._checkParameter('name', install_name)
        
        # Generate select SQL
        sql = '''
        SELECT
            inst.install_id,
            ii.inventory_id,
            inv.name
        FROM install inst
        LEFT JOIN inventory__install ii ON(inst.install_id = ii.install_id)
        LEFT JOIN inventory inv ON(ii.inventory_id = inv.inventory_id)
        WHERE
        '''
        
        # Check description
        description = None
        
        if 'description' in kws and kws['description'] != None:
            description = kws['description']
        
        # Check gap
        gap = None
        
        if 'gap' in kws and kws['gap'] != None:
            gap = kws['gap']
        
        # Check phase1
        if 'phase1' in kws and kws['phase1'] != None:
            phase1 = kws['phase1']
        
        # Check phase2
        if 'phase2' in kws and kws['phase2'] != None:
            phase2 = kws['phase2']
        
        # Check phase3
        if 'phase3' in kws and kws['phase3'] != None:
            phase3 = kws['phase3']
        
        # Check phase4
        if 'phase4' in kws and kws['phase4'] != None:
            phase4 = kws['phase4']
        
        # Check phasemode
        if 'phasemode' in kws and kws['phasemode'] != None:
            phasemode = kws['phasemode']
        
        # Check polarmode
        if 'polarmode' in kws and kws['polarmode'] != None:
            polarmode = kws['polarmode']
        
        # Check status
        if 'status' in kws and kws['status'] != None:
            status = kws['status']
        
        vals = []
        
        # Append name parameter
        sqlVals = self._checkWildcardAndAppend('inst.field_name', install_name, sql, vals)
        
        try:
            # Execute SQL
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            # Get last id
            res = cur.fetchall()
            resdict = {}
            
            # Construct return dict
            for r in res:
                inventoryname = r[2]
                results = self.retrieveOfflineData(inventory_name=inventoryname, description=description, gap=gap, phase1=phase1, phase2=phase2, phase3=phase3, phase4=phase4, phasemode=phasemode, polarmode=polarmode, status=status)
            
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching offline data from installation:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching offline data from installation:\n%s (%d)' %(e.args[1], e.args[0]))