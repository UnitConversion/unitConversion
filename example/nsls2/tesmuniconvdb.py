'''
Created on Jan 28, 2013

@author: shengb
'''
from __future__ import print_function
import sys
import MySQLdb
#import pprint

if __name__ == '__main__':
    host = None
    if sys.version_info[:2] > (3,0):
        host = input ('Please give MySQL server name:')
    else:
        host = raw_input('Please give MySQL server name:')
    
    user = None
    if sys.version_info[:2] > (3,0):
        user = input ('Please give user name on that MySQL server:')
    else:
        user = raw_input('Please give user name on that MySQL server:')
    
    pwd = None
    if sys.version_info[:2] > (3,0):
        pwd = input ('Please give password for user ($s):'%(user))
    else:
        pwd = raw_input ('Please give password for user ($s):'%(user))

    db = None
    if sys.version_info[:2] > (3,0):
        db = input ('Which database are you going to access? ')
    else:
        db = raw_input ('Which database are you going to access? ')

    conn = MySQLdb.connect(host=host, user=user, passwd=pwd, db=db)
    cur = conn.cursor()
    printdata = False
    
    type2drawsql = '''
    select cmpnt_type_name, description, cmpnt_type_prop_value 
    from cmpnt_type, cmpnt_type_prop, cmpnt_type_prop_type 
    where 
    cmpnt_type.cmpnt_type_id = cmpnt_type_prop.cmpnt_type_id 
    and cmpnt_type_prop.cmpnt_type_prop_type_id = cmpnt_type_prop_type.cmpnt_type_prop_type_id 
    and cmpnt_type_prop_type_name = 'Reference Drawing'
    and cmpnt_type_name like %s
    '''
    
    #####################################
    # Get Dipole information
    #####################################
    sql = '''
    select field_name, cmpnt_type_name, description
    from install, cmpnt_type 
    where 
    install.cmpnt_type_id=cmpnt_type.cmpnt_type_id 
    and install.field_name like "%G%C%" 
    and cmpnt_type.cmpnt_type_name like "%Dip%"
    and cmpnt_type.cmpnt_type_name not like "%trim%";
    '''
    cur.execute(sql)
    # return format
    #  install_id | cmpnt_type_id | field_name | cmpnt_type_name | description
    res = cur.fetchall()
    dtype2drawsql = type2drawsql %('"Dip%"') + " and cmpnt_type_name not like '%trim%'"
    cur.execute(dtype2drawsql)
    type2drawres = cur.fetchall()
    if printdata:
        print('dipolelist = [')
        for val in res:
            print (list(val), ',') 
        print(']')
        print('dipoletype2draw = [')
        for val in type2drawres:
            print (list(val), ',') 
        print(']')            
    else:
        print('Dipole', len(res))

    sql = '''
    select field_name, cmpnt_type_name, description
    from install, cmpnt_type 
    where install.cmpnt_type_id=cmpnt_type.cmpnt_type_id 
    and install.field_name like %s 
    and cmpnt_type.cmpnt_type_name like %s
    '''
    #####################################
    # Get Quadrupole information
    #####################################
    cur.execute(sql, ("%G%C%", "%Quad%",))
    # return format
    #  install_id | cmpnt_type_id | field_name | cmpnt_type_name | description
    res = cur.fetchall()    
    cur.execute(type2drawsql, ('Quad%',))
    type2drawres = cur.fetchall()
    if printdata:
        print('quadlist = [')
        for val in res:
            print (list(val), ',') 
        print(']')
        print('quadtype2draw = [')
        for val in type2drawres:
            print (list(val), ',') 
        print(']')            
    else:
        print('Quadrupole', len(res))

    #####################################
    # Get Sextupole information
    #####################################
    cur.execute(sql, ("%G%C%", "%Sext%",))
    # return format
    #  install_id | cmpnt_type_id | field_name | cmpnt_type_name | description
    res = cur.fetchall()    
    cur.execute(type2drawsql, ('Sext%',))
    type2drawres = cur.fetchall()
    if printdata:
        print('sextlist = [')
        for val in res:
            print (list(val), ',') 
        print(']')
        print('sexttype2draw = [')
        for val in type2drawres:
            print (list(val), ',') 
        print(']')            
    else:
        print('Sextupole', len(res))

    #####################################
    # Get horizontal corrector information
    #####################################
    cur.execute(sql, ("C%G%C%", "%Corr%horizontal",))
    # return format
    #  install_id | cmpnt_type_id | field_name | cmpnt_type_name | description
    res = cur.fetchall()    
    cur.execute(type2drawsql, ('%Corr%horizontal',))
    type2drawres = cur.fetchall()
    if printdata:
        print('hcorlist = [')
        for val in res:
            print (list(val), ',') 
        print(']')
        print('hcortype2draw = [')
        for val in type2drawres:
            print (list(val), ',') 
        print(']')            
    else:
        print('Horizontal Corrector', len(res))

    #####################################
    # Get vertical corrector information
    #####################################
    cur.execute(sql, ("C%G%C%", "%Corr%vertical",))
    # return format
    #  install_id | cmpnt_type_id | field_name | cmpnt_type_name | description
    res = cur.fetchall()    
    cur.execute(type2drawsql, ('%Corr%vertical',))
    type2drawres = cur.fetchall()
    if printdata:
        print('vcorlist = [')
        for val in res:
            print (list(val), ',') 
        print(']')
        print('vcortype2draw = [')
        for val in type2drawres:
            print (list(val), ',') 
        print(']')            
    else:
        print('Vertical Corrector', len(res))

    #####################################
    # Get skew quadrupole information
    #####################################
    sql = '''
    select field_name, cmpnt_type_name, description
    from install, cmpnt_type 
    where 
    install.cmpnt_type_id=cmpnt_type.cmpnt_type_id 
    and install.field_name like "C%G%C%" 
    and cmpnt_type.cmpnt_type_name="Corr D"
    '''
    cur.execute(sql)
    # return format
    #  install_id | cmpnt_type_id | field_name | cmpnt_type_name | description
    res = cur.fetchall()    
    cur.execute(type2drawsql, ('Corr D',))
    type2drawres = cur.fetchall()
    if printdata:
        print('squadlist = [')
        for val in res:
            print (list(val), ',') 
        print(']')
        print('squadtype2draw = [')
        for val in type2drawres:
            print (list(val), ',') 
        print(']')            
    else:
        print('Skew Quadrupole', len(res))


    #####################################
    # Get mapping from alias name to reference drawing
    #####################################
    alias2drawsql = '''
    select distinct alias, serial_no, cmpnt_type_name, cmpnt_type_prop_value 
    from 
    rot_coil_data, inventory, cmpnt_type, cmpnt_type_prop 
    where 
    rot_coil_data.inventory_id = inventory.inventory_id 
    and inventory.cmpnt_type_id = cmpnt_type.cmpnt_type_id 
    and cmpnt_type.cmpnt_type_id = cmpnt_type_prop.cmpnt_type_id 
    and cmpnt_type_name like %s and cmpnt_type_prop_value like %s;
    '''
    cur.execute(alias2drawsql, ("Quad%", "%QD%"))
    res = cur.fetchall()
    if printdata:
        print('squadalias2draw = [')
        for val in res:
            print (list(val), ',') 
        print(']')
    else:
        print('quad alias 2 draw', len(res))
    cur.execute(alias2drawsql, ("Sext%", "%STP%"))
    res = cur.fetchall()
    if printdata:
        print('sextalias2draw = [')
        for val in res:
            print (list(val), ',') 
        print(']')
    else:
        print('sext alias 2 draw', len(res))

    type2drawmapsql = '''
    select cmpnt_type.cmpnt_type_id, cmpnt_type_name, cmpnt_type_prop_value 
    from 
    cmpnt_type, cmpnt_type_prop, cmpnt_type_prop_type 
    where 
    cmpnt_type.cmpnt_type_id = cmpnt_type_prop.cmpnt_type_id 
    and cmpnt_type_prop.cmpnt_type_prop_type_id = cmpnt_type_prop_type.cmpnt_type_prop_type_id 
    and cmpnt_type_prop_type_name = "Reference Drawing";
    '''
    cur.execute(type2drawmapsql)
    type2drawmap = cur.fetchall()
    type2drawmapdict = {}
    for type2draw in type2drawmap:
        type2drawmapdict[type2draw[1]] = list(type2draw)

    
    