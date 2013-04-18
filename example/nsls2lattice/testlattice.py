'''
Created on Mar 19, 2013

@author: shengb
'''
#import os
#import errno
#import tempfile
#def unique_file(file_name):
#    dirname, filename = os.path.split(file_name)
#    prefix, suffix = os.path.splitext(filename)
#
#    try:
#        os.makedirs(dirname)
#    except OSError as exc:
#        if exc.errno == errno.EEXIST and os.path.isdir(dirname):
#            pass
#        else: 
#            raise
#
#    fd, filename = tempfile.mkstemp(suffix, prefix+"_", dirname)
#    return os.fdopen(fd, 'w+'), filename
#
#if __name__ == '__main__':
#    f, fname = unique_file('documents/2013/3/18/lattice.txt')
#    f.write("a, b, c")
#    f.close()
#    print fname, f
#    
#    f, fname = unique_file('documents/2013/3/18/lattice')
#    f.write("a, b, c")
#    f.close()
#    print fname, f

import MySQLdb
from pylattice import lattice

host=''
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

    lat = lattice(conn)
    supportedlatticetype = [{'name': 'tab flat', 'format': 'txt'},
                            {'name': 'tracy3',  'format': 'lat'},
                            {'name': 'tracy4',  'format': 'lat'},
                            {'name': 'elegant', 'format': 'lte'},
                            {'name': 'xal',     'format': 'xdxf'}]

    savelattice = False
    if savelattice:
        sql = '''
        delete from element_prop;
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
    
    retrievelattice = False
    if retrievelattice:
        lattices = lat.retrievelattice('CD3-Oct3-12-30Cell-addID-par', '20121003', 'design', withdata=True, rawdata=False)
        print "costed time: %s seconds" %(time.time()-start)
        print lattices
    
    #CD3-Oct3-12-30Cell-addID-par
    #print lat.retrievelattice("*", "*", "*")
    
    lat.savegoldlattice('CD3-Oct3-12-30Cell-addID-par', '20121003', 'design', creator='Guobao', status=2)
    lat.savegoldlattice('CD3-Oct3-12-30Cell-addID-par', '20121003', 'design', status=3)
    print lat.retrievegoldlattice('CD3-Oct3-12-30Cell-addID-par', '20121003', 'design')

