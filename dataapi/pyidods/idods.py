import logging
import MySQLdb

from collections import OrderedDict
from dataapi.utils import (_wildcardformat)
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

        # use django transaction manager
        self.transaction = transaction

    def _retrievevendor(self, vendorname):
        '''
        Retrieve vendor by its name

        parameters:
            vendorname:     name of the vendor we are looking for

        return: vendor
        '''

        try:
            cur = self.conn.cursor()

            # Generate SQL statement
            sql = '''
            select vendor_id, vendor_name, vendor_description from vendor where vendor_name = %s
            '''
            cur.execute(sql, (vendorname,))
            # get any one since it should be unique
            res = cur.fetchall()

        except MySQLdb.Error as e:
            self.logger.info('Error when fetching vendor:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when fetching vendor:\n%s (%d)' %(e.args[1], e.args[0]))

        return res

    def saveinventory(self, name, **kws):
        '''
        save insertion device into inventory using any of the acceptable key words:

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

        :Raises: ValueError, AttributeError

        '''

        # Check name parameter
        res = self.retrieveinventory(name)
        if len(res) != 0:
            raise ValueError("Insertion device (%s) exists in inventory already." % (name))

        # Check device type parameter
        dtypeid=None

        if kws.has_key('dtype') and kws['dtype'] != None:
            res = self.retrievecomponenttype(kws['dtype'])

            if len(res) != 1:
                raise ValueError("Insertion device type (%s) does not exist."%(kws['dtype']))
            else:
                dtypeid=res(0)

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
            vendor = kws['vendor']
            res = self._retrievevendor(vendor);

            if(len(res) == 0):
                raise ValueError("Vendor with name (%s) doen't exist." % (vendor));

        # Check properties parameter
        props=None

        if kws.has_key('props') and kws['props'] != None:
            props = kws['props']


    def retrieveinventory(self, invname):
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
                         'dtype':                       # string
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

        :Raises: Exception

        '''

        try:
            cur = self.conn.cursor()
            sql = '''
            select inv.inventory_id, inv.name, inv.alias, inv.serial_no,
            ctype.name, ctype.description,
            vendor.name,
            invp.length, invp.up_corrector_position, invp.middle_corrector_position, invp.down_corrector_position,
            invp.gap_min, invp.gap_max, invp.gap_tolerance,
            invp.phase1_min, invp.phase1_max,
            invp.phase2_min, invp.phase2_max,
            invp.phase3_min, invp.phase3_max,
            invp.phase4_min, invp.phase4_max,
            invp.phase_tolerance,
            invp.k_max_linear, invp.k_max_circular,
            invp.phase_mode_p, invp.phase_mode_a1, invp.phase_mode_a1
            from inventory_prop invp
            join inventory inv on invp.inventory_id = inv.inventory_id
            join vendor on vendor.vendor_id = inv.vendor_id
            join cmpnt_type ctype on ctype.cmpnt_type_id = inv.cmpnt_type_id
            where inv.name
            '''
            if '*' in invname or '?' in invname:
                sql += ''' like %s '''
                cur.execute(sql, (_wildcardformat(invname), ))
            else:
                sql += ''' = %s '''
                cur.execute(sql, (invname,))
            # get any one since it should be unique
            res = cur.fetchall()
        except MySQLdb.Error as e:
            self.logger.info('Error when fetching insertion device inventory:\n%s (%d)' %(e.args[1], e.args[0]))
            raise Exception('Error when fetching insertion device inventory:\n%s (%d)' %(e.args[1], e.args[0]))

        return res

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

    def savecomponenttype(self, dtype, description=None):
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

        :Raises: KeyError, AttributeError

        '''

    def retrievecomponenttype(self, dtype, description=None):
        '''Retrieve a component type using the key words:

        - dtype
        - description

        :param dtype: device type name
        :type dtype: str

        :param description: description for this device
        :type desctiprion: str

        :return: a map with structure like:

            .. code-block: python

                {'id1': {'name': device type name, 'description': device type description},
                 ...
                }

        :Raises: KeyError, AttributeError
        '''

        sql = '''
        SELECT cmpnt_type_id, cmpnt_type_name, description FROM converter.cmpnt_type WHERE
        '''

        if dtype != None:
            raise AttributeError("Device type parameter (%s) doesn't exist." % (dtype));

        if '*' in description or '?' in description:
            sql += ''' description like %s '''
            cur.execute(sql, (_wildcardformat(description), ))

        else:
            sql += ''' description = %s '''
            cur.execute(sql, (description,))

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