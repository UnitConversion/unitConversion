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

from utils import (_assemblesql, _wildcardformat)

class lattice(object):
    def __init__(self, conn):
        ''''''
        self.logger = logging.getLogger('lattice')
        hdlr = logging.FileHandler('/var/tmp/lattice.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.WARNING)

        self.conn = conn

    def retrievelatticelist(self, name, version=None, branch=None, description=None):
        '''
        retrieve lattice header information. It gives lattice name, description, version, branch, 
        created info (by who & when), updated info (by who & when)
        according given information.
        Real lattice data (geometric layout and strength can be retrieved thru retrievelattice())
        
        return: dictionary with format
                {'lattice name': {'id': ,                      # identifier of this lattice
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
            [{'name': 'tab flat', 'format': 'txt'},
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
            tempdict = {'id': r[0],
                        'version': r[2],
                        'branch': r[3]}
            if r[4] != None:
                tempdict['description'] = r[4]
            if r[5] != None:
                tempdict['creator'] = r[5]
            if r[6] != None:
                tempdict['originalDate'] = r[6].isoformat()
            if r[7] != None:
                tempdict['update'] = r[7]
            if r[8] != None:
                tempdict['lastModified'] =  r[8].isoformat()
            if r[9] != None:
                tempdict['latticeType'] = r[9]
            if r[10] != None:
                tempdict['latticeFormat'] = r[10]
            resdict[r[1]] = tempdict
            urls[r[1]] = r[11]
        return urls, resdict

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
        [{'name': 'tab flat', 'format': 'txt'},
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
            self.conn.commit()
            res = cur.lastrowid
        except MySQLdb.Error as e:
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
                raise
    
        fd, filename = tempfile.mkstemp(suffix, prefix+"_", dirname)
        return fd, filename

    def _processlatticedata(self, latticefile, latticedata, latticetypeid=0, savefile=True):
        '''
        latticefile: lattice file name
        latticedata: body having real data
        
        latticetypeid: identify lattice file format id: 
            0. tab format; 1. tracy-3 format; 2. tracy-4 format; 3. elegant format
            By default, it is 0, which means a tab-formatted lattice.
            at current stage, only tab-formatted lattice is supported.
        
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
                    f.write(data)
        
        # keep element order
        elemdict = OrderedDict()
        unitdict = {}
        if latticetypeid == 0:
            # tab formatted lattice file
            if len(latticedata) <= 3:
                # do nothing since no real data
                return url, elemdict, unitdict
            latticehead = latticedata[:3]
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
            cols = latticehead[0].split()
            #if cols[0].startswith('#') or cols[0].startswith('!'):
            #    cols = cols[1:]
            units = latticehead[1].split()
            #if units[0].startswith('#') or units[0].startswith('!'):
            #    units = units[1:]

            skipcount = 0
            unitdict={}
            for i in range(len(cols)):
                if str.lower(cols[i]) in ['elementtype', 'type', 'elementname', 'name', 'map', 'kickmap', 'fieldmap']:
                    skipcount += 1
                else:
                    unitdict[cols[i]] = units[i-skipcount]
                

            latticebody = latticedata[3:]
            for i in range(len(latticebody)):
                body = latticebody[i]
                attrs = body.split()
                
                # the line is not empty and not commented out by "#" or "!"
                if not attrs[0].startswith('#') and not attrs[0].startswith('!') and len(attrs) > 0:
                    tmpdict = {}
                    typeprop = []
                    for j in range(len(attrs)):
                        temp = str.lower(cols[j])
                        if temp in ['elementname', 'name']:
                            tmpdict['name'] = attrs[j]
                        elif temp in ['elementtype', 'type']:
                            tmpdict['type'] = attrs[j]
                        elif temp in ['l', 'length']:
                            tmpdict['length'] = attrs[j]
                        elif temp in ['s', 'position']:
                            tmpdict['position'] = attrs[j]
                        elif temp in ['map', 'kickmap', 'fieldmap']:
                            tmpdict['map'] = attrs[j]
                        else:
                            if float(attrs[j]) != 0.0:
                                typeprop.append(cols[j])
                                tmpdict[cols[j]] = attrs[j]
                    tmpdict['typeprop'] = typeprop
                    elemdict[str(i)] = tmpdict
        elif latticetypeid == 1:
            # tracy-3 format
            raise TypeError("tracy-3 lattice format is not supported yet.")
        elif latticetypeid == 2:
            # tracy-4 format
            raise TypeError("tracy-4 lattice format is not supported yet.")
        elif latticetypeid == 3:
            # elegant format
            raise TypeError("elegant lattice format is not supported yet.")
        else:
            raise TypeError("unknown lattice format.")
        
        # remove duplicates in typelist, not order preserving since it does not matter
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
                      'data':
                     }
        '''
        if not isinstance(lattice, dict) or not lattice.has_key('name') or not lattice.has_key('data'):
            raise ValueError('No lattice data found.')
        
        latticefile = lattice['name']
        latticedata = lattice['data']
        # pre-process and reorganize the data
        url, elemdict, unitdict = self._processlatticedata(latticefile, 
                                                           latticedata,
                                                           latticetypeid=0)
        if url != None:
            sql = '''update lattice SET url = %s '''
            cur.execute(sql,(url, ))

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
                    for etypeprop in etypeprops:
                        if not tempdict.has_key(etypeprop):
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
                            tempdict = {'id': res[0]}
                            if res[4] == None:
                                tempdict[res[3]] = [res[1]]
                            else:
                                tempdict[res[3]] = [res[1], res[4]]
                        typedict.update({etypename: tempdict})
                    else:
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
                                if typeins[1] == None:
                                    raise ValueError ('type (%s) property (%s) id is empty'%(typeins[2], typeins[3]))
                                elif typeins[4] == None:
                                    tempdict[typeins[3]] = [typeins[1]]
                                else:
                                    tempdict[typeins[3]] = [typeins[1], typeins[4]]
                        typedict.update({etypename: tempdict})
                 
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
                            elempropsql += '''(%s, %s, %s, %s),'''%(elementid, 
                                                                    typedict[etypename][etypeprop][0],
                                                                    v[etypeprop],
                                                                    unitdict[etypeprop])
                        else:
                            elempropsql += '''(%s, %s, %s, NULL),'''%(elementid, 
                                                                      typedict[etypename][etypeprop][0],
                                                                      v[etypeprop])
                    elif len(etypeproptidunit) == 1:
                        # no unit
                        elempropsql += '''(%s, %s, %s, NULL),'''%(elementid, 
                                                                  typedict[etypename][etypeprop][0],
                                                                  v[etypeprop])
                    else:
                        raise TypeError("Unknown structure for element type property value and unit.")
            # get rid of last comma from SQL statement.
            # save element type property value
            cur.execute(elempropsql[:-1])

    def _savetracy3lattice(self, cur, latticeid, params):
        '''
        '''
        print("To be implemented later")
    def _savetracy4lattice(self, cur, latticeid, params):
        '''
        '''
        print("To be implemented later")
    def _saveelegantlattice(self, cur, latticeid, params):
        '''
        '''
        print("To be implemented later")

    def savelattice(self, name, version, branch, latticetype=None, **params):
        '''
        Save lattice header information.
        Note: the update should be dropped since lattice has
        parameters:
            name:        lattice name
            version:     version number
            branch:      branch name
            latticetype: a dictionary which consists of {'name': , 'format': }
                         it is a predefined structure: [{'name': 'tab flat', 'format': 'txt'},
                                                        {'name': 'tracy3',  'format': 'lat'},
                                                        {'name': 'tracy4',  'format': 'lat'},
                                                        {'name': 'elegant', 'format': 'lte'},
                                                        {'name': 'xal',     'format': 'xdxf'}]
                         a lattice identifier is determined by the lattice type dictionary, which are as below:
                             0. tab format; 
                             1. tracy-3 format; 
                             2. tracy-4 format; 
                             3. elegant format
            
            description: description for this lattice, allow user put any info here (< 255 characters)
            creator:     original creator
            lattice:     lattice data, a dictionary:
                         {'name': ,
                          'data':
                         }
                         name: file name to be saved into disk, it is same with lattice name by default
                         data: lattice geometric and strength with predefined format
        
        return: lattice id if success, otherwise, raise an exception
        '''

        latticetypeid = None
        
        if latticetype != None:
            # lattice type has been given.
            # try to get lattice type id
            latticetypename=None
            latticetypeformat=None
            try:
                latticetypename=latticetype["name"]
                latticetypeformat=latticetype["format"]
            except:
                pass
            latticetypeid = self.retrievelatticetype(latticetypename, latticetypeformat)
            if len(latticetypeid) == 1:
                # get lattice type id
                latticetypeid = latticetypeid[0][0]
            else:
                # no lattice type found, or more than one found.
                raise ValueError("Does not support lattice with given type (%s) and format (%s)"%(latticetypename, latticetypeformat))

        latticeid = None
        try:
            cur = self.conn.cursor()
            _, res = self.retrievelatticelist(name, version, branch)

            desc = None
            if params.has_key('description'):
                desc = params['description']
            creator = None
            if params.has_key('creator'):
                creator = params['creator']

            if len(res) == 0:
                # no lattice entry found.
                # add a new one
                sql = '''
                insert into lattice 
                (lattice_type_id, lattice_name, lattice_version, lattice_branch, lattice_description, created_by, create_date) 
                values
                (%s, %s, %s, %s, %s, %s, now())
                '''
                cur.execute(sql,(latticetypeid, name, version, branch, desc, creator))
                # cursor.lastrowid is a dbapi/PEP249 extension supported by MySQLdb.
                # it is cheaper than connection.insert_id(), and much more cheaper than "select last_insert_id()"
                # it is per connection.
                latticeid = cur.lastrowid
            elif len(res) == 1:
                # a unique lattice entry founded
                # ensure there is no any element associated with this lattice
                lattice=res.itervalues().next()
                
                latticeid = lattice['id']
                sql = '''
                select element_id from element where lattice_id = %s limit 1;
                '''
                cur.execute(sql, (latticeid,))
                
                if cur.fetchone() == None:
                    sql = '''
                    update lattice 
                    set updated_by = %s, update_date = now()
                    '''
                    cur.execute(sql, (creator,))
                else:
                    self.conn.rollback()
                    raise ValueError('lattice %s (version: %s, branch: %s) is not empty'
                                     %(name, version, branch))
            else:
                # more than one lattice found
                # this should never happen
                self.conn.rollback()
                raise ValueError('More than one lattice found for %s (version: %s, branch %s)'
                                 %(name, version, branch))
            
            if params.has_key('lattice'):
                # save lattice data
                if latticetypename == 'tab flat':
                    latticeid = self._savetabformattedlattice(cur, latticeid, params['lattice'])
                elif latticetypename == 'tracy3':
                    latticeid = self._savetracy3lattice(cur, latticeid, params['lattice'])
                elif latticetypename == 'tracy4':
                    latticeid = self._savetracy4lattice(cur, latticeid, params['lattice'])
                elif latticetypename == 'elegant':
                    latticeid = self._saveelegantlattice(cur, latticeid, params['lattice'])
                else:
                    raise ValueError('Unknown lattice type (%s)' %(latticetypename))
            self.conn.commit()
        except MySQLdb.Error as e:
            self.conn.rollback()
            self.logger.info('Error when saving lattice:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when saving lattice:\n%s (%d)' %(e.args[1], e.args[0]))
        return latticeid

    def retrievelattice(self, name, version, branch, description=None, latticetype=None, withdata=False, rawdata=False):
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
            {'lattice name': {'id': ,                      # identifier of this lattice
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
                              'rawlattice':   [optional]   # raw lattice data the server received
                             } 
             }
        '''
        urls, lattices = self.retrievelatticelist(name, version, branch, description=description)
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
                latticeid = v['id']
                cur=self.conn.cursor()
                cur.execute(sql, (latticeid, ))
                results = cur.fetchall()
                tempdict = {}
                columns = []
                typepropunits={}
                for res in results:
                    typeproplist = []
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
                                typepropunits[res[14]] = res[15]
                    tempdict[res[0]] = innerdict
                        
                if len(columns) > 0:
                    tempdict['columns'] = columns
                if typepropunits:
                    tempdict['typeunit'] = typepropunits
                v['lattice'] = tempdict
                lattices[k] = v
        if rawdata and urls:
            for k, v in urls.iteritems():
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
                
            self.conn.commit()
        except MySQLdb.Error as e:
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
            insert into element_type_prop
            (element_type_id, element_type_prop_name, element_type_prop_unit)
            values
            '''
            cur=self.conn.cursor()
            try:
                sql += "(%s, %s, %s)"
                cur.execute(sql, (elementtypeid, etypeprop, etypepropunits[etypeprop]))
            except:
                sql += "(%s, %s, NULL)"
                cur.execute(sql, (elementtypeid, etypeprop,))
            etypepropid = cur.lastrowid
        except MySQLdb.Error as e:
            self.conn.rollback()
            self.logger.info('Error when saving element type (%s) property (%s):\n%s (%d)' 
                             %(etypename, etypeprop, e.args[1], e.args[0]))
            raise Exception('Error when saving element type (%s) property (%s):\n%s (%d)' 
                            %(etypename, etypeprop, e.args[1], e.args[0]))
        return etypepropid
    
    def retrievegoldlattice(self, name, version, branch, **params):
        '''
        Get golden lattice with given name, version, branch, and other conditions
        parameters:
            name:    lattice name
            version: lattice version
            branch:  lattice branch
            status:  0: used to be a golden lattice, but not any more
                     1: alternative golden lattice
                     2: current golden lattice
        '''
        name = _wildcardformat(name)
        branch = _wildcardformat(branch)
        if isinstance(version, (str, unicode)):
            version = _wildcardformat(version)
        status = "%"
        if params.has_key('status'):
            status = params['status']
            if isinstance(status, (str, unicode)):
                status = _wildcardformat(params['status'])
        sql = '''
        select gold_lattice_id, lattice_name, lattice_version, lattice_branch, 
               gl.created_by, gl.create_date,
               gl.updated_by, gl.update_date,
               gl.gold_status_ind
        from gold_lattice gl
        left join lattice on lattice.lattice_id = gl.lattice_id
        where
        lattice.lattice_name like %s and lattice.lattice_version like %s and lattice.lattice_branch like %s
        and gl.gold_status_ind like %s
        '''
        try:
            cur=self.conn.cursor()
            cur.execute(sql, (name, version, branch, status))
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when retrieving golden lattice:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
            raise Exception('Error when retrieving golden lattice:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
        
        return res
    
    def savegoldlattice(self, name, version, branch, **params):
        '''
        Set a lattice to a golden lattice
        Parameters:
            name:    lattice name
            version: lattice version
            branch:  lattice branch
            creator: who craeted it, or changed the status last time
            status:  0: used to be a golden lattice, but not any more
                     1: alternative golden lattice
                     2: current golden lattice
        
        return: True if saving gold lattice successfully, otherwise, raise an exception
        '''
        creator = None
        if params.has_key('creator'):
            creator=params['creator']
        status = 2
        if params.has_key('status'):
            status=params['status']
        _, lattices = self.retrievelatticelist(name, version, branch)
        for _, lattice in lattices.iteritems():
            latticeid = lattice['id']
        res = self.retrievegoldlattice(name, version, branch)
        if len(res) == 0:
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
        else:
            if creator == None:
                sql = '''
                update gold_lattice
                set gold_status_ind = %s, update_date = now() 
                '''
                vals = (status)
            else:
                sql = '''
                update gold_lattice
                set gold_status_ind = %s, updated_by = %s, update_date = now() 
                '''
                vals = (status, creator)
        try:
            cur=self.conn.cursor()
            cur.execute(sql, vals)
            self.conn.commit()
        except MySQLdb.Error as e:
            self.conn.rollback()
            self.logger.info('Error when saving golden lattice:\n%s (%d)' 
                             %(e.args[1], e.args[0]))
            raise Exception('Error when saving golden lattice:\n%s (%d)' 
                             %(e.args[1], e.args[0]))

        return True
