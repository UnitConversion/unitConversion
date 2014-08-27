'''
Created on Feb 10, 2014

@author dejan.dezman@cosylab.com
'''

import logging
import MySQLdb
import os
import base64
import time

from utils import (_generateFilePath, _checkParameter, _checkWildcardAndAppend, _generateUpdateQuery, _checkRangeAndAppend)
from _mysql_exceptions import MySQLError
from pyphysics.physics import physics

try:
    from django.utils import simplejson as json
except ImportError:
    import json


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

        self.physics = physics(conn, transaction)

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

        :return: a map with structure like:

            .. code-block:: python

                {'id': {
                    'id': ,
                    'name': ,
                    'description':
                    }
                 ...
                }
        '''

        # Get any one since it should be unique
        res = self.physics.retrieveVendor(name, description)
        resdict = {}

        # Generate return dictionary
        for r in res:
            resdict[r[0]] = {
                'id': r[0],
                'name': r[1],
                'description': r[2]
            }

        return resdict

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
        '''

        # Get last row id
        vendorid = self.physics.saveVendor(name, description)
        return {'id': vendorid}

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
            _checkParameter('id', vendor_id, 'prim')
            whereKey = 'vendor_id'
            whereValue = vendor_id

        # Check old name
        if old_name:
            _checkParameter('name', old_name)
            whereKey = 'vendor_name'
            whereValue = old_name

        # Check where condition
        if whereKey is None:
            raise ValueError("Vendor id or old vendor name should be present to execute an update!")

        # Check for vendor name parameter
        _checkParameter('name', name)
        queryDict['vendor_name'] = name

        # Append description
        if 'description' in kws:
            queryDict['vendor_description'] = kws['description']

        # Generate SQL
        sqlVals = _generateUpdateQuery('vendor', queryDict, whereKey, whereValue)

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating vendor:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating vendor:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveInventoryPropertyTemplate(self, name, cmpnt_type=None):
        '''
        Retrieve inventory property template by its name

        :param name: Inventory property name
        :type name: str

        :param cmpnt_type: component type name
        :type cmpnt_type: str

        :return: a map with structure like:

            .. code-block:: python

                {
                    'id': {
                        'id': ,             # int
                        'cmpnt_type': ,     # string
                        'name': ,           # string
                        'description': ,    # string
                        'default': ,        # string
                        'unit':             # string
                    }
                }

        :Raises: ValueError, MySQLError
        '''

        # Check for vendor name parameter
        _checkParameter('name', name)

        # Append component type id
        cmpnt_type_id = None

        if cmpnt_type is not None:
            cmpnt = self.retrieveComponentType(cmpnt_type)

            if len(cmpnt) == 0:
                raise ValueError("Component type (%s) doesn't exist in the database!" % cmpnt_type)

            cmpntKeys = cmpnt.keys()
            cmpnt_type_id = cmpnt[cmpntKeys[0]]['id']

        resdict = {}
        res = self.physics.retrieveInventoryPropertyTemplate(name, cmpnt_type_id)

        # Construct return dict
        for r in res:
            resdict[r[0]] = {
                'id': r[0],
                'name': r[1],
                'description': r[2],
                'default': r[3],
                'unit': r[4],
                'cmpnt_type': r[5]
            }

        return resdict

    def saveInventoryPropertyTemplate(self, cmpnt_type, name, description=None, default=None, unit=None):
        '''
        Insert new inventory property template into database

        :param cmpnt_type: component type name M
        :type cmpnt_type: str

        :param name: property template name M
        :type name: str

        :param description: property template description O
        :type description: str

        :param default: property template default value O
        :type default: str

        :param unit: property template unit O
        :type unit: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': propertytemplateid}

        :Raises: ValueError, MySQLError
        '''

        # Raise an error if inventory property template exists
        existingInventoryPropertyTemplate = self.retrieveInventoryPropertyTemplate(name, cmpnt_type)

        if len(existingInventoryPropertyTemplate):
            raise ValueError("Inventory property template (%s) already exists in the database!" % name)

        # Check component type
        result = self.retrieveComponentType(cmpnt_type)

        if len(result) == 0:
            raise ValueError("Component type (%s) does not exist in the database." % (cmpnt_type))

        cmpnt_typeid = result.keys()[0]

        # Check name
        _checkParameter("name", name)

        result = self.physics.saveInventoryPropertyTemplate(name, cmpnt_typeid, description, default, unit)

        return {'id': result}

    def updateInventoryPropertyTemplate(self, tmplt_id, cmpnt_type, name, **kws):
        '''
        Update inventory property template in a database

        :param tmplt_id: property template id M
        :type tmplt_id: int

        :param cmpnt_type: component type name M
        :type cmpnt_type: str

        :param name: property template name M
        :type name: str

        :param description: property template description O
        :type description: str

        :param default: property template default value O
        :type default: str

        :param unit: property template unit O
        :type unit: str

        :return: True if update succeeded

        :Raises: ValueError, MySQLError
        '''

        # Set query dict
        queryDict = {}
        whereKey = 'inventory_prop_tmplt_id'

        # Check id
        _checkParameter('id', tmplt_id, 'prim')
        whereValue = tmplt_id

        # Check component type
        result = self.retrieveComponentType(cmpnt_type)

        if len(result) == 0:
            raise ValueError("Component type (%s) does not exist in the database." % (cmpnt_type))

        cmpnt_typeid = result.keys()[0]
        queryDict['cmpnt_type_id'] = cmpnt_typeid

        # Check name
        _checkParameter("name", name)
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
        sqlVals = _generateUpdateQuery('inventory_prop_tmplt', queryDict, whereKey, whereValue)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating inventory property template:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating inventory property template:\n%s (%d)' % (e.args[1], e.args[0]))

    def _retrieveInventoryProperty(self, inventoryId, inventoryPropertyTemplateId=None, value=None):
        '''
        Retrieve id and value from inventory property table

        :param inventoryId: id of the inventory entry
        :type inventoryId: int

        :param inventoryPropertyTemplateId: id of the inventory property template
        :type inventoryPropertyTemplateId: int

        :param value: value of the property template
        :type value: str

        :returns: Python dict

            { 'id': {
                    'id': #int,
                    'value': #string,
                    'inventoryname': #string,
                    'templatename': #string
                }
            }
        '''

        # Call retrieve from physics
        res = self.physics.retrieveInventoryProperty(inventoryId, inventoryPropertyTemplateId, value)
        resdict = {}

        for r in res:
            resdict[r[0]] = {
                'id': r[0],
                'value': r[1],
                'inventoryname': r[5],
                'templatename': r[4]
            }

        return resdict

    def retrieveInventoryProperty(self, inventoryName, inventoryPropertyTemplateName=None, value=None, cmpnt_type=None):
        '''
        Retrieve id and value from inventory property table

        :param inventoryName: name of the inventory entry
        :type inventoryName: str

        :param inventoryPropertyTemplateName: name of the inventory property template
        :type inventoryPropertyTemplateName: str

        :param value: value of the property template
        :type value: str

        :param cmpnt_type: component type name
        :type cmpnt_type: str

        :return: a map with structure like:

            .. code-block:: python

                { 'id': {
                        'id': #int,
                        'value': #string,
                        'inventoryname': #string,
                        'templatename': #string
                    }
                }

        :Raises: ValueError
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
            retrieveInventoryPropertyTemplate = self.retrieveInventoryPropertyTemplate(inventoryPropertyTemplateName, cmpnt_type)

            if len(retrieveInventoryPropertyTemplate) == 0:

                if cmpnt_type is not None:
                    inventoryPropertyTemplateId = self.saveInventoryPropertyTemplate(cmpnt_type, inventoryPropertyTemplateName)['id']

                else:
                    raise ValueError("Inventory property template (%s) doesn't exist in the database!" % inventoryPropertyTemplateName)

            else:
                retrieveInventoryPropertyTemplateKeys = retrieveInventoryPropertyTemplate.keys()
                inventoryPropertyTemplateId = retrieveInventoryPropertyTemplate[retrieveInventoryPropertyTemplateKeys[0]]['id']

        return self._retrieveInventoryProperty(inventoryId, inventoryPropertyTemplateId, value)

    def saveInventoryProperty(self, inventoryName, inventoryPropertyTemplateName, value, cmpnt_type=None):
        '''
        Save inventory property into database

        :param inventoryName: name of the inventory we are saving property for
        :type inventoryName: str

        :param inventoryPropertyTemplateName: name of the property template/inventory property key name
        :type inventoryPropertyTemplateName: str

        :param value: value of the property template/property key name
        :type value: str

        :param cmpnt_type: component type name. If it is not set to None then property template will be saved silently
        :type cmpnt_type: str


        :returns: Python dict::

            {'id': new inventory property id}

        :raises: ValueError, MySQLError
        '''

        # Check for previous inventory property
        retrieveInventoryProperty = self.retrieveInventoryProperty(inventoryName, inventoryPropertyTemplateName, cmpnt_type=cmpnt_type)

        if len(retrieveInventoryProperty) != 0:
            raise ValueError("Inventory property for inventory (%s) and template (%s) already exists in the database!" % (inventoryName, inventoryPropertyTemplateName))

        # Check inventory
        retrieveInventory = self.retrieveInventory(inventoryName)

        if len(retrieveInventory) == 0:
            raise ValueError("Inventory (%s) doesn't exist in the database!" % inventoryName)

        retrieveInventoryKeys = retrieveInventory.keys()
        inventoryId = retrieveInventory[retrieveInventoryKeys[0]]['id']

        # Check inventory property template
        retrieveInventoryPropertyTemplate = self.retrieveInventoryPropertyTemplate(inventoryPropertyTemplateName, cmpnt_type)

        if len(retrieveInventoryPropertyTemplate) == 0:

            # System parameters should be added automatically
            if inventoryPropertyTemplateName.startswith('__') and inventoryPropertyTemplateName.endswith('__'):
                res = self.saveInventoryPropertyTemplate(cmpnt_type, inventoryPropertyTemplateName, 'System parameter')
                inventoryPropertyTemplateId = res['id']

            else:
                raise ValueError("Inventory property template (%s) doesn't exist in the database!" % inventoryPropertyTemplateName)

        else:
            retrieveInventoryPropertyTemplateKeys = retrieveInventoryPropertyTemplate.keys()
            inventoryPropertyTemplateId = retrieveInventoryPropertyTemplate[retrieveInventoryPropertyTemplateKeys[0]]['id']

        result = self.physics.saveInventoryProperty(inventoryId, inventoryPropertyTemplateId, value)

        return {'id': result}

    def updateInventoryProperty(self, oldInventoryName, oldInventoryPropertyTemplateName, value, cmpnt_type=None):
        '''
        Update inventory property in a database

        :prop oldInventoryName: name of the inventory we are saving property for
        :type oldInventoryName: str

        :prop oldInventoryPropertyTemplateName: name of the property template/inventory property key name
        :type oldInventoryPropertyTemplateName: str

        :prop value: value of the property template/property key name
        :type value: str

        :returns: True if everything is ok

        :raises: ValueError, MySQLError
        '''

        # Check inventory
        retrieveInventory = self.retrieveInventory(oldInventoryName)

        if len(retrieveInventory) == 0:
            raise ValueError("Inventory (%s) doesn't exist in the database!" % oldInventoryName)

        retrieveInventoryKeys = retrieveInventory.keys()
        inventoryId = retrieveInventory[retrieveInventoryKeys[0]]['id']

        # Check inventory property template
        retrieveInventoryPropertyTemplate = self.retrieveInventoryPropertyTemplate(oldInventoryPropertyTemplateName, cmpnt_type)

        if len(retrieveInventoryPropertyTemplate) == 0:
            raise ValueError("Inventory property template (%s) doesn't exist in the database!" % oldInventoryPropertyTemplateName)

        retrieveInventoryPropertyTemplateKeys = retrieveInventoryPropertyTemplate.keys()
        inventoryPropertyTemplateId = retrieveInventoryPropertyTemplate[retrieveInventoryPropertyTemplateKeys[0]]['id']
        self.logger.info(inventoryPropertyTemplateId)
        return self.physics.updateInventoryProperty(inventoryId, inventoryPropertyTemplateId, value)

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
        compnttypeid = None
        cmpnt_type_name = None

        if 'cmpnt_type' in kws and kws['cmpnt_type'] is not None:

            # Check component type parameter
            _checkParameter("component type", kws['cmpnt_type'])
            cmpnt_type_name = kws['cmpnt_type']

            res = self.retrieveComponentType(kws['cmpnt_type'])
            reskeys = res.keys()

            if len(res) != 1:
                raise ValueError("Insertion device type (%s) does not exist." % (kws['dtype']))

            else:
                compnttypeid = res[reskeys[0]]['id']

        # Check alias parameter
        alias = None

        if 'alias' in kws and kws['alias'] is not None:
            alias = kws['alias']

        # Check serial number parameter
        serialno = None

        if 'serialno' in kws and kws['serialno'] is not None:
            serialno = kws['serialno']

        # Check vendor parameter
        vendor = None

        if 'vendor' in kws and kws['vendor'] is not None:

            # Check parameter
            _checkParameter("vendor name", kws['vendor'])

            res = self.retrieveVendor(kws['vendor'])

            if len(res) == 0:
                raise ValueError("Vendor with name (%s) doesn't exist." % kws['vendor'])

            resKeys = res.keys()
            vendor = res[resKeys[0]]['id']

        invid = self.physics.saveInventory(name, compnttypeid, alias, serialno, vendor)

        # Inventory is saved, now we can save properties into database
        if 'props' in kws and kws['props'] is not None:
            props = kws['props']

            # Convert to json
            if isinstance(props, (dict)) is False:
                props = json.loads(props)

            # Save all the properties
            for key in props:
                value = props[key]

                # Dump value if it is dictionary
                if isinstance(value, (dict)):
                    value = json.dumps(value)

                # Save it into database
                self.saveInventoryProperty(name, key, value, cmpnt_type=cmpnt_type_name)

        return {'id': invid}

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
            _checkParameter('id', inventory_id, 'prim')
            whereKey = 'inventory_id'
            whereValue = inventory_id

        # Check old name
        if old_name:
            _checkParameter('name', old_name)
            whereKey = 'name'
            whereValue = old_name

        if whereKey is None:
            raise ValueError("Id or old name should be present to execute an update!")

        # Check name parameter
        _checkParameter('name', name)
        queryDict['name'] = name

        compnttypename = None

        # Check device type parameter
        if 'cmpnt_type' in kws and kws['cmpnt_type'] is not None:

            # Check component type parameter
            _checkParameter("component type", kws['cmpnt_type'])

            res = self.retrieveComponentType(kws['cmpnt_type'])
            reskeys = res.keys()

            if len(res) != 1:
                raise ValueError("Insertion device type (%s) does not exist." % (kws['dtype']))

            else:
                compnttypeid = res[reskeys[0]]['id']

            compnttypename = kws['cmpnt_type']
            queryDict['cmpnt_type_id'] = compnttypeid

        # Check for component type
        if compnttypename is None:
            raise ValueError("Component type has to be set when updating!")

        # Check alias parameter
        if 'alias' in kws:
            queryDict['alias'] = kws['alias']

        # Check serial number parameter
        if 'serialno' in kws:
            queryDict['serial_no'] = kws['serialno']

        # Check vendor parameter
        if 'vendor' in kws and kws['vendor'] is not None:

            # Check parameter
            _checkParameter("vendor name", kws['vendor'])

            res = self.retrieveVendor(kws['vendor'])

            if len(res) == 0:
                raise ValueError("Vendor with name (%s) doesn't exist." % kws['vendor'])

            resKeys = res.keys()
            vendor = res[resKeys[0]]['id']
            queryDict['vendor_id'] = vendor

        sqlVals = _generateUpdateQuery('inventory', queryDict, whereKey, whereValue)

        try:
            # Insert inventory into database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            # Inventory is updated, now we can update properties
            if 'props' in kws and kws['props'] is not None:
                props = kws['props']

                # Convert to json
                if isinstance(props, (dict)) is False:
                    props = json.loads(props)

                currentTemplates = self.retrieveInventoryProperty(name, cmpnt_type=compnttypename)
                currentTemplatesDict = {}

                # Map current properties
                for key in currentTemplates.keys():
                    currentTemplatesDict[currentTemplates[key]['templatename']] = currentTemplates[key]['value']

                # Update all properties
                for key in props:
                    value = props[key]

                    # Dump value if it is dictionary
                    if isinstance(value, (dict)):
                        value = json.dumps(value)

                    if key in currentTemplatesDict:

                        # Update property
                        self.updateInventoryProperty(name, key, value, cmpnt_type=compnttypename)

                    else:
                        # Save property
                        self.saveInventoryProperty(name, key, value, cmpnt_type=compnttypename)

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating inventory:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating inventory:\n%s (%d)' % (e.args[1], e.args[0]))

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
                         'alias':,                      # string
                         'cmpnt_type':                  # string
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
                         'prop_keys':                   ['key1', 'key2']
                        }
                }

        :Raises: ValueError, MySQLError
        '''

        # Check name parameter
        _checkParameter('name', name)

        startedd = time.time()

        res = self.physics.retrieveInventory(name, None, None, None)

        total = time.time() - startedd
        total = total*1000
        print '=> elapsed time idods.retrieveInventory.DB: %f ms' % total

        resdict = {}

        for r in res:
            resdict[r[0]] = {
                'id': r[0],
                'name': r[1],
                'alias': r[2],
                'serialno': r[3],
                'cmpnt_type': r[4],
                'vendor': r[6],
                'prop_keys': []
            }

            # Get the rest of the properties
            properties = self._retrieveInventoryProperty(r[0])

            # Append properties to existing object
            for prop in properties:
                obj = properties[prop]
                resdict[r[0]][obj['templatename']] = obj['value']
                resdict[r[0]]['prop_keys'].append(obj['templatename'])

        return resdict

    def retrieveRawData(self, raw_data_id):
        '''
        Retrieve raw data by its id

        :param raw_data_id: raw data id
        :type raw_data_id: int

        :return: a map with structure like:

            .. code-block:: python

                {'id': {
                    'id': ,
                    'name': ,
                    'data':
                    }
                 ...
                }

        :Raises: ValueError, exception
        '''

        # Check id parameer
        _checkParameter('id', raw_data_id, 'prim')

        # Generate SQL statement
        sql = '''
        SELECT id_raw_data_id, data FROM id_raw_data WHERE id_raw_data_id = %s
        '''

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sql, raw_data_id)

            # Get record
            res = cur.fetchall()
            resdict = {}

            # Generate return dictionary
            for r in res:
                is_ascii = True

                try:
                    r[1].decode('ascii')

                except:
                    is_ascii = False

                resdict[r[0]] = {
                    'id': r[0],
                    'data': base64.b64encode(r[1]),
                    'is_ascii': is_ascii
                }

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching raw data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching raw data:\n%s (%d)' % (e.args[1], e.args[0]))

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
            startedd = time.time()

            # Insert data into database
            cur = self.conn.cursor()
            cur.execute(sql, data)

            # Get last id
            dataid = cur.lastrowid

            # Handle transaction
            if self.transaction is None:
                self.conn.commit()

            total = time.time() - startedd
            total = total*1000
            print '=> elapsed time idods.saveRawData.DB: %f ms' % total

            return {'id': dataid}

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving new raw data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving new raw data:\n%s (%d)' % (e.args[1], e.args[0]))

    def concatRawData(self, data, raw_data_id):
        '''
        Concat large data in the database

        :param data: part of the data we want to save in a blob
        :type data: blob

        :param raw_data_id: id of the raw data we need to update
        :type raw_data_id: int

        :raises: MySQLError

        :returns:
            True if everything is ok

        '''

        # Generate SQL
        sql = '''
        UPDATE id_raw_data SET data=CONCAT(data, %s) WHERE id_raw_data_id = %s
        '''

        try:
            # Insert data into database
            cur = self.conn.cursor()
            cur.execute(sql, (data, raw_data_id))

            # Handle transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving new raw data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving new raw data:\n%s (%d)' % (e.args[1], e.args[0]))

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
        _checkParameter('id', rawDataId, 'prim')
        whereKey = 'id_raw_data_id'
        whereValue = rawDataId

        # Set data parameter
        queryDict['data'] = data

        # Generate SQL
        sqlVals = _generateUpdateQuery('id_raw_data', queryDict, whereKey, whereValue)

        try:
            # Insert data into database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Handle transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating raw data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating raw data:\n%s (%d)' % (e.args[1], e.args[0]))

    def deleteRawData(self, raw_data_id):
        '''
        Delete raw data

        :param raw_data_id: raw data id
        :type raw_data_id: int

        :return: True if everything was ok

        :Raises: ValueError, MySQLError
        '''

        # Generate SQL
        sql = "DELETE FROM id_raw_data WHERE id_raw_data_id = %s"
        vals = [raw_data_id]

        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when deleting raw data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when deleting raw data:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveMethodAndOfflineData(
            self, inventory_name=None, username=None, method=None,
            method_desc=None, data_desc=None, data_file_name=None,
            data_id=None, status=None, gap=None, phase1=None, phase2=None,
            phase3=None, phase4=None, phase_mode=None, polar_mode=None
            ):
        '''
        Save data method and offline data into the database

        :param inventory_name: inventory name
        :type inventory_name: str

        :param username: username of the user who saved the offline data
        :type username: str

        :param method: data method name
        :type method: str

        :param method_desc: data method description
        :type method_desc: str

        :param data_desc: offline data description
        :type data_desc: str

        :param data_file_name: data file name
        :type data_file_name: str

        :param data_id: id of the saved raw data
        :type data_id: int

        :param status: is offline data Active = 1 or Obsolete - 0
        :type status: int

        :param gap: gap
        :type gap: float

        :param phase1: phase1
        :type phase1: float

        :param phase2: phase2
        :type phase2: float

        :param phase3: phase3
        :type phase3: float

        :param phase4: phase4
        :type phase4: float

        :param phase_mode: phase mode
        :type phase_mode: str

        :param polar_mode: polar mode
        :type polar_mode: str

        :rasies: ValueError, MySQLError

        :return: {'id': id of the new offline data}
        '''

        # Save method if it is provided
        if method is not None:

            if len(self.retrieveDataMethod(method).keys()) == 0:
                self.saveDataMethod(method, method_desc)

        result = self.saveOfflineData(
            inventory_name=inventory_name,
            data_file_name=data_file_name,
            username=username,
            description=data_desc,
            gap=gap,
            phase1=phase1,
            phase2=phase2,
            phase3=phase3,
            phase4=phase4,
            phasemode=phase_mode,
            polarmode=polar_mode,
            data_id=data_id,
            status=status
        )

        return result

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
        - data_id
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

        :param data_id: id of the raw data
        :type data_id: str

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

        if 'inventory_name' in kws and kws['inventory_name'] is not None:
            inventoryname = kws['inventory_name']

            returnedInventory = self.retrieveInventory(inventoryname)

            if len(returnedInventory) == 0:
                raise ValueError("Invnetory (%s) does not exist in the database!" % inventoryname)

            returnedInventoryKeys = returnedInventory.keys()
            inventoryid = returnedInventory[returnedInventoryKeys[0]]['id']

        # Check username parameter
        username = None

        if 'username' in kws and kws['username'] is not None:
            username = kws['username']
            _checkParameter('username', username)

        # Check description
        description = None

        if 'description' in kws and kws['description'] is not None:
            description = kws['description']

        # Check gap
        gap = None

        if 'gap' in kws and kws['gap'] is not None:
            gap = kws['gap']

        # Check phase1
        phase1 = None

        if 'phase1' in kws and kws['phase1'] is not None:
            phase1 = kws['phase1']

        # Check phase2
        phase2 = None

        if 'phase2' in kws and kws['phase2'] is not None:
            phase2 = kws['phase2']

        # Check phase3
        phase3 = None

        if 'phase3' in kws and kws['phase3'] is not None:
            phase3 = kws['phase3']

        # Check phase4
        phase4 = None

        if 'phase4' in kws and kws['phase4'] is not None:
            phase4 = kws['phase4']

        # Check phasemode
        phasemode = None

        if 'phasemode' in kws and kws['phasemode'] is not None:
            phasemode = kws['phasemode']

        # Check polarmode
        polarmode = None

        if 'polarmode' in kws and kws['polarmode'] is not None:
            polarmode = kws['polarmode']

        # Check status
        status = None

        if 'status' in kws and kws['status'] is not None:
            status = kws['status']

        # Check data_file_name
        datafilename = None

        if 'data_file_name' in kws and kws['data_file_name'] is not None:
            datafilename = kws['data_file_name']

        # Check data_file_ts
        datafilets = None

        if 'data_file_ts' in kws and kws['data_file_ts'] is not None:
            datafilets = kws['data_file_ts']

        # Check data
        data = None

        if 'data_id' in kws and kws['data_id'] is not None:
            data = kws['data_id']

        # Check script_name
        scriptname = None

        if 'script_name' in kws and kws['script_name'] is not None:
            scriptname = kws['script_name']

        # Check script
        script = None

        if 'script' in kws and kws['script'] is not None:
            script = kws['script']

        # Check method_name
        methodname = None
        methodid = None

        if 'method_name' in kws and kws['method_name'] is not None:
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
            %s,%s,%s,%s,%s,NOW(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        '''

        try:
            vals = [
                inventoryid,
                methodid,
                data,
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

            startedd2 = time.time()

            # Insert offline data into database
            cur = self.conn.cursor()
            cur.execute(sql, vals)

            # Get last row id
            offlinedataid = cur.lastrowid

            # Create transactions
            if self.transaction is None:
                self.conn.commit()

            total2 = time.time() - startedd2
            total2 = total2*1000
            print '=> elapsed time idods.saveOfflineData.DB: %f ms' % total2

            return {'id': offlinedataid}

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving new offline data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving new offline data:\n%s (%d)' % (e.args[1], e.args[0]))

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
        - data_id
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

        :param data_id: id of the raw data
        :type data_id: str

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
        _checkParameter('id', offline_data_id, 'prim')
        whereKey = 'id_offline_data_id'
        whereValue = offline_data_id

        # Check inventoryname
        if 'inventory_name' in kws and kws['inventory_name'] is not None:
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
        if 'data_file_ts' in kws and kws['data_file_ts'] is not None:
            queryDict['result_file_time'] = kws['data_file_ts']

        # Check data id
        if 'data_id' in kws and kws['data_id'] is not None:
            data = kws['data_id']
            queryDict['id_raw_data_id'] = data

        # Check script_name
        if 'script_name' in kws:
            queryDict['script_file_name'] = kws['script_name']

        # Check script
        if 'script' in kws:
            queryDict['script_file_content'] = kws['script']

        # Check method_name
        if 'method_name' in kws and kws['method_name'] is not None:
            methodname = kws['method_name']

            retrievedMethod = self.retrieveDataMethod(methodname)

            if len(retrievedMethod) == 0:
                raise ValueError("Data method (%s) doesn't exist in the database!" % methodname)

            retrievedMethodKeys = retrievedMethod.keys()
            methodid = retrievedMethod[retrievedMethodKeys[0]]['id']
            queryDict['id_data_method_id'] = methodid

        # Genreate SQL
        sqlVals = _generateUpdateQuery('id_offline_data', queryDict, whereKey, whereValue)

        try:

            # Insert offline data into database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transactions
            if self.transaction is None:
                self.conn.commit()

            return True

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating offline data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating offline data:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveOfflineData(self, **kws):
        '''Retrieve insertion device offline data using any of the acceptable key words:

        - offlineid
        - description
        - date
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

        :param date: offline data date
        :type date: str

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
                        'data_id':,        # int
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
        if 'offlineid' in kws and kws['offlineid'] is not None:
            _checkParameter('id', kws['offlineid'], 'prim')
            sql += ' AND id_offline_data_id = %s '
            vals.append(kws['offlineid'])

        # Append description parameter
        if 'description' in kws and kws['description'] is not None:
            sqlVal = _checkWildcardAndAppend('iod.description', kws['description'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]

        # Append date parameter
        if 'date' in kws and kws['date'] is not None:
            sqlVal = _checkRangeAndAppend('iod.date', kws['date'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]

        # Append gap parameter
        if 'gap' in kws and kws['gap'] is not None:
            sqlVal = _checkRangeAndAppend('iod.gap', kws['gap'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]

        # Append phase1 parameter
        if 'phase1' in kws and kws['phase1'] is not None:
            sqlVal = _checkRangeAndAppend('iod.phase1', kws['phase1'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]

        # Append phase2 parameter
        if 'phase2' in kws and kws['phase2'] is not None:
            sqlVal = _checkRangeAndAppend('iod.phase2', kws['phase2'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]

        # Append phase3 parameter
        if 'phase3' in kws and kws['phase3'] is not None:
            sqlVal = _checkRangeAndAppend('iod.phase3', kws['phase3'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]

        # Append phase4 parameter
        if 'phase4' in kws and kws['phase4'] is not None:
            sqlVal = _checkRangeAndAppend('iod.phase4', kws['phase4'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]

        # Append phasemode parameter
        if 'phasemode' in kws and kws['phasemode'] is not None:
            sqlVal = _checkWildcardAndAppend('iod.phase_mode', kws['phasemode'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]

        # Append polarmode parameter
        if 'polarmode' in kws and kws['polarmode'] is not None:
            sqlVal = _checkWildcardAndAppend('iod.polar_mode', kws['polarmode'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]

        # Append status parameter
        if 'status' in kws and kws['status'] is not None:
            sql += ' AND iod.data_status = %s '
            vals.append(kws['status'])

        # Append method name parameter
        if 'method_name' in kws and kws['method_name'] is not None:
            sqlVal = _checkWildcardAndAppend('idm.method_name', kws['method_name'], sql, vals, 'AND')
            sql = sqlVal[0]
            vals = sqlVal[1]

        # Append inventory name
        if 'inventory_name' in kws and kws['inventory_name'] is not None:
            sqlVal = _checkWildcardAndAppend('inv.name', kws['inventory_name'], sql, vals, 'AND')
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
                    'data_id': r[3],
                    'script_name': r[17],
                    'script': r[18],
                    'method_name': r[19],
                    'methoddesc': r[20],
                    'inventory_name': r[21]
                }

                # Format time if it is not null
                if r[16] is not None:
                    resdict[r[0]]['data_file_ts'] = r[16].strftime("%Y-%m-%d %H:%M:%S")

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching offline data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching offline data:\n%s (%d)' % (e.args[1], e.args[0]))

    def deleteOfflineData(self, offline_data_id):
        '''
        Delete offline data

        :param offline_data_id: offline data id
        :type offline_data_id: int

        :return: True if everything was ok

        :Raises: ValueError, MySQLError
        '''

        # Retrieve offline data
        offlineData = self.retrieveOfflineData(offlineid=offline_data_id)

        if len(offlineData) == 0:
            raise ValueError("Offline data doesn't exist in the database!")

        offlineDataKey = offlineData.keys()[0]
        offlineDataObj = offlineData[offlineDataKey]

        # Generate SQL
        sql = "DELETE FROM id_offline_data WHERE id_offline_data_id = %s"
        vals = [offline_data_id]

        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            # Delete raw data
            self.deleteRawData(offlineDataObj['data_id'])

            return True

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when deleting offline data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when deleting offline data:\n%s (%d)' % (e.args[1], e.args[0]))

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

        startedd = time.time()

        # Raise and error if data method with the same name already exists in the database
        existingDataMethod = self.retrieveDataMethod(name, description)

        if len(existingDataMethod):
            raise ValueError("Data method (%s) already exists in the database!" % name)

        # Check name parameter
        _checkParameter('name', name)

        # Generate SQL
        sql = '''
        INSERT INTO id_data_method
            (method_name, description)
        VALUES
            (%s, %s)
        '''

        try:
            startedd2 = time.time()
            cur = self.conn.cursor()
            cur.execute(sql, (name, description))

            # Get last id
            dataMethodId = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            total2 = time.time() - startedd2
            total2 = total2*1000
            print '=> elapsed time idods.saveDataMethod.DB: %f ms' % total2

            total = time.time() - startedd
            total = total*1000
            print '=> elapsed time view.saveDataMethod.W: %f ms' % total

            return {'id': dataMethodId}

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving new data method:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving new data method:\n%s (%d)' % (e.args[1], e.args[0]))

    def updateDataMethod(self, datamethod_id, old_name, name, **kws):
        '''Update data method by id or name.

        :param datamethod_id id of the data method we want to update by
        :type datamethod_id: int

        :param old_name: name of the method we want to update by
        :type old_name: str

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
        if datamethod_id:
            _checkParameter('id', datamethod_id, 'prim')
            whereKey = 'id_data_method_id'
            whereValue = datamethod_id

        # Check name
        if old_name:
            _checkParameter('name', old_name)
            whereKey = 'method_name'
            whereValue = old_name

        # Check if id or name is present
        if whereKey is None:
            raise ValueError("Id or old name should be present to execute an update!")

        # Check name parameter
        _checkParameter('name', name)
        queryDict['method_name'] = name

        # Check description parameter
        if 'description' in kws:
            queryDict['description'] = kws['description']

        # Generate SQL
        sqlVals = _generateUpdateQuery('id_data_method', queryDict, whereKey, whereValue)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating data method:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating data method:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveDataMethod(self, name, description=None):
        '''
        Retrieve a method name and its description which is used when producing data set for an insertion device.

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

        startedd = time.time()

        # Check name
        _checkParameter('name', name)

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
        sqlAndVals = _checkWildcardAndAppend('method_name', name, sql, vals)

        # Check if description exists
        if description:
            sqlAndVals = _checkWildcardAndAppend('description', description, sqlAndVals[0], sqlAndVals[1], 'AND')

        try:
            startedd2 = time.time()

            # Execute SQL
            cur = self.conn.cursor()
            cur.execute(sqlAndVals[0], sqlAndVals[1])

            res = cur.fetchall()

            total2 = time.time() - startedd2
            total2 = total2*1000
            print '=> elapsed time idods.retrieveDataMethod.DB: %f ms' % total2

            resdict = {}

            # Construct return dict
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'name': r[1],
                    'description': r[2]
                }

            total = time.time() - startedd
            total = total*1000
            print '=> elapsed time idods.retrieveDataMethod.W: %f ms' % total

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching data method:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching data method:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveInventoryToInstall(self, inventory_to_install_id, install_name, inv_name):
        '''
        Return installed devices or psecific map

        :param inventory_to_install_id: id of the inventory to install map
        :type inventory_to_install_id: int

        :param install_name: label name after installation
        :type install_name: str

        :param inv_name: name in its inventory
        :type inv_name: str

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
        if inventory_to_install_id:
            sql += ' AND ii.inventory__install_id = %s '
            vals.append(inventory_to_install_id)

        # Check inventory name
        if inv_name:
            sqlVals = _checkWildcardAndAppend('inv.name', inv_name, sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]

        # Check install name
        if install_name:
            sqlVals = _checkWildcardAndAppend('inst.field_name', install_name, sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]

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
            self.logger.info('Error when fetching installed devices:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching installed devices:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveInventoryToInstall(self, install_name, inv_name):
        '''
        Link a device as installed once it is installed into field

        :param install_name: label name after installation
        :type install_name: str

        :param inv_name: name in its inventory
        :type inv_name: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': id of new inventorytoinstall record}

        :Raises: ValueError, MySQLError
        '''

        # Check install name
        install = self.retrieveInstall(install_name)

        if len(install) < 1:
            raise ValueError("Install with name (%s) doesn't exist in the database!" % install_name)

        installKeys = install.keys()
        installObject = install[installKeys[0]]

        # Check inventory name
        inventory = self.retrieveInventory(inv_name)

        if len(inventory) < 1:
            raise ValueError("Inventory with name (%s) doesn't exist in the database!" % inv_name)

        inventoryKeys = inventory.keys()
        inventoryObject = inventory[inventoryKeys[0]]

        # Check if inventory already installed
        existing = self.retrieveInventoryToInstall(None, None, inv_name)

        if len(existing):
            raise ValueError("Inventory already installed!")

        # Check if install already exists
        existing = self.retrieveInventoryToInstall(None, install_name, None)

        if len(existing):
            raise ValueError("Install position already taken!")

        res = self.physics.saveInventoryToInstall(installObject['id'], inventoryObject['id'])

        return {'id': res}

    def updateInventoryToInstall(self, inventory_to_install_id, install_name, inv_name):
        '''
        Update a device as installed when its installation has been changed using the key words:

        - inventory_to_install_id
        - install_name
        - inv_name

        :param install_name: label name after installation
        :type install_name: str

        :param inv_name: name in its inventory
        :type inv_name: str

        :return: True if everything was ok

        :Raises: ValueError, MySQLError
        '''

        # Get current map
        i2iMap = self.retrieveInventoryToInstall(inventory_to_install_id, None, None)

        if len(i2iMap) < 1:
            raise ValueError("Inventory to install map with id (%s) doesn't exist in the database!" % inventory_to_install_id)

        i2iKeys = i2iMap.keys()
        i2i = i2iMap[i2iKeys[0]]

        # Check if nothing has changed
        if i2i['installname'] == install_name and i2i['inventoryname'] == inv_name:
            return True

        # Define query dict
        queryDict = {}

        # Check id
        _checkParameter('id', inventory_to_install_id, 'prim')
        whereKey = 'inventory__install_id'
        whereValue = inventory_to_install_id

        # Check install name
        install = self.retrieveInstall(install_name)

        if len(install) < 1:
            raise ValueError("Install with name (%s) doesn't exist in the database!" % install_name)

        installKeys = install.keys()
        installObject = install[installKeys[0]]
        queryDict['install_id'] = installObject['id']

        # Check inventory name
        inventory = self.retrieveInventory(inv_name)

        if len(inventory) < 1:
            raise ValueError("Inventory with name (%s) doesn't exist in the database!" % inv_name)

        inventoryKeys = inventory.keys()
        inventoryObject = inventory[inventoryKeys[0]]
        queryDict['inventory_id'] = inventoryObject['id']

        # Check if inventory already installed
        existing = self.retrieveInventoryToInstall(None, None, inv_name)

        if i2i['inventoryname'] == inv_name and len(existing) > 1:
            raise ValueError("Inventory already installed!")

        elif i2i['inventoryname'] != inv_name and len(existing):
            raise ValueError("Inventory already installed!")

        # Check if install already exists
        existing = self.retrieveInventoryToInstall(None, install_name, None)

        if i2i['installname'] == install_name and len(existing) > 1:
            raise ValueError("Install position already taken!")

        elif i2i['installname'] != install_name and len(existing):
            raise ValueError("Install position already taken!")

        # Generate SQL
        sqlVals = _generateUpdateQuery('inventory__install', queryDict, whereKey, whereValue)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating inventory to install:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating inventory to install:\n%s (%d)' % (e.args[1], e.args[0]))

    def deleteInventoryToInstall(self, inventory_to_install_id, delete_online_data=None):
        '''
        Delete inventory to install map

        :param inventory_to_install_id: id of the map
        :type inventory_to_install_id: int

        :param delete_online_data: should online data be deleted or just set to deprecated
        :type delete_online_data: boolean

        :return: True if everything was ok

        :Raises: ValueError, MySQLError
        '''

        # Retrieve inventory to install
        i2i = self.retrieveInventoryToInstall(inventory_to_install_id, None, None)
        i2iKeys = i2i.keys()
        i2iObj = i2i[i2iKeys[0]]

        # Retrieve online data
        onlineData = self.retrieveOnlineData(install_name=i2iObj['installname'])

        for key in onlineData:
            onlineDataObj = onlineData[key]

            # Delete online data
            if delete_online_data is True:
                self.deleteOnlineData(onlineDataObj['id'])

            else:
                self.updateOnlineData(onlineDataObj['id'], status=0)

        # Generate SQL
        sql = "DELETE FROM inventory__install WHERE inventory__install_id = %s"
        vals = [inventory_to_install_id]

        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when deleting inventory to install:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when deleting inventory to install:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveComponentTypePropertyType(self, name):
        '''
        Retrieve component type property type by its name

        :param name: property type name
        :type name: str

        :return: a map with structure like:

            .. code-block:: python

                {
                    'id': {
                        'id': ,              # int
                        'name': ,           # string
                        'description': ,    # string
                    }
                }
        '''

        # Retrieve component type property type
        res = self.physics.retrieveComponentTypePropertyType(name)
        resdict = {}

        # Construct return dict
        for r in res:
            resdict[r[0]] = {
                'id': r[0],
                'name': r[1],
                'description': r[2]
            }

        return resdict

    def saveComponentTypePropertyType(self, name, description=None):
        '''
        Insert new component type property type into database

        - name: name of the component type property type M
        - description: description of the component type property type O

        :return: a map with structure like:

            .. code-block:: python

                {'id': propertytypeid}
        '''

        # Execute save
        typeid = self.physics.saveComponentTypePropertyType(name, description)
        return {'id': typeid}

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
            _checkParameter('id', property_type_id, 'prim')
            whereKey = 'cmpnt_type_prop_type_id'
            whereValue = property_type_id

        # Check old name
        if old_name:
            _checkParameter('name', old_name)
            whereKey = 'cmpnt_type_prop_type_name'
            whereValue = old_name

        if whereKey is None:
            raise ValueError("Id or old name should be present to execute an update!")

        # Check name
        _checkParameter("name", name)
        queryDict['cmpnt_type_prop_type_name'] = name

        # Append description
        if 'description' in kws:
            queryDict['cmpnt_type_prop_type_desc'] = kws['description']

        # Generate SQL
        sqlVals = _generateUpdateQuery('cmpnt_type_prop_type', queryDict, whereKey, whereValue)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating component type property type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating component type property type:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveComponentTypeProperty(self, componentTypeName, componentTypePropertyTypeName=None, value=None):
        '''
        Retrieve component type property from the database by name

        :param componentTypeName: name of the component type
        :type componentTypeName: str

        :param componentTypePropertyTypeName: name of the component type property type
        :type componentTypePropertyTypeName: str

        :param value: value of the component type property type
        :type value: str

        :returns: a map with structure like:

            .. code-block:: python

                { 'id': {
                        'id': #int,
                        'value': #string,
                        'typeid': #int,
                        'cmpnt_typeid': #int,
                        'cmpnt_typename': #string,
                        'typename': #string
                    }
                }

        :raises: ValueError, MySQLError
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
                raise ValueError("Component type property type (%s) doesn't exist in the database!" % componentTypePropertyTypeName)

            retrieveComponentTypePropertyTypeKeys = retrieveComponentTypePropertyType.keys()
            componentTypePropertyTypeId = retrieveComponentTypePropertyType[retrieveComponentTypePropertyTypeKeys[0]]['id']

        properties = self.physics.retrieveComponentTypeProperty(componentTypeId, componentTypePropertyTypeId, value)

        resdict = {}

        for r in properties:
            resdict[r[0]] = {
                'id': r[0],
                'value': r[1],
                'cmpnt_typeid': r[2],
                'typeid': r[3],
                'typename': r[4],
                'cmpnt_typename': r[5]
            }

        return resdict

    def saveComponentTypePropertyById(self, componentTypeId, componentTypePropertyTypeName, value):
        '''
        Save inventory property into database

        :param componentTypeId: id of the component type
        :type componentTypeId: int

        :param componentTypePropertyTypeName: name of the component type property type
        :type componentTypePropertyTypeName: str

        :param value: value of the component type property
        :type value: str

        :return: {'id': new component type property id}

        :raise: ValueError, MySQLError
        '''

        # Check component type property type
        retrieveComponentTypePropertyType = self.retrieveComponentTypePropertyType(componentTypePropertyTypeName)

        if len(retrieveComponentTypePropertyType) == 0:
            self.saveComponentTypePropertyType(componentTypePropertyTypeName)
            retrieveComponentTypePropertyType = self.retrieveComponentTypePropertyType(componentTypePropertyTypeName)

        retrieveComponentTypePropertyTypeKeys = retrieveComponentTypePropertyType.keys()
        componentTypePropertyTypeId = retrieveComponentTypePropertyType[retrieveComponentTypePropertyTypeKeys[0]]['id']

        # Call save from physics dataapi
        result = self.physics.saveComponentTypeProperty(componentTypeId, componentTypePropertyTypeId, value)

        return {'id': result}

    def saveComponentTypeProperty(self, componentTypeName, componentTypePropertyTypeName, value):
        '''
        Save inventory property into database

        :param componentTypeName: name of the component type
        :type componentTypeName: str

        :param componentTypePropertyTypeName: name of the component type property type
        :type componentTypePropertyTypeName: str

        :param value: value of the component type property
        :type value: str

        :return: {'id': new component type property id}

        :raise: ValueError, MySQLError
        '''

        # Check for previous component type property
        retrieveComponentTypeProperty = self.retrieveComponentTypeProperty(componentTypeName, componentTypePropertyTypeName)

        if len(retrieveComponentTypeProperty) != 0:
            raise ValueError("Component type property for component type (%s) and property type (%s) already exists in the database!" % (componentTypeName, componentTypePropertyTypeName))

        # Check component type
        retrieveComponentType = self.retrieveComponentType(componentTypeName)

        if len(retrieveComponentType) == 0:
            raise ValueError("Component type (%s) doesn't exist in the database!" % componentTypeName)

        retrieveComponentTypeKeys = retrieveComponentType.keys()
        componentTypeId = retrieveComponentType[retrieveComponentTypeKeys[0]]['id']

        # Check component type property type
        retrieveComponentTypePropertyType = self.retrieveComponentTypePropertyType(componentTypePropertyTypeName)

        if len(retrieveComponentTypePropertyType) == 0:
            raise ValueError("Component type property type (%s) doesn't exist in the database!" % componentTypePropertyTypeName)

        retrieveComponentTypePropertyTypeKeys = retrieveComponentTypePropertyType.keys()
        componentTypePropertyTypeId = retrieveComponentTypePropertyType[retrieveComponentTypePropertyTypeKeys[0]]['id']

        # Call save from physics dataapi
        result = self.physics.saveComponentTypeProperty(componentTypeId, componentTypePropertyTypeId, value)

        return {'id': result}

    def updateComponentTypeProperty(self, oldComponentTypeName, oldComponentTypePropertyTypeName, value):
        '''
        Save inventory property into database

        :param oldComponentTypeName: name of the component type
        :type oldComponentTypeName: str

        :param oldComponentTypePropertyTypeName: name of the component type property type
        :type oldComponentTypePropertyTypeName: str

        :param value: value of the component type property
        :type value: int/str

        :returns: True if everything is ok

        :raises: ValueError, MySQLError
        '''

        # Check component type
        retrieveComponentType = self.retrieveComponentType(oldComponentTypeName)

        if len(retrieveComponentType) == 0:
            raise ValueError("Component type (%s) doesn't exist in the database!" % oldComponentTypeName)

        retrieveComponentTypeKeys = retrieveComponentType.keys()
        componentTypeId = retrieveComponentType[retrieveComponentTypeKeys[0]]['id']

        # Check component type property type
        retrieveComponentTypePropertyType = self.retrieveComponentTypePropertyType(oldComponentTypePropertyTypeName)

        if len(retrieveComponentTypePropertyType) == 0:
            raise ValueError("Component type property type (%s) doesn't exist in the database!" % oldComponentTypePropertyTypeName)

        retrieveComponentTypePropertyTypeKeys = retrieveComponentTypePropertyType.keys()
        componentTypePropertyTypeId = retrieveComponentTypePropertyType[retrieveComponentTypePropertyTypeKeys[0]]['id']

        # Call update from physics dataapi
        return self.physics.updateComponentTypeProperty(componentTypeId, componentTypePropertyTypeId, value)

    def retrieveComponentType(self, name, description=None):
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
                    'propNkey': propNvalue,
                    'prop_keys': ['key1', 'key2']
                    },
                 ...
                }

        :Raises: ValueError, MySQLError
        '''

        # Check component type parameter
        _checkParameter("component type", name)

        # Start SQL
        sql = '''
        SELECT cmpnt_type_id, cmpnt_type_name, description FROM cmpnt_type WHERE 1=1
        '''

        vals = []

        # Append component type
        sqlAndVals = _checkWildcardAndAppend("cmpnt_type_name", name, sql, vals, "AND")
        sql = sqlAndVals[0]
        vals = sqlAndVals[1]

        # Append description if exists
        if description is not None:

            # Append description
            sqlAndVals = _checkWildcardAndAppend("description", description, sqlAndVals[0], sqlAndVals[1], "AND")
            sql = sqlAndVals[0]
            vals = sqlAndVals[1]

        # Execute SQL
        try:
            startedd = time.time()

            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()

            total = time.time() - startedd
            total = total*1000
            print '=> elapsed time idods.retrieveComponentType.DB: %f ms' % total

            # Create return dictionry
            resdict = {}

            for r in res:
                resdict[r[0]] = {}
                resdict[r[0]]['id'] = r[0]
                resdict[r[0]]['name'] = r[1]
                resdict[r[0]]['description'] = r[2]
                resdict[r[0]]['prop_keys'] = []

                # Get the rest of the properties
                properties = self.physics.retrieveComponentTypeProperty(r[0])

                propdict = {}

                for pr in properties:
                    propdict[pr[0]] = {
                        'id': pr[0],
                        'value': pr[1],
                        'cmpnt_typename': pr[5],
                        'typename': pr[4]
                    }

                # Append properties to existing object
                for prop in propdict:
                    obj = propdict[prop]
                    resdict[r[0]][obj['typename']] = obj['value']
                    resdict[r[0]]['prop_keys'].append(obj['typename'])

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching component type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching component type:\n%s (%d)' % (e.args[1], e.args[0]))

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
        _checkParameter("component type", name)

        # Check if component type already exists
        componenttype = self.retrieveComponentType(name)

        if len(componenttype):
            raise ValueError("Component type (%s) already exists in the database!" % name)

        # Save it into database and return its new id
        sql = ''' INSERT into cmpnt_type (cmpnt_type_name, description) VALUES (%s, %s) '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (name, description))
            componenttypeid = cur.lastrowid

            # Commit transaction
            if self.transaction is None:
                self.conn.commit()

            # Add mandatory properties
            if props is None:
                props = {'insertion_device': 'true'}

            # Component type is saved, now we can save properties into database
            if props is not None:

                # Convert to json
                if isinstance(props, (dict)) is False:
                    props = json.loads(props)

                # Add mandatory properties
                props['insertion_device'] = 'true'

                # Save all the properties
                for key in props:
                    value = props[key]

                    # Save it into database
                    self.saveComponentTypePropertyById(componenttypeid, key, value)

            return {'id': componenttypeid}

        except MySQLError as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving component type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving component type:\n%s (%d)' % (e.args[1], e.args[0]))

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
            _checkParameter('id', component_type_id, 'prim')
            whereKey = 'cmpnt_type_id'
            whereValue = component_type_id

        # Check old name
        if old_name:
            _checkParameter('name', old_name)
            whereKey = 'cmpnt_type_name'
            whereValue = old_name

        # Check where condition
        if whereKey is None:
            raise ValueError("Component type id or old component type name should be present to execute an update!")

        # Check device type
        _checkParameter("component type", name)
        queryDict['cmpnt_type_name'] = name

        # Add description
        if 'description' in kws:
            queryDict['description'] = kws['description']

        # Save it into database and return its new id
        sqlVals = _generateUpdateQuery('cmpnt_type', queryDict, whereKey, whereValue)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Commit transaction
            if self.transaction is None:
                self.conn.commit()

            # Component type is saved, now we can update properties
            if 'props' in kws and kws['props'] is not None:
                props = kws['props']

                # Convert to json
                if isinstance(props, (dict)) is False:
                    props = json.loads(props)

                # Get current properties
                currentProps = self.retrieveComponentTypeProperty(name)
                currentPropsDict = {}

                # Map current properties
                for key in currentProps.keys():
                    currentPropsDict[currentProps[key]['typename']] = currentProps[key]['value']

                # Update all the properties
                for key in props:
                    value = props[key]

                    if key in currentPropsDict:

                        # Update property
                        self.updateComponentTypeProperty(name, key, value)

                    else:

                        # Save new property
                        self.saveComponentTypeProperty(name, key, value)

            return True

        except MySQLError as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating component type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating component type:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveInstallRelPropertyType(self, name):
        '''
        Retrieve install relationship property type by its name

        :param name: property type name
        :type name: str

        :return: a map with structure like:

            .. code-block:: python

                {
                    'id': {
                        'id': ,             # int
                        'name': ,           # string
                        'description': ,    # string
                        'unit': ,          # string
                    }
                }

        :Raises: ValueError, MySQLError
        '''

        # Check name
        _checkParameter("name", name)

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
        sqlAndVals = _checkWildcardAndAppend("install_rel_prop_type_name", name, sql, vals)

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
                    'unit': r[3]
                }

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching installation relationship property type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching installation ralationship property type:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveInstallRelPropertyType(self, name, description=None, unit=None):
        '''
        Insert new install relationship property type into database

        :param name: name of the install relationship property type M
        :type name: str

        :param description: description of the install relationship property type O
        :type description: str

        :param unit: unit used for this property type O
        :type unit: str

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
        _checkParameter("name", name)

        # Generate SQL
        sql = '''
        INSERT INTO install_rel_prop_type
            (install_rel_prop_type_name, install_rel_prop_type_desc, install_rel_prop_type_units)
        VALUES
            (%s, %s, %s)
        '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (name, description, unit))

            # Get last row id
            typeid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return {'id': typeid}

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving new install rel property type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving new install rel property type:\n%s (%d)' % (e.args[1], e.args[0]))

    def updateInstallRelPropertyType(self, type_id, old_name, name, **kws):
        '''
        Update install relationship property type

        - type_id: id of the install rellationship property type we want to update by O
        - old_name: name of the install relationship property type we want to update by O
        - name: name of the install relationship property type M
        - description: description of the install relationship property type O
        - unit: units used for this property type O

        :return: True if everything is ok

        :Raises: ValueError, MySQLError
        '''

        # Define query dictionary
        queryDict = {}
        whereKey = None
        whereValue = None

        # Check if
        if type_id:
            _checkParameter('id', type_id, 'prim')
            whereKey = 'install_rel_prop_type_id'
            whereValue = type_id

        # Check name
        if old_name:
            _checkParameter('name', old_name)
            whereKey = 'install_rel_prop_type_name'
            whereValue = old_name

        # Check if where key is set
        if whereKey is None:
            raise ValueError("Id or old name should be present to execute an update!")

        # Check name
        _checkParameter("name", name)
        queryDict['install_rel_prop_type_name'] = name

        # Check description
        if 'description' in kws:
            queryDict['install_rel_prop_type_desc'] = kws['description']

        # Check units
        if 'unit' in kws:
            queryDict['install_rel_prop_type_units'] = kws['unit']

        # Generate SQL
        sqlVals = _generateUpdateQuery('install_rel_prop_type', queryDict, whereKey, whereValue)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating install rel property type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating install rel property type:\n%s (%d)' % (e.args[1], e.args[0]))

    def _retrieveInstallRelProperty(self, installRelId, installRelPropertyTypeId=None, value=None):
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
            sqlVals = _checkWildcardAndAppend('install_rel_prop_value', value, sqlVals[0], sqlVals[1], 'AND')

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
            self.logger.info('Error when retrieving install rel property from the table:\n%s (%s)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when retrieving install rel property from the table:\n%s (%s)' % (e.args[1], e.args[0]))

    def retrieveInstallRelProperty(self, install_rel_id, install_rel_property_type_name=None, install_rel_property_value=None):
        '''
        Retrieve component type property from the database by name

        :param install_rel_id: id of the install rel
        :type install_rel_id: int

        :param install_rel_property_type_name: name of the install rel property type
        :type install_rel_property_type_name: str

        :param install_rel_property_value: value of the property type
        :type install_rel_property_value: str

        :return: a map with structure like:

            .. code-block:: python

                { 'id': {
                        'id': #int,
                        'value': #string,
                        'typename': #string
                    }
                }

        :raises: ValueError
        '''

        # Check install rel property type
        # of a specific component type

        installRelPropertyTypeId = None

        if install_rel_property_type_name:
            retrieveInstallRelPropertyType = self.retrieveInstallRelPropertyType(install_rel_property_type_name)

            if len(retrieveInstallRelPropertyType) == 0:

                # System parameters should be added automatically
                if install_rel_property_type_name.startswith('__') and install_rel_property_type_name.endswith('__'):
                    res = self.saveInstallRelPropertyType(install_rel_property_type_name, 'System parameter')
                    installRelPropertyTypeId = res['id']

                else:
                    raise ValueError("Install rel property type (%s) doesn't exist in the database!" % install_rel_property_type_name)

            else:
                retrieveInstallRelPropertyTypeKeys = retrieveInstallRelPropertyType.keys()
                installRelPropertyTypeId = retrieveInstallRelPropertyType[retrieveInstallRelPropertyTypeKeys[0]]['id']

        return self._retrieveInstallRelProperty(install_rel_id, installRelPropertyTypeId, install_rel_property_value)

    def saveInstallRelPropertyByMap(self, install_rel_parent, install_rel_child, install_rel_property_type_name, install_rel_property_value):
        '''
        Save install rel property by install rel map

        :param install_rel_parent: name of the parent in the install rel
        :type install_rel_parent: str

        :param install_rel_child: name of the child in the install rel
        :type install_rel_child: str

        :param install_rel_property_type_name: name of the install rel property type
        :type install_rel_property_type_name: str

        :param install_rel_property_value: value of the install rel property
        :type install_rel_property_value: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': new install rel property id}
        '''

        # Check install rel
        retrieveInstallRel = self.retrieveInstallRel(None, install_rel_parent, install_rel_child)

        if len(retrieveInstallRel) == 0:
            raise ValueError("Install rel doesn't exist in the database!")

        retrieveInstallRelKeys = retrieveInstallRel.keys()
        retrieveInstallRelObject = retrieveInstallRel[retrieveInstallRelKeys[0]]

        relid = retrieveInstallRelObject['id']

        return self.saveInstallRelProperty(relid, install_rel_property_type_name, install_rel_property_value)

    def saveInstallRelProperty(self, install_rel_id, install_rel_property_type_name, install_rel_property_value):
        '''
        Save install rel property into database

        :param install_rel_id: id of the install rel
        :type install_rel_id: int

        :param install_rel_property_type_name: name of the install rel property type
        :type install_rel_property_type_name: str

        :param install_rel_property_value: value of the install rel property
        :type install_rel_property_value: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': new install rel property id}

        :raises: ValueError, MySQLError
        '''

        # Check for previous install rel property
        retrieveInstallRelProperty = self.retrieveInstallRelProperty(install_rel_id, install_rel_property_type_name)

        if len(retrieveInstallRelProperty) != 0:
            raise ValueError("Install rel property for component type (%s) and property type (%s) already exists in the database!" % (install_rel_id, install_rel_property_type_name))

        # Check install rel property type
        retrieveInstallRelPropertyType = self.retrieveInstallRelPropertyType(install_rel_property_type_name)

        if len(retrieveInstallRelPropertyType) == 0:

            # System parameters should be added automatically
            if install_rel_property_type_name.startswith('__') and install_rel_property_type_name.endswith('__'):
                res = self.saveInstallRelPropertyType(install_rel_property_type_name, 'System parameter')
                installRelPropertyTypeId = res['id']

            else:
                raise ValueError("Install rel property type (%s) doesn't exist in the database!" % install_rel_property_type_name)

        else:
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
            cur.execute(sql, (install_rel_id, installRelPropertyTypeId, install_rel_property_value))

            # Get last row id
            propid = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return {'id': propid}

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving install rel property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving install rel property:\n%s (%d)' % (e.args[1], e.args[0]))

    def updateInstallRelPropertyByMap(self, install_rel_parent, install_rel_child, install_rel_property_type_name, install_rel_property_value):
        '''
        Update install rel property

        :param install_rel_parent: name of the parent in the install rel
        :type install_rel_parent: str

        :param install_rel_child: name of the child in the install rel
        :type install_rel_child: str

        :param install_rel_property_type_name: name of the install rel property type
        :type install_rel_property_type_name: str

        :param install_rel_property_value: value of the install rel property
        :type install_rel_property_value: str

        :return: True if everything was ok

        :raises: ValueError, MySQLError
        '''

        # Define query dictionary
        queryDict = {}
        whereDict = {}

        # Check install rel
        retrieveInstallRel = self.retrieveInstallRel(None, install_rel_parent, install_rel_child)

        if len(retrieveInstallRel) == 0:
            raise ValueError("Install rel doesn't exist in the database!")

        retrieveInstallRelKeys = retrieveInstallRel.keys()
        retrieveInstallRelObject = retrieveInstallRel[retrieveInstallRelKeys[0]]

        whereDict['install_rel_id'] = retrieveInstallRelObject['id']

        # Check install rel property type
        retrieveInstallRelPropertyType = self.retrieveInstallRelPropertyType(install_rel_property_type_name)

        if len(retrieveInstallRelPropertyType) == 0:
            raise ValueError("Install rel property type (%s) doesn't exist in the database!" % install_rel_property_type_name)

        retrieveInstallRelPropertyTypeKeys = retrieveInstallRelPropertyType.keys()
        installRelPropertyTypeId = retrieveInstallRelPropertyType[retrieveInstallRelPropertyTypeKeys[0]]['id']
        whereDict['install_rel_prop_type_id'] = installRelPropertyTypeId

        # Add value parameter into query
        if install_rel_property_value:
            queryDict['install_rel_prop_value'] = install_rel_property_value

        # Generate SQL
        sqlVals = _generateUpdateQuery('install_rel_prop', queryDict, None, None, whereDict)

        try:
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating install rel property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating install rel property:\n%s (%d)' % (e.args[1], e.args[0]))

    def deleteInstallRelProperty(self, install_rel_id):
        '''
        Delete install rel property

        :param install_rel_id: Id in the install rel table
        :type install_rel_id: int

        :return: True if everything was ok

        :raises:
            ValueError, MySQLError
        '''

        # Generate SQL
        sql = "DELETE FROM install_rel_prop WHERE install_rel_id = %s"
        vals = [install_rel_id]

        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when deleting install rel property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when deleting install rel property:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveInstallRel(self, parent_install, child_install, description=None, order=None, props=None):
        '''
        Save install relationship in the database.

        :param parent_install: name of the parent element
        :type parent_install: str

        :param child_install: name of the child element
        :type child_install: str

        :param description: description of the relationship
        :type description: str

        :param order: order of the child in the relationship
        :type order: int

        :param props: properties are passed as a map

            .. code-block:: python

                {
                    'key1': 'value1',
                    ...
                    'keyN': 'valueN'
                }

        :type props: dict

        :return:  a map with structure like:

            .. code-block:: python

                {'id': id of the saved install rel}

        :raises: ValueError, MySQLError
        '''

        # Check if the same relationship already exists in the database
        existingRel = self.retrieveInstallRel(None, parent_install, child_install)

        if len(existingRel):
            raise ValueError("Same relationship already exists in the database!")

        # Check if parent exists in install
        existingParent = self.retrieveInstall(parent_install)

        if len(existingParent) == 0:
            raise ValueError("Parent with id (%s) does not exist in the database!" % parent_install)

        parentKeys = existingParent.keys()
        parentObject = existingParent[parentKeys[0]]

        # Check if child exists in install
        existingChild = self.retrieveInstall(child_install)

        if len(existingChild) == 0:
            raise ValueError("Child with id (%s) does not exist in the database!" % child_install)

        childKeys = existingChild.keys()
        childObject = existingChild[childKeys[0]]

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
            cur.execute(sql, (parentObject['id'], childObject['id'], description, order))

            # Get last row id
            idrel = cur.lastrowid

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            # Install rel is saved, now we can save properties
            if props:

                # Convert to json
                if isinstance(props, (dict)) is False:
                    props = json.loads(props)

                # Save each property
                for key in props:
                    value = props[key]
                    self.saveInstallRelProperty(idrel, key, value)

            return {'id': idrel}

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            if isinstance(e, ValueError):
                raise e

            else:
                self.logger.info('Error when saving new install rel:\n%s (%d)' % (e.args[1], e.args[0]))
                raise MySQLError('Error when saving new install rel:\n%s (%d)' % (e.args[1], e.args[0]))

    def updateInstallRel(self, parent_install, child_install, **kws):
        '''
        Update install relationship.

        :param parent_install: name of the parent element we want ot update by
        :type parent_install: str

        :param child_install: name of the child element we want ot update by
        :type child_install: str

        :param description: description of the relationship
        :type description: str

        :param order: order of the child in the relationship
        :type order: int

        :param props:

            .. code-block:: python

                {
                    'key1': 'value1',
                    ...
                    'keyN': 'valueN'
                }

        :returns: True if everything is ok

        :raises: ValueError, MySQLError
        '''

        # Define query dictionary
        queryDict = {}
        whereDict = {}

        # Check if parent exists in install
        existingParent = self.retrieveInstall(parent_install)

        if len(existingParent) == 0:
            raise ValueError("Parent with id (%s) does not exist in the database!" % parent_install)

        parentKeys = existingParent.keys()
        parentObject = existingParent[parentKeys[0]]

        whereDict['parent_install_id'] = parentObject['id']

        # Check if child exists in install
        existingChild = self.retrieveInstall(child_install)

        if len(existingChild) == 0:
            raise ValueError("Child with id (%s) does not exist in the database!" % child_install)

        childKeys = existingChild.keys()
        childObject = existingChild[childKeys[0]]

        whereDict['child_install_id'] = childObject['id']

        # Add description
        if 'description' in kws:
            queryDict['logical_desc'] = kws['description']

        # Add order
        if 'order' in kws:
            queryDict['logical_order'] = kws['order']

        # Generate SQL
        sqlVals = _generateUpdateQuery('install_rel', queryDict, None, None, whereDict)

        try:
            # Insert entity
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            # Install rel is saved, now we can save properties
            if 'props' in kws and kws['props'] is not None:
                props = kws['props']

                # Convert to json
                if isinstance(props, (dict)) is False:
                    props = json.loads(props)

                installRel = self.retrieveInstallRel(None, parent_install, child_install)

                if len(installRel) != 1:
                    raise ValueError("There should be one install rel with parent name (%s) and child name (%s) in the database!" % (parent_install, child_install))

                installRelKeys = installRel.keys()
                relObj = installRel[installRelKeys[0]]

                # Save each property
                for key in props:
                    value = props[key]

                    if key in relObj['prop_keys']:

                        # Update property
                        self.updateInstallRelPropertyByMap(parent_install, child_install, key, value)

                    else:
                        # Save new property
                        self.saveInstallRelProperty(relObj['id'], key, value)

            return True

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating install rel:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating install rel:\n%s (%d)' % (e.args[1], e.args[0]))

    def deleteInstallRel(self, parent_install, child_install):
        '''
        Delete install relationships down the tree. Also delete all the properties of the relationships being deleted.

        :param parent_install: name of the parent install
        :type parent_install: string

        :param child_install: name of the child install
        :type child_install: string
        '''

        # Check for existing install rel
        existingInstallRel = self.retrieveInstallRel(None, parent_install, child_install)

        if len(existingInstallRel) == 0:
            raise ValueError("Install rel with parent id (%s) and child id (%s) does not exist in the database!" % (parent_install, child_install))

        relKeys = existingInstallRel.keys()
        relObject = existingInstallRel[relKeys[0]]

        # Find children
        childrenRel = self.retrieveInstallRel(None, child_install, None)

        for rel in childrenRel:
            child = childrenRel[rel]

            self.deleteInstallRel(child['parentname'], child['childname'])

        # Delete properties
        self.deleteInstallRelProperty(relObject['id'])

        # Delete install rel
        self.deleteInstallRelRaw(relObject['id'])

    def deleteInstallRelRaw(self, install_rel_id):
        '''
        Delete install relationship.

        :param parent_install: name of the parent install
        :type parent_install: string

        :param child_install: name of the child install
        :type child_install: string

        :returns: True if everything is ok

        :raises: ValueError, MySQLError
        '''

        # Generate SQL
        sql = "DELETE FROM install_rel WHERE install_rel_id = %s"
        vals = [install_rel_id]

        try:
            # Insert entity
            cur = self.conn.cursor()
            cur.execute(sql, vals)

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when deleting install rel:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when deleting install rel:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveInstallRel(self, install_rel_id=None, parent_install=None, child_install=None, description=None, order=None, date=None, expected_property=None):
        '''
        Retrieve install rel from the database. Specific relation can be retrieved or all the children of specific parent or
        all the parents of specific child.

        :param install_rel_id: id of the install_rel table
        :type install_rel_id: int

        :param parent_install: name of the parent install element
        :type parent_install: str

        :param child_install: name of the child install element
        :type child_install: str

        :param description: description of a relationship
        :type description: str

        :param order: order number of child element in the parent element; accepts a range in a tuple
        :type order: int

        :param date: date of the device installation; accepts a range in a tuple
        :type date: str

        :param prop: if we want to search for relationships with specific property set to a specific value, we
              can prepare a dict and pass it to the function e.g. {'beamline': 'xh*'} will return all of the
              beamlines with names starting with xh or {'beamline': None} will return all of the beamlines
        :type prop: dict

        :return: a map with structure like:

            .. code-block:: python

                {
                    'id': {
                        'id':           #int,
                        'parentid':     #int,
                        'parentname':   #string,
                        'childid':      #int,
                        'childname':    #string,
                        'description':  #string,
                        'order':        #int,
                        'date':         #string,
                        'prop1key':     #string,
                        ...
                        'propNkey':     #string,
                        'prop_keys':    ['prop1key', 'propNkey']
                    }
                }

        :raises: ValueError, MySQLError
        '''

        # Create vals list
        vals = []

        # Generate SQL
        if expected_property is None:
            sql = '''
            SELECT
                ir.install_rel_id,
                ir.parent_install_id,
                ir.child_install_id,
                ir.logical_desc,
                ir.logical_order,
                ir.install_date,
                insp.field_name,
                insc.field_name
            FROM install_rel ir
            LEFT JOIN install insp ON(ir.parent_install_id = insp.install_id)
            LEFT JOIN install insc ON(ir.child_install_id = insc.install_id)
            WHERE ir.child_install_id != ir.parent_install_id
            '''
        else:

            # Check expected property parameter
            if len(expected_property.keys()) > 1:
                raise ValueError("Expected property dictionary can contain only one key. Current dictionary contains (%s) keys." % len(expected_property))

            expectedPropertyKeys = expected_property.keys()

            sql = '''
            SELECT
                ir.install_rel_id,
                ir.parent_install_id,
                ir.child_install_id,
                ir.logical_desc,
                ir.logical_order,
                ir.install_date,
                insp.field_name,
                insc.field_name
            FROM install_rel ir
            LEFT JOIN install_rel_prop irp ON(ir.install_rel_id = irp.install_rel_id)
            LEFT JOIN install_rel_prop_type irpt ON(irp.install_rel_prop_type_id = irpt.install_rel_prop_type_id)
            LEFT JOIN install insp ON(ir.parent_install_id = insp.install_id)
            LEFT JOIN install insc ON(ir.child_install_id = insc.install_id)
            WHERE irpt.install_rel_prop_type_name = %s
            '''

            vals.append(expectedPropertyKeys[0])

            # Check if expected property value is not None and append it
            if expected_property[expectedPropertyKeys[0]] is not None:
                sql += ' AND irp.install_rel_prop_value = %s '
                vals.append(expected_property[expectedPropertyKeys[0]])

        # Check install_rel_id parameter
        if install_rel_id:
            sql += ' AND ir.install_rel_id = %s '
            vals.append(install_rel_id)

        # Check parent_install
        if parent_install:
            sql += ' AND insp.field_name = %s '
            vals.append(parent_install)

        # Check child_install
        if child_install:
            sql += ' AND insc.field_name = %s '
            vals.append(child_install)

        # Check description parameter
        if description:
            sqlVals = _checkWildcardAndAppend('ir.logical_desc', description, sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]

        # Check order parameter
        if order:
            sqlVals = _checkRangeAndAppend('ir.logical_order', order, sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]

        # Check date parameter
        if date:
            sqlVals = _checkRangeAndAppend('ir.install_date', date, sql, vals, 'AND')
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
                    'parentname': r[6],
                    'childid': r[2],
                    'childname': r[7],
                    'description': r[3],
                    'order': r[4],
                    'date': r[5].strftime("%Y-%m-%d %H:%M:%S"),
                    'prop_keys': []
                }

                # Get the rest of the properties
                properties = self._retrieveInstallRelProperty(r[0])

                # Append properties to existing object
                for prop in properties:
                    obj = properties[prop]
                    resdict[r[0]][obj['typename']] = obj['value']
                    resdict[r[0]]['prop_keys'].append(obj['typename'])

            return resdict

        except MySQLdb.Error as e:

            self.logger.info('Error when fetching install rel:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching install rel:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveTrees(self, install_name, rel=None, tree=None, parent_install=None):
        '''
        Retrieve installation relation as a tree

        :param install_name: name of the install
        :type install_name: str

        :param rel_id: relation id
        :type rel_id: int

        :param tree: current tree structure
        :type tree: str

        :return: install relations in a tree
        '''

        start = False

        if tree is None:
            tree = {}
            start = True

        else:
            tree[install_name] = {}
            tree[install_name]['children'] = []
            tree[install_name]['name'] = install_name
            tree[install_name]['id'] = rel['id']
            tree[install_name]['obj'] = rel
            tree[install_name]['parent'] = parent_install

            # Get self map
            selfRel = self.retrieveInstallRel(child_install=install_name, parent_install=install_name, expected_property={'__virtual_rel__': 'true'})

            # Append self map
            if len(selfRel) != 0:
                tree[install_name]['data'] = selfRel[selfRel.keys()[0]]

        if start:

            if install_name == "root":
                rootRel = self.retrieveInstallRel(expected_property={'__node_type__': 'root'})

            else:
                rootRel = self.retrieveInstallRel(parent_install=install_name)

            # If root element was not found, return empty tree
            if len(rootRel) == 0:
                return tree

            rootNode = rootRel[rootRel.keys()[0]]

            # Add link to root
            if install_name == "root":
                tree["/"] = {}
                tree["/"]['name'] = "/"
                tree["/"]['children'] = [rootNode['parentname']]

            install_name = rootNode['parentname']

            # Get self map
            selfRel = self.retrieveInstallRel(child_install=install_name, parent_install=install_name, expected_property={'__virtual_rel__': 'true'})

            # Start making a tree
            tree[install_name] = {}
            tree[install_name]['children'] = []
            tree[install_name]['name'] = install_name
            tree[install_name]['id'] = rootNode['id']
            tree[install_name]['obj'] = rootNode
            tree[install_name]['parent'] = "/"

            # Append self map
            if len(selfRel) != 0:
                tree[install_name]['data'] = selfRel[selfRel.keys()[0]]

            children = self.retrieveInstallRel(None, install_name)

        else:
            children = self.retrieveInstallRel(None, install_name)

        # Go through children
        for childKey in children.keys():
            child = children[childKey]
            tree[install_name]['children'].append(child['childname'])
            self.retrieveTrees(child['childname'], child, tree, install_name)

        return tree

        # start = False

        # if tree is None:
        #     tree = {}
        #     start = True

        # else:
        #     tree[install_name] = {}
        #     tree[install_name]['children'] = {}
        #     tree[install_name]['name'] = install_name
        #     tree[install_name]['id'] = rel_id
        #     tree[install_name]['parent'] = parent_install

        #     # Get self map
        #     selfRel = self.retrieveInstallRel(child_install=install_name, parent_install=install_name, expected_property={'__virtual_rel__': 'true'})

        #     # Append self map
        #     if len(selfRel) != 0:
        #         tree[install_name]['data'] = selfRel[selfRel.keys()[0]]

        # if start:

        #     if install_name == "root":
        #         rootRel = self.retrieveInstallRel(expected_property={'__node_type__': 'root'})

        #     else:
        #         rootRel = self.retrieveInstallRel(parent_install=install_name)

        #     # If root element was not found, return empty tree
        #     if len(rootRel) == 0:
        #         return tree

        #     rootNode = rootRel[rootRel.keys()[0]]
        #     install_name = rootNode['parentname']

        #     # Get self map
        #     selfRel = self.retrieveInstallRel(child_install=install_name, parent_install=install_name, expected_property={'__virtual_rel__': 'true'})

        #     # Start making a tree
        #     tree[install_name] = {}
        #     tree[install_name]['children'] = {}
        #     tree[install_name]['name'] = install_name
        #     tree[install_name]['id'] = rootNode['id']
        #     tree[install_name]['parent'] = ["/"]

        #     # Append self map
        #     if len(selfRel) != 0:
        #         tree[install_name]['data'] = selfRel[selfRel.keys()[0]]

        #     newTree = tree[install_name]['children']
        #     children = self.retrieveInstallRel(None, install_name)

        # else:
        #     newTree = tree[install_name]['children']
        #     children = self.retrieveInstallRel(None, install_name)

        # currentParent = tree[install_name]['parent']

        # # Go through children
        # for childKey in children.keys():
        #     child = children[childKey]
        #     nextParent = currentParent
        #     nextParent.append(install_name)
        #     self.retrieveTrees(child['childname'], child['id'], newTree, nextParent)

        # return tree

    def idStatusHelper(self, inputStr):
        '''
        Clean ID status string and return correct int values

        :param inputStr: Input string
        :type inputStr: str

        :return: cleaned status

        '''

        if inputStr == "Y":
            return 0

        else:
            return 1

    def idNoneHelper(self, inputStr, returnType=None):
        '''
        Clean ID input parameter

        :param inputStr: Input string
        :type inputStr: str

        :param returnType: Type of the returned data
        :type returnType: str

        :return: cleaned input

        '''

        # Strip input string of spaces
        inputStr = inputStr.strip()

        if inputStr == "None":
            return None

        else:

            if returnType is not None:

                if returnType == "float":
                    return float(inputStr)

                else:
                    return inputStr

            else:
                return inputStr

    def saveInsertionDevice(
            self, install_name=None, coordinate_center=None, project=None,
            beamline=None, beamline_desc=None, install_desc=None,
            inventory_name=None, down_corrector=None, up_corrector=None,
            length=None, gap_max=None, gap_min=None, gap_tolerance=None,
            phase1_max=None, phase1_min=None, phase2_max=None,
            phase2_min=None, phase3_max=None, phase3_min=None,
            phase4_max=None, phase4_min=None, phase_tolerance=None,
            k_max_circular=None, k_max_linear=None, phase_mode_a1=None,
            phase_mode_a2=None, phase_mode_p=None, type_name=None, type_desc=None
            ):
        '''
        Save insertion device

        :param install_name: installation name
        :type install_name: str

        :param coordinate_center: coordinate center
        :type coordinate_center: float

        :param project: project name
        :type project: str

        :param beamline: beamline name
        :type beamline: str

        :param beamline_desc: beamline description
        :type beamline_desc: str

        :param install_desc: install description
        :type install_desc: str

        :param inventory_name: inventory name
        :type inventory_name: str

        :param down_corrector: inventory property down corrector
        :type down_corrector: str

        :param up_corrector: inventory property up corrector
        :type up_corrector: str

        :param length: inventory property length
        :type length: str

        :param gap_max: invnetory property gap maximum
        :type gap_max: str

        :param gap_min: inventory property gap minimum
        :type gap_min: str

        :param gap_tolerance: inventory property gap tolerance
        :type gap_tolerance: str

        :param phase1_max: inventory property phase1 maximum
        :type phase1_max: str

        :param phase1_min: inventory property phase1 minimum
        :type phase1_min: str

        :param phase2_max: inventory prperty phase2 maximum
        :type phase2_max: str

        :param phase2_min: inventory property phase2 minimum
        :type phase2_min: str

        :param phase3_max: inventory property phase3 maximum
        :type phase3_max: str

        :param phase3_min: inventory property phase3 minimum
        :type phase3_min: str

        :param phase4_max: inventory property phase4 maximum
        :type phase4_max: str

        :param phase4_min: inventory property phase4 minimum
        :type phase4_min: str

        :param phase_tolerance: inventory property phase tolerance
        :type phase_tolerance: str

        :param k_max_circular: inventory property k maximum circular
        :type k_max_circular: str

        :param k_max_linear: inventory property k maximum linear
        :type k_max_linear: str

        :param phase_mode_a1: inventory property phase mode a1
        :type phase_mode_a1: str

        :param phase_mode_a2: inventory property phase mode a2
        :type phase_mode_a2: str

        :param phase_mode_p: inventory property phase mode p
        :type phase_mode_p: str

        :param type_name: component type name
        :type type_name: str

        :param type_desc: component type description
        :type type_desc: str

        :return: True if everything went ok

        :raise: ValueError, MySQLError
        '''

        # Check install name and inventory name. Both should not be None
        if install_name is None and inventory_name is None:
            raise ValueError('Both inventory name and install name should not be None!')

        # Create component types
        # if len(self.retrieveComponentType('root').keys()) == 0:
        #     raise ValueError('You are saving insertion device for the first time. Please run idodsInstall() and than insert device again.')

        # Install name is provided, beamline and project name should be defined
        if install_name:

            if beamline is None or project is None:
                raise ValueError('If install name is defined, project and beamline should also be defined!')

            # Save project
            # if len(self.retrieveInstall(project).keys()) == 0:
            #    res = self.saveInstall(project, description='__system__', cmpnt_type='project')

            # Save beamline
            # if len(self.retrieveInstall(beamline).keys()) == 0:
            #     self.saveInstall(beamline, description='__system__', cmpnt_type='project')

            # # Save beamline  - project rel
            # if len(self.retrieveInstallRel(None, 'Beamline project', project).keys()) == 0:
            #     self.saveInstallRel('Beamline project', project)

            # # Save project  - beamline rel
            # if len(self.retrieveInstallRel(None, project, beamline).keys()) == 0:
            #     self.saveInstallRel(project, beamline, description=beamline_desc)

        # Component type should not be None
        if type_name is None:
            raise ValueError('Component type parameter is missing!')

        # Save component type
        if len(self.retrieveComponentType(type_name).keys()) == 0:
            self.saveComponentType(type_name, type_desc)

        # Save inventory if inventory name is defined
        if inventory_name:

            # Save inventory
            self.saveInventory(inventory_name, cmpnt_type=type_name, props={
                'down_corrector': down_corrector,
                'up_corrector': up_corrector,
                'length': length,
                'gap_maximum': gap_max,
                'gap_minimum': gap_min,
                'gap_tolerance': gap_tolerance,
                'phase1_maximum': phase1_max,
                'phase1_minimum': phase1_min,
                'phase2_maximum': phase2_max,
                'phase2_minimum': phase2_min,
                'phase3_maximum': phase3_max,
                'phase3_minimum': phase3_min,
                'phase4_maximum': phase4_max,
                'phase4_minimum': phase4_min,
                'phase_tolerance': phase_tolerance,
                'k_max_circular': k_max_circular,
                'k_max_linear': k_max_linear,
                'phase_mode_a1': phase_mode_a1,
                'phase_mode_a2': phase_mode_a2,
                'phase_mode_p': phase_mode_p
            })

        # Save install if install name is defined
        if install_name:

            # Save install
            res = self.saveInstall(
                install_name,
                coordinatecenter=coordinate_center,
                description=install_desc,
                cmpnt_type=type_name
            )

            # Create property types if they do not exist and save their values
            if len(self.retrieveInstallRelPropertyType('project').keys()) == 0:
                self.saveInstallRelPropertyType('project', 'System parameter')

            self.saveInstallRelProperty(res['rel_id'], 'project', project)

            if len(self.retrieveInstallRelPropertyType('project').keys()) == 0:
                self.saveInstallRelPropertyType('project', 'System parameter')

            self.saveInstallRelProperty(res['rel_id'], 'beamline', beamline)

            ### Beamline description

        # Save beamline  - install rel
        # if len(self.retrieveInstallRel(None, beamline, install_name).keys()) == 0:
        #     self.saveInstallRel(beamline, install_name)

        # Only install device if inventory name and install name are defined
        if install_name and inventory_name:

            # Save inventory to install
            if len(self.retrieveInventoryToInstall(None, install_name, inventory_name).keys()) == 0:
                self.saveInventoryToInstall(install_name, inventory_name)

        return True

    def saveInstall(self, name, **kws):
        '''
        Save insertion device installation using any of the acceptable key words:

        :param name: installation name, which is its label on field
        :type name: str

        :param description: installation description
        :type description: str

        :param cmpnt_type: component type of the device
        :type cmpnt_type: str

        :param coordinatecenter: coordinate center number
        :type coordinatecenter: float

        :return: a map with structure like:

            .. code-block:: python

                {'id': new install id}

        :raises: ValueError, Exception
        '''
        startedd = time.time()
        # Check name parameter
        _checkParameter('name', name)

        # Check name parameter
        res = self.retrieveInstall(name)

        if len(res) != 0:
            raise ValueError("Install (%s) already exists in database." % (name))

        # Check component type
        if 'cmpnt_type' in kws and kws['cmpnt_type'] is not None:
            componentType = self.retrieveComponentType(kws['cmpnt_type'])
            componentTypeKeys = componentType.keys()

        else:
            raise ValueError("Cmpnttype attribute should be present when inserting new installation!")

        # Check install description
        description = None

        if 'description' in kws and kws['description'] is not None:
            description = kws['description']

        # Check coordinate center
        coordinate = None

        if 'coordinatecenter' in kws and kws['coordinatecenter'] is not None:
            coordinate = kws['coordinatecenter']

        startedd2 = time.time()
        key = componentType[componentTypeKeys[0]]['id']
        invid = self.physics.saveInstall(name, description, key, coordinate)

        total2 = time.time() - startedd2
        total2 = total2*1000
        print '=> elapsed time idods.saveInstall.DB: %f ms' % total2

        total = time.time() - startedd
        total = total*1000
        print '=> elapsed time idods.saveInstall.W: %f ms' % total

        # Save install rel so properties can be saved fot install
        mapid = self.physics.saveInstallRel(invid, invid)
        self.saveInstallRelProperty(mapid, '__virtual_rel__', 'true')

        return {'id': invid, 'rel_id': mapid}

    def updateInstall(self, install_id, old_name, name, **kws):
        '''Update insertion device installation using any of the acceptable key words:

        :param name: installation name, which is its label on field
        :type name: str

        :param description: installation description
        :type description: str

        :param cmpnt_type: component type of the device
        :type cmpnt_type: str

        :param coordinatecenter: coordinate center number
        :type coordinatecenter: float

        :raises: ValueError, MySQLError

        :return: True if everything is ok
        '''

        # Define query dictionary
        queryDict = {}
        whereKey = None
        whereValue = None

        # Check id
        if install_id:
            _checkParameter('id', install_id, 'prim')
            whereKey = 'install_id'
            whereValue = install_id

        # Check name
        if old_name:
            _checkParameter('name', old_name)
            whereKey = 'field_name'
            whereValue = old_name

        # Check if where key is set
        if whereKey is None:
            raise ValueError("Id or old name should be present to execute an update!")

        # Check name parameter
        _checkParameter('name', name)
        queryDict['field_name'] = name

        # Check component type
        if 'cmpnt_type' in kws:
            componentType = self.retrieveComponentType(kws['cmpnt_type'])
            componentTypeKeys = componentType.keys()
            queryDict['cmpnt_type_id'] = componentType[componentTypeKeys[0]]['id']

        # Check install description
        if 'description' in kws:
            description = kws['description']
            queryDict['location'] = description

        # Check coordinate center
        if 'coordinatecenter' in kws:
            coordinate = kws['coordinatecenter']
            queryDict['coordinate_center'] = coordinate

        # Generate SQL
        sqlVals = _generateUpdateQuery('install', queryDict, whereKey, whereValue)

        try:
            # Insert record into database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            return True

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating inventory:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating inventory:\n%s (%d)' % (e.args[1], e.args[0]))

    def _retrieveInstallById(self, installid):
        '''
        Retrieve install its id.

        :param installid: id of the install entity
        :type installid: int

        :return: a map with structure like:

            .. code-block:: python

                {'id': {
                        'id':                  #int,
                        'cmpnt_type':           #string,
                        'name':                #string,
                        'description':         #string,
                        'coordinationcenter':  #float
                    }
                }

        :raises: ValueError, MySQLError
        '''

        # Check install id
        if installid is None:
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
            self.logger.info('Error when fetching install from the database:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching install from the database:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveInstall(self, name, **kws):
        '''
        Retrieve insertion device installation using any of the acceptable key words:

        :param name: installation name, which is its label on field
        :type name: str

        :param description: installation description
        :type description: str

        :param cmpnt_type: component type name of the device
        :type cmpnt_type: str

        :param coordinatecenter: coordinate center number
        :type coordinatecenter: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': {
                        'id':                     #int,
                        'name':                   #string,
                        'description':            #string,
                        'cmpnt_type':             #string,
                        'cmpnt_type_description': #string,
                        'coordinatecenter':       #float,
                        'key1':                   #str,
                        ...
                        'prop_keys':              ['key1', 'key2']
                    }
                }

        :Raises: ValueError, MySQLError
        '''
        startedd2 = time.time()
        # Check name
        _checkParameter('name', name)

        # Generate SQL
        sql = '''
        SELECT
            inst.install_id,
            inst.cmpnt_type_id,
            inst.field_name,
            inst.location,
            inst.coordinate_center,
            ct.cmpnt_type_name,
            ct.description
        FROM install inst
        LEFT JOIN cmpnt_type ct ON(inst.cmpnt_type_id = ct.cmpnt_type_id)
        WHERE
        '''

        vals = []

        # Append name parameter
        sqlVals = _checkWildcardAndAppend('inst.field_name', name, sql, vals)

        # Append description parameter
        if 'description' in kws and kws['description'] is not None:
            # Append description
            sqlVals = _checkWildcardAndAppend('inst.location', kws['description'], sqlVals[0], sqlVals[1], 'AND')

        # Append component type parameter
        if 'cmpnt_type' in kws and kws['cmpnt_type'] is not None:
            sqlVals = _checkWildcardAndAppend('ct.cmpnt_type_name', kws['cmpnt_type'], sqlVals[0], sqlVals[1], 'AND')

        # Append coordination center parameter
        if 'coordinatecenter' in kws and kws['coordinatecenter'] is not None:
            sqlVals = _checkRangeAndAppend('inst.coordinate_center', kws['coordinatecenter'], sqlVals[0], sqlVals[1], 'AND')

        try:

            startedd = time.time()

            # Execute SQL
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Get last id
            res = cur.fetchall()
            resdict = {}
            total = time.time() - startedd
            total = total*1000
            print '=> elapsed time idods.retrieveInstall.DB: %f ms' % total

            # Construct return dict
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'name': r[2],
                    'description': r[3],
                    'cmpnt_type': r[5],
                    'coordinatecenter': r[4],
                    'cmpnt_type_description': r[6],
                    'prop_keys': []
                }

                # Get rel
                selfRel = self.retrieveInstallRel(None, r[2], r[2], expected_property={'__virtual_rel__': 'true'})

                if len(selfRel) > 0:
                    relid = selfRel.keys()[0]
                    props = self.retrieveInstallRelProperty(relid)

                    for p in props:
                        prop = props[p]
                        resdict[r[0]][prop['typename']] = prop['value']
                        resdict[r[0]]['prop_keys'].append(prop['typename'])

            total2 = time.time() - startedd2
            total2 = total2*1000
            print '=> elapsed time idods.retrieveInstall.W: %f ms' % total2
            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching installation:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching installation:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveFile(self, file_name, data):
        '''
        Save file that was uploaded and return file path

        :param file_name: name of the file we want to save
        :type file_name: str

        :param data: data we want to save
        :type data: blob

        :return: a map with structure like:

            .. code-block:: python

                {'path': path to a file}

        :raises: IOError
        '''
        path, absolutePath = _generateFilePath()
        filePath = os.path.join(absolutePath, file_name)

        try:
            with open(filePath, 'w') as f:
                f.write(data)

            return {'path': os.path.join(path, file_name)}

        except IOError as e:
            self.logger.info('Error when writing to a file:\n%s (%d)' % (e.args[1], e.args[0]))
            raise IOError('Error when writing to a file:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveOnlineData(self, install_name, **kws):
        '''Save insertion device online data.

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

        :param feedforward_table_id: id of the raw data
        :type feedforward_table_id: str

        :return: a map with structure like:

            .. code-block:: python

                {'id': data id}

        :Raises: ValueError, MySQLError
        '''

        # Check install name
        _checkParameter('name', install_name)

        returnedInstall = self.retrieveInstall(install_name)

        if len(returnedInstall) == 0:
            raise ValueError("Install (%s) does not exist in the database!" % install_name)

        returnedInstallKeys = returnedInstall.keys()
        installid = returnedInstall[returnedInstallKeys[0]]['id']

        # Check username
        username = None

        if 'username' in kws and kws['username'] is not None:
            username = kws['username']

        # Check description
        description = None

        if 'description' in kws and kws['description'] is not None:
            description = kws['description']

        # Check url
        url = None

        if 'url' in kws and kws['url'] is not None:
            url = kws['url']

        # Check status
        status = None

        if 'status' in kws and kws['status'] is not None:
            status = kws['status']

        # Check feedforward table id
        feedforward_table_id = None

        if 'feedforward_table_id' in kws and kws['feedforward_table_id'] is not None:
            feedforward_table_id = kws['feedforward_table_id']

        # Generate SQL
        sql = '''
        INSERT INTO id_online_data (
            install_id,
            login_name,
            description,
            data_url,
            date,
            status,
            feedforward_table
        ) VALUES (
            %s, %s, %s, %s, NOW(), %s, %s
        )
        '''

        try:
            # Insert data into database
            cur = self.conn.cursor()
            cur.execute(sql, (
                installid,
                username,
                description,
                url,
                status,
                feedforward_table_id
            ))

            # Get last row id
            onlinedataid = cur.lastrowid

            # Create transactions
            if self.transaction is None:
                self.conn.commit()

            return {'id': onlinedataid}

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when saving new online data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when saving new online data:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveOnlineData(self, **kws):
        '''Retrieve insertion device online data.

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
                        'id':,                      #int
                        'installid':,               #int
                        'install_name':,            #string
                        'username':,                #string
                        'description':,             #string
                        'url':,                     #url
                        'date':,                    #date
                        'status':,                  #int
                        'feedforward_table_id':,    #int
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
            inst.field_name,
            iod.feedforward_table
        FROM id_online_data iod
        LEFT JOIN install inst ON(iod.install_id = inst.install_id)
        WHERE 1=1
        '''

        vals = []

        # Append online id
        if 'onlineid' in kws and kws['onlineid'] is not None:
            _checkParameter('id', kws['onlineid'], 'prim')
            sql += ' AND id_online_data_id = %s '
            vals.append(kws['onlineid'])

        # Append username
        if 'username' in kws and kws['username'] is not None:
            sqlVals = _checkWildcardAndAppend('iod.login_name', kws['username'], sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]

        # Append description
        if 'description' in kws and kws['description'] is not None:
            sqlVals = _checkWildcardAndAppend('iod.description', kws['description'], sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]

        # Append url
        if 'url' in kws and kws['url'] is not None:
            sqlVals = _checkWildcardAndAppend('iod.data_url', kws['url'], sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]

        # Append status
        if 'status' in kws and kws['status'] is not None:
            sqlVals = _checkRangeAndAppend('iod.status', kws['status'], sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]

        # Append install name
        if 'install_name' in kws and kws['install_name'] is not None:
            sqlVals = _checkWildcardAndAppend('inst.field_name', kws['install_name'], sql, vals, 'AND')
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
                    'status': r[6],
                    'feedforward_table_id': r[8]
                }

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching online data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching online data:\n%s (%d)' % (e.args[1], e.args[0]))

    def updateOnlineData(self, online_data_id, **kws):
        '''
        Update insertion device online data.

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

        :param feedforward_table_id: id of the raw data
        :type feedforward_table_id: str

        :return: True if everything is ok

        :Raises: ValueError, MySQLError
        '''

        # Define query dict
        queryDict = {}

        # Check id
        _checkParameter('id', online_data_id, 'prim')
        whereKey = 'id_online_data_id'
        whereValue = online_data_id

        # Check install name
        if 'install_name' in kws and kws['install_name'] is not None:
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
            queryDict['data_url'] = kws['url']

        # Check status
        if 'status' in kws:
            queryDict['status'] = kws['status']

        # Check feedforward table id
        if 'feedforward_table_id' in kws:
            queryDict['feedforward_table'] = kws['feedforward_table_id']

        # Generate SQL
        sqlVals = _generateUpdateQuery('id_online_data', queryDict, whereKey, whereValue)

        try:
            # Insert offline data into database
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])

            # Create transactions
            if self.transaction is None:
                self.conn.commit()

            return True

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when updating online data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating online data:\n%s (%d)' % (e.args[1], e.args[0]))

    def deleteOnlineData(self, online_data_id):
        '''
        Delete online data

        :param online_data_id: online data id
        :type online_data_id: int

        :return: True if everything was ok

        :Raises: ValueError, MySQLError
        '''

        # Retrieve offline data
        onlineData = self.retrieveOnlineData(onlineid=online_data_id)

        if len(onlineData) == 0:
            raise ValueError("Online data doesn't exist in the database!")

        onlineDataKey = onlineData.keys()[0]
        onlineDataObj = onlineData[onlineDataKey]

        if onlineDataObj['url'] == '':
            raise ValueError("Online data url is broken!")

        # Generate path and remove file
        ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
        savePath = os.path.split(ROOT_PATH)
        savePath = os.path.split(savePath[0])
        savePath = os.path.join(savePath[0], 'physics_dev', 'physics_django')

        if onlineDataObj['url'] is not None:
            filePath = os.path.join(savePath, onlineDataObj['url'])

            try:
                os.remove(filePath)

            except:
                raise IOError("File (%s) cannot be deleted!" % filePath)

        # Generate SQL
        sql = "DELETE FROM id_online_data WHERE id_online_data_id = %s"
        vals = [online_data_id]

        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)

            # Create transaction
            if self.transaction is None:
                self.conn.commit()

            # Delete raw data
            self.deleteRawData(onlineDataObj['feedforward_table_id'])

            return True

        except Exception as e:

            # Rollback changes
            if self.transaction is None:
                self.conn.rollback()

            self.logger.info('Error when deleting online data:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when deleting online data:\n%s (%d)' % (e.args[1], e.args[0]))

    def retrieveInstallOfflineData(self, install_name, **kws):
        '''Retrieve insertion device offline data using any of the acceptable key words:

        :param install_name: name of installed device on field
        :type install_name: str

        :param description: a brief description for this data entry
        :type description: str

        :param date: offline data date
        :type date: str

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

                {'offlinedata_id': {
                        'install_name': ,  # string
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
                        'data_id':,           # int
                        'methodname':,     # string
                        'methoddesc':,     # string
                    }
                }

        :Raises: ValueError, MySQLError
        '''

        # Check name
        _checkParameter('name', install_name)

        # Generate select SQL
        sql = '''
        SELECT
            inst.install_id,
            ii.inventory_id,
            inv.name,
            inst.field_name
        FROM install inst
        LEFT JOIN inventory__install ii ON(inst.install_id = ii.install_id)
        LEFT JOIN inventory inv ON(ii.inventory_id = inv.inventory_id)
        WHERE
        '''

        # Check description
        description = None

        if 'description' in kws and kws['description'] is not None:
            description = kws['description']

        # Check gap
        gap = None

        if 'gap' in kws and kws['gap'] is not None:
            gap = kws['gap']

        # Check date
        dateP = None

        if 'date' in kws and kws['date'] is not None:
            dateP = kws['date']

        # Check phase1
        phase1 = None

        if 'phase1' in kws and kws['phase1'] is not None:
            phase1 = kws['phase1']

        # Check phase2
        phase2 = None

        if 'phase2' in kws and kws['phase2'] is not None:
            phase2 = kws['phase2']

        # Check phase3
        phase3 = None

        if 'phase3' in kws and kws['phase3'] is not None:
            phase3 = kws['phase3']

        # Check phase4
        phase4 = None

        if 'phase4' in kws and kws['phase4'] is not None:
            phase4 = kws['phase4']

        # Check phasemode
        phasemode = None

        if 'phasemode' in kws and kws['phasemode'] is not None:
            phasemode = kws['phasemode']

        # Check polarmode
        polarmode = None

        if 'polarmode' in kws and kws['polarmode'] is not None:
            polarmode = kws['polarmode']

        # Check status
        status = None

        if 'status' in kws and kws['status'] is not None:
            status = kws['status']

        # Check method_name
        method_name = None

        if 'method_name' in kws and kws['method_name'] is not None:
            method_name = kws['method_name']

        vals = []

        # Append name parameter
        sqlVals = _checkWildcardAndAppend('inst.field_name', install_name, sql, vals)

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
                installname = r[3]

                # Skip if there is no map
                if inventoryname is None:
                    continue

                offlineData = self.retrieveOfflineData(
                    inventory_name=inventoryname,
                    description=description,
                    date=dateP,
                    gap=gap,
                    phase1=phase1,
                    phase2=phase2,
                    phase3=phase3,
                    phase4=phase4,
                    phasemode=phasemode,
                    polarmode=polarmode,
                    status=status,
                    method_name=method_name
                )

                # Go though the results and map them in result dictionary
                for key in offlineData:
                    offlineDatum = offlineData[key]
                    resdict[key] = offlineDatum
                    resdict[key]['install_name'] = installname

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching offline data from installation:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when fetching offline data from installation:\n%s (%d)' % (e.args[1], e.args[0]))

    def idodsInstall(self):
        '''
        Create necessary database entries
        '''

        # Create component type property type for identifying ID devices
        # if len(self.retrieveComponentTypePropertyType('insertion_device').keys()) == 0:
        #    self.saveComponentTypePropertyType('insertion_device')

        # Create install property types
        if len(self.retrieveInstallRelPropertyType('__device_category__').keys()) == 0:
            self.saveInstallRelPropertyType('__device_category__', 'System parameter')

        if len(self.retrieveInstallRelPropertyType('__node_type__').keys()) == 0:
            self.saveInstallRelPropertyType('__node_type__', 'System parameter')

        if len(self.retrieveInstallRelPropertyType('__virtual_rel__').keys()) == 0:
            self.saveInstallRelPropertyType('__virtual_rel__', 'System parameter')

        if len(self.retrieveInstallRelPropertyType('beamline').keys()) == 0:
            self.saveInstallRelPropertyType('beamline', 'Beamline name')

        if len(self.retrieveInstallRelPropertyType('project').keys()) == 0:
            self.saveInstallRelPropertyType('project', 'Project name')

        # Create component types
        if len(self.retrieveComponentType('__virtual_device__').keys()) == 0:
            self.saveComponentType('__virtual_device__', 'Device is not an actual device but a tree node')

        return True

    def retrieveRotCoilData(self, inventory_name):
        '''
        Return rotation coil data

        :param inventory_name: name of the device in the inventory
        :type inventory_name: str

        :return: dictionary with a structure like:

            .. code-block:: python

                {
                    'id': {
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
                        b_ref_int,
                        roll_angle,
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
                        inventory_name
                    },
                    ...
                }

        :Raises: ValueError, MySQLError
        '''

        # Check inventory
        inventory = self.retrieveInventory(inventory_name)

        if len(inventory) == 0:
            raise ValueError("Inventory (%s) does not exist in the database." % (inventory_name))

        inventory_id = inventory.keys()[0]

        resdict = {}
        res = self.physics.retrieveRotCoilData(inventory_id)

        # Construct return dict
        for r in res:
            resdict[r[0]] = {
                'id': r[0],
                'inventory_id': r[1],
                'alias': r[2],
                'meas_coil_id': r[3],
                'ref_radius': r[4],
                'magnet_notes': r[5],
                'login_name': r[6],
                'cond_curr': r[7],
                'meas_loc': r[8],
                'run_number': r[9],
                'sub_device': r[10],
                'current_1': r[11],
                'current_2': r[12],
                'current_3': r[13],
                'up_dn_1': r[14],
                'up_dn_2': r[15],
                'up_dn_3': r[16],
                'analysis_number': r[17],
                'integral_xfer_function': r[18],
                'orig_offset_x': r[19],
                'orig_offset_y': r[20],
                'b_ref_int': r[21],
                'roll_angle': r[22],
                'meas_notes': r[23],
                'meas_date': r[24].strftime("%Y-%m-%d %H:%M:%S"),
                'author': r[25],
                'a1': r[26],
                'a2': r[27],
                'a3': r[28],
                'b1': r[29],
                'b2': r[30],
                'b3': r[31],
                'a4_21': r[32],
                'b4_21': r[33],
                'data_issues': r[34],
                'data_usage': r[35],
                'inventory_name': r[36]
            }

        return resdict

    def saveRotCoilData(
            self, inventory_name, alias=None, meas_coil_id=None, ref_radius=None, magnet_notes=None, login_name=None, cond_curr=None,
            meas_loc=None, run_number=None, sub_device=None, current_1=None, current_2=None, current_3=None, up_dn_1=None, up_dn_2=None, up_dn_3=None,
            analysis_number=None, integral_xfer_function=None, orig_offset_x=None, orig_offset_y=None, b_ref_int=None, roll_angle=None,
            meas_notes=None, author=None, a1=None, a2=None, a3=None, b1=None, b2=None, b3=None, a4_21=None, b4_21=None, data_issues=None, data_usage=None
            ):
        '''
        Save rotation coil data

        :param inventory_name: name of the device in the inventory
        :type inventory_name: str

        :param alias: alias name
        :type alias: str

        :param meas_coil_id: ID number of device used for this measurement
        :type meas_coil_id: str

        :param ref_radius: reference radius
        :type ref_radius: double

        :param magnet_notes: comment for this magnet measurement data set
        :type magnet_notes: str

        :param login_name: user who generated this data set
        :type login_name: str

        :param cond_curr: condition current
        :type cond_curr: double

        :param meas_loc: measurement location
        :type meas_loc: str

        :param run_number: in which run this data was produced
        :type run_number: str

        :param sub_device: name of the sub device
        :type sub_device: str

        :param current_1: 1 st measurement current
        :type current_1: double

        :param current_2: 2 nd measurement current
        :type current_2: double

        :param current_3: 3 rd measurement current
        :type current_3: double

        :param up_dn_1: direction of 1 st current
        :type up_dn_1: str

        :param up_dn_2: direction of 2 nd current
        :type up_dn_2: str

        :param up_dn_3: direction of 4 rd current
        :type up_dn_3: str

        :param analysis_number: in which analysis does this data belongs
        :type analysis_number: str

        :param integral_xfer_function: integral transfer function
        :type integral_xfer_function: double

        :param orig_offset_x: horizontal origin offset
        :type orig_offset_x: double

        :param orig_offset_y: vertical origin offset
        :type orig_offset_y: double

        :param b_ref_int: integrated reference field
        :type b_ref_int: double

        :param roll_angle: rolling angle
        :type roll_angle: double

        :param meas_notes: comments for each measuring data point
        :type meas_notes: str

        :param author: who measured it
        :type author: str

        :param a1: magnetic field (a1)
        :type a1: double

        :param a2: magnetic field (a2)
        :type a2: double

        :param a3: magnetic field (a3)
        :type a3: double

        :param b1: magnetic field (b1)
        :type b1: double

        :param b2: magnetic field (b2)
        :type b2: double

        :param b3: magnetic field (b3)
        :type b3: double

        :param a4_21: high order magnetic field (a4 to a21)
        :type a4_21: str

        :param b4_21: high order magnetic field (b4 to b21)
        :type b4_21: str

        :param data_issues: Reserved: special field to note each measure point
        :type data_issues: str

        :param data_usage: Reserved
        :type data_usage: int

        :return: a map with structure like:

            .. code-block:: python

                {'id': rot coil data id}

        :Raises: ValueError, MySQLError
        '''

        # Check inventory
        inventory = self.retrieveInventory(inventory_name)

        if len(inventory) == 0:
            raise ValueError("Inventory (%s) does not exist in the database." % (inventory_name))

        inventory_id = inventory.keys()[0]

        result = self.physics.saveRotCoilData(
            inventory_id, alias, meas_coil_id, ref_radius, magnet_notes, login_name, cond_curr,
            meas_loc, run_number, sub_device, current_1, current_2, current_3, up_dn_1, up_dn_2, up_dn_3,
            analysis_number, integral_xfer_function, orig_offset_x, orig_offset_y, b_ref_int, roll_angle,
            meas_notes, author, a1, a2, a3, b1, b2, b3, a4_21, b4_21, data_issues, data_usage)

        return {'id': result}

    def updateRotCoilData(
            self, rot_coil_data_id, inventory_name=None, alias=None, meas_coil_id=None, ref_radius=None, magnet_notes=None, login_name=None, cond_curr=None,
            meas_loc=None, run_number=None, sub_device=None, current_1=None, current_2=None, current_3=None, up_dn_1=None, up_dn_2=None, up_dn_3=None,
            analysis_number=None, integral_xfer_function=None, orig_offset_x=None, orig_offset_y=None, b_ref_int=None, roll_angle=None,
            meas_notes=None, author=None, a1=None, a2=None, a3=None, b1=None, b2=None, b3=None, a4_21=None, b4_21=None, data_issues=None, data_usage=None):
        '''
        Update rotation coil data

        :param rot_coil_data_id:
        :type rot_coil_data_id: int

        :param inventory_name: name of the device in the inventory
        :type inventory_name: str

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

        :raises: ValueError, MySQLError
        '''

        # Check id
        _checkParameter('id', rot_coil_data_id, 'prim')

        inventory_id = None

        if inventory_name:
            # Check inventory
            retrieveInventory = self.retrieveInventory(inventory_name)

            if len(retrieveInventory) == 0:
                raise ValueError("Inventory (%s) doesn't exist in the database!" % oldInventoryName)

            retrieveInventoryKeys = retrieveInventory.keys()
            inventory_id = retrieveInventory[retrieveInventoryKeys[0]]['id']

        return self.physics.updateRotCoilData(
            rot_coil_data_id, inventory_id, alias, meas_coil_id, ref_radius, magnet_notes, login_name, cond_curr,
            meas_loc, run_number, sub_device, current_1, current_2, current_3, up_dn_1, up_dn_2, up_dn_3,
            analysis_number, integral_xfer_function, orig_offset_x, orig_offset_y, b_ref_int, roll_angle,
            meas_notes, author, a1, a2, a3, b1, b2, b3, a4_21, b4_21, data_issues, data_usage)

    def deleteRotCoilData(self, inventory_name, rot_coil_data_id=None):
        '''
        Delete one or more rot coil data

        :param inventory_name: name of the device in the inventory
        :type inventory_name: str

        :param rot_coil_data_id: id of data in the table
        :type rot_coil_data_id: int

        :return: True if everything was ok

        :raises: ValueError, MySQLError
        '''

        # Get existing inventory
        inv = self.retrieveInventory(inventory_name)

        if len(inv) == 0:
            raise ValueError("Inventory (%s) doesn't exist in the database!" % inventory_name)

        retrieveInventoryKeys = inv.keys()
        inventory_id = inv[retrieveInventoryKeys[0]]['id']

        return self.physics.deleteRotCoilData(inventory_id, rot_coil_data_id)

    def retrieveHallProbeData(self, inventory_name):
        '''
        Return hall probe data

        :param inventory_name: name of the device in the inventory
        :type inventory_name: str

        :return: dictionary with a structure like:

            .. code-block:: python

                {
                    'id': {
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
                        inventory_name
                    },
                    ...
                }

        :Raises: ValueError, MySQLError
        '''

        # Check inventory
        inventory = self.retrieveInventory(inventory_name)

        if len(inventory) == 0:
            raise ValueError("Inventory (%s) does not exist in the database." % (inventory_name))

        inventory_id = inventory.keys()[0]

        resdict = {}
        res = self.physics.retrieveHallProbeData(inventory_id)

        # Construct return dict
        for r in res:
            resdict[r[0]] = {
                'id': r[0],
                'inventory_id': r[1],
                'alias': r[2],
                'meas_date': r[3].strftime("%Y-%m-%d %H:%M:%S"),
                'measured_at_location': r[4],
                'sub_device': r[5],
                'run_identifier': r[6],
                'login_name': r[7],
                'conditioning_current': r[8],
                'current_1': r[9],
                'current_2': r[10],
                'current_3': r[11],
                'up_dn1': r[12],
                'up_dn2': r[13],
                'up_dn3': r[14],
                'mag_volt_1': r[15],
                'mag_volt_2': r[16],
                'mag_volt_3': r[17],
                'x': r[18],
                'y': r[19],
                'z': r[20],
                'bx_t': r[21],
                'by_t': r[22],
                'bz_t': r[23],
                'meas_notes': r[24],
                'data_issues': r[25],
                'data_usage': r[26],
                'inventory_name': r[27]
            }

        return resdict

    def saveHallProbeData(
            self, inventory_name, sub_device, alias=None, measured_at_location=None,
            run_identifier=None, login_name=None, conditioning_current=None, current_1=None, current_2=None,
            current_3=None, up_dn1=None, up_dn2=None, up_dn3=None, mag_volt_1=None, mag_volt_2=None, mag_volt_3=None,
            x=None, y=None, z=None, bx_t=None, by_t=None, bz_t=None, meas_notes=None, data_issues=None, data_usage=None
            ):
        '''
        Save hall probe data

        :param inventory_name: name of the device in the inventory
        :type inventory_name: str

        :param alias: alias name
        :type alias: str

        :param sub_device: sub device name
        :type sub_device: str

        :param measured_at_location: where was it measured
        :type measured_at_location: str

        :param run_identifier:  in which run this data was produced
        :type run_identifier: str

        :param login_name: who generated this data set
        :type login_name: str

        :param conditioning_current: condition current
        :type conditioning_current: double

        :param current_1: 1 st measurement current
        :type current_1: double

        :param current_2: 2 nd measurement current
        :type current_2: double

        :param current_3: 3 rd measurement current
        :type current_3: double

        :param up_dn1: direction of 1 st current
        :type up_dn1: str

        :param up_dn2: direction of 2 nd current
        :type up_dn2: str

        :param up_dn3: direction of 3 rd current
        :type up_dn3: str

        :param mag_volt_1: voltage at 1 st current given to magnet
        :type mag_volt_1: double

        :param mag_volt_2: voltage at 2 nd current given to magnet
        :type mag_volt_2: double

        :param mag_volt_3: voltage at 3 rd current given to magnet
        :type mag_volt_3: double

        :param x: x position
        :type x: double

        :param y: y position
        :type y: double

        :param z: z position
        :type z: double

        :param bx_t: magnetic field along x axis
        :type bx_t: double

        :param by_t: magnetic field along y axis
        :type by_t: double

        :param bz_t: magnetic field along z axis
        :type bz_t: double

        :param meas_notes: comments for each measuring data point
        :type meas_notes: str

        :param data_issues: reserved
        :type data_issues: str

        :param data_usage: reserved
        :type data_usage: int

        :return: a map with structure like:

            .. code-block:: python

                {'id': hall probe data id}

        :Raises: ValueError, MySQLError
        '''

        # Check inventory
        inventory = self.retrieveInventory(inventory_name)

        if len(inventory) == 0:
            raise ValueError("Inventory (%s) does not exist in the database." % (inventory_name))

        inventory_id = inventory.keys()[0]

        # Check parameter
        _checkParameter('sub device', sub_device)

        result = self.physics.saveHallProbeData(
            inventory_id, sub_device, alias, measured_at_location,
            run_identifier, login_name, conditioning_current, current_1, current_2,
            current_3, up_dn1, up_dn2, up_dn3, mag_volt_1, mag_volt_2, mag_volt_3,
            x, y, z, bx_t, by_t, bz_t, meas_notes, data_issues, data_usage)

        return {'id': result}

    def updateHallProbeData(
            self, hall_probe_id, inventory_name=None, sub_device=None, alias=None, measured_at_location=None,
            run_identifier=None, login_name=None, conditioning_current=None, current_1=None, current_2=None,
            current_3=None, up_dn1=None, up_dn2=None, up_dn3=None, mag_volt_1=None, mag_volt_2=None, mag_volt_3=None,
            x=None, y=None, z=None, bx_t=None, by_t=None, bz_t=None, meas_notes=None, data_issues=None, data_usage=None):
        '''
        Update hall probe data

        :param hall_probe_id: id hall probe
        :type hall_probe_id: int

        :param inventory_name: name of the device in the inventory
        :type inventory_name: str

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

        :raises: ValueError, MySQLError
        '''

        # Check id
        _checkParameter('id', hall_probe_id, 'prim')

        inventory_id = None

        if inventory_name:
            # Check inventory
            retrieveInventory = self.retrieveInventory(inventory_name)

            if len(retrieveInventory) == 0:
                raise ValueError("Inventory (%s) doesn't exist in the database!" % oldInventoryName)

            retrieveInventoryKeys = retrieveInventory.keys()
            inventory_id = retrieveInventory[retrieveInventoryKeys[0]]['id']

        return self.physics.updateHallProbeData(
            hall_probe_id, inventory_id, sub_device, alias, measured_at_location,
            run_identifier, login_name, conditioning_current, current_1, current_2,
            current_3, up_dn1, up_dn2, up_dn3, mag_volt_1, mag_volt_2, mag_volt_3,
            x, y, z, bx_t, by_t, bz_t, meas_notes, data_issues, data_usage)

    def deleteHallProbeData(self, inventory_name, hall_probe_id=None):
        '''
        Delete one or more hall probe data

        :param inventory_name: name of the device in the inventory
        :type inventory_name: str

        :param hall_probe_id: id of data in the table
        :type hall_probe_id: int

        :return: True if everything was ok

        :raises: ValueError, MySQLError
        '''

        # Get existing inventory
        inv = self.retrieveInventory(inventory_name)

        if len(inv) == 0:
            raise ValueError("Inventory (%s) doesn't exist in the database!" % inventory_name)

        retrieveInventoryKeys = inv.keys()
        inventory_id = inv[retrieveInventoryKeys[0]]['id']

        return self.physics.deleteHallProbeData(inventory_id, hall_probe_id)