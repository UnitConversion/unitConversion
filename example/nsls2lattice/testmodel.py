'''
Created on Apr 16, 2013

@author: shengb
'''

import MySQLdb

from pylattice import model

host=''
user = ''
pw = ''
db = ''
port = 3306

if __name__ == '__main__':
    if host.startswith("/"):
        conn = MySQLdb.connect(unix_socket=host, user=user, passwd=pw, db=db)
    else:
        conn = MySQLdb.connect(host=host, user=user, passwd=pw, db=db, port=port)

    modelinst = model(conn)