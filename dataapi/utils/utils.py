'''
Created on Mar 5, 2013

@author: shengb
'''
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
    return regxval.replace("*","%").replace("?","_")

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
            s = _wildcardformat(s)
            if "%" in s or "_" in s:
                sql += strpattern1
            elif s == "":
                pass
            else:
                sql += strpattern3
            res.append(s)
        sql = sql[:-2]
        sql += " ) "
    else:
        data = _wildcardformat(data)
        if "%" in data or "_" in data:
            sql += strpattern2
        elif data == "":
            pass
        else:
            sql += strpattern4
        res.append(data)
    return res, sql
