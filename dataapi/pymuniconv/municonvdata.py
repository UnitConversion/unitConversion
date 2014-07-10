'''
The municonvdata class is an interface to read/write data from/into IRMIS database.
It covers tables listed as below:
  -- install
  -- cmpnt_type_prop_type
  -- cmpnt_type_prop
  -- cmpnt_type
  -- inventory
  -- inventory_prop_tmplt
  -- inventory_prop
  -- vendor
  and 2 index table:
  -- inventory__install
  -- cmpnttype__vendor

It does not touch 2 raw tables that are for rotating coil and hall probe raw data respectively.
This function is subject to be added upon requirement.

Created on Oct 2, 2012

@author: shengb
'''

import logging
import MySQLdb

from utils import (_wildcardformat, _assemblesql)
from pyphysics.physics import physics
from _mysql_exceptions import MySQLError


class municonvdata(object):
    '''Save magnet unit conversion data class'''
    def __init__(self, connection=None):
        self.logger = logging.getLogger('municonv')
        hdlr = logging.FileHandler('/var/tmp/municonv.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.WARNING)

        if connection is not None:
            self.conn = connection

        self.cachedconversioninfo = {}
        self.physics = physics(connection, None)

    def connectdb(self, host=None, user=None, pwd=None, db=None, port=3306):
        if host is None or user is None or pwd is None or db is None:
            raise ValueError("Cannot initialize municonv database since information is not sufficient.")

        if host.startswith("/"):
            self.conn = MySQLdb.connect(unix_socket=host, user=user, passwd=pwd, db=db)
        else:
            self.conn = MySQLdb.connect(host=host, user=user, passwd=pwd, db=db, port=port)
        return self.conn

    def disconnectdb(self):
        if self.conn:
            self.conn.close()
        return True

    def commit(self):
        try:
            self.conn.commit()
        except MySQLdb.Error:
            self.conn.rollback()
            return False

        return True

    def retrievecmpnttype(self, name, desc=None, vendor=None):
        '''
        Retrieve id of a given component type name, description [optional], and vendor [optional].

        Wildcards are support in component type name search, which uses "*" for multiple match,
        and "?" for single character match.

        Return: tuple of component ((id, name, description, vendor, vendor id), ...) if vendor is provided,
                otherwise ((id, name, description), ...).
        '''

        # Name should not be none
        if name is None:
            return ()

        resWithVendor = ()

        try:
            res = self.physics.retrieveComponentType(name, desc)

            # Append vendor if parameter exists
            if vendor:
                vendorObj = self.physics.retrieveVendor(vendor)

                # If there is no vendor there is also no cmpnttype_vendor map
                if len(vendorObj) == 0:
                    return ()

                # Ge through results and append vendor parts
                for r in res:
                    vendorMap = self.physics.retrieveComponentTypeVendor(r[0], vendorObj[0][0])

                    if len(vendorMap) != 0:
                        r += (vendorMap[0][4], vendorMap[0][3])
                        resWithVendor += (r,)

                return resWithVendor

            return res

        except MySQLError as e:
            raise Exception(e)

    def savecmpnttype(self, name, desc, vendor=None):
        '''
        Save a new component type, and link this component with the given vendor.
        Link this component type to given vendor, or throw an exception if component exist already
        and is linked to given vendor.

        Return component type id, or a tuple of (component type id, vendor id),
        or raise an exception if it exists already.
        '''
        if not isinstance(name, (str, unicode)) or not isinstance(desc, (str, unicode)):
            raise Exception('Both component type name and description have to be string.')

        # check whether component type exists or not
        res = self.retrievecmpnttype(name, desc=desc, vendor=vendor)
        if len(res):
            if vendor:
                raise ValueError('Component (%s) with description (%s) for vendor (%s) exists already.' % (name, desc, vendor))
            else:
                raise ValueError('Component (%s) with description (%s) exists already.' % (name, desc))

        res = self.retrievecmpnttype(name, desc)

        try:
            if len(res) == 0:
                typeid = self.physics.saveComponentType(name, desc)

            else:
                typeid = res[0][0]

            cur = self.conn.cursor()

            if vendor:
                # obtain vendor
                vendorObj = self.physics.retrieveVendor(vendor)

                if len(vendorObj) == 0:
                    vndrid = self.physics.saveVendor(vendor)

                else:
                    vndrid = vendorObj[0][0]

                self.physics.saveComponentTypeVendor(typeid, vndrid)

                return (typeid, vndrid)

            else:
                return typeid

        except MySQLError as e:
            raise Exception(e)

    def retrievecmpnttypeproptype(self, name, desc=None):
        '''Retrieve id of a given component type property type name, and description [optional]

        Wildcards are support in property type name search, which uses "*" for multiple match,
        and "?" for single character match.

        Return: tuple of property type of component type ((id, name, description), ...).
        '''

        try:
            res = self.physics.retrieveComponentTypePropertyType(name, desc)
            return res

        except MySQLError as e:
            raise Exception(e)

        except ValueError as e:
            self.logger.info(e)
            raise Exception(e)

    def savecmpnttypeproptype(self, name, desc):
        '''Save a new component type property type with description.
        Any property belonging to component type and shared by all inventory instances is save in the component type property table.
        The type name of that property is defined in the component type property type table.

        Return: property type id, or raise an exception if it exists already.
        '''
        try:
            res = self.physics.saveComponentTypePropertyType(name, desc)
            return res

        except MySQLError as e:
            raise Exception(e)

        except ValueError as e:
            self.logger.info(e)
            raise Exception(e)

    def retrievecmpnttypeprop(self, ctypeid, cptypeid, value=None):
        '''
        Retrieve value and id of given component type id and component type property type id.
        Any property belonging to component type and shared by all inventory instances is save in the component type property table.
        The type name of that property is defined in the component type property type table.

        :Return: tuple of component type property value and id ((component property id, property value)).
        '''
        try:
            res = self.physics.retrieveComponentTypeProperty(ctypeid, cptypeid, value)
            return res

        except MySQLError as e:
            raise Exception(e)

        except ValueError as e:
            self.logger.info(e)
            raise Exception(e)

    def savecmpnttypeprop(self, value, ctypeid, cptypeid):
        '''
        Save value to component type property table with given component type id and component type property type id.
        Any property belonging to component type and shared by all inventory instances is save in the component type property table.
        The type name of that property is defined in the component type property type table.

        :Return: component type property id.
        '''
        if not isinstance(value, (str, unicode)):
            raise Exception("Component type property value has to be a string ")

        res = self.retrievecmpnttypeprop(ctypeid, cptypeid)
        if len(res) > 0:
            raise ValueError('A value has been given')

        try:
            res = self.physics.saveComponentTypeProperty(ctypeid, cptypeid, value)
            return res

        except MySQLError as e:
            raise Exception(e)

    def updatecmpnttypeprop(self, value, ctypeid, cptypeid):
        '''Update value of component type property value column in component type property table
        with given component type id and component type property type id.

        return True if success, otherwise, throw out an exception.
        '''
        if not isinstance(value, (str, unicode)):
            raise Exception("Component type property value has to be a string ")

        res = self.retrievecmpnttypeprop(ctypeid, cptypeid)
        if len(res) == 0:
            raise Exception('No entity found.')

        try:
            res = self.physics.updateComponentTypeProperty(ctypeid, cptypeid, value)
            return res

        except MySQLError as e:
            raise Exception(e)

    def retrieveinventoryproptmplt(self, name, ctypeid=None, desc=None):
        '''Retrieve id of a given inventory property template name, with optional component type id or description

        Wildcards are support in name search, which uses "*" for multiple match,
        and "?" for single character match.

        Return all inventory property template ids.
        '''
        if not isinstance(name, (str, unicode)):
            raise Exception('Inventory property template name has to be a string.')

        try:
            return self.physics.retrieveInventoryPropertyTemplate(name, ctypeid, desc)

        except MySQLError as e:
            raise Exception(e)

    def saveinventoryproptmplt(self, name, ctypeid, desc=None, default=None, units=None):
        '''Save an inventory property template instance with given name, component type id, and some optional field.

        return id if success, otherwise throw out an exception.
        '''
        if not isinstance(name, (str, unicode)):
            raise Exception('Inventory property template name has to be a string.')

        res = self.retrieveinventoryproptmplt(name, ctypeid, desc=desc)
        if len(res) > 0:
            raise Exception('Name (%s) with given component type id (%s) for inventory property template exists already'
                            % (name, ctypeid))

        try:
            return self.physics.saveInventoryPropertyTemplate(name, ctypeid, desc, default, units)

        except MySQLError as e:
            raise Exception(e)

    def retrieveinventoryprop(self, inventoryid, iproptmpltid, value=None):
        '''
        Retrieve id and value from inventory property table with given inventory id and inventory property template id.
        An inventory property has to belong to a property template, which belongs to component type.

        Use component type property table to retrieve a property, which is common for a component type.

        Return: tuple of inventory property id, inventory property value, property template id and inventory_id,
                ((property id, inventory property value, property template id, inventory_id), ...).
        '''

        # So it works like previous code did
        if iproptmpltid is None:
            return ()

        try:
            return self.physics.retrieveInventoryProperty(inventoryid, iproptmpltid, value)

        except MySQLError as e:
            raise Exception(e)

    def saveinventoryprop(self, value, inventoryid, iproptmpltid):
        '''
        Save value to inventory property table with given inventory id and inventory property template id.
        The inventory property could be for a particular device, and in this case, inventory id has to be give.
        Otherwise, it is a common property for given component type.

        return inventory property id, or throw an exception if existing already.
        '''
        if not isinstance(value, (str, unicode)):
            # could be a json dumped text.
            raise Exception("Inventory value has to be a string ")

        res = self.retrieveinventoryprop(inventoryid, iproptmpltid)
        if len(res) > 0:
            raise Exception('A value exists already.')

        try:
            return self.physics.saveInventoryProperty(inventoryid, iproptmpltid, value)

        except MySQLError as e:
            raise Exception(e)

    def updateinventoryprop(self, value, inventoryid, iproptmpltid):
        '''
        Update value to inventory property table with given inventory id and inventory property template id.

        return True if success, otherwise, throw out an exception.
        '''
        if not isinstance(value, (str, unicode)):
            raise Exception("Inventory value has to be a string ")

        res = self.retrieveinventoryprop(inventoryid, iproptmpltid)

        if len(res) == 0:
            raise Exception('No entity found in inventory property table.')

        try:
            return self.physics.updateInventoryProperty(inventoryid, iproptmpltid, value)

        except MySQLError as e:
            raise Exception(e)

    def retrieveinstall(self, name, ctypename=None, location=None):
        '''
        Retrieve installed device name with table id upon giving device name.

        :return: tuple with format as ((id, field name, location, component type name, description, vendor), ...)
        '''
        result_block = ()

        try:
            res = self.physics.retrieveInstall(name, ctypename, location)

            for r in res:
                install_id = r[0]
                install_name = r[1]
                install_location = r[2]
                component_type_name = r[3]
                component_type_description = r[4]
                component_type_id = r[5]
                vendor = None

                vendor_res = self.physics.retrieveComponentTypeVendor(component_type_id, None)

                if len(vendor_res) > 0:
                    vendor = vendor_res[0][4]

                result_line = (install_id, install_name, install_location, component_type_name, component_type_description, vendor)
                result_block += (result_line,)

            return result_block

        except MySQLError as e:
            raise Exception(e)

    def saveinstall(self, name, ctypeid, location, inventoryid=None):
        '''
        Save installed device into install table.

        Return id if success, otherwise throw out an exception.
        '''
        if not isinstance(name, (str, unicode)) or not isinstance(location, (str, unicode)):
            raise Exception('Both device name and location info have to be string.')

        sql = 'select cmpnt_type_name from cmpnt_type where cmpnt_type_id = %s'
        cur = self.conn.cursor()
        cur.execute(sql, (ctypeid,))
        ctypename = cur.fetchone()

        if ctypename is not None:
            ctypename = ctypename[0]

        else:
            raise ValueError("component type (id=%s) does not exist." % (ctypeid))

        res = self.retrieveinstall(name, ctypename=ctypename, location=location)

        if len(res) > 0:
            raise Exception('Device (%s) exists already' % (name))

        try:
            # Save install
            instid = self.physics.saveInstall(name, location, ctypeid, None)

            # create relationship between inventory and install
            if inventoryid:
                res = self.physics.retrieveInventoryToInstall(None, instid, inventoryid)

                # create a new entry if it does not exist
                if len(res) == 0:
                    self.physics.saveInventoryToInstall(instid, inventoryid)

            return instid

        except MySQLError as e:
            raise Exception(e)

    def retrieveinventory(self, serial, ctypename=None, vendor=None):
        '''
        Retrieve an inventory information according given serial number, vendor name, and component type name.

        Wildcards are support in all parameters (device name, serial number, component type name, and vendor),
        which uses "*" for multiple match, and "?" for single character match.

        return: tuple of inventory id, serial number like:
            with vendor name, component type name, and component type description if both component type and vendor are given
                like ((inventory id, serial no, component type name, type description, vendor), ...)
        '''
        if not isinstance(serial, (str, unicode)):
            raise Exception('Serial no has to be string.')

        serial = _wildcardformat(serial)

        try:
            res = self.physics.retrieveInventory(None, serial, ctypename, vendor)
            result_block = ()

            for r in res:
                install_id = None
                inventory_id = r[0]
                install_name = None
                location = None
                serial_number = r[3]
                component_type_name = r[4]
                component_type_description = r[5]
                vendor_name = r[6]

                install = self.physics.retrieveInventoryToInstall(None, None, inventory_id)

                if len(install) > 0:
                    installObj = install[0]

                    install_id = installObj[1]
                    install_name = installObj[3]
                    location = installObj[5]

                result_line = (install_id, inventory_id, install_name, location, serial_number, component_type_name, component_type_description, vendor_name)
                result_block += (result_line,)

            return result_block

        except MySQLError as e:
            raise Exception(e)

    def saveinventory(self, serial, ctype, vendor):
        '''
        Save inventory with given device name, vendor, and component type.
        An assumption here is that it a component type from a given vendor is unique.
        Therefore, it forces a hardware from one vendor, which belongs to certain component type is unique.

        The given component type for given vendor has to be linked in advance, and the given vendor from given vendor has to be unique.
        Otherwise, an exception will be rise.

        return: inventory id if success, otherwise raise an exception.
        '''
        if not isinstance(serial, (str, unicode)):
            raise Exception('Serial no has to be a string.')

        # check whether entry exists.
        res = self.retrieveinventory(serial, ctype, vendor)
        if len(res) != 0:
            # entry exists already.
            raise Exception("Device (%s) with component type (%s) from vendor (%s) exists already." % (serial, ctype, vendor))

        res = self.retrievecmpnttype(ctype, vendor=vendor)

        # if len(res) == 0:
        if len(res) != 1:
            # Throw an exception since either the entry is not unique, or not linked in advance
            raise Exception("Component type (%s) from vendor (%s) does not exist, or not unique." % (ctype, vendor))

        ctypeid = res[0][0]
        vendorid = res[0][4]

        try:
            return self.physics.saveInventory(None, ctypeid, None, serial, vendorid)

        except MySQLError as e:
            raise Exception(e)

    def retrieveinstalledinventory(self, name, serial, ctypename=None, vendor=None, location=None):
        '''
        Retrieve devices from inventory what have been installed according given device name, serial number, component type and vendor.

        Wildcards are support in all parameters (device name, serial number, component type name, and vendor),
        which uses "*" for multiple match, and "?" for single character match.

        Return: tuple with format like ((install id, inventory id, device name, location, serial number, component type name, description, vendor name), ...).
        '''

        # Check name
        if name is None:
            raise Exception('Name should not be None!')

        # Check serial number
        if serial is None:
            raise Exception('Serial number should not be None!')

        try:
            result_block = ()

            res = self.physics.retrieveInstall(name, ctypename, location)

            # Go through all results
            for r in res:
                install_id = r[0]
                install_name = r[1]
                install_description = r[2]
                component_type_name = r[3]
                component_type_description = r[4]

                # Get map, there should be only one inventory mapped to one install and vice versa
                ii_map = self.physics.retrieveInventoryToInstall(None, install_id, None)

                if len(ii_map) > 0:
                    inventory_id = ii_map[0][2]

                    # Get inventory by its id
                    inventory_res = self.physics.retrieveInventory(None, None, None, None, inventory_id)

                    if len(inventory_res) > 0:
                        vendor = inventory_res[0][6]
                        serial_no = inventory_res[0][3]

                        result_line = (install_id, inventory_id, install_name, install_description, serial_no, component_type_name, component_type_description, vendor)
                        result_block += (result_line,)

            return result_block

        except MySQLError as e:
            raise Exception(e)

    def inventory2install(self, installid, inventoryid):
        '''
        link an inventory as installed device
        '''
        sqlinst = '''select 1 from install where install_id = %s'''
        sqlinv = '''select 1 from inventory where inventory_id = %s'''

        cur = self.conn.cursor()

        if not cur.execute(sqlinst, (installid,)) or not cur.execute(sqlinv, (inventoryid,)):
            raise ValueError('Given install id (%s) or inventory id (%s) does not exist. Can not link them together.'
                             % (installid, inventoryid))
        sql = '''select inventory__install_id, install_id, inventory_id from inventory__install where install_id = %s or inventory_id = %s'''
        cur.execute(sql, (installid, inventoryid))
        res = cur.fetchall()

        if len(res):
            ii_id = res
            if len(res) > 1:
                # either inventory id or install can be in inventory__install table once.
                # One device in inventory can only be installed in one place.
                self.logger.info("More than one entry found for installed (id: %s) device in inventory (%s)" % (installid, inventoryid))
                raise ValueError("More than one entry found for installed (id: %s) device in inventory (%s)" % (installid, inventoryid))

            else:

                if res[0][1] == installid or res[0][2] == inventoryid:
                    self.logger.info("Install or inventory entity already mapped")
                    raise ValueError("Install or inventory entity already mapped")

            ii_id = res[0][0]

        else:

            try:
                ii_id = self.physics.saveInventoryToInstall(installid, inventoryid)

            except MySQLError as e:
                raise Exception(e)

        return ii_id

    def updateinventory2install(self, installid, inventoryid):
        '''
        link an inventory as installed device
        '''
        ii_id = self.inventory2install(installid, inventoryid)

        sql = '''
        UPDATE inventory__install
        SET
        inventory_id = %s
        WHERE
        install_id = %s
        '''
        cur = self.conn.cursor()
        try:
            cur.execute(sql, (inventoryid, installid))
            self.commit()
        except MySQLdb.Error as e:
            self.conn.rollback()
            self.logger.info('Error when linking install (id: %s) with inventory (id: %s):\n%s (%s)'
                             % (installid, inventoryid, e.args[1], e.args[0]))
            raise Exception('Error when linking install (id: %s) with inventory (id: %s):\n%s (%s)'
                            % (installid, inventoryid, e.args[1], e.args[0]))

        return ii_id

    def retrievesystem(self, location=None):
        '''
        retrieve location information from install table
        '''
        sql = '''
        select distinct location from install where
        '''
        val = None
        if location is None:
            sql += " location like %s "
            val = "%"
        else:
            val = []
            val, sql = _assemblesql(sql, location, " location ", val)
        try:
            cur = self.conn.cursor()
            if isinstance(val, (list, tuple)):
                cur.execute(sql, val)
            else:
                cur.execute(sql, (val,))
            rawres = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching system from install table:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when fetching system from install table:\n%s (%d)' % (e.args[1], e.args[0]))

        system = []
        for r in rawres:
            system.append(r[0])
        return system

    def retrievemuniconv4inventory(self, invid, invproptmpltname, invproptmpltdesc):
        '''
        Get magnet unit conversion information for given inventory id with inventory property template name and its description.
        '''
        sql = '''
        select install.field_name, install.location, inventory.serial_no, cmpnt_type.cmpnt_type_name, inventory_prop.inventory_prop_value
        from inventory
        left join inventory__install on inventory__install.inventory_id = inventory.inventory_id
        left join install on inventory__install.install_id = install.install_id
        left join inventory_prop on inventory_prop.inventory_id = inventory.inventory_id
        left join inventory_prop_tmplt on inventory_prop_tmplt.inventory_prop_tmplt_id = inventory_prop.inventory_prop_tmplt_id
        left join cmpnt_type on inventory.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        where
        inventory.inventory_id = %s
        and inventory_prop_tmplt.inventory_prop_tmplt_name like %s
        and inventory_prop_tmplt.inventory_prop_tmplt_desc like %s
        '''
        invproptmpltname = _wildcardformat(invproptmpltname)
        invproptmpltdesc = _wildcardformat(invproptmpltdesc)

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (invid, invproptmpltname, invproptmpltdesc))
            res = cur.fetchone()

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching magnet unit conversion information for inventory:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when fetching magnet unit conversion information for inventory:\n%s (%d)' % (e.args[1], e.args[0]))

        return res

    def retrievemuniconvbycmpnttype4inventory(self, invid, ctypeproptypetmpltname, ctypeproptmpltdesc):
        '''
        Get magnet unit conversion information for given inventory id with component type property template name and its description.
        This method retrieve a common information for given magnet type.

        Use this method only when the measurement data for each individual magnet is not available.
        '''
        sql = '''
        select install.field_name, install.location, inventory.serial_no, cmpnt_type.cmpnt_type_name, cmpnt_type_prop.cmpnt_type_prop_value
        from inventory
        left join inventory__install on inventory__install.inventory_id = inventory.inventory_id
        left join install on inventory__install.install_id = install.install_id
        left join cmpnt_type on inventory.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        left join cmpnt_type_prop on cmpnt_type_prop.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        left join cmpnt_type_prop_type on cmpnt_type_prop.cmpnt_type_prop_type_id = cmpnt_type_prop_type.cmpnt_type_prop_type_id
        where
        inventory.inventory_id = %s
        and cmpnt_type_prop_type.cmpnt_type_prop_type_name like %s
        and cmpnt_type_prop_type.cmpnt_type_prop_type_desc like %s
        '''
        ctypeproptypetmpltname = _wildcardformat(ctypeproptypetmpltname)
        ctypeproptmpltdesc = _wildcardformat(ctypeproptmpltdesc)

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (invid, ctypeproptypetmpltname, ctypeproptmpltdesc))
            res = cur.fetchone()

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching magnet unit conversion information for inventory with given component type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when fetching magnet unit conversion information for inventory with given component type:\n%s (%d)' % (e.args[1], e.args[0]))

        return res

    def retrievemuniconv4install(self, name, ctypeproptypetmpltname, ctypeproptmpltdesc):
        '''
        Get magnet unit conversion information for given field name with component type property template name and its description.
        This method retrieve a common information for given magnet type.
        '''
        sql = '''
        select install.field_name, install.location, inventory.serial_no, cmpnt_type.cmpnt_type_name, cmpnt_type_prop.cmpnt_type_prop_value
        from install
        left join inventory__install on inventory__install.install_id = install.install_id
        left join inventory on inventory__install.inventory_id = inventory.inventory_id
        left join cmpnt_type on install.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        left join cmpnt_type_prop on cmpnt_type_prop.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        left join cmpnt_type_prop_type on cmpnt_type_prop.cmpnt_type_prop_type_id = cmpnt_type_prop_type.cmpnt_type_prop_type_id
        where
        install.field_name like %s
        and cmpnt_type_prop_type.cmpnt_type_prop_type_name like %s
        and cmpnt_type_prop_type.cmpnt_type_prop_type_desc like %s
        '''
        name = _wildcardformat(name)
        ctypeproptypetmpltname = _wildcardformat(ctypeproptypetmpltname)
        ctypeproptmpltdesc = _wildcardformat(ctypeproptmpltdesc)

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (name, ctypeproptypetmpltname, ctypeproptmpltdesc))
            res = cur.fetchone()

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching magnet unit conversion information for install:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when fetching magnet unit conversion information for install:\n%s (%d)' % (e.args[1], e.args[0]))

        return res

    def retrieveinventoryid(self, name):
        ''''''
        sql = '''
        select field_name, ii.inventory_id
        from install
        left join inventory__install ii on ii.install_id = install.install_id
        where
        '''
        vals = []
        vals, sql = _assemblesql(sql, name, " field_name ", vals)

        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching device name and inventory information:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when fetching device name and inventory information:\n%s (%d)' % (e.args[1], e.args[0]))

        return res
