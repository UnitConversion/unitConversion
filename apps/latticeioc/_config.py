def getpvtablefromfile(fname):
    '''
    This function returns three data with structure as:
    1. set point pv dictionary with structure looks like:
        { 'element name': {'I': 'sp pv name for I':
                           'B': 'sp pv name for B',
                           'K': 'sp pv name for K'},
         ...
        }
    2. read back pv dictionary with structure looks like:
        { 'element name': {'I': 'rb pv name for I':
                           'B': 'rb pv name for B',
                           'K': 'rb pv name for K'},
         ...
        }
    '''
    with file(fname, 'r') as f:
        pvlist = f.readlines()
    
    pvspsdict = {}
    # set point pvs
    # the structure looks like:
    # { 'element name': {'I': 'sp pv name for I':
    #                    'B': 'sp pv name for B',
    #                    'K': 'sp pv name for K'},
    #  ...
    # }
    
    
    pvrbsdict = {}
    # read back pvs
    # the structure looks like:
    # { 'element name': {'I': 'rb pv name for I':
    #                    'B': 'rb pv name for B',
    #                    'K': 'rb pv name for K'},
    #  ...
    # }
    
    for pvs in pvlist:
        pvs = pvs.strip()
        if not (pvs.startswith("#") or pvs.startswith("//")) and pvs.strip() != "":
            # get name    type    current SP    current RB    field SP    field RB    K SP    K RB
            pvprop = pvs.split()
            
            #
            if pvspsdict.has_key(pvprop[0]) or pvrbsdict.has_key(pvprop[0]):
                raise ValueError('Duplicated element found for %s'%(pvprop[0]))

            pvspsdict[pvprop[0]] = {'I': pvprop[2],
                                    'B': pvprop[4],
                                    'K': pvprop[6]}
            pvrbsdict[pvprop[0]] = {'I': pvprop[3],
                                    'B': pvprop[5],
                                    'K': pvprop[7]}
    
    return pvspsdict, pvrbsdict

def getnormalizedvalue(valfile):
    '''Check the file format. It suppose having a header like
         magnet              KL                                    SP-PV      current(A)
    ----------------------------------------------------------------------------------------
    
    '''
    normalizedvalue = {}
    with file(valfile) as f:
        data = f.readlines()
    for val in data[2:]:
        vals = val.split()
        if normalizedvalue.has_key(vals[2]):
            raise ValueError('Duplicated Value for %s (%s)'%(vals[2], vals[0]))
        normalizedvalue[vals[2]] = {'Name': vals[0],
                                    'KL': vals[1],
                                    'I': vals[3]}
    return normalizedvalue

if __name__ == "__main__":
    normalizedvalue = getnormalizedvalue('yli_pv_cur.txt')
    getpvtablefromfile('pvtable.txt')
    
    