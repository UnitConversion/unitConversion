'''
This module is to interface with lattice table.

Created on Feb 28, 2013

@author: shengb
'''
import os
import errno
import datetime
from collections import OrderedDict
import tempfile

import logging
import MySQLdb

import base64

from utils import (_assemblesql, _wildcardformat)

from .tracyunit import elementpropunits as tracypropunits
from _mysql_exceptions import MySQLError

class lattice(object):
    def __init__(self, conn, transaction=None):
        ''''''
        self.logger = logging.getLogger('lattice')
        hdlr = logging.FileHandler('/var/tmp/lattice.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.WARNING)

        self.conn = conn
        # use django transaction manager
        self.transaction = transaction

    def retrievelatticeinfo(self, name, version=None, branch=None, description=None, latticetype=None, creator=None):
        '''
        retrieve lattice header information. It gives lattice name, description, version, branch, 
        created info (by who & when), updated info (by who & when)
        according given information.
        Real lattice data (geometric layout and strength can be retrieved thru retrievelattice())
        
        return: dictionary with format
                {'id': {'lattice name': ,            # identifier of this lattice
                        'version': ,                 # version of this lattice
                        'branch': ,                  # branch this lattice belongs to
                        'description':  [optional],  # lattice description
                        'creator':      [optional],  # who created this lattice first time
                        'originalDate': [optional],  # when this lattice was create first time
                        'updated':      [optional],  # who updated last time
                        'lastModified': [optional],  # when this lattice was updated last time
                        'latticeType':  [optional],  # lattice type name
                        'latticeFormat':[optional],  # lattice type format
                        }
                 ...
                } 
            supported lattice type name and format is as below:
            [{'name': 'plain', 'format': 'txt'},
             {'name': 'tracy3',  'format': 'lat'},
             {'name': 'tracy4',  'format': 'lat'},
             {'name': 'elegant', 'format': 'lte'},
             {'name': 'xal',     'format': 'xdxf'}
            ]
        '''
        sql = '''
        select lattice.lattice_id, lattice_name, lattice_version, lattice_branch, lattice_description, 
               created_by, create_date, 
               updated_by, update_date, 
               lattice_type_name, lattice_type_format,
               url
        from lattice 
        left join lattice_type on lattice_type.lattice_type_id = lattice.lattice_type_id
        where
        '''
        vals = []
        vals, sql = _assemblesql(sql, name, "lattice_name", vals)
        
        if version != None:
            if isinstance(version, (list, tuple)) and "" in version:
                vals, sql = _assemblesql(sql, "*", "lattice_version", vals, connector="and")
            else:
                vals, sql = _assemblesql(sql, version, "lattice_version", vals, connector="and")

        if branch != None:
            if isinstance(branch, (list, tuple)) and "" in branch:
                vals, sql = _assemblesql(sql, "*", "lattice_branch", vals, connector="and")
            else:
                vals, sql = _assemblesql(sql, branch, "lattice_branch", vals, connector="and")

        if description != None:
            if isinstance(description, (list, tuple)) and "" in description:
                vals, sql = _assemblesql(sql, "*", "lattice_description", vals, connector="and")
            else:
                vals, sql = _assemblesql(sql, description, "lattice_description", vals, connector="and")

        if creator != None:
            if isinstance(creator, (list, tuple)) and "" in creator:
                vals, sql = _assemblesql(sql, "*", "created_by", vals, connector="and")
            else:
                vals, sql = _assemblesql(sql, creator, "created_by", vals, connector="and")

        if latticetype != None and isinstance(latticetype, dict):
            if latticetype.has_key('name'):
                if isinstance(latticetype['name'], (list, tuple)) and "" in latticetype['name']:
                    vals, sql = _assemblesql(sql, "*", "lattice_type_name", vals, connector="and")
                else:
                    vals, sql = _assemblesql(sql, latticetype['name'], "lattice_type_name", vals, connector="and")
            if latticetype.has_key('format'):
                if isinstance(latticetype['format'], (list, tuple)) and "" in latticetype['format']:
                    vals, sql = _assemblesql(sql, "*", "lattice_type_format", vals, connector="and")
                else:
                    vals, sql = _assemblesql(sql, latticetype['format'], "lattice_type_format", vals, connector="and")
        
        try:
            cur = self.conn.cursor()
            cur.execute(sql, vals)
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching lattice information:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when fetching lattice information:\n%s (%d)' %(e.args[1], e.args[0]))
        
        resdict = {}
        urls = {}
        for r in res:
            tempdict = {'name': r[1],
                        'version': r[2],
                        'branch': r[3]}
            if r[4] != None:
                tempdict['description'] = r[4]
            if r[5] != None:
                tempdict['creator'] = r[5]
            if r[6] != None:
                tempdict['originalDate'] = r[6].isoformat()
            if r[7] != None:
                tempdict['updated'] = r[7]
            if r[8] != None:
                tempdict['lastModified'] =  r[8].isoformat()
            if r[9] != None:
                tempdict['latticeType'] = r[9]
            if r[10] != None:
                tempdict['latticeFormat'] = r[10]
            resdict[r[0]] = tempdict
            urls[r[0]] = r[11]
        return urls, resdict

    def savelatticeinfo(self, name, version, branch, **params):
        '''
        save lattice header information. 
        Real lattice data (geometric layout and strength) can be saved thru savelatticedata() method.
        
        parameters:
            name:        lattice name
            version:     version number
            branch:      branch name
            latticetype: a dictionary which consists of {'name': , 'format': }
                         it is a predefined structure: [{'name': 'plain', 'format': 'txt'},
                                                        {'name': 'tracy3',  'format': 'lat'},
                                                        {'name': 'tracy4',  'format': 'lat'},
                                                        {'name': 'elegant', 'format': 'lte'},
                                                        {'name': 'xal',     'format': 'xdxf'}]
            
            description: description for this lattice, allow user put any info here (< 255 characters)
            creator:     original creator
        
        return: lattice id if success, otherwise, raise an exception
        '''
        try:
            float(version)
        except ValueError as e:
            self.logger.info('Version should be a numeric value:\n%s (%d)' %(e.args[1], e.args[0]))
            raise ValueError('Version should be a numeric value:\n%s (%d)' %(e.args[1], e.args[0]))
        
        _, lattices = self.retrievelatticeinfo(name, version, branch)
        if len(lattices) != 0:
            raise ValueError('lattice (name: %s, version: %s, branch: %s) exists already.'
                             %(name, version, branch))

        latticetypeid = None
        latticetypename=None
        latticetypeformat=None
        if params.has_key('latticetype') and params['latticetype'] != None:
            # lattice type has been given.
            # try to get lattice type id
            try:
                latticetypename=params['latticetype']["name"]
                latticetypeformat=params['latticetype']["format"]
                latticetypeid = self.retrievelatticetype(latticetypename, latticetypeformat)
            except KeyError:
                pass
            if len(latticetypeid) == 1:
                # get lattice type id
                latticetypeid = latticetypeid[0][0]
            else:
                # no lattice type found, or more than one found.
                raise ValueError("Does not support lattice type (%s) with given format (%s)."
                                 %(latticetypename, latticetypeformat))
        
        try:
            cur = self.conn.cursor()

            desc = None
            if params.has_key('description'):
                desc = params['description']
            creator = None
            if params.has_key('creator'):
                creator = params['creator']

            # no lattice entry found.
            # add a new one
            if latticetypeid:
                sql = '''
                insert into lattice 
                (lattice_type_id, lattice_name, lattice_version, lattice_branch, lattice_description, created_by, create_date) 
                values
                (%s, %s, %s, %s, %s, %s, now())
                '''
                cur.execute(sql,(latticetypeid, name, version, branch, desc, creator))
            else:
                sql = '''
                insert into lattice 
                (lattice_type_id, lattice_name, lattice_version, lattice_branch, lattice_description, created_by, create_date) 
                values
                (NULL, %s, %s, %s, %s, %s, now())
                '''
                cur.execute(sql,(name, version, branch, desc, creator))
                
            # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
            # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
            # it is per connection.
            latticeid = cur.lastrowid
            if self.transaction:
                self.transaction.commit_unless_managed()
            else:
                self.conn.commit()
        except MySQLError as e:
            if self.transaction:
                self.transaction.rollback_unless_managed()
            else:
                self.conn.rollback()
            
            self.logger.info('Error when saving lattice information:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when saving lattice information:\n%s (%d)' %(e.args[1], e.args[0]))
    
        return latticeid
    
    def updatelatticeinfo(self, name, version, branch, **params):
        '''
        update lattice header information. 
        Real lattice data (geometric layout and strength) can be updated thru updatelatticedata() method.
        
        parameters:
            name:        lattice name
            version:     version number
            branch:      branch name
            latticetype: a dictionary which consists of {'name': , 'format': }
                         it is a predefined structure: [{'name': 'plain', 'format': 'txt'},
                                                        {'name': 'tracy3',  'format': 'lat'},
                                                        {'name': 'tracy4',  'format': 'lat'},
                                                        {'name': 'elegant', 'format': 'lte'},
                                                        {'name': 'xal',     'format': 'xdxf'}]
            
            description: description for this lattice, allow user put any info here (< 255 characters)
            creator:     original creator
        
        return: True, otherwise, raise an exception
        '''
        _, lattices = self.retrievelatticeinfo(name, version, branch)
        latticeid = None
        if len(lattices) == 0:
            raise ValueError('Did not find lattice (name: %s, version: %s, branch: %s).'
                             %(name, version, branch))
        elif len(lattices) > 1:
            # lattice with given name, version, and branch should be unique.
            raise ValueError('More than one lattice found lattice (name: %s, version: %s, branch: %s).'
                             %(name, version, branch))
        else:
            for k, _ in lattices.iteritems():
                latticeid = k

        latticetypeid = None
        latticetypename=None
        latticetypeformat=None
        if params.has_key('latticetype') and params['latticetype'] != None:
            # lattice type has been given.
            # try to get lattice type id
            try:
                latticetypename=params['latticetype']["name"]
                latticetypeformat=params['latticetype']["format"]
                latticetypeid = self.retrievelatticetype(latticetypename, latticetypeformat)
                if len(latticetypeid) == 1:
                    # get lattice type id
                    latticetypeid = latticetypeid[0][0]
                else:
                    # no lattice type found, or more than one found.
                    raise ValueError("Does not support lattice with given type (%s) and format (%s)."
                                     %(latticetypename, latticetypeformat))
            except:
                pass
        if latticeid == None:
            raise ValueError("Did not find lattice (name: %s, version: %s, branch: %s)."
                             %(name, version, branch))
        
        try:
            cur = self.conn.cursor()
            sql = '''UPDATE lattice SET '''
            vals = []
            desc = None
            if params.has_key('description'):
                desc = params['description']
            if desc:
                sql += '''lattice_description=%s,'''
                vals.append(desc)
            
            if latticetypeid:
                sql += ''' lattice_type_id=%s,'''
                vals.append(latticetypeid)
                
            creator = None
            if params.has_key('creator'):
                creator = params['creator']
            if creator:
                sql += ''' updated_by=%s,update_date=now()'''
                vals.append(creator)
            else:
                sql += ''' updated_by=NULL,update_date=now()'''
            
            sql += ' where lattice_id = %s'
            vals.append(latticeid)
            
            cur.execute(sql, vals)

            if self.transaction:
                self.transaction.commit_unless_managed()
            else:
                self.conn.commit()
        except MySQLError as e:
            if self.transaction:
                self.transaction.rollback_unless_managed()
            else:
                self.conn.rollback()
            
            self.logger.info('Error when updating lattice information:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when updating lattice information:\n%s (%d)' %(e.args[1], e.args[0]))
    
        return True
        
    def _retrievelatticeinfobyid(self, latticeid):
        '''
        Retrieve lattice information with given lattice id.
        '''
        sql = '''select lattice_name, lattice_version, lattice_branch from lattice where lattice_id = %s'''
        try:
            cur=self.conn.cursor()
            cur.execute(sql, (latticeid,))
            res=cur.fetchone()
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching lattice information:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when fetching lattice information:\n%s (%d)' %(e.args[1], e.args[0]))
        return res

    def retrievelatticetype(self, name, typeformat=None):
        '''
        Retrieve supported lattice type information.
        '''
        name = _wildcardformat(name)
        typeformat = _wildcardformat(typeformat)
        try:
            cur = self.conn.cursor()
            sql = '''
            select lattice_type_id, lattice_type_name, lattice_type_format
            from lattice_type
            where
            lattice_type_name like %s
            '''
            if typeformat != None:
                sql += ''' and lattice_type_format like %s '''
                cur.execute(sql, (name, typeformat,))
            else:
                cur.execute(sql, (name,))
            # get any one since it should be unique
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching lattice type information:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when fetching lattice type information:\n%s (%d)' %(e.args[1], e.args[0]))
        
        return res

    def savelatticetype(self, name, typeformat):
        '''
        Save a new lattice type.
        
        supported lattice type so far:
        [{'name': 'plain', 'format': 'txt'},
         {'name': 'tracy3',  'format': 'lat'},
         {'name': 'tracy4',  'format': 'lat'},
         {'name': 'elegant', 'format': 'lte'},
         {'name': 'xal',     'format': 'xdxf'}]

        Return lattice type id if success, otherwise, raise an exception.
        '''
        
        res = self.retrievelatticetype(name, typeformat)
        if len(res) != 0:
            raise ValueError("Lattice type (%s) with given format (%s) exists already."%(name, typeformat))
        sql = '''
        insert into lattice_type (lattice_type_name, lattice_type_format)
        values 
        (%s, %s)
        '''
        try:
            cur=self.conn.cursor()
            cur.execute(sql, (name, typeformat))
            
            if self.transaction:
                self.transaction.commit_unless_managed()
            else:
                self.conn.commit()
            res = cur.lastrowid
        except MySQLdb.Error as e:
            if self.transaction:
                self.transaction.rollback_unless_managed()
            else:
                self.conn.rollback()
            self.logger.info('Error when saving a new lattice type:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when saving a new lattice type:\n%s (%d)' %(e.args[1], e.args[0]))
        return res

    def _uniquefile(self, file_name):
        dirname, filename = os.path.split(file_name)
        prefix, suffix = os.path.splitext(filename)
    
        try:
            os.makedirs(dirname)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(dirname):
                pass
            else: 
                raise Exception("Could not create a directory to save lattice file")
    
        fd, filename = tempfile.mkstemp(suffix, prefix+"_", dirname)
        return fd, filename

    def _processlatticedata(self, latticefile, latticedata, latticetypeid=0, savefile=True):
        '''
        latticefile: lattice file name
        latticedata: body having real data
        
        latticetypeid: identify lattice file format id: 
            0. tab format; 1. tracy-3 format; 2. tracy-4 format; 3. elegant format
            By default, it is 0, which means a plain lattice.
            at current stage, only plain lattice is supported.
        
        savefile: flag to save the lattice file into hard disk
        
        return: url, typelist, elemdict, unitdict
        '''
        url = None
        if savefile:
            now = datetime.datetime.now()
            dirname = 'documents/%s/%s/%s'%(now.year, now.month, now.day)
            fd, url = self._uniquefile('/'.join((dirname, latticefile)))
            with os.fdopen(fd,'w') as f:
                for data in latticedata:
                    if data.endswith('\n'):
                        f.write(data)
                    else:
                        f.write(data+'\n')
        
        # keep element order
        elemdict = OrderedDict()
        unitdict = {}
        latticedatalen = len(latticedata)
        headercount = 3
        for i in range(latticedatalen):
            if latticedata[i].strip() != '':
                headercount -= 1
            if headercount == 0:
                break
        headerlen = i
        if headerlen >= latticedatalen or headercount != 0:
            raise ValueError("Incomplete lattice data header.")
        if latticetypeid == 0:
            # tab formatted lattice file
            if len(latticedata) <= headerlen:
                # do nothing since no real data
                return url, elemdict, unitdict
            latticehead = latticedata[:headerlen]
            # lattice head has to have the following format:
            # the first 3 lines are column description
            # 1st line is for the column name which defines properties
            # the alignment errors and some additional attributes are optional
            # 2nd line is the unit for each column if appliable
            # 3rd line is divider between body and head.
            # ElementName  ElementType    L    s    K1    K2    Angle  [dx  dy  dz  pitch  yaw  roll  kickmap]
            #                             m    m   1/m2  1/m3   rad    [m   m   m    rad   rad  rad          ]
            # -------------------------------------------------------------------------------
            # Pitch, Yaw, and Roll are rotations about the x, y, and z axes respectively
            # Pitch = Theta_x, Yaw = Theta_y, Roll = Theta_z
            cols=None
            units=None
            for h in latticehead:
                if h.strip() != '':
                    if not cols:
                        cols = str(h).split()
                    elif not units:
                        units = str(h).split()
            if cols==None or units==None:
                raise ValueError("Incomplete lattice data header.")
            elif len(cols) < 2 or len(units) < len(cols)-3:
                raise ValueError("Incomplete lattice data header.")
            
            skipcount = 0
            unitdict={}
            for i in range(len(cols)):
                if str.lower(cols[i]) in ['elementtype', 'type', 'elementname', 'name', 'map', 'kickmap', 'fieldmap']:
                    skipcount += 1
                else:
                    unitdict[cols[i]] = units[i-skipcount]

            latticebody = latticedata[headerlen+1:]
            for i in range(len(latticebody)):
                body = latticebody[i]
                attrs = body.split()
                
                # the line is not empty and not commented out by "#" or "!"
                if  len(attrs) > 0 and not attrs[0].startswith('#') and not attrs[0].startswith('!'):
                    # check whether lattice body matches lattice header
                    if len(attrs) < len(cols)-1:
                        # the last kickmap column could be empty
                        
                        raise ValueError("lattice property values is not complete.")
                    tmpdict = {}
                    typeprop = []
                    for j in range(len(attrs)):
                        temp = str.lower(cols[j])
                        # get rid of " or '
                        attr = attrs[j].replace("'", '').replace('"', '')
                        if temp in ['elementname', 'name']:
                            tmpdict['name'] = attr
                        elif temp in ['elementtype', 'type']:
                            tmpdict['type'] = attr
                        elif temp in ['l', 'length']:
                            tmpdict['length'] = attr
                        elif temp in ['s', 'position']:
                            tmpdict['position'] = attr
                        elif temp in ['map', 'kickmap', 'fieldmap']:
                            tmpdict[cols[j]] = attr
                            typeprop.append(cols[j])
                        else:
                            if float(attrs[j]) != 0.0:
                                if cols[j].lower() not in ['dx', 'dy', 'dz', 'pitch', 'yaw', 'roll']:
                                    typeprop.append(cols[j])
                                tmpdict[cols[j]] = attr
                    tmpdict['typeprop'] = typeprop
                    elemdict[str(i)] = tmpdict
        else:
            raise TypeError('Wrong lattice format. Expecting a plain lattice.')
        
        return url, elemdict, unitdict

    def _getelemprop(self, value, keyname):
        res=None
        try:
            res=value[keyname]
        except:
            pass
        return res

    def _retrieveelementbylatticeid(self, latticeid, cursor):
        '''
        Retrieve all about element ids, names, and their orders belongs to given lattice id 
        '''
        elementidsql = '''
        select element_id, element_name, element_order
        from element
        where lattice_id = %s
        order by element_order
        ''' 
        
        cursor.execute(elementidsql, (latticeid, ))
        return cursor.fetchall()

    def _savetabformattedlattice(self, cur, latticeid, lattice):
        '''
        save real lattice data information
        
        cur: database connection cursor
        latticeid: lattice id to identify which lattice the data belongs to.
        lattice:   lattice data dictionary:
                     {'name': ,
                      'data': ,
                      'map': {}
                     }
        '''
        if not isinstance(lattice, dict) or not lattice.has_key('name') or not lattice.has_key('data'):
            raise ValueError('No lattice data found.')
        
        latticefile = lattice['name']
        latticedata = lattice['data']
        if latticefile==None or latticedata==None:
            raise ValueError("Lattice data is not complete.")
        # pre-process and reorganize the data
        url, elemdict, unitdict = self._processlatticedata(latticefile, 
                                                           latticedata,
                                                           latticetypeid=0)
        if url != None:
            if lattice.has_key('map'):
                self._savemapfile(url, lattice['map'])

            sql = '''update lattice SET url = %s where lattice_id = %s'''
            cur.execute(sql,(url, latticeid))

        typedict = {}

        sql = '''
        insert into element
        (lattice_id, element_type_id, element_name, element_order, insert_date, s, length, 
        dx, dy, dz, pitch, yaw, roll)
        values
        '''
        if elemdict:
            for k, v in elemdict.iteritems():
                etypeprops = v['typeprop']
                etypename=v['type']
                elemtypeid = None
                if typedict.has_key(etypename):
                    tempdict = typedict[etypename]
                    elemtypeid = tempdict['id']
                    etypepropres = self.retrieveelemtype(etypename)
                    for etypeprop in etypeprops:
                        if not tempdict.has_key(etypeprop):
                            etypepropid = None
                            for etypepropresinst in etypepropres:
                                if etypeprop == etypepropresinst[3]:
                                    etypepropid = etypepropresinst[1]
                                    break
                            if etypepropid == None:
                                etypepropid = self.updateelemtypeprop(etypename, etypeprop, unitdict)
                            try:
                                tempdict[etypeprop] = [etypepropid, unitdict[etypeprop]]
                            except KeyError:
                                tempdict[etypeprop] = [etypepropid]
                    typedict.update({etypename: tempdict})
                else:
                    res = self.retrieveelemtype(etypename)
                    if len(res) == 0:
                        elemtypeid= self.saveelemtype(etypename, etypeprops, unitdict)
                        results = self.retrieveelemtype(etypename)
                        
                        tempdict = {}
                        for res in results:
                            if not tempdict.has_key('id'):
                                tempdict = {'id': res[0]}
                            if not tempdict.has_key(res[3]):
                                if res[4] == None:
                                    tempdict[res[3]] = [res[1]]
                                else:
                                    tempdict[res[3]] = [res[1], res[4]]
                        typedict[etypename] = tempdict
                    else:
                        etypepropstemps = []
                        for typeins in res:
                            if typedict.has_key(typeins[2]):
                                tempdict = typedict[typeins[2]]
                                if tempdict['id'] != typeins[0]:
                                    raise ValueError('Type (%s) is not unique'%(etypename))
                            else:
                                tempdict = {'id': typeins[0]}
                            if elemtypeid == None:
                                elemtypeid = typeins[0]
                            if typeins[3] != None and not tempdict.has_key(typeins[3]):
                                etypepropstemps.append(typeins[3])
                                if typeins[1] == None:
                                    raise ValueError ('type (%s) property (%s) id is empty'%(typeins[2], typeins[3]))
                                elif typeins[4] == None:
                                    tempdict[typeins[3]] = [typeins[1]]
                                else:
                                    tempdict[typeins[3]] = [typeins[1], typeins[4]]
                            typedict[etypename] = tempdict
                        if len(etypeprops) > 0:
                            etypepropscopies = etypeprops[:]
                            for etypepropscopy in etypepropscopies:
                                if etypepropscopy not in etypepropstemps:
                                    # some new properties
                                    etypepropid = self.updateelemtypeprop(etypename, etypepropscopy, unitdict)
                                    if typedict.has_key(etypename):
                                        tempdict = typedict[etypename]
                                    else:
                                        tempdict = {'id': typeins[0]}
                                    try:
                                        tempdict[etypepropscopy] = [etypepropid, unitdict[etypepropscopy]]
                                    except KeyError:
                                        tempdict[etypepropscopy] = [etypepropid]
                                    typedict[etypename] = tempdict

                sql += '''(%s, %s, '%s', %s, now(), %s, %s, '''%(latticeid, elemtypeid, v['name'], k, v['position'], v['length'])
                dx = self._getelemprop(v, 'dx')
                if dx == None:
                    sql += 'NULL, '
                else:
                    sql += '%s, '%dx
                dy = self._getelemprop(v, 'dy')
                if dy == None:
                    sql += 'NULL, '
                else:
                    sql += '%s, '%dy
                dz = self._getelemprop(v, 'dz')
                if dz == None:
                    sql += 'NULL, '
                else:
                    sql += '%s, '%dz
                pitch = self._getelemprop(v, 'pitch')
                if pitch == None:
                    sql += 'NULL, '
                else:
                    sql += '%s, '%pitch
                yaw= self._getelemprop(v, 'yaw')
                if yaw == None:
                    sql += 'NULL, '
                else:
                    sql += '%s, '%yaw
                roll = self._getelemprop(v, 'roll')
                if roll == None:
                    sql += 'NULL '
                else:
                    sql += '%s '%roll
                
                sql += '),'
        
            # get rid of last comma from SQL statement.
            # save element geometric value
            cur.execute(sql[:-1])
            
            # save element values
            elempropsql = '''
            insert into element_prop
            (element_id, element_type_prop_id, element_prop_value, element_prop_unit)
            values
            '''
            
            elementidres = self._retrieveelementbylatticeid(latticeid, cur)
            
            elementiddict = {}
            for elementid in elementidres:
                elementiddict[str(elementid[2])] = elementid
            for k, v in elemdict.iteritems():
                etypeprops = v['typeprop']
                etypename=v['type']
                if k != str(elementiddict[k][2]):
                    # check the element order to ensure same element
                    raise ValueError("Element not same")
                elementid = elementiddict[k][0]
                
                for etypeprop in etypeprops:
                    etypeproptidunit = typedict[etypename][etypeprop]
                    if len(etypeproptidunit) == 2:
                        if etypeproptidunit[1] != unitdict[etypeprop]:
                            elempropsql += '''('%s', '%s', '%s', '%s'),'''%(elementid, 
                                                                    typedict[etypename][etypeprop][0],
                                                                    v[etypeprop],
                                                                    unitdict[etypeprop])
                        else:
                            elempropsql += '''('%s', '%s', '%s', NULL),'''%(elementid, 
                                                                      typedict[etypename][etypeprop][0],
                                                                      v[etypeprop])
                    elif len(etypeproptidunit) == 1:
                        # no unit
                        elempropsql += '''('%s', '%s', '%s', NULL),'''%(elementid, 
                                                                  typedict[etypename][etypeprop][0],
                                                                  v[etypeprop])
                    else:
                        raise TypeError("Unknown structure for element type property value and unit.")
            # get rid of last comma from SQL statement.
            # save element type property value
            cur.execute(elempropsql[:-1])
    
    def _savemapfile(self, url, fieldmaps, b64decode=False):
        '''
        '''
        # save field map files
        if len(fieldmaps) > 0:
            for mapname, mapvalue in fieldmaps.iteritems():
                dirname, _ = os.path.split(mapname)
                try:
                    # create a sub directory to store field map
                    os.makedirs('/'.join((url+"_map",dirname)))
                except OSError as exc:
                    if exc.errno == errno.EEXIST and os.path.isdir('/'.join((url+"_map",dirname))):
                        pass
                    else: 
                        raise Exception("Can not create a sub directory to store map")
                with file('/'.join((url+"_map", mapname)), 'w') as f:
                    if b64decode:
                        f.write(base64.b64decode(mapvalue))
                    else:
                        for data in mapvalue:
                            f.write(data)

    def _savetracylattice(self, cur, latticeid, params):
        '''
        save real lattice data information
        
        cur: database connection cursor
        latticeid: lattice id to identify which lattice the data belongs to.
        params:   lattice data dictionary:
                     {'name': ,
                      'data': ,
                      'raw': ,
                      'map': ,
                      'alignment': 
                     }        
        '''
        if not isinstance(params, dict) or not params.has_key('name'):
            raise ValueError('No lattice name given.')

        if (not params.has_key('data') or params['data']==None) and (not params.has_key('raw') or len(params['raw'])==0):
            raise ValueError('No lattice data found.')

        if params.has_key('map') and params['map'] != None and not params.has_key('raw'):
            raise ValueError('Cannot save field map files since raw lattice is missing.')

        # save raw lattice file
        if params.has_key('raw') and len(params['raw'])!=0:
            now = datetime.datetime.now()
            dirname = 'documents/%s/%s/%s'%(now.year, now.month, now.day)
            fd, url = self._uniquefile('/'.join((dirname, params['name'])))
            with os.fdopen(fd,'w') as f:
                for data in params['raw']:
                    f.write(data)
            
            if params.has_key('map'):
                self._savemapfile(url, params['map'])
            
            sql = '''update lattice SET url = %s where lattice_id = %s'''
            cur.execute(sql,(url,latticeid))
        
        #
        if params.has_key('data') and params['data']!=None:
            # save lattice information
            self._savetracylatticeelement(cur, latticeid, params)
        
    def _savetracylatticeelement(self, cur, latticeid, params):
        # save element statement
        sql = '''
        insert into element
        (lattice_id, element_type_id, element_name, element_order, insert_date, s, length, 
        dx, dy, dz, pitch, yaw, roll)
        values
        '''
        # prepare type dictionary
        # type dictionary format: 
        # {'type name': {'id': , 
        #                'type property': [type property id],
        #                'type property': [type property id, type property unit],
        #                'type property': [type property id, type property unit],
        #                ...
        #               }
        # }
        typedict = {}
        for k, v in params['data'].iteritems():
            if v.has_key('type'):
                etypename = v['type']
                
                # get all properties for given element type
                # key word in ['name', 'position', 'length', 'type'] is not a type property
                etypeprops = []
                etypepropunits = {}
                for etypeprop in v.keys():
                    if etypeprop not in ['name', 'position', 'length', 'type', 
                                         'dx', 'dy', 'dz', 'pitch', 'yaw', 'roll']:
                        etypeprops.append(etypeprop)
                        tmp = etypeprop.upper()
                        if tmp == 'K':
                            if etypename.upper() in ['BENDING','QUADRUPOLE']:
                                etypepropunits[etypeprop] = tracypropunits['K1']
                            elif etypename.upper() == 'SEXTUPOLE':
                                etypepropunits[etypeprop] = tracypropunits['K2']
                            else:
                                raise TypeError('Unknown element type (%s)'%(etypename))
                        if tracypropunits.has_key(tmp):
                            etypepropunits[etypeprop] = tracypropunits[tmp]

                # cache type dictionary
                if typedict.has_key(etypename):
                    tmptypedict = typedict[etypename]
                else:
                    tmptypedict = {}

                # retrieve element type information, which includes also all properties belonging to this type
                etypepropsres = self.retrieveelemtype(etypename)
                if len(etypepropsres) == 0:
                    # element type does not exist yet.
                    # insert a new entry
                    elemtypeid = self.saveelemtype(etypename, etypeprops, etypepropunits)
                    
                    # add a new entry, 'id',  into type dictionary
                    tmptypedict['id'] = elemtypeid
                    etypepropsres = self.retrieveelemtype(etypename)
                    for etypepropres in etypepropsres:
                        if etypepropres[3] != None:
                            if etypepropres[4] == None:
                                tmptypedict[etypepropres[3]] = [etypepropres[1]]
                            else:
                                tmptypedict[etypepropres[3]] = [etypepropres[1], etypepropres[4]]
                else:
                    elemtypeid = etypepropsres[0][0]
                    if not tmptypedict:
                        # check whether type dictionary is empty
                        tmptypedict['id'] = elemtypeid
                        for etypepropres in etypepropsres:
                            if etypepropres[3] != None:
                                if etypepropres[4] == None:
                                    tmptypedict[etypepropres[3]] = [etypepropres[1]]
                                else:
                                    tmptypedict[etypepropres[3]] = [etypepropres[1], etypepropres[4]]
                    else:
                        # not empty, therefore the element type id has to be same
                        assert tmptypedict['id'] == elemtypeid, 'element type id does not match'
                    
                    # check whether all properties are in database
                    if len(etypeprops) > 0:
                        for etypeprop in etypeprops:
                            if not tmptypedict.has_key(etypeprop):
                                etypepropid = self.updateelemtypeprop(etypename, etypeprop, etypepropunits)
                                try:
                                    # element type property has unit
                                    tmptypedict[etypeprop] = [etypepropid, etypepropunits[etypeprop]]
                                except KeyError:
                                    # element type property does not have unit
                                    tmptypedict[etypeprop] = [etypepropid]

                typedict[etypename] = tmptypedict
            else:
                raise ValueError('Unknown element type for %s'%(v['name']))

            # start to prepare insert statement
            if v.has_key('length'):
                sql += '''(%s, %s, '%s', %s, now(), %s, %s, '''%(latticeid, elemtypeid, v['name'], k, v['position'], v['length'])
            else:
                sql += '''(%s, %s, '%s', %s, now(), %s, NULL, '''%(latticeid, elemtypeid, v['name'], k, v['position'])
            dx = self._getelemprop(v, 'dx')
            if dx == None:
                sql += 'NULL, '
            else:
                sql += '%s, '%dx
            dy = self._getelemprop(v, 'dy')
            if dy == None:
                sql += 'NULL, '
            else:
                sql += '%s, '%dy
            dz = self._getelemprop(v, 'dz')
            if dz == None:
                sql += 'NULL, '
            else:
                sql += '%s, '%dz
            pitch = self._getelemprop(v, 'pitch')
            if pitch == None:
                sql += 'NULL, '
            else:
                sql += '%s, '%pitch
            yaw= self._getelemprop(v, 'yaw')
            if yaw == None:
                sql += 'NULL, '
            else:
                sql += '%s, '%yaw
            roll = self._getelemprop(v, 'roll')
            if roll == None:
                sql += 'NULL '
            else:
                sql += '%s '%roll
            
            sql += '),'
        
        # get rid of last comma from SQL statement.
        # save element geometric value
        cur.execute(sql[:-1])
        
        elementidres = self._retrieveelementbylatticeid(latticeid, cur)

        # save element property value statement
        elempropsql = '''
        insert into element_prop
        (element_id, element_type_prop_id, element_prop_value, element_prop_unit)
        values
        '''
        
        elementiddict = {}
        for elementid in elementidres:
            elementiddict[str(elementid[2])] = elementid
        for k, v in params['data'].iteritems():
            if k != str(elementiddict[k][2]):
                # check the element order to ensure same element
                raise ValueError("Element not same")
            elementid = elementiddict[k][0]
            etypename=v['type']
            for etypeprop in v.keys():
                if etypeprop not in  ['name', 'position', 'length', 'type', 
                                         'dx', 'dy', 'dz', 'pitch', 'yaw', 'roll']:
                    etypeprops.append(etypeprop)
                    etypeproptidunit = typedict[etypename][etypeprop]

                    if len(etypeproptidunit) > 0:
                            elempropsql += '''('%s', '%s', '%s', NULL),'''%(elementid, 
                                                                      typedict[etypename][etypeprop][0],
                                                                      v[etypeprop])
                    else:
                        raise TypeError("Unknown structure for element type property value and unit.")
        # get rid of last comma from SQL statement.
        # save element type property value
        cur.execute(elempropsql[:-1])
        
        return True
        
    def _saveelegantlatticeelement(self, cur, latticeid, params):
        '''
        '''
        # save element statement
        sql = '''
        insert into element
        (lattice_id, element_type_id, element_name, element_order, insert_date, s, length, 
        dx, dy, dz, pitch, yaw, roll)
        values
        '''
        # prepare type dictionary
        # type dictionary format: 
        # {'type name': {'id': , 
        #                'type property': [type property id],
        #                'type property': [type property id, type property unit],
        #                'type property': [type property id, type property unit],
        #                ...
        #               }
        # }
        typedict = {}
        for k, v in params['data'].iteritems():
            if v.has_key('type'):
                etypename = v['type']
                
                # get all properties for given element type
                # key word in ['name', 'position', 'length', 'type'] is not a type property
                etypeprops = []
                etypepropunits = {}
                for etypeprop in v.keys():
                    if etypeprop not in ['name', 'position', 'length', 'type', 
                                         'dx', 'dy', 'dz', 'pitch', 'yaw', 'roll']:
                        etypeprops.append(etypeprop)

                # cache type dictionary
                if typedict.has_key(etypename):
                    tmptypedict = typedict[etypename]
                else:
                    tmptypedict = {}

                # retrieve element type information, which includes also all properties belonging to this type
                etypepropsres = self.retrieveelemtype(etypename)
                if len(etypepropsres) == 0:
                    # element type does not exist yet.
                    # insert a new entry
                    elemtypeid = self.saveelemtype(etypename, etypeprops, etypepropunits)
                    
                    # add a new entry, 'id',  into type dictionary
                    tmptypedict['id'] = elemtypeid
                    etypepropsres = self.retrieveelemtype(etypename)
                    for etypepropres in etypepropsres:
                        if etypepropres[3] != None:
                            if etypepropres[4] == None:
                                tmptypedict[etypepropres[3]] = [etypepropres[1]]
                            else:
                                tmptypedict[etypepropres[3]] = [etypepropres[1], etypepropres[4]]
                else:
                    elemtypeid = etypepropsres[0][0]
                    if not tmptypedict:
                        # check whether type dictionary is empty
                        tmptypedict['id'] = elemtypeid
                        for etypepropres in etypepropsres:
                            if etypepropres[3] != None:
                                if etypepropres[4] == None:
                                    tmptypedict[etypepropres[3]] = [etypepropres[1]]
                                else:
                                    tmptypedict[etypepropres[3]] = [etypepropres[1], etypepropres[4]]
                    else:
                        # not empty, therefore the element type id has to be same
                        assert tmptypedict['id'] == elemtypeid, 'element type id does not match'
                    
                    # check whether all properties are in database
                    if len(etypeprops) > 0:
                        for etypeprop in etypeprops:
                            if not tmptypedict.has_key(etypeprop):
                                etypepropid = self.updateelemtypeprop(etypename, etypeprop, etypepropunits)
                                try:
                                    # element type property has unit
                                    tmptypedict[etypeprop] = [etypepropid, etypepropunits[etypeprop]]
                                except KeyError:
                                    # element type property does not have unit
                                    tmptypedict[etypeprop] = [etypepropid]

                typedict[etypename] = tmptypedict
            else:
                raise ValueError('Unknown element type for %s'%(v['name']))

            # start to prepare insert statement
            if v.has_key('length'):
                sql += '''(%s, %s, '%s', %s, now(), %s, %s, '''%(latticeid, elemtypeid, v['name'], k, v['position'], v['length'])
            else:
                sql += '''(%s, %s, '%s', %s, now(), %s, NULL, '''%(latticeid, elemtypeid, v['name'], k, v['position'])
            dx = self._getelemprop(v, 'dx')
            if dx == None:
                sql += 'NULL, '
            else:
                sql += '%s, '%dx
            dy = self._getelemprop(v, 'dy')
            if dy == None:
                sql += 'NULL, '
            else:
                sql += '%s, '%dy
            dz = self._getelemprop(v, 'dz')
            if dz == None:
                sql += 'NULL, '
            else:
                sql += '%s, '%dz
            pitch = self._getelemprop(v, 'pitch')
            if pitch == None:
                sql += 'NULL, '
            else:
                sql += '%s, '%pitch
            yaw= self._getelemprop(v, 'yaw')
            if yaw == None:
                sql += 'NULL, '
            else:
                sql += '%s, '%yaw
            roll = self._getelemprop(v, 'roll')
            if roll == None:
                sql += 'NULL '
            else:
                sql += '%s '%roll
            
            sql += '),'
        
        # get rid of last comma from SQL statement.
        # save element geometric value
        cur.execute(sql[:-1])
        
        elementidres = self._retrieveelementbylatticeid(latticeid, cur)

        # save element property value statement
        elempropsql = '''
        insert into element_prop
        (element_id, element_type_prop_id, element_prop_value, element_prop_unit)
        values
        '''
        
        elementiddict = {}
        for elementid in elementidres:
            elementiddict[str(elementid[2])] = elementid
        for k, v in params['data'].iteritems():
            if k != str(elementiddict[k][2]):
                # check the element order to ensure same element
                raise ValueError("Element not same")
            elementid = elementiddict[k][0]
            etypename=v['type']
            for etypeprop in v.keys():
                if etypeprop not in  ['name', 'position', 'length', 'type', 
                                         'dx', 'dy', 'dz', 'pitch', 'yaw', 'roll']:
                    etypeprops.append(etypeprop)
                    etypeproptidunit = typedict[etypename][etypeprop]

                    if len(etypeproptidunit) > 0:
                            elempropsql += '''('%s', '%s', '%s', NULL),'''%(elementid, 
                                                                            typedict[etypename][etypeprop][0],
                                                                            v[etypeprop])
                    else:
                        raise TypeError("Unknown structure for element type property value and unit.")
        # get rid of last comma from SQL statement.
        # save element type property value
        cur.execute(elempropsql[:-1])
        
        return True
    
    def _saveelegantlattice(self, cur, latticeid, params):
        '''
        save real lattice data information
        
        cur: database connection cursor
        latticeid: lattice id to identify which lattice the data belongs to.
        params:   lattice data dictionary:
                     {'name': ,
                      'data': ,
                      'raw': ,
                      'map': ,
                      'alignment': ,
                      'control': 
                     }        
        '''
        if not isinstance(params, dict) or not params.has_key('name'):
            raise ValueError('No lattice name given.')

        if (not params.has_key('data') or params['data']==None) and (not params.has_key('raw') or len(params['raw'])==0):
            raise ValueError('No lattice data found.')

        if params.has_key('map') and params['map'] != None and not params.has_key('raw'):
            raise ValueError('Cannot save field map files since raw lattice is missing.')

        # save raw lattice file
        if params.has_key('raw') and len(params['raw'])!=0:
            now = datetime.datetime.now()
            dirname = 'documents/%s/%s/%s'%(now.year, now.month, now.day)
            fd, url = self._uniquefile('/'.join((dirname, params['name'])))
            with os.fdopen(fd,'w') as f:
                for data in params['raw']:
                    f.write(data)
            
            if params.has_key('map'):
                self._savemapfile(url, params['map'], b64decode=True)
            sql = '''update lattice SET url = %s where lattice_id = %s'''
            cur.execute(sql,(url,latticeid))
        
        #
        if params.has_key('data') and params['data']!=None:
            # save lattice information
            self._saveelegantlatticeelement(cur, latticeid, params)

    def savelattice(self, name, version, branch, **params):
        '''
        Save lattice data.
        parameters:
            name:        lattice name
            version:     version number
            branch:      branch name
            latticetype: a dictionary which consists of {'name': , 'format': }
                         it is a predefined structure: [{'name': 'plain', 'format': 'txt'},
                                                        {'name': 'tracy3',  'format': 'lat'},
                                                        {'name': 'tracy4',  'format': 'lat'},
                                                        {'name': 'elegant', 'format': 'lte'},
                                                        {'name': 'xal',     'format': 'xdxf'}]
            
            description: description for this lattice, allow user put any info here (< 255 characters)
            creator:     original creator
            lattice:     lattice data, a dictionary:
                         {'name': ,
                          'data': ,
                          'raw': ,
                          'map': {'name': ,
                                  'value': },
                          'alignment': ,
                         }
                         name: file name to be saved into disk, it is same with lattice name by default
                         data: lattice geometric and strength with predefined format
                         raw:  raw data that is same with data but in original lattice format
                         map:  name-value pair dictionary
                         alignment: mis-alignment information
        return: lattice id if success, otherwise, raise an exception
        '''
        
        _, lattices = self.retrievelatticeinfo(name, version, branch)
        if len(lattices) != 0:
            raise ValueError('lattice (name: %s, version: %s, branch: %s) description information exists already. Please update it.'
                             %(name, version, branch))
        else:
            latticeid= self.savelatticeinfo(name, version, branch, **params)

        latticetypename=None
        if params.has_key('latticetype') and params['latticetype'] != None:
            try:
                latticetypename=params['latticetype']["name"]
            except:
                pass
        try:
            cur = self.conn.cursor()
            if params.has_key('lattice') and params['lattice'] != None:

                # save lattice data
                if latticetypename == 'plain':
                    self._savetabformattedlattice(cur, latticeid, params['lattice'])
                elif latticetypename == 'tracy3' or latticetypename == 'tracy4':
                    self._savetracylattice(cur, latticeid, params['lattice'])
                elif latticetypename == 'elegant':
                    self._saveelegantlattice(cur, latticeid, params['lattice'])
                else:
                    raise ValueError('Unknown lattice type (%s)' %(latticetypename))
            if self.transaction:
                self.transaction.commit_unless_managed()
            else:
                self.conn.commit()
        except MySQLdb.Error as e:
            if self.transaction:
                self.transaction.rollback_unless_managed()
            else:
                self.conn.rollback()
            self.logger.info('Error when saving lattice:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when saving lattice:\n%s (%d)' %(e.args[1], e.args[0]))
        
        return latticeid

    def _checkelementbylatticeid(self, cursor, latticeid):
        sql = '''select count(element_id) from element where lattice_id = %s'''
        cursor.execute(sql, (latticeid))
        res=cursor.fetchone()
        return res

    def updatelattice(self, name, version, branch, **params):
        '''
        update lattice data.
        parameters:
            name:        lattice name
            version:     version number
            branch:      branch name
            latticetype: a dictionary which consists of {'name': , 'format': }
                         it is a predefined structure: [{'name': 'plain', 'format': 'txt'},
                                                        {'name': 'tracy3',  'format': 'lat'},
                                                        {'name': 'tracy4',  'format': 'lat'},
                                                        {'name': 'elegant', 'format': 'lte'},
                                                        {'name': 'xal',     'format': 'xdxf'}]
            
            description: description for this lattice, allow user put any info here (< 255 characters)
            creator:     original creator
            lattice:     lattice data, a dictionary:
                         {'name': ,
                          'data': ,
                          'map': {'name': 'value'},
                          'raw': ,
                          'alignment': 
                         }
                         name: file name to be saved into disk, it is same with lattice name by default
                         data: lattice geometric and strength with predefined format
                         raw:  raw data that is same with data but in original lattice format
                         map:  name-value pair dictionary
                         alignment: mis-alignment information
            
        return: True if success, otherwise, raise an exception
        '''
        _, lattices = self.retrievelatticeinfo(name, version, branch)
        if len(lattices) == 0:
            raise ValueError('Cannot find lattice (name: %s, version: %s, branch: %s) information.'
                             %(name, version, branch))
        elif len(lattices) > 1:
            raise ValueError('Lattice (name: %s, version: %s, branch: %s) information is not unique.'
                             %(name, version, branch))
        else:
            for k, _ in lattices.iteritems():
                latticeid = k
        try:
            sql = '''select count(url) from lattice where lattice_id = %s'''
            cur=self.conn.cursor()
            cur.execute(sql, (latticeid))
            res=cur.fetchone()
            if res[0] > 0:
                raise ValueError("Lattice file exists already. Give up.")

            self._checkelementbylatticeid(cur, latticeid)
            if res[0] > 0:
                raise ValueError("Lattice geometric and strength is there already. Give up.")
        except MySQLdb.Error as e:
            self.logger.info('Error when checking lattice elements:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when checking lattice elements:\n%s (%d)' %(e.args[1], e.args[0]))

        self.updatelatticeinfo(name, version, branch, **params)

        latticetypename=None
        if params.has_key('latticetype') and params['latticetype'] != None:
            # lattice type has been given.
            # try to get lattice type id
            try:
                latticetypename=params['latticetype']["name"]
            except:
                pass
        try:
            cur = self.conn.cursor()
            if params.has_key('lattice') and params['lattice'] != None:
                # save lattice data
                if latticetypename == 'plain':
                    latticeid = self._savetabformattedlattice(cur, latticeid, params['lattice'])
                elif latticetypename == 'tracy3' or latticetypename == 'tracy4':
                    latticeid = self._savetracylattice(cur, latticeid, params['lattice'])
                elif latticetypename == 'elegant':
                    latticeid = self._saveelegantlattice(cur, latticeid, params['lattice'])
                else:
                    raise ValueError('Unknown lattice type (%s)' %(latticetypename))
            if self.transaction:
                self.transaction.commit_unless_managed()
            else:
                self.conn.commit()
        except MySQLdb.Error as e:
            if self.transaction:
                self.transaction.rollback_unless_managed()
            else:
                self.conn.rollback()
            self.logger.info('Error when saving lattice:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when saving lattice:\n%s (%d)' %(e.args[1], e.args[0]))
        return True

    def _isbinary(self, filename):
        """Return true if the given filename is binary.
        @raise EnvironmentError: if the file does not exist or cannot be accessed.
        @attention: found @ http://bytes.com/topic/python/answers/21222-determine-file-type-binary-text on 6/08/2010
        @author: Trent Mick <TrentM@ActiveState.com>
        @author: Jorge Orpinel <jorge@orpinel.com>"""
        fin = open(filename, 'rb')
        try:
            CHUNKSIZE = 1024
            while 1:
                chunk = fin.read(CHUNKSIZE)
                if '\0' in chunk: # found null byte
                    return True
                if len(chunk) < CHUNKSIZE:
                    break # done
            # A-wooo! Mira, python no necesita el "except:". Achis... Que listo es.
        finally:
            fin.close()
        return False

    def retrievelattice(self, name, version, branch, description=None, creator=None, latticetype=None, withdata=False, rawdata=False):
        '''
        Retrieve lattice geometric layout with magnetic strength. All information are provided here, 
        which is able to construct a desired lattice deck.
        Parameters:
            name:        lattice name
            version:     lattice version
            branch:      lattice branch
            description: lattice description
            latticetype: a dictionary to identify lattice type {'name': , 'format': }
                         By default, a tab formatted table is provided. 
                         Other format to be implemented later.
            withdata:    flag to identify to get real lattice data with head or not.
                         True  -- get the lattice geometric and strength
                         False -- get lattice header description only
                         False by default.
            rawdata:     flag to identify whether to get raw file back.
                         This flag will try to get the raw data received.
        
        return: a lattice table
            {'id':  # identifier of this lattice
                    {'lattice name':                       # lattice name
                     'version': ,                 # version of this lattice
                     'branch': ,                  # branch this lattice belongs to
                     'description':  [optional],  # lattice description
                     'creator':      [optional],  # who created this lattice first time
                     'originalDate': [optional],  # when this lattice was create first time
                     'updated':      [optional],  # who updated last time
                     'lastModified': [optional],  # when this lattice was updated last time
                     'latticeType':  [optional],  # lattice type name
                     'latticeFormat':[optional],  # lattice type format
                     'lattice':      [optional],  # real lattice data
                     'rawlattice':   [optional],  # raw lattice data the server received
                     'map':          [optional]   # file map. A dictionary which has name-value pair
                    } 
             }
        '''
        urls, lattices = self.retrievelatticeinfo(name, version, branch, description=description, latticetype=latticetype, creator=creator)
        if len(lattices) == 0:
            return {}

        if withdata:
            sql = '''
            select e.element_order, e.element_name, e.element_id, e.s, e.length, e.dx, e.dy, e.dz, e.pitch, e.yaw, e.roll,
            et.element_type_name,
            ep.element_prop_value, ep.element_prop_unit,
            etp.element_type_prop_name, etp.element_type_prop_unit 
            from element e
            left join element_type et on e.element_type_id = et.element_type_id
            left join element_prop ep on ep.element_id = e.element_id
            left join element_type_prop etp on etp.element_type_prop_id = ep.element_type_prop_id
            where 
            e.lattice_id = %s
            order by element_order
            '''
            for k, v in lattices.iteritems():
                latticeid = k
                cur=self.conn.cursor()
                cur.execute(sql, (latticeid, ))
                results = cur.fetchall()
                tempdict = {}
                columns = []
                typepropunits={}
                for res in results:
                    typeproplist = []
                    etypename = res[11]
                    if tempdict.has_key(res[0]):
                        innerdict = tempdict[res[0]]
                        if res[14] != None and res[12] != None:
                            if innerdict.has_key('typeprops'):
                                typeproplist = innerdict['typeprops']
                            if res[14] not in columns:
                                columns.append(res[14])
                            if res[14] not in typeproplist:
                                typeproplist.append(res[14])
                                innerdict['typeprops'] = typeproplist
                            if res[13] != None:
                                innerdict[res[14]] = [res[12], res[13]]
                            else:
                                innerdict[res[14]] = [res[12]]
                            if res[15] != None:
                                # assume tracy if key is K for BENDING, QUADRUPOLE, and SEXTUPOLE
                                if res[14]=='K':
                                    if etypename.upper() in ['BENDING','QUADRUPOLE']:
                                        typepropunits['K1'] = res[15]
                                    elif etypename.upper() == 'SEXTUPOLE':
                                        typepropunits['K2'] = res[15]
                                    else:
                                        typepropunits[res[14]] = res[15]
                                else:
                                    typepropunits[res[14]] = res[15]
                    else:
                        innerdict={'name': res[1],
                                   'id': res[2],
                                   'position': res[3],
                                   'length': res[4],
                                   'type': res[11]
                                  }
                        if res[5] != None:
                            innerdict['dx'] = res[5]
                            columns.append('dx')
                        if res[6] != None:
                            innerdict['dy'] = res[6]
                            columns.append('dy')
                        if res[7] != None:
                            innerdict['dz'] = res[7]
                            columns.append('dz')
                        if res[8] != None:
                            innerdict['pitch'] = res[8]
                            columns.append('pitch')
                        if res[9] != None:
                            innerdict['yaw'] = res[9]
                            columns.append('yaw')
                        if res[10] != None:
                            innerdict['roll'] = res[10]
                            columns.append('roll')
                        
                        if res[14] != None and res[12] != None:
                            if res[14] not in columns:
                                columns.append(res[14])
                            if res[14] not in typeproplist:
                                typeproplist.append(res[14])
                                innerdict['typeprops'] = typeproplist                            
                            if res[13] != None:
                                innerdict[res[14]] = [res[12], res[13]]
                            else:
                                innerdict[res[14]] = [res[12]]
                            if res[15] != None:
                                # assume tracy if key is K for BENDING, QUADRUPOLE, and SEXTUPOLE
                                if res[14]=='K':
                                    if etypename.upper() in ['BENDING','QUADRUPOLE']:
                                        typepropunits['K1'] = res[15]
                                    elif etypename.upper() == 'SEXTUPOLE':
                                        typepropunits['K2'] = res[15]
                                    else:
                                        typepropunits[res[14]] = res[15]
                                else:
                                    typepropunits[res[14]] = res[15]
                    tempdict[res[0]] = innerdict
                        
                if len(columns) > 0:
                    tempdict['columns'] = columns
                if typepropunits:
                    tempdict['typeunit'] = typepropunits
                v['lattice'] = tempdict
                lattices[k] = v
        if urls and (withdata or rawdata):
            for k, v in urls.iteritems():
                if v != None:
                    maps = {}
                    if os.path.isdir(v+'_map'):
                        for path, _, files in os.walk(v+'_map'):
                            for name in files:
                                isbinary = self._isbinary(os.path.join(path, name))
                                with file(os.path.join(path, name), 'r') as f:
                                    if isbinary:
                                        # binary read file data
                                        maps[name] = base64.b64encode(f.read())
                                    else:
                                        #read as text file
                                        maps[name] = f.readlines()
                    if len(maps) > 0:
                        temp = lattices[k]
                        temp['map'] = maps
                        lattices[k] = temp
                    if rawdata:
                        temp=lattices[k]
                        try:
                            with file(v, 'r') as f:
                                data = f.readlines()
                            basefile=os.path.basename(v)
                            basefile=os.path.splitext(basefile)
                            v=basefile[0][:-7]+basefile[1]
                        except IOError:
                            data = 'No raw lattice file found.'
                        
                        temp['rawlattice'] = {'name': v, 'data': data}
                        lattices[k]=temp

        return lattices
        
    def retrieveelemtype(self, etypename):
        '''
        Retrieve element type information with given element type name.
        
        Wildcast matching for element type name are provided.
            * for multiple characters matching
            ? for single character matching
        
        return: a tuple of (element type id, element type property id, 
                            element type name, element type property name,
                            element type property unit)
        '''
        sql = '''
        select 
        element_type.element_type_id, element_type_prop_id, element_type_name, element_type_prop_name, element_type_prop_unit
        from element_type
        left join element_type_prop on element_type.element_type_id = element_type_prop.element_type_id
        where element_type_name
        '''
        etypename = _wildcardformat(etypename)
        if '_' in etypename or '%' in etypename:
            sql += " like %s"
        elif etypename == "":
            sql += " like %s"
            etypename = "*"
        else:
            sql += " = %s "
        try:
            cur=self.conn.cursor()
            cur.execute(sql, (etypename,))
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching element type information:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when fetching element type information:\n%s (%d)' %(e.args[1], e.args[0]))
        
        return res
        
    def saveelemtype(self, etypename, etypeprops, etypepropunits=None):
        '''
        Save element type, and its associated properties.
        parameters:
            etypename: element type name
            etypeprops: lsit of all property names for given element type
            etypepropunits: a dictionary, which has type property as its key, and unit for that property as its value.
        
        use updateelemtypeprop() if element type exists already.
        
        return: element type id if success, raise an exception when element type exists already.
        '''
        res = self.retrieveelemtype(etypename)
        if len(res) != 0:
            raise ValueError("Element type (%s) exists already."%(etypename))
        
        try:
            sql = '''
            insert into element_type
            (element_type_name)
            values (%s) '''
            cur=self.conn.cursor()
            cur.execute(sql, (etypename,))
            etypeid = cur.lastrowid
            
            if len(etypeprops) != 0:
                sql = '''
                insert into element_type_prop
                (element_type_id, element_type_prop_name, element_type_prop_unit)
                values
                '''
                for etypeprop in etypeprops:
                    etypepropunit = None
                    if etypepropunits.has_key(etypeprop):
                        etypepropunit = etypepropunits[etypeprop]
                    sql += ''' (%s, '%s', ''' %(etypeid, etypeprop)
                    if etypepropunit != None:
                        sql += ''' '%s'),''' %etypepropunit
                    else:
                        sql += '''NULL),'''
                sql = sql[:-1]
                cur.execute(sql)
            if self.transaction:
                self.transaction.commit_unless_managed()
            else:
                self.conn.commit()
        except MySQLdb.Error as e:
            if self.transaction:
                self.transaction.rollback_unless_managed()
            else:
                self.conn.rollback()
            self.logger.info('Error when saving lattice:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when saving lattice:\n%s (%d)' %(e.args[1], e.args[0]))
        return etypeid
    
    def updateelemtypeprop(self, etypename, etypeprop, etypepropunits=None):
        '''
        Add a new entry to element type property table
        parameters:
            etypename: element type name
            etypeprops: lsit of all property names for given element type
            etypepropunits: a dictionary, which has type property as its key, and unit for that property as its value.
                    
        use saveelemtype() if element type does not exist yet.
        
        return: element type property id if success, otherwise, raise an exception.
        '''
        res = self.retrieveelemtype(etypename)
        if len(res) == 0:
            raise ValueError("Can not find element type (%s)."%(etypename))
        else:
            elementtypeid = res[0][0]
    
        try:
            sql = '''
            select element_type_id 
            from element_type_prop
            where element_type_id = %s and element_type_prop_name = %s
            '''
            cur=self.conn.cursor()
            cur.execute(sql, (elementtypeid, etypeprop, ))
            results = cur.fetchone()
            if results != None:
                raise ValueError('property for given element type exist already.')
            
            sql = '''
            insert into element_type_prop
            (element_type_id, element_type_prop_name, element_type_prop_unit)
            values
            '''
            try:
                cur.execute(sql + "(%s, %s, %s)", (elementtypeid, etypeprop, etypepropunits[etypeprop]))
            except KeyError:
                cur.execute(sql + "(%s, %s, NULL)", (elementtypeid, etypeprop,))
            etypepropid = cur.lastrowid
            if self.transaction:
                self.transaction.commit_unless_managed()
            else:
                self.conn.commit()
        except MySQLdb.Error as e:
            if self.transaction:
                self.transaction.rollback_unless_managed()
            else:
                self.conn.rollback()
            self.logger.info('Error when saving element type (%s) property (%s):\n%s (%d)' 
                             %(etypename, etypeprop, e.args[1], e.args[0]))
            raise Exception('Error when saving element type (%s) property (%s):\n%s (%d)' 
                            %(etypename, etypeprop, e.args[1], e.args[0]))
        return etypepropid
    
    def retrievelatticestatus(self, name, version, branch, status=0, ignorestatus=False):
        '''
        Get lattice status with given name, version, branch, and other conditions
        parameters:
            name:    lattice name
            version: lattice version
            branch:  lattice branch
            status:  0: current golden lattice
                     1: alternative golden lattice
                     2: lattice from live machine
                     3: previous golden lattice, but not any more
                     other number can be defined by a user
            ignorestatus: get all lattice no matter whatever its status is.
        '''
        name = _wildcardformat(name)
        branch = _wildcardformat(branch)
        if isinstance(version, (str, unicode)):
            version = _wildcardformat(version)
        if isinstance(status, (str, unicode)):
            status = _wildcardformat(status)
        sql = '''
        select gold_lattice_id, lattice_name, lattice_version, lattice_branch, 
               gl.created_by, gl.create_date,
               gl.updated_by, gl.update_date,
               gl.gold_status_ind, gl.lattice_id
        from gold_lattice gl
        left join lattice on lattice.lattice_id = gl.lattice_id
        where
        lattice.lattice_name like %s and lattice.lattice_version like %s and lattice.lattice_branch like %s
        '''
        try:
            cur=self.conn.cursor()
            if ignorestatus:
                cur.execute(sql, (name, version, branch))
            else:
                cur.execute(sql+''' and gl.gold_status_ind like %s''', (name, version, branch, status))
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving golden lattice:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
            raise Exception('Error when retrieving golden lattice:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
        
        return res
    
    def savelatticestatus(self, name, version, branch, **params):
        '''
        Save a lattice status
        Parameters:
            name:    lattice name
            version: lattice version
            branch:  lattice branch
            creator: who craeted it, or changed the status last time
            status:  0: current golden lattice [by default]
                     1: current live lattice
                     2: alternative golden lattice
                     3: previous golden lattice, but not any more
                     other number can be defined by a user
        
        return: True if saving gold lattice successfully, otherwise, raise an exception
        '''
        creator = None
        if params.has_key('creator'):
            creator=params['creator']
        status = 0
        if params.has_key('status'):
            status=params['status']
        _, lattices = self.retrievelatticeinfo(name, version, branch)

        if len(lattices) != 1:
            raise ValueError("Can not find lattice (name: %s, version: %s, beanch: %s), or more than one found."%(name, version, branch))
        for k, _ in lattices.iteritems():
            latticeid = k
        # get all lattice no matter its status.
        res = self.retrievelatticestatus(name, version, branch, ignorestatus=True)
        
        if len(res) == 0:
            # if not found, flag lattice with given status.
            # by default, flag it as current golden lattice
            if creator == None:
                sql = '''
                insert into gold_lattice
                (lattice_id, created_by, create_date, gold_status_ind)
                values
                (%s, NULL, now(), %s)
                '''
                vals=(latticeid, status)
            else:
                sql = '''
                insert into gold_lattice
                (lattice_id, created_by, create_date, gold_status_ind)
                values
                (%s, %s, now(), %s)
                '''
                vals=(latticeid, creator, status)
        elif len(res) == 1:
            if creator == None:
                sql = '''
                update gold_lattice
                set gold_status_ind = %s, updated_by=NULL, update_date = now()
                where gold_lattice_id = %s 
                '''
                vals = (status, res[0][0])
            else:
                sql = '''
                update gold_lattice
                set gold_status_ind = %s, updated_by = %s, update_date = now()
                where gold_lattice_id = %s 
                '''
                vals = (status, creator, res[0][0])
        else:
            raise ValueError('More than one golden lattice found for given lattice (name: %s, version: %s, beanch: %s)'
                             %(name, version, branch))
        try:
            cur=self.conn.cursor()
            cur.execute(sql, vals)
            if self.transaction:
                self.transaction.commit_unless_managed()
            else:
                self.conn.commit()
        except MySQLdb.Error as e:
            if self.transaction:
                self.transaction.rollback_unless_managed()
            else:
                self.conn.rollback()
                
            self.logger.info('Error when saving golden lattice:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
            raise Exception('Error when saving golden lattice:\n%s (%d)' 
                             %(e.args[1], e.args[0]))

        return True

