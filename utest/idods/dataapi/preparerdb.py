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

        sql = 'DELETE FROM vendor WHERE vendor_name = %s'
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
            sql = 'DELETE FROM cmpnt_type WHERE cmpnt_type_name = %s'
            cur.execute(sql, (name))

        conn.commit()

    conn.close()

def cleanComponentTypePropertyType(namelist):
    '''
    Clean component type property type
    '''
    conn=connect()

    if len(namelist) > 0:
        cur = conn.cursor()

        for name in namelist:
            sql = 'DELETE FROM cmpnt_type_prop_type WHERE cmpnt_type_prop_type_name = %s'
            cur.execute(sql, (name))

        conn.commit()

    conn.close()
    
def cleanComponentTypeProperty(componentTypeName, componentTypePropertyTypeName):
    '''
    Clean component type property entry
    '''
    conn=connect()
    cur = conn.cursor()

    sql = '''
    DELETE FROM cmpnt_type_prop WHERE
    cmpnt_type_id = (SELECT cmpnt_type_id FROM cmpnt_type WHERE cmpnt_type_name = %s)
    AND cmpnt_type_prop_type_id = (SELECT cmpnt_type_prop_type_id FROM cmpnt_type_prop_type WHERE cmpnt_type_prop_type_name = %s)'''
    cur.execute(sql, (componentTypeName, componentTypePropertyTypeName))

    conn.commit()
    conn.close()

def cleanInventory(namelist):
    '''
    Clean inventory table of specific entries
    '''
    conn=connect()

    if len(namelist) > 0:
        cur = conn.cursor()

        for name in namelist:
            sql = 'DELETE FROM inventory WHERE name = %s'
            cur.execute(sql, (name))

        conn.commit()

    conn.close()

def cleanInventoryPropertyTemplate(namelist):
    '''
    Clean inventory property template
    '''
    conn=connect()

    if len(namelist) > 0:
        cur = conn.cursor()

        for name in namelist:
            sql = 'DELETE FROM inventory_prop_tmplt WHERE inventory_prop_tmplt_name = %s'
            cur.execute(sql, (name))

        conn.commit()

    conn.close()

def cleanInventoryProperty(ivnentoryName, templateName):
    '''
    Clean inventory property entry
    '''
    conn=connect()
    cur = conn.cursor()

    sql = '''
    DELETE FROM inventory_prop WHERE
    inventory_id = (SELECT inventory_id FROM inventory WHERE name = %s)
    AND inventory_prop_tmplt_id = (SELECT inventory_prop_tmplt_id FROM inventory_prop_tmplt WHERE inventory_prop_tmplt_name = %s)'''
    cur.execute(sql, (ivnentoryName, templateName))

    conn.commit()
    conn.close()

def cleanDataMethod(namelist):
    '''
    Clean data method of specific entries
    '''
    conn=connect()

    if len(namelist) > 0:
        cur = conn.cursor()

        for name in namelist:
            sql = 'DELETE FROM id_data_method WHERE method_name = %s'
            cur.execute(sql, (name))

        conn.commit()

    conn.close()
