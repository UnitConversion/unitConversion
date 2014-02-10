'''
Created on Mar 5, 2013

@author: shengb
'''
import collections

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
