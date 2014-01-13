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

def cleanvendor(namelist):
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

def cleancomponenttype(namelist):
    '''
    Clean componenttype table
    '''
    conn=connect()

    if len(namelist) > 0:
        cur = conn.cursor()

        sql = 'DELETE FROM cmpnt_type WHERE name IN (%s)'
        cur.execute(sql, (namelist))
        conn.commit()

    conn.close()

def deletelattice(name, version, branch):
    '''
    '''
    conn=connect()
    sql = '''select lattice_id from lattice where lattice_name=%s and lattice_version=%s and lattice_branch=%s'''
    cur=conn.cursor()
    cur.execute(sql, (name, version, branch))
    latticeid = cur.fetchone()
    if latticeid != None:
        latticeid = latticeid[0]
        sql = '''delete from lattice where lattice_id = %s'''

        cur.execute(sql, (latticeid))
        conn.commit()

    conn.close()


def truncatelattice():
    '''
    '''
    sql = '''
    delete from beam_parameter;
    delete from gold_model;
    delete from model;
    delete from element_prop;
    delete from element;
    delete from element_type_prop;
    delete from element_type;
    delete from gold_lattice;
    delete from lattice;
    '''
    conn=connect()

    conn.cursor().execute(sql)
    conn.commit()
    conn.close()

def cleanmodelcode(codeinfo):
    '''
    '''
    conn=connect()
    if len(codeinfo) > 0:
        cur = conn.cursor()
        for col in codeinfo:
            if col.has_key('algorithm') and col['algorithm']!=None:
                sql = 'delete from model_code where code_name = %s and algorithm = %s'
                cur.execute(sql, (col['name'], col['algorithm']))
            else:
                sql = 'delete from model_code where code_name = %s and algorithm is NULL'
                cur.execute(sql, (col['name']))

        conn.commit()
    conn.close()


