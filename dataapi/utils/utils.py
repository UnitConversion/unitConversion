'''
Created on Mar 5, 2013

@author: shengb
@updated: dejan.dezman@cosylab.com Feb 26, 2014
'''
import collections
import datetime
import os
import errno

def _wildcardformat(regxval):
    """
    The LIKE condition allows user to use wildcards in the where clause of an SQL statement.
    This allows user to perform pattern matching. The LIKE condition can be used in any valid
    SQL statement - select, insert, update, or delete.
    The patterns that a user can choose from are:
        % allows you to match any string of any length (including zero length)
        _ allows you to match on a single character

    The client uses "*" for multiple match, and "?" for single character match.
    This function replaces "*" with "%", and "?" with "_".

    For example:
    >>> _wildcardformat("a*b?c*d*e?f")
    u'a%b_c%d%e_f'
    """
    if regxval == None:
        return None
    else:
        try:
            return regxval.replace("*","%").replace("?","_")
        except AttributeError:
            return regxval

def _assemblesql(sql, data, strpattern, res, connector=""):
    ''''''
    strpattern = " "+ strpattern
    strpattern1 = strpattern + " like %s or"
    strpattern2 = strpattern + " like %s " 
    strpattern3 = strpattern + " = %s or"
    strpattern4 = strpattern + " = %s " 
    sql += " " + connector + " "
    if isinstance(data, (tuple, list)):
        sql += " ( "
        for s in data:
            if isinstance(data, collections.Iterable):
                s = _wildcardformat(s)
                if "%" in s or "_" in s:
                    sql += strpattern1
                elif s == "":
                    pass
                else:
                    sql += strpattern3
                res.append(s)
            else:
                if s != None:
                    sql += strpattern3
                    res.append(s)
        sql = sql[:-2]
        sql += " ) "
    else:
        if isinstance(data, collections.Iterable):
            data = _wildcardformat(data)
            if "%" in data or "_" in data:
                sql += strpattern2
                res.append(data)
            elif data == "":
                pass
            else:
                sql += strpattern4
                res.append(data)
        else:
            if data != None:
                sql += strpattern4
                res.append(data)
    return res, sql

def _checkkeys(keys, expectedkeys):
    '''
    Check if all the keys are in the expected keys list
    
    params:
        - keys: keys found in the method call
        - expectedkeys: list of keys that need to be present
    '''
    
    illegalkey = [] 
    for key in keys:
        if key not in expectedkeys:
            illegalkey.append(key)
    if len(illegalkey) != 0:
        raise ValueError ("argument (%s) are not supported."%(",".join(illegalkey)))
    else:
        return True

def _retrievecmddict(httpcmd):
    '''
    Retrieve GET/POST/PUT/DELETE request parameters, lower all keys, and return parameter dictionary.
    '''

    # multiple values support.
    httpdict = {}
    for k, v in httpcmd.iteritems():
        vlist = httpcmd.getlist(k)
        if len(vlist) > 1:
            httpdict[k.lower()] = list(set(vlist))
        else:
            httpdict[k.lower()] = v
    return httpdict

def _generateFilePath():
    '''
    Generate path for the uploaded file
    '''
    #now = datetime.datetime.now()
    #dirname = 'documents/%s/%s/%s'%(now.year, now.month, now.day)
    dirname = 'documents/%s'%datetime.datetime.now().strftime("%Y%m%d/%H%M%S/%f")
    try:
        os.makedirs(dirname)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dirname):
            pass
        else: 
            raise Exception("Could not create a directory to save lattice file")
    return dirname

def _checkParameter(parameterKey, paramaterValue, parameterTypeWeAreCheckingFor = "string"):
    '''
    Check different types of input parameters. Parameter should match agreed criteria or exception will be thrown
    
    parameters:
        - parameterKey: name of the parameter
        - parameterValue: value of the parameter
        - parameterTypeWeAreCheckingFor: which type are we chacking
            * string: if we are checking string value
            * prim: if we are checking primary key value
        
    raise:
        ValueError if parameter don'r match agreed criteria
    '''
    
    # Check string
    if parameterTypeWeAreCheckingFor == "string":
        
        if not isinstance(paramaterValue, (str, unicode)):
            raise ValueError("Parameter %s is missing!" % parameterKey)
        
    # Check primary key
    elif parameterTypeWeAreCheckingFor == "prim":
        
        try:
            paramaterValue = int(paramaterValue)
            
        except ValueError as e:
            raise ValueError("Parameter %s cannot be None. %s." % (parameterKey, e.args[0]))

def _checkWildcardAndAppend(parameterKey, parameterValue, sqlString, valsList, prependedOperator = None):
    '''
    Check for wildcard characters in a parameter value and append appropriate sql
    
    parameters:
        - parameterKey: name of the parameter in the DB table
        - parameterValue: value of this parameter
        - sqlString: existing sql string that was generated outside of this function
        - valsList: list of formated values that should be inserted into sql statement
        - prepandedOperator: sql operator that will be prepended before the new condition
        
    return:
        tuple of new sql string and new list of values
    '''
    
    # Prepend operator if it exists
    if prependedOperator != None:
        sqlString += " " + prependedOperator + " "
        
    # Do not check for wildcard parameters if we have a number
    if isinstance(parameterValue, (int, float, long, complex)):
        sqlString += " " + parameterKey + " = %s "
        valsList.append(parameterValue)
        return (sqlString, valsList)
    
    # Check if user wants all objects
    if parameterValue == "*":
        sqlString += " 1=1 "
    
    # Check for wildcard characters
    elif "*" in parameterValue or "?" in parameterValue:
        sqlString += " " + parameterKey + " like %s "
        valsList.append(_wildcardformat(parameterValue))
        
    # All of the other options
    else:
        sqlString += " " + parameterKey + " = %s "
        valsList.append(parameterValue)
        
    return (sqlString, valsList)

def _generateUpdateQuery(tableName, queryDict, whereKey, whereValue, whereDict = None):
    '''
    Check number of parameters that are set and generate update SQL
    
    params:
        - tableName: name of the table we are updating
        - queryDict: dictionary where every key is an attribute name and every value new attribute value
        - whereKey: attribute by which we are updating
        - whereValue: attribute value by which we are updating
        - whereDict: dictionary of where keys and values
    
    raises:
        ValueError if no attributes are set
    '''
    
    # Create value list
    vals = []
    
    # Check the number of attributes that are set
    if len(queryDict) < 1:
        raise ValueError("At least one attribute has to be set to a new value!")
    
    # Generate SQL
    sql = 'UPDATE ' + tableName + ' SET '
    sqlList = []
    
    # Go through parameters
    for attr in queryDict.keys():
        value = queryDict[attr]
        sqlList.append(' ' + attr + ' = %s ')
        vals.append(value)
    
    sql += ','.join(sqlList)
    
    if whereDict == None:
        # Append where condition
        sql += ' WHERE ' + whereKey + ' = %s '
        vals.append(whereValue)
        
    else:
        sql += ' WHERE '
        sqlList = []
        
        # Go through where keys
        for whereKey in whereDict.keys():
            whereValue = whereDict[whereKey]
            sqlList.append(' ' + whereKey + ' = %s ')
            vals.append(whereValue)
            
        sql += " AND ".join(sqlList)
    
    return (sql, vals)
