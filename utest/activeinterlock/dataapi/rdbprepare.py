'''
Created on Aug 20, 2013

@author: shengb
'''
'''
Created on May 9, 2013

this model is developed to help lattice/model unit test since some functions might not be available
thru web service.

@author: shengb
'''

import MySQLdb

from rdbinfo import (host, user, pw, db)

def connect():
    if host.startswith("/"):
        conn = MySQLdb.connect(unix_socket=host, user=user, passwd=pw, db=db)
    else:
        conn = MySQLdb.connect(host=host, user=user, passwd=pw, db=db, port=3306)
    return conn

def close(conn):
    conn.close()
    