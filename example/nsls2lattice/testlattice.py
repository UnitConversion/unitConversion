'''
Created on Mar 19, 2013

@author: shengb
'''
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

if __name__ == "__main__":
    import time
    start = time.time()

    conn = connect()
    lat = lattice(conn)
    
    cleanrdb(conn)

    print 'test case 1'
    latticefile = 'CD3-Oct3-12-30Cell-addID-par.txt'
    latticename = 'CD3-Oct3-12-30Cell-addID-par'
    test_savelattice(conn, lat, latticefile, latticename)

    print 'test case 2'
    latticefile = 'CD3-example1.txt'
    latticename = 'CD3-example1'
    test_savelattice(conn, lat, latticefile, latticename)

    print 'test case 3'
    latticefile = 'CD3-example2.txt'
    latticename = 'CD3-example12'
    test_savelattice(conn, lat, latticefile, latticename)

    print "costed time: %s seconds" %(time.time()-start)
