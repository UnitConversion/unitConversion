""" 
Created on Aug 15, 2013

@author: shengb

"""

import logging
import MySQLdb

from collections import OrderedDict

from utils import (_wildcardformat)

from _mysql_exceptions import MySQLError

__all__ = []
__version__ = [1, 0, 0]

class epsai(object):
    '''
    Data API for active interlock system.
    '''
    def __init__(self, conn, transaction=None):
        '''initialize active interlock class.
        
        :param conn: MySQL connection object
        :type conn: object

        :param transaction: Django MySQL transaction object. If this is set, it uses Django's transaction manager to manage each transaction.
        :type transaction: object
        
        :returns:  epsai -- class object
        
        '''
        self.logger = logging.getLogger('interlock')
        hdlr = logging.FileHandler('/var/tmp/active_interlock.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.DEBUG)

        self.conn = conn
        
        # use django transaction manager
        self.transaction = transaction
        
    def retrieveactiveinterlock(self, status, datefrom=None, dateto=None, withdata=True, rawdata=False):
        '''Retrieve a data set according its saved time, and status.
        One data set should have same properties for all device although its value could be empty.
        
        data structure:
        
        .. code-block:: python
        
            {id: {
                  'status': ,
                  'rawdata': {'name':, 'data': },
                  'description': , 
                  'author': ,
                  'initialdate': ,
                  'lastmodified': ,
                  'modifieddate': ,
                  'data':{'label':       [], # str, column's name, also property type collections for one active interlock unit.
                          'units':       [], # str, units for each columns. Empty string if it does not have one.
                         
                          # the following are those columns appeared in ``label`` field.
                          'name':        [], # str, active interlock device name 
                          'definition':  [], # str, definition for that device
                          'logicname':   [], # str, active interlock envelop name
                          'shape':       [], # str, allowed shape in phase space
                          's':           [], # double, s position in a lattice, particularly in a installation lattice
                          'offset':      [], # double, offset relative to the center of a straight section
                          'safecurent':  [], # double, allowed beam current for safe operation.  
                                             # no need for active interlock if beam current is lower than this value.
                          'aihol':       [], # double, allowed horizontal offset limit
                          'aivol':       [], # double, allowed vertical offset limit
                          'aihal':       [], # double, allowed horizontal angle limit
                          'aival':       [], # double, allowed vertical angle limit
                          'up_name':     [], # str, upstream BPM name involved in this active interlock unit
                          'up_definition': [], #str, upstream device definition
                          'up_offset':   [], # double, offset of upstream BPM relative to the center of a straight section
                          'up_aihol':    [], # double, allowed horizontal offset limit of upstream BPM
                          'up_aivol':    [], # double, allowed vertical offset limit of upstream BPM
                          'down_name':   [], # str, downstream BPM name involved in this active interlock unit
                          'down_definition': [], #str, downstream device definition
                          'down_offset': [], # double, offset of downstream BPM relative to the center of a straight section
                          'down_aihol':  [], # double, allowed horizontal offset limit of downstream BPM
                          'down_aivol':  [], # double, allowed vertical offset limit of downstream BPM
                          'logiccode':   [], # logic algorithm encoding code
                         }
                 },
                 ...
            }
            
        label is now defined as below:
         
        .. code-block:: python
         
            ['name', 'definition', 'logicname', 'shape', 'logic', 'logiccode'
             's', 'offset', 'safecurent', 'aihol', 'aivol', 'aihal', 'aival',
             'up_name', 'up_definition', 'up_offset', 'up_aihol', 'up_aivol',
             'down_name', 'down_definition', 'down_offset', 'down_aihol', 'down_aivol',
            ]
        
        units is for each columns contained in ``label``, therefore, it should have exact sequence as it appears in label
        except ``units`` itself which should be the last one.
        is most like as below:
        
        .. code-block:: python
         
            ['', '', '', '', '', '', 
             'm', 'm', 'mA', 'mm', 'mm', 'mrad', 'mrad',
             '', '', 'm', 'mm', 'mm',
             '', '', 'm', 'mm', 'mm'
            ]
        
        :param status: Current status.
        :type status: int
        
        :param datefrom: data saved after this time. Default is None, which means data from very beginning. It has format as **yyyy-MM-dd hh:mm:ss** since dates in MySql are represented with the format.
        :type datafrom: datetime
        
        :param dateto: data saved before this time. Default is None, which means data till current. It has format as **yyyy-MM-dd hh:mm:ss** since dates in MySql are represented with the format.
        :type datato: datetime
        
        :param withdata: get data set. Default is true, which means always gets data by default. Otherwise, only device names are retrieved for desired data set.
        :type withdata: boolean
        
        :param rawdata: get raw data back also. Default is false, which means no raw data.
        :type rawdata: boolean
        
        :Returns: dict
            
        :Raises: KeyError, AttributeError
        
        '''
        if withdata:
            return self._retrievedataset(status, datefrom=datefrom, dateto=dateto, rawdata=rawdata)
        else:
            return self._retrievedataheader(status, datefrom=datefrom, dateto=dateto, rawdata=rawdata)

    def _retrievedataheader(self, status, datefrom=None, dateto=None, rawdata=False):
        '''Retrieve data set header information only.'''
        sql = '''
        select ai.active_interlock_id, ai.status, ai.description, 
        ai.created_by, ai.created_date, ai.modified_by, ai.modified_date
        from active_interlock ai
        where
        '''
        if rawdata:
            sql = '''
            select ai.active_interlock_id, ai.status, ai.description, 
            ai.created_by, ai.created_date, ai.modified_by, ai.modified_date, ai.rawdata
            from active_interlock ai
            where
            '''
        vals=[]
        if status not in ['*', '?']:
            sql += ' ai.status = %s '
            vals.append(status)
        else:
            sql += ' ai.status like %s '
            vals.append('%')
        
        if datefrom != None:
            if len(vals) > 0:
                sql+=' and '
            sql+= ' ai.created_date >= %s '
            vals.append(datefrom)
            
        if dateto != None:
            if len(vals) > 0:
                sql+=' and '
            sql+= ' ai.created_date <= %s '
            vals.append(dateto)
        
        try:
            cur=self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching active interlock data set headers:\n%s (%d)' %(e.args[1], e.args[0]))
            raise e

        resdict = {}
        for r in res:
            tmp = {'status': r[1]}
            if r[2] != None:
                tmp['description'] = r[2]
            if r[3] != None:
                tmp['author'] = r[3]
            if r[4] != None:
                tmp['initialdate'] = r[4].isoformat()
            if r[5] != None:
                tmp['lastmodified'] = r[5]
            if r[6] != None:
                tmp['modifieddate'] = r[6].isoformat()

            if len(r) == 8:
                tmp['rawdata'] = r[7]
            resdict[r[0]] = tmp

        return resdict
    
    def _retrievedataset(self, status, datefrom=None, dateto=None, rawdata=False):
        '''Retrieve data set'''
        
        res = self._retrievedataheader(status, datefrom=datefrom, dateto=dateto, rawdata=rawdata)
        sql = '''
        select 
        aid.device_name, aid.definition,
        ail.name, ail.shape, ail.logic, ail.logic_code, 
        aipt.name, aipt.description, aipt.unit, aipt.created_date,
        aip.value, aip.inserted_date
        from active_interlock_prop aip
        left join active_interlock_device aid on aip.active_interlock_device_id = aid.active_interlock_device_id
        left join active_interlock_logic ail on ail.active_interlock_logic_id=aid.active_interlock_logic_id
        left join active_interlock_prop_type aipt on aipt.active_interlock_prop_type_id=aip.active_interlock_prop_type_id
        where aid.active_interlock_id = %s order by aid.device_name
        '''
        try:
            cur=self.conn.cursor()
            for aiid, aidata in res.iteritems():
                devicename=''
                cur.execute(sql, (aiid,))
                resdata = cur.fetchall()
                firstround = True
                label=['name', 'definition', 'logicname', 'shape', 'logic', 'logiccode']
                units=['', '', '', '', '', '']
                
    
                innerdata = OrderedDict((('label', label),
                                         ('units', units),
                                         ('name', []),
                                         ('definition', []),
                                         ('logicname', []),
                                         ('shape', []),
                                         ('logic', []),
                                         ('logiccode', []),
                                         ))
                for restmp in resdata:
                    if devicename != restmp[0]:
                        for i in range(6):
                            innerdata[label[i]].append(restmp[i])

                        if devicename != '':
                            firstround=False
                        devicename = restmp[0]
                    if firstround:
                        label.append(restmp[6])
                        if restmp[8] == None:
                            units.append('')
                        else:
                            units.append(restmp[8])
                        innerdata[restmp[6]]=[restmp[10]]
                    else:
                        innerdata[restmp[6]].append(restmp[10])

                aidata['data'] = innerdata
                res[aiid]=aidata

        except MySQLdb.Error as e:
            self.logger.info('Database error when fetching active interlock data set:\n%s (%d)' %(e.args[1], e.args[0]))
            raise
        except KeyError as e:
            self.logger.info('Data set error when fetching active interlock data set:\n%s (%d)' %(e.args[1], e.args[0]))
            raise e

        return res
    
    def saveactiveinterlock(self, data, description=None, rawdata=None, active=True, author=None):
        '''Save a new data set of active interlock.
        By default, it deactivates existing active data set, and active this new data set.
        Only one active data is allowed.
        
        A logic of active interlock has to be saved first, otherwise, an AttributeError might raise if logic can not be found.
        
        data structure:
        
        .. code-block:: python
        
            {'label':       [], # str, column's name, also property type collections for one active interlock unit.
             'units':       [], # str, units for each columns. Empty string if it does not have one.
             
             # the following are those columns appeared in ``label`` field.
             'name':        [], # str, active interlock device name 
             'definition':  [], # str, definition for that device
             'logicname':   [], # str, active interlock envelop name
             'shape':       [], # str, allowed shape in phase space
             's':           [], # double, s position in a lattice, particularly in a installation lattice
             'offset':      [], # double, offset relative to the center of a straight section
             'safecurent':  [], # double, allowed beam current for safe operation.  
                                # no need for active interlock if beam current is lower than this value.
             'aihol':       [], # double, allowed horizontal offset limit
             'aivol':       [], # double, allowed vertical offset limit
             'aihal':       [], # double, allowed horizontal angle limit
             'aival':       [], # double, allowed vertical angle limit
             'up_name':     [], # str, upstream BPM name involved in this active interlock unit
             'up_definition': [], #str, upstream device definition
             'up_offset':   [], # double, offset of upstream BPM relative to the center of a straight section
             'up_aihol':    [], # double, allowed horizontal offset limit of upstream BPM
             'up_aivol':    [], # double, allowed vertical offset limit of upstream BPM
             'down_name':   [], # str, downstream BPM name involved in this active interlock unit
             'down_definition': [], #str, downstream device definition
             'down_offset': [], # double, offset of downstream BPM relative to the center of a straight section
             'down_aihol':  [], # double, allowed horizontal offset limit of downstream BPM
             'down_aivol':  [], # double, allowed vertical offset limit of downstream BPM
            }
            
        label is now defined as below:
         
        .. code-block:: python
         
            ['name', 'definition', 'logicname', 'shape',
             's', 'offset', 'safecurent', 'aihol', 'aivol', 'aihal', 'aival',
             'up_name', 'up_definition', 'up_offset', 'up_aihol', 'up_aivol',
             'down_name', 'down_definition', 'down_offset', 'down_aihol', 'down_aivol',
            ]
            
        units is for each columns contained in ``label``, therefore, it should have exact sequence as it appears in label
        except ``units`` itself which should be the last one.
        is most like as below:
        
        .. code-block:: python
         
            ['', '', '', '',
             'm', 'm', 'mA', 'mm', 'mm', 'mrad', 'mrad',
             '', '', 'm', 'mm', 'mm',
             '', '', 'm', 'mm', 'mm'
            ]
            
        :param data: original data structure is described as above.
        :type data: dict
            
        :param description: comments or any other notes for this data set.
        :type description: str
        
        :param rawdata: raw data serialized into a JSON string. Its original format is as below: 
            
            .. code-block:: python

                'rawdata': {'name':, 
                            'data': 
                           }

        :type rawdata: str

        
        :param active: set current data set active. It sets new data set as active by default unless it is explicitly set to keep old active data set.
        :type active: boolean
        
        :param author: the person who set this data set.
        :type author: str
        
        :Returns: active interlock internal id if saved successfully.
            
        :Raises: ValueError, MySQLError, KeyError, AttributeError 

        '''
        proptypes=data['label']
        proptypeunits=data['units']

        if len(proptypes) != len(proptypeunits):
            raise ValueError('units are missing for %s columns.'%(len(proptypes) - len(proptypeunits)))
        
        try:
            cur=self.conn.cursor()
            
            # get property type internal id
            proptypeids = {}
            for i in range(len(proptypes)):
                tmp = self.retrieveactiveinterlockproptype(proptypes[i], unit=proptypeunits[i])
                if len(tmp['id']) == 0:
                    # should add a new entry
                    proptypeids[proptypes[i]] = self.saveactiveinterlockproptype(proptypes[i], unit=proptypeunits[i])
                elif len(tmp['id']) == 1:
                    proptypeids[proptypes[i]] = tmp['id'][0]
                else:
                    raise ValueError('property type (name: %s, unit: %s) is not unique.'%(proptypes[i], proptypeunits[i]))
            
            # get active interlock logic internal id
            logicids=[]
            #proptypes_tmp = proptypes.copy()
            proptypes_tmp = proptypes[:]
            if 'logicname' in proptypes_tmp: 
                proptypes_tmp.remove('logicname')
            else:
                raise AttributeError('active interlock logic is not defined.')
            if 'shape' in proptypes_tmp: 
                proptypes_tmp.remove('shape')
            else:                        
                raise AttributeError('active interlock allowed shape in phase space is not defined.')

            for i in range(len(data['logicname'])):
                tmp = self.retrieveactiveinterlocklogic(data['logicname'][i], data['shape'][i])
                if len(tmp['id']) != 1:
                    raise AttributeError('Given activeinterlock envelop (name: %s, shape: %s) does not exist yet.'%(data['logicname'][i], data['shape'][i]))
                else:
                    logicids.append(tmp['id'][0])

            # save header onformation of a active interlock data set
            sql = '''
            insert into active_interlock (created_date, status
            '''
            sqlext = 'values (now(), %s'
            sqlvals = []

            if active:
                # find existing active interlock internal id for active data set
                cur.execute('select active_interlock_id from active_interlock where status = 1')
                active_aiid = cur.fetchone()
                if active_aiid != None:
                    # find one, otherwise, there is no active data set.
                    # deactivate existing active data set
                    self.updateactiveinterlockstatus(active_aiid[0], 0, author=author)
                sqlvals.append('1')
            else:
                sqlvals.append('0')
                
            
            if description != None:
                sql += ', description '
                sqlext+= ', %s '
                sqlvals.append(description)
            
            if author != None:
                sql += ', created_by '
                sqlext+= ', %s '
                sqlvals.append(author)
            
            if rawdata!=None:
                # use pickle to serialize raw data into binary, and save into a BLOB. 
                sql += ', rawdata '
                sqlext+= ', %s '
                sqlvals.append(rawdata)

            sql = sql+' ) '+sqlext+ ' ) '
            
            cur.execute(sql, sqlvals)
            # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
            # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
            # it is per connection.
            aiid = cur.lastrowid
            
            if 'name' in proptypes_tmp: proptypes_tmp.remove('name')
            if 'definition' in proptypes_tmp: proptypes_tmp.remove('definition')            
            has_definition = False
            if data.has_key('definition'):
                has_definition = True
                
            for i in range(len(data['name'])):
                # save active interlock main device information
                if has_definition:
                    sql = '''insert into active_interlock_device
                    (active_interlock_id, active_interlock_logic_id, device_name, definition)
                    values
                    (%s, %s, %s, %s)
                    '''
                    cur.execute(sql, (aiid, logicids[i], data['name'][i], data['definition'][i]))
                else:
                    sql = '''insert into active_interlock_device
                    (active_interlock_id, activeinterlock_logic_id, device_name)
                    values
                    (%s, %s, %s)
                    '''
                    cur.execute(sql, (aiid, logicids[i], data['name'][i]))
                aidid = cur.lastrowid
                
                # save other information of an active interlock unit
                for ptype in proptypes_tmp:
                    sql = '''insert into active_interlock_prop
                    (active_interlock_device_id, active_interlock_prop_type_id, value, inserted_date)
                    values
                    (%s, %s, %s, now())
                    '''
                    cur.execute(sql, (aidid, proptypeids[ptype], data[ptype][i]))
                
            if self.transaction == None:
                self.conn.commit()
                
        except MySQLError as e:
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when updating active interlock data status:\n%s (%d)' %(e.args[1], e.args[0]))
            raise
        
        return aiid
        
    def updateactiveinterlockstatus(self, aiid, status, author=None):
        '''Update status of a data set.
        Once data is saved into database, only its status is allowed to be updated between active & inactive.
        Only up to one (1) data set is allowed to be active. When the status is to active a particular data set,
        it deactivates current active data set.
        
        Currently, the status is either active and inactive as defined as below: ::
        
            0: inactive
            1: active 
        
        However, the definition could be extended when there is other requirement.
        
        :param aiid: internal id of an active interlock data set
        :type aiid: int
        
        :param status: new status code
        :type status: int
        
        :param author: name who requests this update
        :type author: str
            
        :Returns: boolean
            
            The return code: ::
                
                True -- when the status is changed.
                False -- when the status is not changed.
        
        :Raises: MySQLError, ValueError, AttributeError
        
        '''
        
        if status not in [0, 1]:
            raise AttributeError('status for active interlock data has to be either 0 or 1.')

        try:
            cur=self.conn.cursor()
            cur.execute('''select status from active_interlock where active_interlock_id = %s''', (aiid,))
            aiid_status = cur.fetchone()
            
            if aiid_status == None:
                raise ValueError("given internal id (%s) of active interlock data set does not exist"%(aiid))
            aiid_status = aiid_status[0]
            
            if aiid_status == status:
                # Nothing to do since status is same for that particular data set
                return False
            
            deactivate=False
            active_id = -1
            
            if status == 1:
                # activate this particular data set, therefore, current active data set has to be deactivated.
                
                # get current active data set id
                cur.execute('''select active_interlock_id from active_interlock where status = 1''')
                active_id = cur.fetchone()
                if len(active_id) != 0:
                    # find active data set, has to deactivate it before setting a new active data set.
                    deactivate=True
                    active_id = active_id[0]
            
            if author == None:
                if deactivate:
                    sql = '''update active_interlock set status=0, modified_by=NULL, modified_date=now() where active_interlock_id = %s'''
                    cur.execute(sql, (active_id,))

                sql = '''update active_interlock set status=%s, modified_by=NULL, modified_date=now() where active_interlock_id = %s'''
                cur.execute(sql, (status, aiid))
            else:
                if deactivate:
                    sql = '''update active_interlock set status=0, modified_by=%s, modified_date=now() where active_interlock_id = %s'''
                    cur.execute(sql, (author, active_id,))

                sql = '''update active_interlock set status=%s, modified_by=%s, modified_date=now() where active_interlock_id = %s'''
                cur.execute(sql, (status, author, aiid))
            if self.transaction == None:
                self.conn.commit()
                
        except MySQLError as e:
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when updating active interlock data status:\n%s (%d)' %(e.args[1], e.args[0]))
            raise
        return True

    def retrieveactiveinterlockproptype(self, name, unit=None, description=None):
        '''Each involved in active interlock system has some properties like offset, AIHOL/AIVOL, AIHAL/AIVAL, safe current, and so on.
        This method is to retrieve active interlock property type information with given name, unit, and/or description.
        
        Wildcast matching is supported with:
        
            - ``*`` for multiple characters match, 
            - ``?`` for single character match.

        :param name: property type name.
        :type name: str
        
        :param unit: unit of given property type.
        :type unit: str
        
        :param description: description of given property type.
        :type description: str
        
        :returns: dict
            
            A python dictionary is return with each field as an list which could be converted into a table. Its structure is as below:
            
            .. code-block:: python
            
                {'label':       [], # str, columns's name
                 'id':          [], # int, internal id of property type
                 'name':        [], # str, active interlock property type name 
                 'unit':        [], # str, active interlock property type unit
                 'description': [], # str, property type description
                 'date':        [], # datetime, when this entry was created
                }
        
        :raises: MySQLError
        
        '''
        sql = '''select active_interlock_prop_type_id, name, unit, description, created_date
        from active_interlock_prop_type where name
        '''
        vals=[]
        if "*" in name or "?" in name:
            sql+= ' like %s '
            name=_wildcardformat(name)
        else:
            sql+= ' = %s '
        vals.append(name)

        if unit!=None:
            if "*" in unit or "?" in unit:
                sql+= ' and unit like %s '
                unit=_wildcardformat(unit)
            else:
                sql+= ' and unit = %s '
            vals.append(unit)
            

        if description!=None:
            if "*" in description or "?" in description:
                sql+= ' and description like %s '
                description=_wildcardformat(description)
            else:
                sql+= ' and description = %s '
            vals.append(description)
            
        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching active interlock property type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise
            
        labels = ['id', 'name', 'unit', 'description', 'date']
        resdict = {'label': labels}

        results = []
        for _ in range(len(labels)):
            results.append([])
        
        for r in res:
            for i in range(len(labels)):
                if i == 4:
                    results[i].append(r[i].isoformat())
                else:
                    results[i].append(r[i])

        for i in range(len(labels)):
            resdict[labels[i]]=results[i]
        
        return resdict
        
    def saveactiveinterlockproptype(self, name, unit=None, description=None):
        '''Each involved in active interlock system has some properties like offset, AIHOL/AIVOL, AIHAL/AIVAL, safe current, and so on.
        This method is to save active interlock property type information with given name, unit, and/or description.
        
        The property name with given unit is unique in the database. It allows user to reuse a property type name, but given it 
        a different unit.
        
        :param name: property type name.
        :type name: str
        
        :param unit: unit of given property type.
        :type unit: str
        
        :param description: description of given property type.
        :type description: str
        
        :returns: internal property type id
            
        :raises: MySQLError, ValueError
        
        '''
        res = self.retrieveactiveinterlockproptype(name, unit=unit)
        emptyproptype=False
        for lbs in res['label']:
            if len(res[lbs]) > 0:
                emptyproptype=True
        if emptyproptype:
            raise ValueError('Active interlock property type (name: %s, unit: %s) exists already.'%(name, unit))

        sql = '''insert into active_interlock_prop_type
        (name, unit, description, created_date)
        values (%s, %s, %s, now())
        '''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (name, unit, description))
            
            # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
            # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
            # it is per connection.
            proptypeid = cur.lastrowid
            if self.transaction == None:
                self.conn.commit()
        except MySQLError as e:
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when saving active interlock property type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise
        return proptypeid
            
    def retrieveactiveinterlocklogic(self, name, shape=None, logic=None):
        '''Retrieve logic information according given search constrains.
        Active interlock envelop name has to be provided as a minimum requirement for this function.
        
        Wildcast matching is supported for name and shape with:
        
            - ``*`` for multiple characters match, 
            - ``?`` for single character match.

        Wildcast is not supported for logic since the * is a math symbol.

        :param name: active interlock envelop name.
        :type name: str
        
        :param shape: active interlock shape name in phase space.
        :type shape: str
        
        :param logic: active interlock logic.
        :type logic: str
        
        :returns: dict 
            
            A python dictionary is return with each field as an list which could be converted into a table. Its structure is as below:
            
            .. code-block:: python
            
                {'label':  [], # str, column's name
                 'id':     [], # int, internal id of active interlock logic
                 'name':   [], # str, name of active interlock envelop 
                 'shape':  [], # str, allowed envelop shape in phase space
                 'logic':  [], # str, logic expression
                 'code':   [], # int, logic code for hardware convenience
                 'author': [], # str, who created this entry
                 'date':   [], # datetime, when this entry was created
                }
        
        :raises: MySQLError
        
        '''
        sql = '''select active_interlock_logic_id, name, shape, logic, logic_code, created_by, created_date
        from active_interlock_logic where name
        '''
        vals=[]
        if "*" in name or "?" in name:
            sql+= ' like %s '
            name=_wildcardformat(name)
        else:
            sql+= ' = %s '
        vals.append(name)

        if shape!=None:
            if "*" in shape or "?" in shape:
                sql+= ' and shape like %s '
                shape=_wildcardformat(shape)
            else:
                sql+= ' and shape = %s '
            vals.append(shape)
            
        if logic!=None:
            # wildmatch is supported for logic since the * is a math symbol.
            sql+= ' and logic = %s '
            vals.append(logic)
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching active interlock logic:\n%s (%d)' %(e.args[1], e.args[0]))
            raise
            #raise Exception('Error when fetching active interlock logic:\n%s (%d)' %(e.args[1], e.args[0]))
    
        labels=['id', 'name', 'shape', 'logic', 'code', 'author', 'date']
        resdict = {'label': labels}
        
        results = []
        for _ in range(len(labels)):
            results.append([])
        
        for r in res:
            for i in range(len(labels)):
                if i == 6:
                    results[i].append(r[i].isoformat())
                else:
                    results[i].append(r[i])

        for i in range(len(labels)):
            resdict[labels[i]]=results[i]
        
        return resdict
    
    
    def saveactiveinterlocklogic(self, name, shape, logic, logiccode, author=None):
        '''Save logic information for active interlock system.
        The time is automatically captured when the data is saved into RDB.
        
        It checks whether given envelop name with given phase space shape and logic exists. If yes, it raises a ValueError exception.
        
        Currently implementation assumes that an active interlock envelop is for a particular shap, which is unique globally. 
        If logic is changed, a new name should be defined.
        
        :param name: active interlock envelop name
        :type name: str
        
        :param shape: active interlock shape name in phase space
        :type shape: str
        
        :param logic: active interlock logic expression
        :type logic: str
        
        :param logiccode: logic algorithm encoding code for hardware convenience
        :type logiccode: int

        :param author: who creates this data set
        :type author: str
            
        :returns: internal id of active interlock logic
                
        :Raises: ValueError, MySQLError
        
        '''
        
        # here logic code should be configured in system configure file, and user configurable.
        # allowed logic code should be checked here.
        # It will be added in next implementation.
        
        res = self.retrieveactiveinterlocklogic(name, shape=shape, logic=logic)
        emptylogic=False
        for lbs in res['label']:
            if len(res[lbs]) > 0:
                emptylogic=True
        if emptylogic:
            # it means entry exists already.
            # raise an error
            self.logger.info('Entry exists already for active interlock logic (name: %s, shape: %s, logic: %s)' %(name, shape, logic))
            raise ValueError('Entry exists already for active interlock logic (name: %s, shape: %s, logic: %s)' %(name, shape, logic))
        
        if author == None:
            sql = '''insert into active_interlock_logic
            (name, shape, logic, logic_code, created_date)
            values
            (%s, %s, %s, %s, now())
            '''
        else:
            sql = '''insert into active_interlock_logic
            (name, shape, logic, logic_code, created_by, created_date)
            values
            (%s, %s, %s, %s, %s, now())
            '''

        try:
            cur=self.conn.cursor()
            if author == None:
                cur.execute(sql, (name, shape, logic, logiccode))
            else:
                cur.execute(sql, (name, shape, logic, logiccode, author))
            # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
            # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
            # it is per connection.
            logicid = cur.lastrowid
            if self.transaction == None:
                self.conn.commit()
        except MySQLError as e:
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when saving active interlock logic:\n%s (%d)' %(e.args[1], e.args[0]))
            raise
        return logicid

