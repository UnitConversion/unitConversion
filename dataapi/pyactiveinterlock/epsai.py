""" 
Created on Aug 15, 2013

@author: shengb

"""

import logging
import MySQLdb

from collections import OrderedDict

from utils import (_wildcardformat, _checkParameter, _checkWildcardAndAppend, _generateUpdateQuery)

from _mysql_exceptions import MySQLError

try:
    from django.utils import simplejson as json
except ImportError:
    import json

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
        
        self.returnDateFormat = "%Y-%m-%d %H:%M:%S"
        
        # use django transaction manager
        self.transaction = transaction
        
        # Define all the properties for id table
        self.id_props = [['cell', '', ''], ['type', '', ''], ['set', '', ''], ['str_sect', '', ''], ['orientation', '', ''], ['logic_name', '', ''], ['shape', '', ''], ['defined_by', '', ''], ['device_name', '', ''], ['pos', 'm', ''], ['pos_from_cent', 'm', ''], ['max_offset', 'mm', ''], ['max_angle', 'mrad', ''], ['extra_offset', '', ''], ['lat_pos_s1', 'm', ''], ['pos_from_cent_s1', 'm', ''], ['offset_s1', 'mm', ''], ['logic_1', '', ''], ['lat_post_s2', 'm', ''], ['pos_from_cent_s2', 'm', ''], ['offset_s2', 'mm', ''], ['lat_pos_s3', 'm', ''], ['pos_from_cent_s3', 'm', ''], ['offset_s3', 'mm', ''], ['logic_2', '', ''], ['angle', 'mrad', '']]
        
        # Define all the properties for the bm table
        self.bm_props = [['bm_cell', '', ''], ['bm_type', '', ''], ['bm_s', 'm', 'approvable'], ['bm_logic_x', '', ''], ['bm_aiolh', 'mm', 'approvable'], ['bm_logic_y', '', ''], ['bm_aiolv', 'mm', 'approvable']]
        
        
    def retrieveActiveInterlockOld(self, status, datefrom=None, dateto=None, withdata=True):
        '''Retrieve a data set according its saved time, and status.
        One data set should have same properties for all device although its value could be empty.
        
        data structure:
        
        .. code-block:: python
        
            {id: {
                  'status': ,
                  'description': , 
                  'created_by': ,
                  'created_date': ,
                  'modified_by': ,
                  'modified_date': ,
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
        
        :Returns: dict
            
        :Raises: KeyError, AttributeError
        
        '''
        
        if withdata:
            return self._retrieveDataSet(status, datefrom=datefrom, dateto=dateto)
        
        else:
            return self._retrieveDataHeader(status, datefrom=datefrom, dateto=dateto)

    def _retrieveDataHeader(self, status, datefrom=None, dateto=None):
        '''Retrieve data set header information only.'''
        
        sql = '''
        select ai.active_interlock_id, ai.status, ai.description, 
        ai.created_by, ai.created_date, ai.modified_by, ai.modified_date
        from active_interlock ai
        where
        '''

        vals=[]
        
        # Append name
        sqlVals = _checkWildcardAndAppend('ai.status', status, sql, vals)
        sql = sqlVals[0]
        vals = sqlVals[1]
        
        # Append date from
        if datefrom != None:
            sql+= ' AND ai.created_date >= %s '
            vals.append(datefrom)
            
        # Append date to
        if dateto != None:
            sql+= ' AND ai.created_date <= %s '
            vals.append(dateto)
        
        try:
            # Execute sql
            cur=self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
            
            resdict = {}
            
            # Generate return dictionary
            for r in res:
                tmp = {'status': r[1]}
                
                if r[2] != None:
                    tmp['description'] = r[2]
                
                if r[3] != None:
                    tmp['created_by'] = r[3]
                
                if r[4] != None:
                    tmp['created_date'] = r[4].strftime(self.returnDateFormat)
                
                if r[5] != None:
                    tmp['modified_by'] = r[5]
                
                if r[6] != None:
                    tmp['modified_date'] = r[6].strftime(self.returnDateFormat)

                resdict[r[0]] = tmp
    
            return resdict
            
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching active interlock data set headers:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching active interlock data set headers:\n%s (%d)' %(e.args[1], e.args[0]))
    
    def _retrieveDataSet(self, status, datefrom=None, dateto=None):
        '''Retrieve data set'''
        
        res = self._retrieveDataHeader(status, datefrom=datefrom, dateto=dateto)
        
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
                label=['name', 'definition', 'logic_name', 'shape', 'logic', 'logic_code']
                units=['', '', '', '', '', '']
    
                innerdata = OrderedDict(
                    (
                        ('label', label),
                        ('units', units),
                        ('name', []),
                        ('definition', []),
                        ('logic_name', []),
                        ('shape', []),
                        ('logic', []),
                        ('logic_code', []),
                    )
                )
                
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
            
            return res

        except MySQLdb.Error as e:
            self.logger.info('Database error when fetching active interlock data set:\n%s (%d)' %(e.args[1], e.args[0]))
            raise
        
        except KeyError as e:
            self.logger.info('Data set error when fetching active interlock data set:\n%s (%d)' %(e.args[1], e.args[0]))
            raise e

    
    def saveActiveInterlock(self, data, description=None, created_by=None):
        '''
        Save a new data set of active interlock.
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
        
        :param active: set current data set active. It sets new data set as active by default unless it is explicitly set to keep old active data set.
        :type active: boolean
        
        :param created_by: the person who set this data set.
        :type created_by: str
        
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
                
                tmp = self.retrieveActiveInterlockPropType(proptypes[i], unit=proptypeunits[i])
                tmpKeys = tmp.keys()
                tmpObject = tmp[tmpKeys[0]]
                
                if len(tmp) == 0:
                    # should add a new entry
                    proptypeids[proptypes[i]] = self.saveActiveInterlockPropType(proptypes[i], unit=proptypeunits[i])
                
                elif len(tmp) == 1:
                    proptypeids[proptypes[i]] = tmpObject['id']
                
                else:
                    raise ValueError('property type (name: %s, unit: %s) is not unique.'%(proptypes[i], proptypeunits[i]))
            
            # Get active interlock logic internal id
            logicids=[]
            
            proptypes_tmp = proptypes[:]
            
            # Check if logic name is present
            if 'logic_name' in proptypes_tmp: 
                proptypes_tmp.remove('logic_name')
                
            else:
                raise ValueError('active interlock logic is not defined.')
            
            # Check if shape is present
            if 'shape' in proptypes_tmp: 
                proptypes_tmp.remove('shape')
            
            else:
                raise AttributeError('active interlock allowed shape in phase space is not defined.')

            # Retrieve logic
            for i in range(len(data['logic_name'])):
                
                tmp = self.retrieveActiveInterlockLogic(data['logic_name'][i], data['shape'][i])
                tmpKeys = tmp.keys()
                tmpObject = tmp[tmpKeys[0]]
                
                if len(tmp) != 1:
                    raise AttributeError('Given activeinterlock envelop (name: %s, shape: %s) does not exist yet.'%(data['logicname'][i], data['shape'][i]))
                
                else:
                    logicids.append(tmpObject['id'])

            # Save header onformation of a active interlock data set
            sql = '''
            INSERT INTO active_interlock (created_date, status, created_by, description) VALUES (NOW(), 0, %s, %s)
            '''
            
            cur.execute(sql, (created_by, description))
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
        
    def updateActiveInterlockStatusOld(self, aiid, status, created_by=None):
        '''
        Update status of a data set.
        
        Current statuses:
        
            0: editable
            1: approved
            2: active
            3: backup
            4: history
        
        :param aiid: internal id of an active interlock data set
        :type aiid: int
        
        :param status: new status code
        :type status: int
        
        :param created_by: name who requests this update
        :type created_by: str
            
        :Returns: boolean
            
            The return code: ::
                
                True -- when the status is changed.
                False -- when the status is not changed.
        
        :Raises: MySQLError, ValueError, AttributeError
        '''
        
        # Check status value
        if status not in [0, 1, 2, 3, 4]:
            raise ValueError('Status of active interlock data has to be either 0, 1, 2, 3 or 4.')

        # Set new status variable for existing datasets
        new_status = status + 1
        
        if new_status > 4:
            new_status = 4

        try:
            cur=self.conn.cursor()
            
            # Get current status
            cur.execute('''select status from active_interlock where active_interlock_id = %s''', (aiid,))
            aiid_status = cur.fetchone()
            
            if aiid_status == None:
                raise ValueError("Given internal id (%s) of active interlock data set does not exist!"%(aiid))
            
            aiid_status = aiid_status[0]
            
            # If old and new status of a dataset is the same, do nothing
            # Nothing to do since status is same for that particular data set
            if aiid_status == status:
                return False
            
            # Get current datadata set with that status
            cur.execute('''select active_interlock_id from active_interlock where status = %s''' , (status))
            active_id = cur.fetchone()
            
            if len(active_id) != 0:
                # find active data set, has to deactivate it before setting a new active data set.
                active_id = active_id[0]
            
                sql = '''update active_interlock set status=%s, modified_by=%s, modified_date=now() where active_interlock_id = %s'''
                cur.execute(sql, (new_status, created_by, active_id,))

            sql = '''update active_interlock set status=%s, modified_by=%s, modified_date=now() where active_interlock_id = %s'''
            cur.execute(sql, (status, created_by, aiid))
            
            # Commit changes
            if self.transaction == None:
                self.conn.commit()
                
            return True
                
        except MySQLError as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when updating active interlock data status:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating active interlock data status:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateActiveInterlockStatus(self, ai_id, status, new_status):
        '''
        Update status of a data set.
        
        Current statuses:
        
            0: editable
            1: approved
            2: active
            3: backup
            4: history
        
        :param aiid: internal id of an active interlock data set
        :type aiid: int
        
        :param status: new status code
        :type status: int
        
        :param created_by: name who requests this update
        :type created_by: str
            
        :Returns: boolean
            
            The return code: ::
                
                True -- when the status is changed.
                Exception -- when there was an error.
        
        :Raises: MySQLError, ValueError
        '''
        
        # Convert
        new_status = int(new_status)
        
        # Check that id or status is set
        if ai_id == None and status == None:
            raise ValueError("Id or status should be provided to update status!")
        
        # Get active interlock id from status
        if status != None and ai_id == None:
            ai = self.retrieveActiveInterlockHeader(status)
            aiKeys = ai.keys()
            
            # If there is no dataset with this status, return True
            if len(aiKeys) == 0:
                return True
            
            aiObj = ai[aiKeys[0]]
            ai_id = aiObj['id']
        
        # Move statuses
        if new_status >= 2 and new_status < 4:
            return self.updateActiveInterlockStatus(ai_id, None, new_status + 1)
        
        # Delete dataset that currently has this status
        if new_status == 0 or new_status == 1:
            self.deleteDevice(new_status)
            #self.updateActiveInterlockStatus(None, new_status, -1)
        
        # Define query dict
        queryDict = {}
        whereDict = {}
        
        # Set status
        queryDict['status'] = new_status
        
        # Set where
        whereDict['active_interlock_id'] = ai_id
        
        # Generate SQL
        sqlVals = _generateUpdateQuery('active_interlock', queryDict, None, None, whereDict)
        print sqlVals
        
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
            
            self.logger.info('Error when updating active interlock status:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating active interlock status:\n%s (%d)' % (e.args[1], e.args[0]))

    def saveDeviceProperties(self):
        '''
        When creating new active interlock for the first time, create all needed properties
        '''
        
        # Get current properties
        propTypes = self.retrieveActiveInterlockPropType('*')
        
        # If table is empty, add properties in it
        if len(propTypes) == 0:
            
            # Save all id properties into the database
            for prop in self.id_props:
                self.saveActiveInterlockPropType(prop[0], prop[1])
            
            # Save all bm properties into the database
            for prop in self.bm_props:
                self.saveActiveInterlockPropType(prop[0], prop[1], prop[2])
        
    def retrieveActiveInterlockProp(self, aid_id, prop_type_name):
        '''
        Retrieve properties of the active interlock device
        
        :param aid_id: active interlock device id
        :type aid_id: int
        
        :param prop_type_name: active interlock property  type name
        :type prop_type_name: str
        
        :returns dict
            {'id':
                'id':            , #int, property id
                'aid_id':        , #int, active interlock device id
                'value':         , #str, property value
                'status':        , #int, property status
                'date':          , #str, date property was set
                'name':          , #str, name of the property type
                'description':   , #str, description of the property type
                'unit':          , #str, property unit
            }
        '''
        
        # Check active interlock device id
        _checkParameter('active interlock device id', aid_id, 'prim')
        
        # Check property type name
        _checkParameter('prop type name', prop_type_name)
        
        # Generate SQL statement
        sql = '''
        SELECT
            aip.active_interlock_prop_id,
            aip.value,
            aip.status,
            aip.date,
            aipt.name,
            aipt.description,
            aipt.unit
        FROM active_interlock_prop aip
        LEFT JOIN active_interlock_prop_type aipt ON(aip.active_interlock_prop_type_id = aipt.active_interlock_prop_type_id)
        WHERE
        '''
        
        vals = []
        
        # Append active interlock id
        sql += " aip.active_interlock_device_id = %s "
        vals.append(aid_id)
        
        # Append property type name
        sqlVals = _checkWildcardAndAppend('aipt.name', prop_type_name, sql, vals, 'AND')
        
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
                    'aid_id': aid_id,
                    'value': r[1],
                    'status': r[2],
                    'date': r[3].strftime(self.returnDateFormat),
                    'name': r[4],
                    'description': [5],
                    'unit': r[6]
                }

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching active interlock property:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching active interlock property:\n%s (%d)' %(e.args[1], e.args[0]))
        
    def saveActiveInterlockProp(self, aid_id, prop_type_name, value):
        '''
        Save active interlock property into database. Property type must exist before saving property value
        '''
        
        # Check active interlock device id
        _checkParameter('active interlock device id', aid_id, 'prim')
        
        # Retrieve property type name
        existingPropType = self.retrieveActiveInterlockPropType(prop_type_name)
        
        # Check if property type exists in the database
        if len(existingPropType) == 0:
            raise ValueError("Active interlock property type (%s) doesn't exist in the database!" % prop_type_name)
        
        propTypeKeys = existingPropType.keys()
        propTypeObject = existingPropType[propTypeKeys[0]]
        
        # Set status
        status = 0
        
        if propTypeObject['description'] == 'approvable':
            status = 2
        
        sql = '''
        INSERT INTO active_interlock_prop (active_interlock_device_id, active_interlock_prop_type_id, value, status, date)
        VALUES
        (%s, %s, %s, %s, NOW())
        '''

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sql, (aid_id, propTypeObject['id'], value, status))

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

            self.logger.info('Error when saving active interlock property:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving active interlock property:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateActiveInterlockProp(self, aid_id, prop_type_name, value):
        '''
        Update active interlock property in the database. Property type must exist before saving property value
        
        :param ai_id: active interlock id
        :type ai_id: int
        
        :param prop_type_name: name of the property type
        :type prop_type_name: str
        
        :param value: value of the property
        :type value: str
        
        :returns boolean or Exception
            True if everything is ok
        
        :raises
            MySQLError, ValueError
        '''
        
        # Define query dict
        queryDict = {}
        whereDict = {}
        
        # Check property type
        proptype = self.retrieveActiveInterlockPropType(prop_type_name)
        
        if len(proptype) == 0:
            raise ValueError("Property type (%s) doesn't exist in the database!" % prop_type_name)
        
        typeKeys = proptype.keys()
        typeObject = proptype[typeKeys[0]]
        whereDict['active_interlock_prop_type_id'] = typeObject['id']
        
        # Set status to unapproved if property is approvable
        if typeObject['description'] == 'approvable':
            queryDict['status'] = 2
        
        # Check active interlock device id
        _checkParameter('active interlock device id', aid_id, 'prim')
        whereDict['active_interlock_device_id'] = aid_id
        
        # Set value parameter
        queryDict['value'] = value
        
        # Generate SQL
        sqlVals = _generateUpdateQuery('active_interlock_prop', queryDict, None, None, whereDict)
        
        try:
            # Insert ai property data into database
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

            self.logger.info('Error when updating active interlock property:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when updating active interlock property:\n%s (%d)' %(e.args[1], e.args[0]))

    def approveCells(self, aid_id, prop_types):
        '''
        Approve cells passed in the props list. Status of the properties will be changed
        from unapproved (2) to approved (3)
        
        :param aid_id: active interlock device id
        :type int
        
        :param props: list of property type names that should be updated
        :type list
        
        :returns
            True if everything is ok or exception
        '''
        
        # Define query dict
        queryDict = {}
        whereDict = {}
        
        # Check active interlock device id
        _checkParameter('active interlock device id', aid_id, 'prim')
        whereDict['active_interlock_device_id'] = aid_id
        
        try:
            
            # Convert to json
            if isinstance(prop_types, (dict)) == False:
                prop_types = json.loads(prop_types)
            
            # Go through all of the properties
            for prop in prop_types:
                # Check property type
                proptype = self.retrieveActiveInterlockPropType(prop)
                
                if len(proptype) == 0:
                    raise ValueError("Property type (%s) doesn't exist in the database!" % prop)
                
                typeKeys = proptype.keys()
                typeObject = proptype[typeKeys[0]]
                whereDict['active_interlock_prop_type_id'] = typeObject['id']
                
                # Set status parameter
                queryDict['status'] = 3
                
                # Generate SQL
                sqlVals = _generateUpdateQuery('active_interlock_prop', queryDict, None, None, whereDict)
                
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
            
            self.logger.info('Error when updating active interlock device property:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating active interlock device property:\n%s (%d)' % (e.args[1], e.args[0]))


    def retrieveDevice(self, ai_id, ai_status, name, definition):
        '''
        Retrieve devices of particular active interlock, name and definition. Name can also be a wildcard
        character to select all devices.
        
        :param ai_id: active interlock id
        :type ai_id: int
        
        :param ai_status: active interlock status
        :type ai_status: int
        
        :param name: device name
        :type name: str
        
        :param definition: type of the dataset (bm/id)
        :type definition: str
        
        :returns: dict 
            
            .. code-block:: python
            
            {'id':
                {'id':              , #int, id of the device in the database
                 'ai_id':           , #int, id of the active interlock
                 'name':            , #str, name of the device
                 'definition':      , #str, definition of the device
                 'logic':           , #str, name of the logic
                 'prop1key':        , #str, first property
                 ...
                 'propNkey':        , #str, Nth property
                 'prop_statuses': {
                         'prop1key': , #int, status of the property,
                         ...
                         'propNkey': , #int, status of the property
                     }
                }
            }
        
        '''
        
        # Check that status or id is set
        if ai_status == None and ai_id == None:
            raise ValueError("Status or id must be provided to retrieve device from the database!")
        
        
        # Check active interlock id
        if ai_id != None:
            _checkParameter('active interlock id', ai_id, 'prim')
        
        # Check status
        if ai_status != None:
            _checkParameter('active interlock status', ai_status, 'prim')
            
            if ai_id == None:
                ai = self.retrieveActiveInterlockHeader(ai_status)
                aiKeys = ai.keys()
                
                # Check the number of active interlocks
                if len(aiKeys) == 0:
                    return {}
                
                aiObject = ai[aiKeys[0]]
                ai_id = aiObject['id']
        
        # Check name
        _checkParameter('name', name)
        
        # Check definition
        _checkParameter('definition', definition)
        
        # Generate SQL statement
        vals = []
        sql = '''
        SELECT
            aid.active_interlock_device_id,
            aid.device_name,
            aid.definition,
            ail.name,
            aid.active_interlock_id
        FROM active_interlock_device aid
        LEFT JOIN active_interlock_logic ail ON(aid.active_interlock_logic_id = ail.active_interlock_logic_id)
        WHERE
        '''
        
        # Append active interlock id
        sql += " aid.active_interlock_id = %s "
        vals.append(ai_id)
        
        # Append device name
        sqlVals = _checkWildcardAndAppend('aid.device_name', name, sql, vals, 'AND')
        
        # Append definition
        sqlVals = _checkWildcardAndAppend('aid.definition', definition, sqlVals[0], sqlVals[1], 'AND')
        
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
                    'ai_id': r[4],
                    'name': r[1],
                    'definition': r[2],
                    'logic': r[3],
                    'prop_statuses': {}
                }
                
                # Retrieve properties
                prop = self.retrieveActiveInterlockProp(r[0], '*')
                propKeys = prop.keys()
                
                for key in propKeys:
                    resdict[r[0]][prop[key]['name']] = prop[key]['value']
                    resdict[r[0]]['prop_statuses'][prop[key]['name']] = prop[key]['status']

            return resdict

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching active interlock device:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching active interlock device:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveDevice(self, ai_status, name, definition, logic, props):
        '''
        Save new device into database
        
        :param ai_id: active interlock id
        :type ai_id: int
        
        :param ai_status: active interlock status
        :type ai_status: int
        
        :param name: active interlock device name
        :type name: str
        
        :param definition: definition of device. It can be bm (bending magnet) or id (insertion device)
        :type definition: str
        
        :param logic: name of the logic that has t be saved in the database
        :type logic: str
        
        :return
         {'id': id of the saved device}
        '''
        
        ai_id = None
        
        # Check that status or id is set
        if ai_status == None and ai_id == None:
            raise ValueError("Status or id must be provided to retrieve device from the database!")
        
        # Check active interlock id
        if ai_id != None:
            _checkParameter('active interlock id', ai_id, 'prim')
        
        # Check status
        if ai_status != None:
            _checkParameter('active interlock status', ai_status, 'prim')
            
            if ai_id == None:
                ai = self.retrieveActiveInterlockHeader(ai_status)
                aiKeys = ai.keys()
                aiObject = ai[aiKeys[0]]
                ai_id = aiObject['id']
        
        # Check name
        _checkParameter('name', name)
        
        # Check definition
        _checkParameter('definition', definition)
        
        # Get logic
        logic = self.retrieveActiveInterlockLogic(logic)
        
        if len(logic) == 0:
            raise ValueError("Logic (%s) doesn't exist in the database!" % logic)

        logicKeys = logic.keys()
        logicObject = logic[logicKeys[0]]
        
        # Generate SQL statement
        sql = '''
        INSERT INTO active_interlock_device (active_interlock_id, active_interlock_logic_id, device_name, definition)
        VALUES (%s, %s, %s, %s)
        '''

        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sql, (ai_id, logicObject['id'], name, definition))

            # Get last row id
            deviceid = cur.lastrowid

            # Convert to json
            if isinstance(props, (dict)) == False:
                props = json.loads(props)

            # Save properties
            for datum in props:
                value = props[datum]
                
                self.saveActiveInterlockProp(deviceid, datum, value)

            # Create transaction
            if self.transaction == None:
                self.conn.commit()

            return {'id': deviceid}

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving active interlock device:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving active interlock device:\n%s (%d)' %(e.args[1], e.args[0]))

    def updateDevice(self, aid_id, name = None, logic = None):
        '''
        Update device's name and logic
        
        :param aid_id: active interlock device id
        :type int
        
        :param name: device name
        :type string
        
        :param logic: device logic name
        :type string
        
        :return
            True if everything is ok
        '''
        
        # Define query dict
        queryDict = {}
        whereDict = {}
        
        # Check if there is something to update
        if name == None and logic == None:
            raise ValueError("There is nothing to update!")
        
        # Check logic
        if logic != None:
            retrieveLogic = self.retrieveActiveInterlockLogic(logic)
            
            if len(retrieveLogic) == 0:
                raise ValueError("There is no logic (%s) in the database!" % logic)
            
            logicKeys = retrieveLogic.keys()
            logicObj = retrieveLogic[logicKeys[0]]
            queryDict['active_interlock_logic_id'] = logicObj['id']
        
        # Set where
        whereDict['active_interlock_device_id'] = aid_id
        
        # Set name
        if name != None:
            queryDict['device_name'] = name
            
        # Generate SQL
        sqlVals = _generateUpdateQuery('active_interlock_device', queryDict, None, None, whereDict)
        
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
            
            self.logger.info('Error when updating active interlock device:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error when updating active interlock device:\n%s (%d)' % (e.args[1], e.args[0]))

    def deleteDevice(self, status):
        '''
        Delete active interlock device by its id
        
        :param status: active interlock status
        :type int
        
        :returns
            True if everything is ok
        '''
        
        # Get active interlock id with specific status
        ai = self.retrieveActiveInterlockHeader(status)
        aiKeys = ai.keys()
        
        # Check the length of the list
        if len(aiKeys) == 0:
            return {}
        
        aiObj = ai[aiKeys[0]]
        
        ai_id = aiObj['id']
        
        # Delete properties
        sqlP = '''
        DELETE FROM active_interlock_prop WHERE
        active_interlock_device_id IN (
            SELECT active_interlock_device_id
            FROM active_interlock_device
            WHERE active_interlock_id = %s
        );
        '''
        
        # Delete active interlock header
        sqlH = '''
        DELETE FROM active_interlock
        WHERE active_interlock_id = %s
        '''
        
        # Delete devices
        sqlD = '''
        DELETE FROM active_interlock_device
        WHERE active_interlock_id = %s
        '''
        
        try:
            cur = self.conn.cursor()
            cur.execute(sqlP, ai_id)
            cur.execute(sqlD, ai_id)
            cur.execute(sqlH, ai_id)

            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return True
            
        except MySQLdb.Error as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error while deleting active interlock:\n%s (%d)' % (e.args[1], e.args[0]))
            raise MySQLError('Error while deleting active interlock:\n%s (%d)' % (e.args[1], e.args[0]))


    def retrieveStatusInfo(self):
        '''
        Retrieve information about active interlock statuses. How many datasets are in each status.
        
        :returns dict
        {'status':
            {
                'status':, #int
                'num':     #int
            }
        }
        '''
        
        resdict = {}
        
        # Retrieve 0 status
        zero = self.retrieveActiveInterlockHeader(status=0)
        
        resdict[0] = {
            'status': 0,
            'num': len(zero)
        }
        
        # Retrieve 1 status
        one = self.retrieveActiveInterlockHeader(status=1)
        
        resdict[1] = {
            'status': 1,
            'num': len(one)
        }
        
        # Retrieve 2 status
        two = self.retrieveActiveInterlockHeader(status=2)
        
        resdict[2] = {
            'status': 2,
            'num': len(two)
        }
        
        # Retrieve 3 status
        three = self.retrieveActiveInterlockHeader(status=3)
        
        resdict[3] = {
            'status': 3,
            'num': len(three)
        }
        
        # Retrieve 4 status
        four = self.retrieveActiveInterlockHeader(status=4)
        
        resdict[4] = {
            'status': 4,
            'num': len(four)
        }
        
        return resdict

    def retrieveActiveInterlockHeader(self, status=None, id=None, datefrom=None, dateto=None):
        '''
        Retrieve a data set according its saved time, status or id.
        
        :param status: Current status.
        :type status: int
        
        :param id: Id in the database.
        :type id: int
        
        :param datefrom: data saved after this time. Default is None, which means data from very beginning. It has format as **yyyy-MM-dd hh:mm:ss** since dates in MySql are represented with the format.
        :type datafrom: datetime
        
        :param dateto: data saved before this time. Default is None, which means data till current. It has format as **yyyy-MM-dd hh:mm:ss** since dates in MySql are represented with the format.
        :type datato: datetime
        
        :param withdata: get data set. Default is true, which means always gets data by default. Otherwise, only device names are retrieved for desired data set.
        :type withdata: boolean
        
        :Returns: dict
        
         {'id'; {
                 'status':,.
                 'id':,
                 'description':,
                 'created_by':,
                 'created_date':,
                 'modified_by':,
                 'modified_date':
             }
         }
            
        :Raises: KeyError, AttributeError
        
        '''
        
        sql = '''
        select ai.active_interlock_id, ai.status, ai.description, 
        ai.created_by, ai.created_date, ai.modified_by, ai.modified_date
        from active_interlock ai
        where
        '''

        vals=[]
        
        # Check that status or id is set
        if status == None and id == None:
            raise ValueError("Status or id must be provided to retrieve active interlock header from the database!")
        
        # Append status
        if status != None:
            sqlVals = _checkWildcardAndAppend('ai.status', status, sql, vals)
            sql = sqlVals[0]
            vals = sqlVals[1]
            
        # Append id
        if id != None:
            sqlVals = _checkWildcardAndAppend('ai.active_interlock_id', id, sql, vals)
            sql = sqlVals[0]
            vals = sqlVals[1]
        
        # Append date from
        if datefrom != None:
            sql+= ' AND ai.created_date >= %s '
            vals.append(datefrom)
            
        # Append date to
        if dateto != None:
            sql+= ' AND ai.created_date <= %s '
            vals.append(dateto)
        
        try:
            # Execute sql
            cur=self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
            
            resdict = {}
            
            # Generate return dictionary
            for r in res:
                tmp = {'status': r[1]}
                
                tmp['id'] = r[0]
                
                if r[2] != None:
                    tmp['description'] = r[2]
                
                if r[3] != None:
                    tmp['created_by'] = r[3]
                
                if r[4] != None:
                    tmp['created_date'] = r[4].strftime(self.returnDateFormat)
                
                if r[5] != None:
                    tmp['modified_by'] = r[5]
                
                if r[6] != None:
                    tmp['modified_date'] = r[6].strftime(self.returnDateFormat)

                resdict[r[0]] = tmp
    
            return resdict
            
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching active interlock data set headers:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching active interlock data set headers:\n%s (%d)' %(e.args[1], e.args[0]))

    def saveActiveInterlockHeader(self, description=None, created_by=None):
        '''
        Save a new data set of active interlock.
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
        
        :param active: set current data set active. It sets new data set as active by default unless it is explicitly set to keep old active data set.
        :type active: boolean
        
        :param created_by: the person who set this data set.
        :type created_by: str
        
        :Returns: active interlock internal id if saved successfully.
            
        :Raises: ValueError, MySQLError, KeyError, AttributeError 

        '''
        
        # Check for created by parameter
        _checkParameter('author', created_by)
        
        # Create property types if there are none
        self.saveDeviceProperties()
        
        # Save header onformation of a active interlock data set
        sql = '''
        INSERT INTO active_interlock (created_date, status, created_by, description) VALUES (NOW(), 0, %s, %s)
        '''
        
        try:
            # Execute sql
            cur = self.conn.cursor()
            cur.execute(sql, (created_by, description))

            # Get last row id
            headerid = cur.lastrowid

            # Create transaction
            if self.transaction == None:
                self.conn.commit()

            return {'id': headerid}

        except MySQLdb.Error as e:

            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()

            self.logger.info('Error when saving active interlock header:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving active interlock header:\n%s (%d)' %(e.args[1], e.args[0]))

    def retrieveActiveInterlockPropType(self, name, unit=None, description=None):
        '''
        Each involved in active interlock system has some properties like offset, AIHOL/AIVOL, AIHAL/AIVAL, safe current, and so on.
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
            
                {'id: {'label':       [], # str, columns's name
                     'id':          [], # int, internal id of property type
                     'name':        [], # str, active interlock property type name 
                     'unit':        [], # str, active interlock property type unit
                     'description': [], # str, property type description
                     'date':        [], # datetime, when this entry was created
                    }
                }
        
        :raises: MySQLError, ValueError
        '''
        
        # Check name parameter
        _checkParameter('name', name)
        
        # Generate SQL statement
        vals = []
        sql = '''
        select active_interlock_prop_type_id, name, unit, description, created_date
        from active_interlock_prop_type where
        '''
        
        # Append name
        sqlVals = _checkWildcardAndAppend('name', name, sql, vals)

        # Append unit
        if unit != None:
            sqlVals = _checkWildcardAndAppend('unit', unit, sqlVals[0], sqlVals[1], 'AND')
            
        # Append description
        if description != None:
            sqlVals = _checkWildcardAndAppend('description', description, sqlVals[0], sqlVals[1], 'AND')
            
        try:
            # Execute SQL
            cur = self.conn.cursor()
            cur.execute(sqlVals[0], sqlVals[1])
            
            res = cur.fetchall()
            resdict = {}
            
            # Generate return dictionary
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'name': r[1],
                    'unit': r[2],
                    'description': r[3],
                    'date': r[4].strftime(self.returnDateFormat)
                }

            return resdict
        
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching active interlock property type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching active interlock property type:\n%s (%d)' %(e.args[1], e.args[0]))
        
    def saveActiveInterlockPropType(self, name, unit=None, description=None):
        '''
        Each involved in active interlock system has some properties like offset, AIHOL/AIVOL, AIHAL/AIVAL, safe current, and so on.
        This method is to save active interlock property type information with given name, unit, and/or description.
        
        The property name with given unit is unique in the database. It allows user to reuse a property type name, but given it 
        a different unit.
        
        :param name: property type name.
        :type name: str
        
        :param unit: unit of given property type.
        :type unit: str
        
        :param description: description of given property type.
        :type description: str
        
        :returns: {'id': internal property type id}
            
        :raises: MySQLError, ValueError
        '''
        
        # Check name parameter
        _checkParameter('name', name)
        
        # Try to retrieve existing property type
        existingPropType = self.retrieveActiveInterlockPropType(name, unit=unit)
        
        if len(existingPropType):
            raise ValueError("Active interlock property type (%s) with unit (%s) already exists in the database!" % (name, unit));

        sql = '''
        insert into active_interlock_prop_type
        (name, unit, description, created_date)
        values (%s, %s, %s, now())
        '''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (name, unit, description))
            
            # Get last row id
            proptypeid = cur.lastrowid
            
            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': proptypeid}
                
        except MySQLError as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when saving active interlock property type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving active interlock property type:\n%s (%d)' %(e.args[1], e.args[0]))
            
    def retrieveActiveInterlockLogic(self, name, shape=None, logic=None):
        '''
        Retrieve logic information according given search constrains.
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
            
            {'id':
                {'label':          [], # str, column's name
                 'id':             [], # int, internal id of active interlock logic
                 'name':           [], # str, name of active interlock envelop 
                 'shape':          [], # str, allowed envelop shape in phase space
                 'logic':          [], # str, logic expression
                 'code':           [], # int, logic code for hardware convenience
                 'created_by':     [], # str, who created this entry
                 'created_date':   [], # datetime, when this entry was created
                }
            }
        
        :raises: MySQLError, ValueError
        '''
        
        # Check name paramater
        _checkParameter('name', name)
        
        # Generate SQL
        vals = []
        sql = '''
        select active_interlock_logic_id, name, shape, logic, logic_code, created_by, created_date
        from active_interlock_logic where
        '''
        
        # Append name
        sqlVals = _checkWildcardAndAppend('name', name, sql, vals)
        sql = sqlVals[0]
        vals = sqlVals[1]

        # Append shape
        if shape != None:
            sqlVals = _checkWildcardAndAppend('shape', shape, sql, vals, 'AND')
            sql = sqlVals[0]
            vals = sqlVals[1]
            
        # Append logic
        if logic != None:
            # wildmatch is supported for logic since the * is a math symbol.
            sql += ' AND logic = %s '
            vals.append(logic)
        
        try:
            # Execure SQL
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
            resdict = {}
            
            # Generate return dictionary
            for r in res:
                resdict[r[0]] = {
                    'id': r[0],
                    'name': r[1],
                    'shape': r[2],
                    'logic': r[3],
                    'code': r[4],
                    'created_by': r[5],
                    'created_date': r[6].strftime(self.returnDateFormat)
                }

            return resdict
            
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching active interlock logic:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when fetching active interlock logic:\n%s (%d)' %(e.args[1], e.args[0]))
    
    def saveActiveInterlockLogic(self, name, shape=None, logic=None, code=None, created_by=None):
        '''
        Save logic information for active interlock system.
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
        
        :param code: logic algorithm encoding code for hardware convenience
        :type code: int

        :param created_by: who creates this data set
        :type created_by: str
            
        :returns: {'id': internal id of active interlock logic}
                
        :Raises: ValueError, Exception
        '''
        
        # here logic code should be configured in system configure file, and user configurable.
        # allowed logic code should be checked here.
        # It will be added in next implementation.
        
        # Check name parameter
        _checkParameter('name', name)
        
        existingLogic = self.retrieveActiveInterlockLogic(name, shape=shape, logic=logic)
        
        if len(existingLogic):
            raise ValueError("Active interlock logic (%s) already exists in the database!" % name);

        # Generate SQL statement
        sql = '''
        insert into active_interlock_logic
        (name, shape, logic, logic_code, created_by, created_date)
        values
        (%s, %s, %s, %s, %s, now())
        '''

        try:
            # Execute SQL
            cur=self.conn.cursor()
            cur.execute(sql, (name, shape, logic, code, created_by))
            
            # Return last row id
            logicid = cur.lastrowid
            
            # Create transaction
            if self.transaction == None:
                self.conn.commit()
                
            return {'id': logicid}
                
        except Exception as e:
            
            # Rollback changes
            if self.transaction == None:
                self.conn.rollback()
            
            self.logger.info('Error when saving active interlock logic:\n%s (%d)' %(e.args[1], e.args[0]))
            raise MySQLError('Error when saving active interlock logic:\n%s (%d)' %(e.args[1], e.args[0]))

