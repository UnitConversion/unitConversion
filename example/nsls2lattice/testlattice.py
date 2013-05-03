'''
Created on Mar 19, 2013

@author: shengb
'''
from collections import OrderedDict

import MySQLdb
from pylattice import lattice

host=''
user = ''
pw = ''
db = ''
port = 3306

supportedlatticetype = [{'name': 'tab flat', 'format': 'txt'},
                        {'name': 'tracy3',  'format': 'lat'},
                        {'name': 'tracy4',  'format': 'lat'},
                        {'name': 'elegant', 'format': 'lte'},
                        {'name': 'xal',     'format': 'xdxf'}]

def connect():
    if host.startswith("/"):
        conn = MySQLdb.connect(unix_socket=host, user=user, passwd=pw, db=db)
    else:
        conn = MySQLdb.connect(host=host, user=user, passwd=pw, db=db, port=port)
        
    return conn

def savelattype(conn, lat):
    for latticetype in supportedlatticetype:
        try:
            lat.savelatticetype(latticetype['name'], latticetype['format'])
        except ValueError:
            pass
    print lat.retrievelatticetype("*")

def cleanrdb(conn):
    sql = '''
    delete from element_prop;
    delete from element;
    delete from element_type_prop;
    delete from element_type;
    '''
    conn.cursor().execute(sql)
    conn.commit()

def test_savelattice(conn, lat, latticefile, latticename):
    latticedata = {}
    with file(latticefile, 'r') as f:
        lines=f.readlines()
        latticedata.update({'name': latticefile,
                            'data': lines})
    if latticedata:
        latticeid = lat.savelattice(latticename, '20121003', 'test', 
                                    latticetype=supportedlatticetype[0], 
                                    description="CD3 lattice released on Oct 13, 2012",
                                    creator='Guobao Shen',
                                    lattice=latticedata)
    else:
        latticeid = lat.savelattice(latticename, '20121003', 'test', 
                                    latticetype=supportedlatticetype[0], 
                                    description="CD3 lattice released on Oct 13, 2012",
                                    creator='Guobao Shen')
    return latticeid

def test_retrievelattice(lat, name, version, branch):
    lattices = lat.retrievelattice(name, version, branch, withdata=True, rawdata=False)
    return lattices
    
def test_savegoldlattice(lat, name, version, branch, status):
    return lat.savegoldlattice('CD3-Oct3-12-30Cell-addID-par', '20121003', 'design', creator='Guobao', status=2)

def test_retrievegoldlattice(lat, name, version, branch, status):
    return lat.retrievegoldlattice(name, version, branch)

def preparetracy3lattice(latfile, twissfile):
    '''
    '''
    # this is not a general purpose routine
    # very specific to lattice input
    latdict=OrderedDict()
    
    with file(latfile,'r') as f:
        templine = ''
        rawlatticedata = f.readlines()
        for line in rawlatticedata:
            if not line.startswith('{') and ':' in line:
                if ';' in line:
                    templine += line
                    templine = ''
                    end=True
                else:
                    templine = line
                    end=False
                if end:
                    lineparts = line.strip()[:-1].split(':')
                    latdict[lineparts[0]] = lineparts[1]

    twissdict = OrderedDict()
    with file(twissfile, 'r') as f:
        for line in f.readlines():
            if not line.strip().startswith('#'):
                lineparts = line.split()
                twissdict[lineparts[0]] = {'name': lineparts[1].upper(),
                                           'position': lineparts[2]}
#    typedict = {}
#    unitdict = {}
    for k, v in twissdict.iteritems():
        if k != '0':
            # twiss file includes element 'BEGIN'
            props = [x.strip() for x in latdict[v['name']].split(',')]
            if props[0].upper() == 'CORRECTOR':
                # find direction info for corrector
                etype = props[0]
                for tmp in props[1:]:
                    if '=' not in tmp:
                        etype = ','.join((etype, tmp))
            else:
                etype = props[0]
            v['type'] = etype
#            if typedict.has_key(etype):
#                etypeproptemp = typedict[etype]
#            else:
#                etypeproptemp = []
            for tmp in props:
                if '=' in tmp:
                    tmpparts = [x.strip() for x in tmp.split('=')]
                    # update value
                    if tmpparts[0] in ['L','l']:
                        v['length'] = tmpparts[1]
                    else:
                        v[tmpparts[0]] = tmpparts[1]
                    
                    # update type and unit
#                    if tmpparts[0].upper() in ['T', 'T1', 'T2'] and tmpparts[0] not in etypeproptemp:
#                        etypeproptemp.append(tmpparts[0])
#                        unitdict[tmpparts[0]] = 'Degree'
#                    elif tmpparts[0].upper()  == 'K':
#                        if etype.upper() == 'QUADRUPOLE' and 'K1' not in etypeproptemp:
#                            etypeproptemp.append('K1')
#                            unitdict['K1'] = '1/m2'
#                        elif etype.upper() == 'SEXTUPOLE' and 'K2' not in etypeproptemp:
#                            etypeproptemp.append('K2')
#                            unitdict['K2'] = '1/m3'
#                        elif etype.upper() == 'BENDING' and 'K1' not in etypeproptemp:
#                            etypeproptemp.append('K1')
#                            unitdict['K1'] = '1/m2'
#                    elif tmpparts[0].upper() == 'FREQUENCY' and  tmpparts[0] not in etypeproptemp:
#                        etypeproptemp.append(tmpparts[0])
#                        unitdict[tmpparts[0]] = 'Hz'
#                    elif tmpparts[0].upper() == 'VOLTAGE' and  tmpparts[0] not in etypeproptemp:
#                        etypeproptemp.append(tmpparts[0])
#                        unitdict[tmpparts[0]] = 'Volt'
#                    elif tmpparts[0].upper() == 'PHASE' and  tmpparts[0] not in etypeproptemp:
#                        etypeproptemp.append(tmpparts[0])
#                        unitdict[tmpparts[0]] = 'Degree'
#                    elif tmpparts[0].upper() == 'L':
#                        pass
#                    elif tmpparts[0] not in etypeproptemp:
#                        etypeproptemp.append(tmpparts[0])
#            typedict[etype] = etypeproptemp
            twissdict[k] = v
        else:
            v['type'] = 'Marker'
            v['length'] = 0.0
            twissdict[k] = v
            
    # original lattice file can be save if adding a 'raw' in like
    # {'name': latfile, 'data': twissdict, 'raw': rawlatticedata}
    return {'name': latfile, 'data': twissdict}

def test_savetracylat(latfile, twissfile, latticename):
    '''
    save tracy-3 lattice
    '''
    latticedata = preparetracy3lattice(latfile, twissfile)
    latticeid = lat.savelattice(latticename, '20121003', 'test', 
                                latticetype=supportedlatticetype[1], 
                                description="CD3 lattice released on Oct 13, 2012",
                                creator='Guobao Shen',
                                lattice=latticedata)
    return latticeid

if __name__ == "__main__":
    import time
    start = time.time()

    conn = connect()
    lat = lattice(conn)
    
    cleanrdb(conn)

    print 'test case 0'
    latticefile = 'CD3-Oct3-12-30Cell-addID-par.txt'
    latticename = 'CD3-Oct3-12-30Cell-addID-par'
    test_savelattice(conn, lat, latticefile, latticename)

    print 'test case 1'
    latticefile = 'CD3-Oct3-12-30Cell-addID-par-YLi.txt'
    latticename = 'CD3-Oct3-12-30Cell-addID-par-YLi'
    test_savelattice(conn, lat, latticefile, latticename)

    print 'test case 2'
    latticefile = 'CD3-example1.txt'
    latticename = 'CD3-example1'
    test_savelattice(conn, lat, latticefile, latticename)

    print 'test case 3'
    latticefile = 'CD3-example2.txt'
    latticename = 'CD3-example12'
    test_savelattice(conn, lat, latticefile, latticename)

    print 'save tracy lattice'
    latfile = 'CD3-Apr07-10-30cell-par.lat'
    twissfile = 'CD3-Apr07-10-30cell-par.twiss'
    latticename = 'CD3-Apr07-10-30cell-par'
    test_savetracylat(latfile, twissfile, latticename)
    print "costed time: %s seconds" %(time.time()-start)    
    