'''
Created on May 9, 2013

@author: shengb
'''

import MySQLdb

from rdbinfo import (host, user, pw, db)

def addlatticetype(typecollection):
    '''
    '''
    sql = '''insert into lattice_type (lattice_type_name, lattice_type_format) values 
    '''
    if host.startswith("/"):
        conn = MySQLdb.connect(unix_socket=host, user=user, passwd=pw, db=db)
    else:
        conn = MySQLdb.connect(host=host, user=user, passwd=pw, db=db, port=3306)
    if len(typecollection) > 0:
        for col in typecollection:
            sql += '("%s", "%s"),'%(col['name'], col['format'])
        cur=conn.cursor()
        cur.execute(sql[:-1])
        conn.commit()
    conn.close()

def cleanlatticetype(typecollection):
    '''
    '''
    if host.startswith("/"):
        conn = MySQLdb.connect(unix_socket=host, user=user, passwd=pw, db=db)
    else:
        conn = MySQLdb.connect(host=host, user=user, passwd=pw, db=db, port=3306)
    if len(typecollection) > 0:
        cur = conn.cursor()
        for col in typecollection:
            sql = 'delete from lattice_type where lattice_type_name = %s and lattice_type_format = %s'
            cur.execute(sql, (col['name'], col['format']))
        conn.commit()
    conn.close()
