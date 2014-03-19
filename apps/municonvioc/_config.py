try:
    haschannelfinder = True
    from channelfinder import ChannelFinderClient
    from channelfinder import Channel, Property, Tag
    from channelfinder.util import ChannelUtil
except ImportError:
    haschannelfinder = False

rectemp = '''
record(ai, "%s") {
}'''

def _getnewpvname(elemname, oldpv, pattern):
    # get cell information from element physics name
    elemname = elemname.upper()
    
    # avoid element name starting with C, for example corrector
    elemname = elemname[2:]
    cell = elemname.find('C')
    if cell != -1:
        cellname = elemname[cell:cell+3]
    else:
        raise ValueError('Element name does not follow NSLS II physics naming conversion for %s'%(elemname))
    
    # get cell information from pv name
    cellpv = oldpv.upper().find('C')
    if cellpv != -1:
        cellinpvname = oldpv[cellpv:cellpv+3]
    else:
        raise ValueError('PV name does not follow NSLS II pv naming conversion for %s'%(oldpv))
    
    newpv = oldpv.replace(cellinpvname, cellname)
    return newpv

def getpvfromfile(fname):
    '''
    This function returns three data with structure as:
    1. set point pv dictionary with structure looks like:
        { 'sp pv name for I': {'element name': {'B': 'sp pv name for B',
                                                'K': 'sp pv name for K'},
                               ...
                              },
        ...
        }
    2. read back pv dictionary with structure looks like:
        { 'rb pv name for I': {'element name': {'B': 'rb pv name for B',
                                                'K': 'rb pv name for K'},
                               ...
                              },
        ...
        }
    3. EPICS db buffer
    4. PV mapping buffer. It has order like:
        name    type    current SP    current RB    field SP    field RB    K SP    K RB
    '''
    with file(fname, 'r') as f:
        pvlist = f.readlines()
    
    # set point pvs
    # the structure looks like:
    # { 'sp pv name for I': {'element name': {'B': 'sp pv name for B',
    #                                         'K': 'sp pv name for K'},
    #                        ...
    #                       },
    # ...
    # }
    pvspsdict = {}
    
    # read back pvs
    # the structure looks like:
    # { 'rb pv name for I': {'element name': {'B': 'rb pv name for B',
    #                                         'K': 'rb pv name for K'},
    #                        ...
    #                       },
    # ...
    # }
    pvrbsdict = {}
    
    dbbuffer = ""
    pvmappings = '''# name     type        current SP                current RB                    field SP                        field RB                        K SP                        K RB\n'''

    for pvs in pvlist:
        pvs = pvs.strip()
        if not (pvs.startswith("#") or pvs.startswith("//")) and pvs.strip() != "":
            # get element name, type, set point pv, read back pv
            pvprop = pvs.split()
            tmpspdict = {}
            tmprbdict = {}
            
            #
            if pvspsdict.has_key(pvprop[2]):
                tmpspdict = pvspsdict[pvprop[2]]
            if pvrbsdict.has_key(pvprop[3]):
                tmprbdict = pvrbsdict[pvprop[3]]
            
            if tmpspdict.has_key(pvprop[0]) or tmprbdict.has_key(pvprop[0]):
                raise ValueError('Duplicated element found for %s'%(pvprop[0]))
            
            #
#            if pvprop[1] in ['HCOR','VCOR']:
#                newsppv = pvprop[2]
#                newrbpv = pvprop[3]
#            else:
#                newsppv = _getnewpvname(pvprop[0], pvprop[2], 'C')
#                newrbpv = _getnewpvname(pvprop[0], pvprop[3], 'C')
            newsppv = _getnewpvname(pvprop[0], pvprop[2], 'C')
            newrbpv = _getnewpvname(pvprop[0], pvprop[3], 'C')
            
            if pvprop[1] == 'QUAD':
                sppv_gl = newsppv.replace("}I", "}GL")
                sppv_k = newsppv.replace("}I", "}K")
                rbpv_gl = newrbpv.replace("}I", "}GL")
                rbpv_k = newrbpv.replace("}I", "}K")
                pvmappings = " ".join((pvmappings, pvs, sppv_gl, rbpv_gl, sppv_k, rbpv_k, '\n'))
                
                dbbuffer = "".join((dbbuffer, rectemp%(sppv_gl), 
                              rectemp%(sppv_k),
                              rectemp%(rbpv_gl), 
                              rectemp%(rbpv_k)))
                tmpspdict [pvprop[0]] = {'B': sppv_gl,
                                         'K': sppv_k
                                         }
                
                tmprbdict [pvprop[0]] = {'B': rbpv_gl,
                                         'K': rbpv_k
                                         }
            elif pvprop[1] == 'SEXT':
                sppv_sl = newsppv.replace("}I", "}SL")
                sppv_k = newsppv.replace("}I", "}K")
                rbpv_sl = newrbpv.replace("}I", "}SL")
                rbpv_k = newrbpv.replace("}I", "}K")
                pvmappings = " ".join((pvmappings, pvs, sppv_sl, rbpv_sl, sppv_k, rbpv_k, '\n'))
                
                dbbuffer = "".join((dbbuffer, rectemp%(sppv_sl), 
                              rectemp%(sppv_k),
                              rectemp%(rbpv_sl), 
                              rectemp%(rbpv_k)))
            
                tmpspdict [pvprop[0]] = {'B': sppv_sl,
                                         'K': sppv_k
                                         }
                
                tmprbdict [pvprop[0]] = {'B': rbpv_sl,
                                         'K': rbpv_k
                                         }
            elif pvprop[1] in ['HCOR', 'VCOR']:
                sppv_bl = newsppv.replace("}I", "}BL")
                sppv_k = newsppv.replace("}I", "}K")
                rbpv_bl = newrbpv.replace("}I", "}BL")
                rbpv_k = newrbpv.replace("}I", "}K")
                pvmappings = " ".join((pvmappings, pvs, sppv_bl, rbpv_bl, sppv_k, rbpv_k, '\n'))
                
                dbbuffer = "".join((dbbuffer, rectemp%(sppv_bl), 
                              rectemp%(sppv_k),
                              rectemp%(rbpv_bl), 
                              rectemp%(rbpv_k)))
            
                tmpspdict [pvprop[0]] = {'B': sppv_bl,
                                         'K': sppv_k
                                         }
                
                tmprbdict [pvprop[0]] = {'B': rbpv_bl,
                                         'K': rbpv_k
                                         }
            pvspsdict[pvprop[2]] = tmpspdict
            pvrbsdict[pvprop[3]] = tmprbdict

    return pvspsdict, pvrbsdict, dbbuffer, pvmappings

def getpvfromcf(url):
    if haschannelfinder:
        cf = ChannelFinderClient(BaseURL=url)
    else:
        raise ValueError("channel finder client library is not available.")
    
    pvspsdict = {}
    pvrbsdict = {}
    dbbuffer = ""
    pvmappings = '''# element name        type        current SP        current RB        field SP        field RB        K SP        K RB\n'''
    
    return pvspsdict, pvrbsdict, dbbuffer, pvmappings

if __name__ == "__main__":
    pvspsdict, pvrbsdict, dbbuffer, pvmappings = getpvfromfile('pvconfig.txt')
    
    
    