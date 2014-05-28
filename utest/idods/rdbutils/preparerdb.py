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
    conn = connect()

    if len(namelist) > 0:
        cur = conn.cursor()

        for name in namelist:
            sql = 'DELETE FROM vendor WHERE vendor_name = %s'
            cur.execute(sql, (name))
        conn.commit()

    conn.close()


def cleanComponentType(namelist):
    '''
    Clean componenttype table
    '''
    conn = connect()

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
    conn = connect()

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
    conn = connect()
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
    conn = connect()

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
    conn = connect()

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
    conn = connect()
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
    conn = connect()

    if len(namelist) > 0:
        cur = conn.cursor()

        for name in namelist:
            sql = 'DELETE FROM id_data_method WHERE method_name = %s'
            cur.execute(sql, (name))

        conn.commit()

    conn.close()


def cleanRawData():
    '''
    Clean raw data of all entries
    '''

    conn = connect()
    cur = conn.cursor()
    sql = 'DELETE FROM id_raw_data WHERE id_raw_data_id >= 1'
    cur.execute(sql)
    conn.commit()

    conn.close()


def cleanOfflineData(descriptionList):
    '''
    Clean offline data table of specific entries
    '''
    conn = connect()

    if len(descriptionList) > 0:
        cur = conn.cursor()

        for dataId in descriptionList:
            sql = 'DELETE FROM id_offline_data WHERE description = %s'
            cur.execute(sql, (dataId))

        conn.commit()

    conn.close()


def cleanOnlineData(descriptionList):
    '''
    Clean online data table of specific entries
    '''
    conn = connect()

    if len(descriptionList) > 0:
        cur = conn.cursor()

        for dataId in descriptionList:
            sql = 'DELETE FROM id_online_data WHERE description = %s'
            cur.execute(sql, (dataId))

        conn.commit()

    conn.close()


def cleanInstall(namelist):
    '''
    Clean install table of specific entries
    '''
    conn = connect()

    if len(namelist) > 0:
        cur = conn.cursor()

        for name in namelist:
            sql = 'DELETE FROM install WHERE field_name = %s'
            cur.execute(sql, (name))

        conn.commit()

    conn.close()


def cleanInstallRel(parentName, childName):
    '''
    Clean install relationships table of specific entries
    '''
    conn = connect()

    cur = conn.cursor()

    sql = '''
    DELETE FROM install_rel
    WHERE parent_install_id =
    (SELECT install_id FROM install WHERE field_name = %s)
    AND child_install_id =
    (SELECT install_id FROM install WHERE field_name = %s)
    '''
    cur.execute(sql, (parentName, childName))

    conn.commit()

    conn.close()


def cleanInstallRelPropType(namelist):
    '''
    Clean install rel property type
    '''
    conn = connect()

    if len(namelist) > 0:
        cur = conn.cursor()

        for name in namelist:
            sql = 'DELETE FROM install_rel_prop_type WHERE install_rel_prop_type_name = %s'
            cur.execute(sql, (name))

        conn.commit()

    conn.close()


def cleanInstallRelProp(typeNameList):
    '''
    Clean install rel property entry identified by special property type name
    '''
    conn = connect()

    if len(typeNameList) > 0:
        cur = conn.cursor()

        for name in typeNameList:

            sql = '''
            DELETE FROM install_rel_prop WHERE
            install_rel_prop_type_id = (SELECT install_rel_prop_type_id FROM install_rel_prop_type WHERE install_rel_prop_type_name = %s)
            '''
            cur.execute(sql, (name))

        conn.commit()

    conn.close()


def cleanDB():
    '''
    Clean complete DB
    '''
    conn = connect()
    cur = conn.cursor()

    sql = [
        'delete from id_offline_data;',
        'delete from id_raw_data;',
        'delete from id_online_data;',
        'delete from id_data_method;',
        'delete from inventory__install;',
        'delete from inventory_prop;',
        'delete from inventory_prop_tmplt;',
        'delete from inventory;',
        'delete from install_rel_prop;',
        'delete from install_rel_prop_type;',
        'delete from install_rel;',
        'delete from vendor;',
        'delete from install;',
        'delete from cmpnt_type_prop;',
        'delete from cmpnt_type_prop_type;',
        'delete from cmpnt_type;'
    ]

    for statement in sql:
        cur.execute(statement)

    conn.commit()

    conn.close()


def cleanInventoryToInstall(installName, ivnentoryName):
    '''
    Clean inventory - install entry
    '''
    conn = connect()
    cur = conn.cursor()

    sql = '''
    DELETE FROM inventory__install WHERE
    inventory_id = (SELECT inventory_id FROM inventory WHERE name = %s)
    AND install_id = (SELECT install_id FROM install WHERE field_name = %s)'''
    cur.execute(sql, (ivnentoryName, installName))

    conn.commit()
    conn.close()