'''
Created on Mar 19, 2013

@author: shengb
'''

import MySQLdb
from pylattice import lattice

host=""
user = ''
pw = ''
db = ''
port = 3306

if __name__ == "__main__":
    import time
    start = time.time()

    if host.startswith("/"):
        conn = MySQLdb.connect(unix_socket=host, user=user, passwd=pw, db=db)
    else:
        conn = MySQLdb.connect(host=host, user=user, passwd=pw, db=db, port=port)

    lat = lattice.lattice(conn)
    supportedlatticetype = [{'name': 'tab flat', 'format': 'txt'},
                            {'name': 'tracy3',  'format': 'lat'},
                            {'name': 'tracy4',  'format': 'lat'},
                            {'name': 'elegant', 'format': 'lte'},
                            {'name': 'xal',     'format': 'xdxf'}]

    sql = '''
    delete from element;
    delete from element_type_prop;
    delete from element_type;
    '''
    conn.cursor().execute(sql)
    conn.commit()

    for latticetype in supportedlatticetype:
        try:
            lat.savelatticetype(latticetype['name'], latticetype['format'])
        except ValueError:
            pass
    
    print lat.retrievelatticetype("*")
    
    latticefile = 'CD3-Oct3-12-30Cell-addID-par.txt'
    latticedata = {}
    with file(latticefile, 'r') as f:
        lines=f.readlines()
        latticedata.update({'name': latticefile,
                            'data': lines})
    
    if latticedata:
        latticeid = lat.savelattice('CD3-Oct3-12-30Cell-addID-par', '20121003', 'design', 
                                    latticetype=supportedlatticetype[0], 
                                    description="CD3 lattice released on Oct 13, 2012",
                                    creator='Guobao Shen',
                                    lattice=latticedata)
    else:
        latticeid = lat.savelattice('CD3-Oct3-12-30Cell-addID-par', '20121003', 'design', 
                                    latticetype=supportedlatticetype[0], 
                                    description="CD3 lattice released on Oct 13, 2012",
                                    creator='Guobao Shen')
    
    print "costed time: %s seconds" %(time.time()-start)
    #CD3-Oct3-12-30Cell-addID-par
    print lat.retrievelatticelist("*")
