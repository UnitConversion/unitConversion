import logging
import MySQLdb

from collections import OrderedDict
from utils import (_wildcardformat)
from _mysql_exceptions import MySQLError

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
    
    def _checkParameter(self, parameterKey, parematerValue, parameterTypeWeAreCheckingFor = "string"):
        '''
        Check different types of input parameters. Parameter should match agreed criteria or exception will be thrown
        
        parameters:
            - parameterKey: name of the parameter
            - parameterValue: value of the parameter
            - parameterTypeWeAreCheckingFor: which type are we chacking
            
        raise:
            ValueError if parameter don'r match agreed criteria
        '''
        
        # Check string
        if parameterTypeWeAreCheckingFor == "string":
            
            if not isinstance(parematerValue, (str, unicode)):
                raise ValueError("Parameter %s is missing!" % parameterKey)

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

                {'id': {'name': ,
                        'description': }
                 ...
                }

        :Raises: ValueError, exception
        '''

        # Check for vendor name parameter
        if not isinstance(name, (str, unicode)):
            raise ValueError("Vendor name parameter is missing!")

        # Generate SQL statement
        vals = []
        sql = '''
        SELECT vendor_id, vendor_name, vendor_description FROM vendor WHERE vendor_name
        '''

        # Check if user wants all the vendors
        if name == "*":
            sql += ""
        
        # Check for wildcard characters
        elif "*" in name or "?" in name:
            sql += " like %s "
            vals.append(_wildcardformat(name))
            
        # Check all of the other options
        else:
            sql += " = %s "
            vals.append(name)

        # Does description exist?
        if description != None:
            
            # Check if user wants all possible descriptions
            if description == "*":
                sql += ""
            
            # Check for wildcard characters in description
            elif "*" in description or "?" in description:
                sql += " and vendor_description like %s "
                vals.append(_wildcardformat(description))
                
            # Check for all the other options
            else:
                sql += " and vendor_description = %s "
                vals.append(description)

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sql, vals)

            # Get any one since it should be unique
            res = cur.fetchall()
            resdict = {}

            # Generate return dictionary
            for r in res:
                resdict[r[0]] = {'name': r[1], 'description': r[2]}

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching vendor:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when fetching vendor:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveVendor(self, name, description=None):
        '''Save vendor and its description into database

        :param name: vendor name
        :type name: str
        
        :param dtype: device type

        :param description: a brief description which could have up to 255 characters
        :type description: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': vendor_id}

        :Raises: ValueError, Exception
        '''
        
        # Check for vendor name parameter
        if not isinstance(name, (str, unicode)):
            raise ValueError("Vendor name parameter is missing!")

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
            raise Exception('Error when saving vendor:\n%s (%d)' %(e.args[1], e.args[0]))

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

        :Raises: ValueError, Exception
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
            raise Exception('Error when fetching inventory property template:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveInventoryPropertyTemplate(self, cmpntType, name, description = None, default = None, unit = None):
        '''
        Insert new inventory property template into database

        - cmpnttype: component type name M
        - name: property template name M
        - description: property template description O
        - default: property template default value O
        - unit: property template unit O

        :return: a map with structure like:

            .. code-block:: python

                {'id': propertytemplateid}

        :Raises: ValueError, Exception
        '''

        # Raise an error if inventory property template exists
        existingInventoryPropertyTemplate = self.retrieveInventoryPropertyTemplate(name)
        
        if len(existingInventoryPropertyTemplate):
            raise ValueError("Inventory property template (%s) already exists in the database!" % name)

        # Check component type
        result = self.retrieveComponentType(cmpntType);

        if len(result) == 0:
            raise ValueError("Component type (%s) does not exist in the database." % (cmpntType))

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
            raise Exception('Error when saving new inventory property template:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveInventoryProperty(self, inventoryName, inventoryPropertyTemplateName = None, value = None, checkForInventory = True):
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
            
        raises:
            ValueError, Exception
        '''
        
        # Check inventory
        if checkForInventory:
            retrieveInventory = self.retrieveInventory(inventoryName)
            
            if len(retrieveInventory) == 0:
                raise ValueError("Inventory (%s) doesn't exist in the database!" % inventoryName)

            retrieveInventoryKeys = retrieveInventory.keys()
            inventoryId = retrieveInventory[retrieveInventoryKeys[0]]['id']

        # Check inventory property template
        # of a specific inventory
        if inventoryPropertyTemplateName:
            retrieveInventoryPropertyTemplate = self.retrieveInventoryPropertyTemplate(inventoryPropertyTemplateName)
            
            if len(retrieveInventoryPropertyTemplate) == 0:
                raise ValueError("Inventory property template (%s) doesn't exist in the database!" % inventoryPropertyTemplateName);
    
            retrieveInventoryPropertyTemplateKeys = retrieveInventoryPropertyTemplate.keys()
            inventoryPropertyTemplateId = retrieveInventoryPropertyTemplate[retrieveInventoryPropertyTemplateKeys[0]]['id']

        # Generate SQL
        sql = '''
        SELECT 
            inventory_prop_id, inventory_prop_value, inventory_prop_tmplt_id, inventory_id
        FROM inventory_prop
        WHERE
        '''
        
        # Add inventory_id parameter
        sql += ' inventory_id = %s '
        vals = [inventoryId]

        # Add inventory_prop_tmplt_id parameter
        if inventoryPropertyTemplateName:
            sql += ' AND inventory_prop_tmplt_id = %s '
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
                    'inventoryname': inventoryName,
                    'templatename': inventoryPropertyTemplateName
                }
                
            return resdict
            
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieve id and vale from inventory property table:\n%s (%s)' %(e.args[1], e.args[0]))
            raise Exception('Error when retrieve id and vale from inventory property table:\n%s (%s)' %(e.args[1], e.args[0]))

    def saveInventoryProperty(self, inventoryName, inventoryPropertyTemplateName, value):
        
        # Check value parameter
        self._checkParameter('value', value)
        
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
            raise Exception('Error when saving inventory property value:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveInventory(self, name, **kws):
        '''
        save insertion device into inventory using any of the acceptable key words:

        - name:  name to identify that device from vendor
        - compnttype: device type name
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

        :Raises: ValueError, Exception

        '''

        # Check name parameter
        res = self.retrieveInventory(name)
        
        if len(res) != 0:
            raise ValueError("Inventory (%s) already exists in inventory." % (name))

        # Check device type parameter
        compnttypeid=None

        if kws.has_key('compnttype') and kws['compnttype'] != None:
            
            # Check component type parameter
            self._checkParameter("component type", kws['compnttype'])
            
            res = self.retrieveComponentType(kws['compnttype'])
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

        # Check properties parameter
        props=None

        if kws.has_key('props') and kws['props'] != None:
            props = kws['props']
            
            # Save all the properties
            for key in props:
                value = props[key]
                
                # Save it into database
                self.saveInventoryProperty(name, key, value)
            
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
                
            return {'id': invid}
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving new inventory:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when saving new inventory:\n%s (%d)' %(e.args[1], e.args[0]))


    def retrieveInventory(self, invname):
        '''Retrieve an insertion device from inventory by device inventory name and type.
        Wildcard matching is supported for inventory name and device type. ::

            * for multiple characters matching
            ? for single character matching


        :param invname: insertion device inventory name, which is usually different from its field name (the name after installation).
        :type invname: str

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

        :Raises: ValueError, Exception
        '''

        # Check name parameter
        self._checkParameter('name', invname)
        
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
        sqlVals = self._checkWildcardAndAppend('inv.name', invname, sql, vals)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            # get any one since it should be unique
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
                #properties = self.retrieveInventoryProperty(r[1], checkForInventory = False)
                
                # Append properties to existing object
                #for property in properties:
                #    object = properties[property]
                #    resdict[r[0]][object['templatename']] = object['value']
            
            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching insertion device inventory:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when fetching insertion device inventory:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateinventory(self, name, **kws):
        '''Update an insertion device properties in its inventory using any of the acceptable key words:

        - name:  name to identify that device from vendor
        - dtype: device type name
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

                {'status': True/False}

        :Raises: KeyError, AttributeError

        '''

    def saveofflinedata(self, **kws):
        '''
        save insertion device offline data using any of the acceptable key words:

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

        :Raises: KeyError, AttributeError
        '''

    def updateofflinedata(self, **kws):
        '''
        update insertion device offline data using any of the acceptable key words:

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

        :param username: author who updated this data entry
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

                {'status': True/False}

        :Raises: KeyError, AttributeError
        '''

    def retrieveofflinedata(self, **kws):
        '''Retrieve insertion device offline data using any of the acceptable key words:

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
                            'data':,           # string
                            'methodname':,     # string
                            'methoddesc':,     # string
                            }
                }

        :Raises: KeyError, AttributeError

        '''

    def savedatamethod(self, name, desc=None):
        '''Save a method with its description which is used when producing data set for an insertion device.

        :param name: name of the method
        :type name: str

        :param desc: description of this method
        :type desc: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': method_id}

        :Raises: KeyError, AttributeError

        '''

    def retrievedatamethod(self, name, desc=None):
        '''Retrieve a method name and its description which is used when producing data set for an insertion device.

        :param name: name of the method
        :type name: str

        :param desc: description of this method
        :type desc: str

        :return: a map with structure like:

            .. code-block:: python

                {'name': method name,
                 'description': description of this method
                }

        :Raises: KeyError, AttributeError
        '''

    def saveinventorytoinstall(self, installname, invname):
        '''Link a device as installed once it is installed into field using the key words:
        - installname
        - invname

        :param installname: label name after installation
        :type installname: str

        :param invname: name in its inventory
        :type invname: str

        :return: a map with structure like:

            .. code-block:: python

                {'result': True/False}

        :Raises: KeyError, AttributeError
        '''

    def updateinstalledinventory(self, installname, invname):
        '''Update a device as installed when its installation has been changed using the key words:

        - installname
        - invname

        :param installname: label name after installation
        :type installname: str

        :param invname: name in its inventory
        :type invname: str

        :return: a map with structure like:

            .. code-block:: python

                {'result': True/False}

        :Raises: KeyError, AttributeError
        '''

    def saveComponentType(self, dtype, description=None):
        '''Save a component type using the key words:

        - dtype
        - description

        :param dtype: device type name
        :type dtype: str

        :param description: description for this device
        :type desctiprion: str

        :return: a map with structure like:

            .. code-block: python

                {'id': device type id}

        :Raises: ValueError, Exception

        '''

        # Check device type
        self._checkParameter("component type", dtype)

        # Check if component type already exists
        componenttype = self.retrieveComponentType(dtype, description);
        
        if len(componenttype):
            raise ValueError("Component type (%s) already exists in the database!" % dtype);

        # Save it into database and return its new id
        sql = ''' INSERT into cmpnt_type (cmpnt_type_name, description) VALUES (%s, %s) '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (dtype, description))
            componenttypeid = cur.lastrowid

            # Commit transaction
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': componenttypeid}

        except MySQLError as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
                
            self.logger.info('Error when saving component type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when saving component type:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveComponentType(self, dtype, description=None):
        '''Retrieve a component type using the key words:

        - dtype
        - description

        :param dtype: device type name
        :type dtype: str

        :param description: description for this device
        :type desctiprion: str

        :return: a map with structure like:

            .. code-block: python

                {'id1': {'id': device type id, 'name': device type name, 'description': device type description},
                 ...
                }

        :Raises: ValueError, Exception
        '''

        # Check component type parameter
        self._checkParameter("component type", dtype)

        # Start SQL
        sql = '''
        SELECT cmpnt_type_id, cmpnt_type_name, description FROM cmpnt_type WHERE
        '''

        vals = []

        # Append component type
        sqlAndVals = self._checkWildcardAndAppend("cmpnt_type_name", dtype, sql, vals)

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

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching component type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when fetching component type:\n%s (%d)' %(e.args[1], e.args[0]))

    def updatecomponenttype(self, dtype, description):
        '''Update description of a device type.
        Once a device type is saved, it is not allowed to change it again since it will cause potential colflict.

        - dtype
        - description

        :param dtype: device type name
        :type dtype: str

        :param description: description for this device
        :type desctiprion: str

        :return: a map with structure like:

            .. code-block: python

                {'result': True/False}

        :Raises: KeyError, AttributeError
        '''

    def saveinstall(self, installname, **kws):
        '''Save insertion device installation using any of the acceptable key words:

        - installname: installation name, which is its label on field
        - beamline: name of beamline
        - beamlinedesc: description of beamline
        - beamlineproject: project name what this beamline belongs to
        - center: coordinate center
        - straight: straight section name
        - straightdesc: straight section description
        - straightoptics: beam optics for this straight section, for example high beta, low beta, dispersion
        '''

    def updateinstall(self, installname, **kws):
        '''Update insertion device installation using any of the acceptable key words:

        - installname: installation name, which is its label on field
        - beamline: name of beamline
        - beamlinedesc: description of beamline
        - beamlineproject: project name what this beamline belongs to
        - center: coordinate center
        - straight: straight section name
        - straightdesc: straight section description
        - straightoptics: beam optics for this straight section, for example high beta, low beta, dispersion

        '''

    def retrieveinstall(self, installname, **kws):
        '''Retrieve insertion device installation using any of the acceptable key words:

        - installname: installation name, which is its label on field
        - beamline: name of beamline
        - beamlinedesc: description of beamline
        - beamlineproject: project name what this beamline belongs to
        - center: coordinate center
        - straight: straight section name
        - straightdesc: straight section description
        - straightoptics: beam optics for this straight section, for example high beta, low beta, dispersion
        '''

    def saveonlinedata(self, **kws):
        '''Save insertion device online data using any of the acceptable key words:

        - installname
        - username
        - description
        - url
        - data
        - meastime
        - status

        The data itself is stored on server's harddisk because its size might blow up to GB level.
        Ths file url is stored in the database.

        :param installname: device name that the data belongs to
        :type installname: str

        :param username: author who updated this data entry
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param url: external url of the data file is stored
        :type url: str

        :param data: real data file, which could be in binary or ASCII format
        :type data: object

        :param meastime: time when this data is measured
        :type meastime: timestamp

        :param status: status of this data set
        :type status: int

        :return: a map with structure like:

            .. code-block:: python

                {'id': data id}

        :Raises: KeyError, AttributeError
        '''

    def updateonlinedata(self, **kws):
        '''update insertion device online data using any of the acceptable key words:

        - installname
        - username
        - description
        - url
        - data
        - meastime
        - status

        The data itself is stored on server's harddisk because its size might blow up to GB level.
        Ths file url is stored in the database.

        :param installname: device name that the data belongs to
        :type installname: str

        :param username: author who updated this data entry
        :type username: str

        :param description: a brief description for this data entry
        :type description: str

        :param url: external url of the data file is stored
        :type url: str

        :param data: real data file, which could be in binary or ASCII format
        :type data: object

        :param meastime: time when this data is measured
        :type meastime: timestamp

        :param status: status of this data set
        :type status: int

        :return: a map with structure like:

            .. code-block:: python

                {'status': True/False}

        :Raises: KeyError, AttributeError
        '''

    def retrieveonlinedata(self, **kws):
        '''Retrieve insertion device online data using any of the acceptable key words:

        - installname
        - description
        - meastime
        - status

        :param installname: name of installed device on field
        :type installname: str

        :param description: a brief description for this data entry
        :type description: str

        :param meastime: time when this data is measured
        :type meastime: timestamp

        :param status: status of this data set
        :type status: int

        :return: a map with structure like:

            .. code-block:: python

                {'data id': {'username': ,
                             'description': ,
                             'meastime': ,
                             'date':
                             'status':,
                             'data': , # should it be an file url?
                            }
                }

        :Raises: KeyError, AttributeError
        '''

    def retrievinstalleofflinedata(self, **kws):
        '''Retrieve insertion device offline data using any of the acceptable key words:

        - installname
        - description
        - gap
        - phase1
        - phase2
        - phase3
        - phase4
        - phasemode
        - polarmode
        - status

        :param installname: name of installed device on field
        :type installname: str

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

        :Raises: KeyError, AttributeError

        '''