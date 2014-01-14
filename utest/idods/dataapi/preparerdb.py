'''
Created on May 9, 2013

this model is developed to help idods unit test since some functions might not be available
thru web service.

@author: shengb
@update: dejan.dezman@cosylab.com
'''

import MySQLdb

from rdbinfo import (host, user, pw, db)

def connect():
    if host.startswith("/"):
        conn = MySQLdb.connect(unix_socket=host, user=user, passwd=pw, db=db)
    else:
        conn = MySQLdb.connect(host=host, user=user, passwd=pw, db=db, port=3306)
    return conn

def cleanVendor(namelist):
    '''
    Clean vendor table
    '''
    conn=connect()

    if len(namelist) > 0:
        cur = conn.cursor()

        sql = 'DELETE FROM vendor WHERE name IN (%s)'
        cur.execute(sql, (namelist))
        conn.commit()

    conn.close()

def cleanComponentType(namelist):
    '''
    Clean componenttype table
    '''
    conn=connect()

    if len(namelist) > 0:
        cur = conn.cursor()

        for name in namelist:
            sql = 'DELETE FROM cmpnt_type WHERE name IN (%s)'
            cur.execute(sql, (name))

        conn.commit()

    conn.close()
