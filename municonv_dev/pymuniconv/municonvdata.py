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

class municonvdata(object):
    '''Save magnet unit conversion data class'''
    def __init__(self, connection=None):
        self.logger = logging.getLogger('municonv')
        hdlr = logging.FileHandler('/var/tmp/municonv.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.WARNING)
        if connection != None:
            self.conn = connection
    
    def connectdb(self, host=None, user=None, pwd=None, db=None):
        if host == None or user == None or pwd == None or db == None:
            raise ValueError("Cannot initialize municonv database since information is not sufficient.")
        
        self.conn = MySQLdb.connect(host=host, user=user, passwd=pwd, db=db)
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
    
    def __wildcardformat(self, regxval):
        """
        The LIKE condition allows user to use wildcards in the where clause of an SQL statement.
        This allows user to perform pattern matching. The LIKE condition can be used in any valid
        SQL statement - select, insert, update, or delete.
        The patterns that a user can choose from are:
            % allows you to match any string of any length (including zero length)
            _ allows you to match on a single character
    
        The client uses "*" for multiple match, and "?" for single character match.
        This function replaces "*" with "%", and "?" with "_".
    
        For example:
        >>> __wildcardformat("a*b?c*d*e?f")
        u'a%b_c%d%e_f'
        """
        return regxval.replace("*","%").replace("?","_")
    
    def retrievecmpnttype(self, name, desc=None, vendor=None):
        '''Retrieve id of a given component type name, description [optional], and vendor [optional].
        
        Wildcards are support in component type name search, which uses "*" for multiple match,
        and "?" for single character match.
        
        Return: tuple of component ((id, name, description, vendor, vendor id), ...) if vendor is provide,
                otherwise ((id, name, description), ...).
        '''
        
        if vendor:
            # retrieve also vendor information 
            sql = '''
            select 
            ctype.cmpnt_type_id, ctype.cmpnt_type_name, ctype.description, vendor.vendor_name, vendor.vendor_id
            from cmpnt_type ctype
            left join cmpnttype__vendor ctvendor on ctvendor.cmpnt_type_id = ctype.cmpnt_type_id
            left join vendor on ctvendor.vendor_id = vendor.vendor_id
            where
            ctype.cmpnt_type_name like %s
            '''
        else:
            # ignore vendor information since vendor is not provided.
            sql = '''
            select 
            ctype.cmpnt_type_id, ctype.cmpnt_type_name, ctype.description
            from cmpnt_type ctype
            where
            ctype.cmpnt_type_name like %s
            '''
        
        name = self.__wildcardformat(name)
        try:
            cur = self.conn.cursor()
            if desc and vendor:
                desc = self.__wildcardformat(desc)
                vendor = self.__wildcardformat(vendor)
                sql += " and ctype.description like %s and vendor.vendor_name like %s "
                cur.execute(sql, (name, desc, vendor))
            elif desc:
                desc = self.__wildcardformat(desc)
                sql += " and ctype.description like %s "
                cur.execute(sql, (name, desc))
            elif vendor:
                vendor = self.__wildcardformat(vendor)
                sql += " and vendor.vendor_name like %s "
                cur.execute(sql, (name, vendor))
            else:
                cur.execute(sql, (name,))
            res = cur.fetchall()
        except MySQLdb.Error, e:
            self.logger.info('Error when fetching component types:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when fetching component types:\n%s (%d)' % (e.args[1], e.args[0]))
        return res
        
    def savecmpnttype(self, name, desc, vendor=None):
        '''Save a new component type, and link this component with the given vendor.
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
                raise ValueError('Component (%s) with description (%s) for vendor (%s) exists already.' %(name, desc, vendor))
            else:
                raise ValueError('Component (%s) with description (%s) exists already.' %(name, desc))
        
        cur = self.conn.cursor()
        # obtain component type id
        sql = '''select cmpnt_type_id from cmpnt_type where cmpnt_type_name = %s and description = %s'''
        try:
            cur.execute(sql, (name, desc))
            ctid = cur.fetchone()
            if not ctid:
                # component type does not exist yet. create a new entry.
                sql = '''insert into cmpnt_type (cmpnt_type_name, description) values (%s, %s)'''
                cur.execute(sql, (name, desc))

                self.commit()
                # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
                # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
                # it is per connection.
                ctid = cur.lastrowid
            else:
                ctid = ctid[0]
        except MySQLdb.Error as e:
            self.logger.info('Error when trying to obtain component type id:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when trying to obtain component type id:\n%s (%d)' % (e.args[1], e.args[0]))
            
        if vendor:
            # obtain vendor id
            sql = '''select vendor_id from vendor where vendor_name = %s'''
            try:
                cur.execute(sql, (vendor,))
                vndrid = cur.fetchone()
                if not vndrid:
                    sql = '''insert into vendor (vendor_name) values (%s)'''
                    cur.execute(sql, (vendor,))
                    self.commit()
                    # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
                    # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
                    # it is per connection.
                    vndrid = cur.lastrowid
                else:
                    vndrid = vndrid[0]

            except MySQLdb.Error, e:
                self.logger.info('Error when trying to obtain vendor id:\n%s (%d)' % (e.args[1], e.args[0]))
                raise Exception('Error when trying to obtain vendor id:\n%s (%d)' % (e.args[1], e.args[0]))
            
            sql = '''select cmpnttype__vendor_id from cmpnttype__vendor where cmpnt_type_id = %s and vendor_id = %s'''
            try:
                cur.execute(sql, (ctid, vndrid))
                res = cur.fetchall()
                if len(res):
                    self.logger.info('component type (%s) has been linked to vendor(%s):\n%s (%d)' % (name, vendor, e.args[1], e.args[0]))
                    raise Exception('component type (%s) has been linked to vendor(%s):\n%s (%d)' % (name, vendor, e.args[1], e.args[0]))
                else:
                    sql = '''insert into cmpnttype__vendor (cmpnt_type_id, vendor_id) values (%s, %s)'''
                    cur.execute(sql, (ctid, vndrid))
                    self.commit()
            except MySQLdb.Error as e:
                self.logger.info('Error when linking component type (%s) to vendor(%s):\n%s (%d)' % (name, vendor, e.args[1], e.args[0]))
                raise Exception('Error when linking component type (%s) to vendor(%s):\n%s (%d)' % (name, vendor, e.args[1], e.args[0]))

            return (ctid, vndrid)                
        else:
            return ctid
        
    def retrievecmpnttypeproptype(self, name, desc=None):
        '''Retrieve id of a given component type property type name, and description [optional]
        
        Wildcards are support in property type name search, which uses "*" for multiple match,
        and "?" for single character match.
        
        Return: tuple of property type of component type ((id, name, description), ...).
        '''
        if not isinstance(name, (str, unicode)):
            raise Exception('Component type property type name has to be a string.')
        
        sql = '''
        select 
        cmpnt_type_prop_type_id, cmpnt_type_prop_type_name, cmpnt_type_prop_type_desc
        from cmpnt_type_prop_type
        where
        cmpnt_type_prop_type_name like %s
        '''
        
        name = self.__wildcardformat(name)
        try:
            cur = self.conn.cursor()
            if desc:
                sql += " and cmpnt_type_prop_type_desc like %s "
                cur.execute(sql, (name, desc))
            else:
                cur.execute(sql, (name,))
            res = cur.fetchall()
        except MySQLdb.Error, e:
            self.logger.into('Error when fetching component type property types:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when fetching component type property types:\n%s (%d)' % (e.args[1], e.args[0]))
        
        return res

    def savecmpnttypeproptype(self, name, desc):
        '''Save a new component type property type with description.
        Any property belonging to component type and shared by all inventory instances is save in the component type property table.
        The type name of that property is defined in the component type property type table.
        
        Return: property type id, or raise an exception if it exists already.
        '''
        res = self.retrievecmpnttypeproptype(name, desc=desc)
        if len(res):
            raise ValueError('Component type property type (%s) with description (%s) exists already.' %(name, desc))

        sql = '''
        insert into cmpnt_type_prop_type
        (cmpnt_type_prop_type_name, cmpnt_type_prop_type_desc)
        values (%s, %s)
        '''

        try:
            cur = self.conn.cursor()
            cur.execute(sql, (name, desc))
            
            self.commit()
            # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
            # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
            # it is per connection.
            lastid = cur.lastrowid
        except MySQLdb.Error, e:
            self.logger.info('Error when saving component type property type:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when saving component type property type:\n%s (%d)' % (e.args[1], e.args[0]))
        
        return lastid

    def retrievecmpnttypeprop(self, ctypeid, cptypeid, value=None):
        '''Retrieve value and id of given component type id and component type property type id.
        Any property belonging to component type and shared by all inventory instances is save in the component type property table.
        The type name of that property is defined in the component type property type table.
        
        Return: tuple of component type property value and id ((component property id, property value)).
        '''
        sql = '''
        select cmpnt_type_prop_id, cmpnt_type_prop_value
        from cmpnt_type_prop
        where
        cmpnt_type_id = %s and cmpnt_type_prop_type_id = %s
        '''
        try:
            cur = self.conn.cursor()
            if value:
                value = self.__wildcardformat(value)
                if "%" in value or "_" in value:
                    sql += " and cmpnt_type_prop_value like %s "
                else:
                    sql += " and cmpnt_type_prop_value = %s "
                cur.execute(sql, (ctypeid, cptypeid, value))
            else:
                cur.execute(sql, (ctypeid, cptypeid))
            res = cur.fetchall()
        except MySQLdb.Error, e:
            self.logger.info("Error when fetching component type property value:\n%s (%d)" %(e.args[1], e.args[0]))
            raise Exception("Error when fetching component type property value:\n%s (%d)" %(e.args[1], e.args[0]))
        return res
    
    def savecmpnttypeprop(self, value, ctypeid, cptypeid):
        '''Save value to component type property table with given component type id and component type property type id.
        Any property belonging to component type and shared by all inventory instances is save in the component type property table.
        The type name of that property is defined in the component type property type table.
        
        return component type property id.
        '''
        if not isinstance (value, (str, unicode)):
            raise Exception("Component type property value has to be a string ")

        res = self.retrievecmpnttypeprop(ctypeid, cptypeid)
        if len(res) > 0:
            raise ValueError('A value has been given')
        
        sql = '''
        insert into cmpnt_type_prop
        (cmpnt_type_id, cmpnt_type_prop_type_id, cmpnt_type_prop_value)
        values(%s, %s, %s)
        '''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (ctypeid, cptypeid, value))
            self.commit()
            # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
            # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
            # it is per connection.
            lastid = cur.lastrowid
        except MySQLdb.Error, e:
            self.logger.info('Error when saving component type property value:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when saving component type property value:\n%s (%d)' % (e.args[1], e.args[0]))
        
        return lastid

    def updatecmpnttypeprop(self, value, ctypeid, cptypeid):
        '''Update value of component type property value column in component type property table
        with given component type id and component type property type id.
        
        return True if success, otherwise, throw out an exception.
        '''
        if not isinstance (value, (str, unicode)):
            raise Exception("Component type property value has to be a string ")

        res = self.retrievecmpnttypeprop(ctypeid, cptypeid)
        if len(res) == 0:
            raise Exception('No entity found.')
        sql = '''
        update cmpnt_type_prop
        SET
        cmpnt_type_prop_value = %s
        WHERE
        cmpnt_type_id = %s AND cmpnt_type_prop_type_id = %s
        '''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (value, ctypeid, cptypeid))
            self.commit()
        except MySQLdb.Error, e:
            self.logger.info('Error when saving component type property value:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when saving component type property value:\n%s (%d)' % (e.args[1], e.args[0]))
        
        return True
    
    def retrieveinventoryproptmplt(self, name, ctypeid=None, desc=None):
        '''Retrieve id of a given inventory property template name, with optional component type id or description
        
        Wildcards are support in name search, which uses "*" for multiple match,
        and "?" for single character match.
        
        Return all inventory property template ids.
        '''
        if not isinstance(name, (str, unicode)):
            raise Exception('Inventory property template name has to be a string.')
        
        sql = '''
        select 
        inventory_prop_tmplt_id, inventory_prop_tmplt_name, inventory_prop_tmplt_desc, inventory_prop_tmplt_default, inventory_prop_tmplt_units
        from inventory_prop_tmplt
        where
        inventory_prop_tmplt_name like %s
        '''
        
        name = self.__wildcardformat(name)
        value = [name]
        
        if ctypeid:
            sql += ' and cmpnt_type_id = %s '
            value.append(ctypeid)

        if desc:
            sql += ' and inventory_prop_tmplt_desc like %s '
            value.append(desc)

        try:
            cur = self.conn.cursor()
            cur.execute(sql, value)
            res = cur.fetchall()
        except MySQLdb.Error, e:
            self.logger.info('Error when fetching inventory property template:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when fetching inventory property template:\n%s (%d)' % (e.args[1], e.args[0]))
        
        return res

    def saveinventoryproptmplt(self, name, ctypeid, desc=None, default=None, units=None):
        '''Save an inventory property template instance with given name, component type id, and some optional field.
        
        return id if success, otherwise throw out an exception.
        '''
        if not isinstance(name, (str, unicode)):
            raise Exception('Inventory property template name has to be a string.')
        
        res = self.retrieveinventoryproptmplt(name, ctypeid, desc=desc)
        if len(res) > 0:
            raise Exception('Name (%s) with given component type id (%s) for inventory property template exists already' 
                            %(name, ctypeid))
        sql = '''
        insert into inventory_prop_tmplt
        (inventory_prop_tmplt_name, cmpnt_type_id 
        '''
        sqlext = ''
        sqlval = ' values (%s, %s'
        val = [name, ctypeid]
        if desc:
            sqlext += ', inventory_prop_tmplt_desc'
            sqlval += ', %s'
            val.append(desc)
        
        if default:
            sqlext += ', inventory_prop_tmplt_default'
            sqlval += ', %s'
            val.append(default)
        
        if units:
            sqlext += ', inventory_prop_tmplt_units'
            sqlval += ', %s'
            val.append(units)
        
        sql += sqlext + ')' + sqlval + ')'
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql, val)
            self.commit()
            # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
            # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
            # it is per connection.
            lastid = cur.lastrowid
        except MySQLdb.Error, e:
            self.logger.info('Error when saving inventory property template name:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when saving inventory property template name:\n%s (%d)' % (e.args[1], e.args[0]))
        
        return lastid
       
        
    def retrieveinventoryprop(self, inventoryid, iproptmpltid, value=None):
        '''Retrieve id and value from inventory property table with given inventory id and inventory property template id. 
        An inventory property has to belong to a property template, which belongs to component type.
        
        Use component type property table to retrieve a property, which is common for a component type.
        
        Return: tuple of inventory property id, inventory property value, property template id and inventory_id,
                ((property id, inventory property value, property template id, inventory_id), ...).
        '''
        sql = '''
        select 
        inventory_prop_id, inventory_prop_value, inventory_prop_tmplt_id, inventory_id
        from inventory_prop
        where
        inventory_id = %s and inventory_prop_tmplt_id = %s
        '''
        values = [inventoryid, iproptmpltid]
        
        if value:
            value = self.__wildcardformat(value)
            if "%" in value or "_" in value:
                sql += " value like %s "
            else:
                sql += " value = %s "
            values.append(value)

        try:
            cur = self.conn.cursor()
            cur.execute(sql, values)
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieve id and vale from inventory property table:\n%s (%s)' %(e.args[1], e.args[0]))
            raise Exception('Error when retrieve id and vale from inventory property table:\n%s (%s)' %(e.args[1], e.args[0]))
        
        return res

    def saveinventoryprop(self, value, inventoryid, iproptmpltid):
        '''Save value to inventory property table with given inventory id and inventory property template id.
        The inventory property could be for a particular device, and in this case, inventory id has to be give.
        Otherwise, it is a common property for given component type. 
        
        return inventory property id, or throw an exception if existing already.
        '''
        if not isinstance (value, (str, unicode)):
            # could be a json dumped text.
            raise Exception("Inventory value has to be a string ")

        res = self.retrieveinventoryprop(inventoryid, iproptmpltid)
        if len(res) > 0:
            raise Exception('A value exists already.')
        
        try:
            cur = self.conn.cursor()
            sql = '''
            insert into inventory_prop
            (inventory_id, inventory_prop_tmplt_id, inventory_prop_value)
            values(%s, %s, %s)
            '''
            
            cur.execute(sql, (inventoryid, iproptmpltid, value))
            self.commit()
            # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
            # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
            # it is per connection.
            lastid = cur.lastrowid
        except MySQLdb.Error as e:
            self.logger.info('Error when saving inventory property value:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when saving inventory property value:\n%s (%d)' % (e.args[1], e.args[0]))
        
        return lastid

    def updateinventoryprop(self, value, inventoryid, iproptmpltid):
        '''Update value to inventory property table with given inventory id and inventory property template id.
        
        return True if success, otherwise, throw out an exception.
        '''
        if not isinstance (value, (str, unicode)):
            raise Exception("Inventory value has to be a string ")

        res = self.retrieveinventoryprop(inventoryid, iproptmpltid)
        if len(res) == 0:
            raise Exception('No entity found in inventory property table.')
        sql = '''
        update inventory_prop
        SET
        inventory_prop_value = %s
        where
        inventory_id = %s and inventory_prop_tmplt_id = %s
        '''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (value, inventoryid, iproptmpltid))
            self.commit()
        except MySQLdb.Error, e:
            self.logger.info('Error when saving component type property value:\n%s (%d)' % (e.args[1], e.args[0]))
            raise Exception('Error when saving component type property value:\n%s (%d)' % (e.args[1], e.args[0]))
        
        return True
        
    def retrieveinstall(self, name, ctypename=None, location=None):
        '''Retrieve installed device name with table id upon giving device name.
        
        return: tuple with format as ((id, field name, location, component type name, description, vendor), ...)
        '''
        if not isinstance(name, (str, unicode)):
            raise Exception('Device name has to be a string.')
        
        name = self.__wildcardformat(name)

        sql = '''
        select install_id, field_name, location, cmpnt_type_name, description, vendor_name
        from install
        left join cmpnt_type on install.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        left join cmpnttype__vendor on cmpnt_type.cmpnt_type_id = cmpnttype__vendor.cmpnt_type_id
        left join vendor on cmpnttype__vendor.vendor_id = vendor.vendor_id
        where
        '''
        
        if '%' in name or '_' in name:
            sql += " field_name like %s "
        else:
            sql += " field_name = %s "
        vals = [name]

        if ctypename:
            ctypename = self.__wildcardformat(ctypename)
            if "%" in ctypename or "_" in ctypename:
                sql += " and cmpnt_type_name like %s "
            else:
                sql += " and cmpnt_type_name = %s "
            vals.append(ctypename)

        if location:
            location = self.__wildcardformat(location)
            if "%" in location or "_" in location:
                sql += " and location like %s "
            else:
                sql += " and location = %s "
            vals.append(location)

        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching device from install table:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when fetching device from install table:\n%s (%d)' %(e.args[1], e.args[0]))
        
        return res

    def saveinstall(self, name, ctypeid, location, inventoryid=None):
        '''Save installed device into install table.
        
        Return id if success, otherwise throw out an exception.
        '''
        if not isinstance(name, (str, unicode)) or not isinstance(location, (str, unicode)):
            raise Exception('Both device name and location info have to be string.')

        sql = 'select cmpnt_type_name from cmpnt_type where cmpnt_type_id = %s'        
        cur=self.conn.cursor()
        cur.execute(sql, (ctypeid,))
        ctypename = cur.fetchone()
        if ctypename != None:
            ctypename=ctypename[0]
        else:
            raise ValueError("component type (id=%s) does not exist."%(ctypeid))
        
        res = self.retrieveinstall(name, ctypename=ctypename, location=location)
        if len(res) > 0:
            raise Exception('Device (%s) exists already' %(name) )
        
        # For data consistency, using transaction to avoid insertion error
        try:
            # insert device name to install table
            sql = '''
            insert into install
            (cmpnt_type_id, field_name, location)
            values (%s, %s, %s)
            '''
            cur.execute(sql, (ctypeid, name, location))
            #self.commit()
            instid = cur.lastrowid
                        
            # create relationship between inventory and install
            if inventoryid:
                sql = '''
                select * from inventory__install
                where
                install_id = %s and inventory_id = %s
                '''
                cur.execute(sql, (instid, inventoryid))
                res = cur.fetchone()
                # create a new entry if it does not exist
                if not res:
                    sql = '''
                    insert into inventory__install
                    (install_id, inventory_id)
                    values (%s, %s)
                    '''
                cur.execute(sql, (instid, inventoryid))
            
        except MySQLdb.Error:
            self.conn.rollback()
            self.logger.info('Error to save device name into install table')
            raise Exception('Error to save device name into install table')
        
        # commit all changes if everything is OK.
        self.commit()
        return instid
        
    def retrieveinventory(self, serial, ctypename=None, vendor=None):
        '''Retrieve an inventory information according given serial number, vendor name, and component type name.

        Wildcards are support in all parameters (device name, serial number, component type name, and vendor), 
        which uses "*" for multiple match, and "?" for single character match.
        
        return: tuple of inventory id, serial number like:
            with vendor name, component type name, and component type description if both component type and vendor are given
                like ((inventory id, serial no, component type name, type description, vendor), ...)
        '''
        if not isinstance(serial, (str, unicode)):
            raise Exception('Serial no has to be string.')

        '''select install.install_id, inventory.inventory_id, install.field_name, install.location,
        inventory.serial_no, 
        cmpnt_type.cmpnt_type_name, cmpnt_type.description,
        vendor.vendor_name
        '''
        
        serial = self.__wildcardformat(serial)
        sql = '''
        select inv.inventory_id, inv.serial_no, ctype.cmpnt_type_name, ctype.description, vendor.vendor_name
        from inventory inv
        left join vendor on vendor.vendor_id = inv.vendor_id
        left join cmpnt_type ctype on ctype.cmpnt_type_id = inv.cmpnt_type_id
        where inv.serial_no like %s 
        '''
        # adjust order order to avoid unexpected error.
#        left join cmpnttype__vendor ctvendor on ctvendor.cmpnt_type_id = ctype.cmpnt_type_id
#        left join vendor on vendor.vendor_id = ctvendor.vendor_id
        vals = [serial]
        try:
            cur=self.conn.cursor()
            if ctypename:
                sql += ' and ctype.cmpnt_type_name like %s '
                ctypename = self.__wildcardformat(ctypename)
                vals.append(ctypename)
            elif vendor:
                sql += ' and vendor.vendor_name like %s '
                vendor = self.__wildcardformat(vendor)
                vals.append(vendor)
            cur.execute(sql, vals)
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching inventory information for a given serial no (%s):\n%s (%b)' %(serial, e.args[1], e.args[0]))
            raise Exception('Error when fetching inventory information for a given serial no (%s):\n%s (%b)' %(serial, e.args[1], e.args[0]))
        
        return res

    def saveinventory(self, serial, ctype, vendor):
        '''Save inventory with given device name, vendor, and component type.
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
            raise Exception("Device (%s) with component type (%s) from vendor (%s) exists already." %(serial, ctype, vendor))

        self.retrievecmpnttype(ctype, vendor=vendor)
        sql = '''
        select ctype.cmpnt_type_id, vendor.vendor_id 
        from cmpnt_type ctype
        left join cmpnttype__vendor ctvndr on ctype.cmpnt_type_id = ctvndr.cmpnt_type_id
        left join vendor on ctvndr.vendor_id = vendor.vendor_id
        where vendor.vendor_name = %s and ctype.cmpnt_type_name = %s
        '''
        cur = self.conn.cursor()
        cur.execute(sql, (vendor, ctype))
        
        res = cur.fetchall()
        #if len(res) == 0:
        if len(res) != 1:
            # Throw an exception since either the entry is not unique, or not linked in advance
            raise Exception("Component type (%s) from vendor (%s) does not exist, or not unique."%(ctype, vendor))
        
        ctypeid, vendorid = res[0]
        
        sql = '''
        insert into inventory (cmpnt_type_id, vendor_id, serial_no)
        values (%s, %s, %s)
        '''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (ctypeid, vendorid, serial))
            # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
            # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
            # it is per connection.
            invid = cur.lastrowid
        except MySQLdb.Error as e:
            self.conn.rollback()
            self.logger.info('Error when inserting device (%s) into inventory with type (%s) from vendor (%s):\n%s (%b)' 
                             %(serial, ctype, vendor, e.args[1], e.args[0]))
            raise Exception('Error when inserting device (%s) into inventory with type (%s) from vendor (%s):\n%s (%b)' 
                            %(serial, ctype, vendor, e.args[1], e.args[0]))
        
        self.commit()
        return invid
    
    def retrieveinstalledinventory(self, name, serial, ctypename=None, vendor=None, location=None):
        '''
        Retrieve devices from inventory what have been installed according given device name, serial number, component type and vendor.

        Wildcards are support in all parameters (device name, serial number, component type name, and vendor), 
        which uses "*" for multiple match, and "?" for single character match.
        
        Return: tuple with format like ((install id, inventory id, device name, location, serial number, component type name, description, vendor name), ...).
        '''
        sql = '''select install.install_id, inventory.inventory_id, install.field_name, install.location,
        inventory.serial_no, 
        cmpnt_type.cmpnt_type_name, cmpnt_type.description,
        vendor.vendor_name
        from install
        left join inventory__install on install.install_id = inventory__install.install_id
        left join inventory on inventory__install.inventory_id = inventory.inventory_id
        left join cmpnt_type on inventory.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        left join cmpnttype__vendor on cmpnt_type.cmpnt_type_id = cmpnttype__vendor.cmpnt_type_id
        left join vendor on vendor.vendor_id = cmpnttype__vendor.vendor_id
        '''
#        if ctypename:
#            sql += '''join cmpnt_type on inventory.cmpnt_type_id = cmpnt_type.cmpnt_type_id
#            '''
#        if vendor:
#            sql += '''join cmpnttype__vendor on cmpnt_type.cmpnt_type_id = cmpnttype__vendor.cmpnt_type_id
#            join vendor on vendor.vendor_id = cmpnttype__vendor.vendor_id
#            '''
#        # use raw sql query instead of calling API for efficiency issue.
#        invres = self.retrieveinventory(serial, ctypename=ctypename, vendor=vendor)
        name = self.__wildcardformat(name)
        if "%" in name or "_" in name:
            sql += ' where install.field_name like %s '
        else:
            sql += ' where install.field_name = %s '
        vals = [name]
        
        serial = self.__wildcardformat(serial)
        if "%" in serial or "_" in serial:
            sql += ' and inventory.serial_no like %s '
        else:
            sql += ' and inventory.serial_no = %s '
        vals.append(serial)
        
        if ctypename:
            ctypename=self.__wildcardformat(ctypename)
            if "%" in ctypename or "_" in ctypename:
                sql += ' and cmpnt_type.cmpnt_type_name like %s '
            else:
                sql += ' and cmpnt_type.cmpnt_type_name = %s '
            vals.append(ctypename)
        
        if vendor:
            vendor = self.__wildcardformat(vendor)
            if "%" in vendor or "_" in vendor:
                sql += ' and vendor.vendor_name like %s '
            else:
                sql += ' and vendor.vendor_name = %s '
            vals.append(vendor)
        if location:
            location = self.__wildcardformat(location)
            if "%" in location or "_" in location:
                sql += ' and install.location like %s '
            else:
                sql += ' and install.location = %s '
            vals.append(location)

        try:
            print(sql, vals)
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when selecting installed device (%s) with serial no (%s) from inventory with type (%s) from vendor (%s):\n%s (%b)' 
                             %(name, serial, ctypename, vendor, e.args[1], e.args[0]))            
            raise Exception('Error when selecting installed device (%s) with serial no (%s) from inventory with type (%s) from vendor (%s):\n%s (%b)' 
                            %(name, serial, ctypename, vendor, e.args[1], e.args[0]))
        
        return res
        
    def inventory2install(self, installid, inventoryid):
        '''
        link an inventory as installed device
        '''
        sqlinst = '''select 1 from install where install_id = %s'''
        sqlinv = '''select 1 from inventory where inventory_id = %s'''
        
        cur=self.conn.cursor()
#        DEBUG = 1
#        if DEBUG:
#            res = cur.execute(sqlinst, (installid,))
#            print(res)
#            res = cur.execute(sqlinv, (inventoryid, ))
#            print(res, inventoryid)
        
        if not cur.execute(sqlinst, (installid,)) or not cur.execute(sqlinv, (inventoryid,)):
            raise ValueError('Given install id (%s) or inventory id (%s) does not exist. Can not link them together.' 
                             %(installid, inventoryid))
        sql = '''select inventory__install_id from inventory__install where install_id = %s or inventory_id = %s'''
        cur.execute(sql, (installid, inventoryid))
        res = cur.fetchall()

        if len(res):
            ii_id = res
            if len(res) > 1:
                # either inventory id or install can be in inventory__install table once.
                # One device in inventory can only be installed in one place.
                self.logger.info("More than one entry found for installed (id: %s) device in inventory (%s)" %(installid, inventoryid))
                raise ValueError("More than one entry found for installed (id: %s) device in inventory (%s)" %(installid, inventoryid))
            ii_id = res[0][0]
        else:
            sql = '''insert into inventory__install (install_id, inventory_id) values(%s, %s)
            '''
            try:
                cur.execute(sql, (installid, inventoryid))
                # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
                # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
                # it is per connection.
                ii_id = cur.lastrowid
            except MySQLdb.Error as e:
                self.conn.rollback()
                self.logger.info('Error when linking install (id: %s) with inventory (id: %s):\n%s (%s)' 
                                 %(installid, inventoryid, e.args[1], e.args[0]))
                raise Exception('Error when linking install (id: %s) with inventory (id: %s):\n%s (%s)' 
                                 %(installid, inventoryid, e.args[1], e.args[0]))
            
            self.commit()
        
        return ii_id
    
    def retrievesystem(self, location = None):
        '''
        retrieve location information from install table
        '''
        sql = '''
        select distinct location from install where location %s
        '''
        val = None
        if location == None:
            sql = sql%("like %s")
            val = "%"
        else:
            val = self.__wildcardformat(location)
            if "%" in val or "_" in val:
                sql = sql%("like %s")
            else:
                sql = sql %(' = %s')
                
        cur = self.conn.cursor()
        cur.execute(sql, (val,))
        rawres = cur.fetchall()
        system = []
        for r in rawres:
            system.append(r[0])
        return system    
        
    def retrievemuniconv4inventory(self, invid, invproptmpltname, invproptmpltdesc):
        '''
        Get magnet unit conversion information for given inventory id with inventory property template name and its description.
        '''
        sql = '''
        select inventory.serial_no, cmpnt_type.cmpnt_type_name, inventory_prop.inventory_prop_value
        from inventory
        left join inventory_prop on inventory_prop.inventory_id = inventory.inventory_id
        left join cmpnt_type on inventory.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        left join inventory_prop_tmplt on inventory_prop_tmplt.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        where
        inventory.inventory_id = %s
        and inventory_prop_tmplt.inventory_prop_tmplt_name like %s
        and inventory_prop_tmplt.inventory_prop_tmplt_desc like %s
        '''
        #'''
        #select inventory.serial_no, cmpnt_type.cmpnt_type_name, inventory_prop.inventory_prop_value
        #from inventory_prop
        #left join inventory on inventory_prop.inventory_id = inventory.inventory_id
        #left join cmpnt_type on inventory.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        #left join inventory_prop_tmplt on inventory_prop_tmplt.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        #where 
        #inventory.inventory_id = %s 
        #and inventory_prop_tmplt.inventory_prop_tmplt_name like %s
        #and inventory_prop_tmplt.inventory_prop_tmplt_desc like %s
        #'''
        invproptmpltname = self.__wildcardformat(invproptmpltname)
        invproptmpltdesc = self.__wildcardformat(invproptmpltdesc)
        
        cur = self.conn.cursor()
        cur.execute(sql, (invid, invproptmpltname, invproptmpltdesc))
        rawres = cur.fetchone()
        return rawres
        
    def retrievemuniconvbycmpnttype4inventory(self, invid, ctypeproptypetmpltname, ctypeproptmpltdesc):
        '''
        Get magnet unit conversion information for given inventory id with component type property template name and its description.
        This method retrieve a common information for given magnet type.
        
        Use this method only when the measurement data for each individual magnet is not available.
        '''
        sql = '''
        select inventory.serial_no, cmpnt_type.cmpnt_type_name, cmpnt_type_prop.cmpnt_type_prop_value
        from inventory
        left join cmpnt_type on inventory.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        left join cmpnt_type_prop on cmpnt_type_prop.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        left join cmpnt_type_prop_type on cmpnt_type_prop.cmpnt_type_prop_type_id = cmpnt_type_prop_type.cmpnt_type_prop_type_id
        where 
        inventory.inventory_id = %s 
        and cmpnt_type_prop_type.cmpnt_type_prop_type_name like %s
        and cmpnt_type_prop_type.cmpnt_type_prop_type_desc like %s
        '''
        ctypeproptypetmpltname = self.__wildcardformat(ctypeproptypetmpltname)
        ctypeproptmpltdesc = self.__wildcardformat(ctypeproptmpltdesc)
        
        cur = self.conn.cursor()
        cur.execute(sql, (invid, ctypeproptypetmpltname, ctypeproptmpltdesc))
        rawres = cur.fetchone()
        return rawres

    def retrievemuniconv4install(self, name, ctypeproptypetmpltname, ctypeproptmpltdesc):
        '''
        Get magnet unit conversion information for given field name with component type property template name and its description.
        This method retrieve a common information for given magnet type.
        '''
        sql = '''
        select field_name, cmpnt_type.cmpnt_type_name, cmpnt_type_prop.cmpnt_type_prop_value
        from install
        left join cmpnt_type on install.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        left join cmpnt_type_prop on cmpnt_type_prop.cmpnt_type_id = cmpnt_type.cmpnt_type_id
        left join cmpnt_type_prop_type on cmpnt_type_prop.cmpnt_type_prop_type_id = cmpnt_type_prop_type.cmpnt_type_prop_type_id
        where 
        install.field_name like %s 
        and cmpnt_type_prop_type.cmpnt_type_prop_type_name like %s
        and cmpnt_type_prop_type.cmpnt_type_prop_type_desc like %s
        '''
        name = self.__wildcardformat(name)
        ctypeproptypetmpltname = self.__wildcardformat(ctypeproptypetmpltname)
        ctypeproptmpltdesc = self.__wildcardformat(ctypeproptmpltdesc)
        
        cur = self.conn.cursor()
        cur.execute(sql, (name, ctypeproptypetmpltname, ctypeproptmpltdesc))
        rawres = cur.fetchone()
        return rawres
        
    def retrieveinventoryid(self, name):
        ''''''
        sql = '''
        select field_name, ii.inventory_id 
        from install 
        left join inventory__install ii on ii.install_id = install.install_id
        where field_name like %s;
        '''
        name = self.__wildcardformat(name)
        cur=self.conn.cursor()
        cur.execute(sql, (name,))
        return cur.fetchall()
        
