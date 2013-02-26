
'''
This script is to read data related to magnet unit conversion for NSLS II injector system,
and save all data into IRMIS database.

Created on Sep 26, 2012

@author: shengb
'''
from __future__ import print_function
import sys

import xlrd

try:
    import simplejson as json
except ImportError:
    import json

from pymuniconv import municonvdata

from pymuniconv.municonvprop import (proptmplt, proptmpltdesc, proptmplt_chain, proptmpltdesc_chain)
from rdbinfo import (host, user, pw, db)

def __readdata(xlname, sheetno=0, sheetname=None):
    '''Read data from Excel spreadsheet file using xlrd library.
    '''
    # the working spreadsheet will be close by open_workbook() method automatically when returning
    # unless using on_demand=True. If on_demand is turned True, the file is not closed, even if the workbook is collected.
    # Should be careful to call release_resources() before letting the workbook go away..
    wb = xlrd.open_workbook(xlname)
    sh = wb.sheet_by_index(sheetno)
    
    raw_data = []
    for rownum in range(sh.nrows):
        raw_data.append(sh.row_values(rownum))
    return raw_data

def savesol(fpath):
    ''' save linac solenoid data
    '''
    datafiles = ['hall_probe_LN-SOL-0002-0044_000.xls',
                 'hall_probe_LN-SOL-0003-0043_000.xls',
                 'hall_probe_LN-SOL-0004-0045_000.xls',
                 'hall_probe_LN-SOL-0005-0053_000.xls',
                 'hall_probe_LN-SOL-0006-0055_000.xls',
                 'hall_probe_LN-SOL-0007-0060_000.xls',
                 'hall_probe_LN-SOL-0008-0062_000.xls',
                 'hall_probe_LN-SOL-0009-0050_000.xls',
                 'hall_probe_LN-SOL-0010-0051_000.xls',
                 'hall_probe_LN-SOL-0011-0059_000.xls',
                 'hall_probe_LN-SOL-0012-0046_000.xls',
                 'hall_probe_LN-SOL-0013-0048_000.xls',
                 'hall_probe_LN-SOL-0014-0049_000.xls',
                 'hall_probe_LN-SOL-0015-0004_000.xls',
                 'hall_probe_LN-SOL-0016-0005_000.xls',
                 'hall_probe_LN-SOL-0017-0047_000.xls',
                 'hall_probe_LN-SOL-0018-0058_000.xls',
                 'hall_probe_LN-SOL-0019-0057_000.xls',
                 'hall_probe_LN-SOL-0020-0056_000.xls']
    devtype = 'LN Solenoid'
    devsn = [44, 43, 45, 53, 55, 60, 62, 50, 51, 59, 46, 48, 49, 4, 5, 47, 58, 57, 56]
    devname = ['LN-SO2', 'LN-SO3', 'LN-SO4', 'LN-SO5', 'LN-SO6', 'LN-SO7',
               'LN-SO8', 'LN-SO9', 'LN-SO10', 'LN-SO11', 'LN-SO12', 'LN-SO13',
               'LN-SO14', 'LN-SO15', 'LN-SO16', 'LN-SO17', 'LN-SO18', 'LN-SO19',
               'LN-SO20']
    section="Linac"
    vendor = "RI"
    
    ####################################
    # save component type
    ####################################
    cmpnttypeid = municonv.retrievecmpnttype(devtype, vendor=vendor)
    if len(cmpnttypeid) == 0:
        cmpnttypeid = municonv.savecmpnttype(devtype, "solenoid accelerator for linac", "RI")
        ctid = cmpnttypeid[0]
        #vndrid = cmpnttypeid[1]
    else:
        ctid = cmpnttypeid[0][0]
        #vndrid = cmpnttypeid[0][4]
    
    ####################################
    # save inventory property template
    # the key name for unit conversion is:
    #    "municonv"
    ####################################
    invproptmplt = municonv.retrieveinventoryproptmplt(proptmplt, ctid, desc=proptmpltdesc)
    if len(invproptmplt):
        invproptmpltid = invproptmplt[0][0]
    else:
        invproptmpltid = municonv.saveinventoryproptmplt(proptmplt, ctid, desc=proptmpltdesc)
    
    ####################################
    # deal with data
    ####################################
    length = len(datafiles)
    if length != len(devsn) or length != len(devname):
        raise ValueError('data length does not match each other.')
    for i in range(length):
        ####################################
        # Read data in first before doing anything
        ####################################        
        datafile = '/'.join((fpath,datafiles[i]))
        data = __readdata(datafile)

        if data[3][0] == 'Serial Number':
            # Raise an exception if the serial non does not match
            if devsn[i] != int(data[3][1]):
                raise ValueError("Serial no (%s) does not match that in spreadsheet file (%s)." %(devsn[i], int(data[3][1])))
        else:
            raise TypeError("Wrong spreadsheet format.")

        ####################################
        # Save inventory
        ####################################
        # check inventory entry first
        res = ()
        try:
            res = municonv.retrieveinventory(str(devsn[i]), devtype, vendor)
        except:
            pass
        if len(res) == 0:
            # save inventory
            invid = municonv.saveinventory(str(devsn[i]), devtype, vendor)
        elif len(res) == 1:
            invid = res[0][0]
        else:
            raise Exception("More than one inventory entity found for %s (SN: %s) at %s with component type %s" 
                            %(devname[i], str(devsn[i]), section, devtype))

        ####################################
        # Save installation
        ####################################
        # retrieve install to check whether it exists already.
        res = ()
        try:
            res = municonv.retrieveinstall(devname[i], ctypename=devtype, location=section)
        except:
            pass
        if len(res) == 0:
            # save install
            instid = municonv.saveinstall(devname[i], ctid, section, inventoryid=invid)
        elif len(res) == 1:
            instid = res[0][0]
        else:
            raise Exception("More than one install entity found for %s at %s with component type %s" 
                            %(devname[i], section, devtype))
        
        ####################################
        # Link inventory and installation
        ####################################
        municonv.inventory2install(instid, invid)

        ####################################
        # Create a parameter dictionary
        ####################################
        paramdict = {'elem_name': devname[i],
                     'device_name': devname[i],
                     'serial': devsn[i],
                     'current_unit': 'A',
                     'field_unit': 'T'
                     }
        slope = None
        if data[0][10] == 'slope' and data[0][11] != '':
            slope = data[0][11]
        offset = None
        if data[2][10] == 'offset' and data[2][11] != '':
            offset = data[2][11]

        #print(slope, offset)
        if slope and offset:
            if offset < 0.0:
                paramdict['i2b'] = [0, '%s*input %s' %(slope, offset)]
            else:
                paramdict['i2b'] = [0, '%s*input + %s' %(slope, offset)]

        if data[4][10] == 'magnet_len_meas' and data[4][11] != '':
            paramdict['magnetic_len_meas'] = data[4][11]
        
        if data[0][1] != "" and data[0][0] == 'Magnet Type':
            paramdict['ref_draw'] = data[0][1] 
        
        if data[5][1] != "" and data[5][0] == 'Reference_Radius':
            paramdict['ref_radius'] = float(data[5][1])/1000.00
        
        current=[]
        sig_current=[]
        field=[]
        sig_field=[]
        mag_len=[]
        direction=[]
        for vals in data[11:]:
            current.append(vals[3])
            sig_current.append(vals[4])
            direction.append(vals[5])
            field.append(vals[8])
            sig_field.append(vals[9])
            mag_len.append(vals[13])
        
        paramdict['current'] = current
        paramdict['sig_current'] = sig_current
        paramdict['field'] = field
        paramdict['sig_field'] = sig_field
        paramdict['direction'] = direction
        paramdict['magnetic_len'] = mag_len

        jsondump = json.dumps({'standard':paramdict})
        try:
            municonv.saveinventoryprop(jsondump, invid, invproptmpltid)
        except:
            municonv.updateinventoryprop(jsondump, invid, invproptmpltid)
        
#    retrievedata = municonv.retrieveinventoryprop(invid, invproptmpltid)
#    if len(retrievedata) == 1:
##        print (retrievedata[0][0], retrievedata[0][2], retrievedata[0][3])
#        dump = retrievedata[0][1]
#        print (dump)
##        print (type(dump))
#        restoredata = json.loads(dump)
##        print (restoredata)
##        print (type(restoredata))
#        print (restoredata['i2b'])
#    else:
#        raise ValueError('More than one entry found in inventory property table for municonv.')

def savesolavg(fpath):
    '''save average solenoid data. The hardware in this group is a chain, and powered by a common power supply.
    '''
    chainedatafile = 'ChainedSolenoidCalibration.xlsx'
    
    devtype = 'LN Solenoid'
    devsn = [43, 45, 53, 55, 60, 62, 50, 51, 59, 46, 48, 49, 4, 5, 47, 58, 57, 56]
    devname = ['LN-SO3', 'LN-SO4', 'LN-SO5', 'LN-SO6', 'LN-SO7',
               'LN-SO8', 'LN-SO9', 'LN-SO10', 'LN-SO11', 'LN-SO12', 'LN-SO13',
               'LN-SO14', 'LN-SO15', 'LN-SO16', 'LN-SO17', 'LN-SO18', 'LN-SO19',
               'LN-SO20']
    section="Linac"
    vendor = "RI"
    
    ####################################
    # check data length
    ####################################    
    if len(devsn) != len(devname):
        raise ValueError('data length does not match each other.')

    ####################################
    # save component type
    ####################################
    cmpnttypeid = municonv.retrievecmpnttype(devtype, vendor=vendor)
    if len(cmpnttypeid) == 0:
        cmpnttypeid = municonv.savecmpnttype(devtype, "solenoid accelerator for linac", "RI")
        ctid = cmpnttypeid[0]
        #vndrid = cmpnttypeid[1]
    else:
        ctid = cmpnttypeid[0][0]
        #vndrid = cmpnttypeid[0][4]
    
    ####################################
    # save inventory property template
    # the key name for unit conversion is:
    #    "municonv_chain"
    ####################################
    invproptmplt = municonv.retrieveinventoryproptmplt(proptmplt_chain, ctid, desc=proptmpltdesc_chain)
    if len(invproptmplt):
        invproptmpltid = invproptmplt[0][0]
    else:
        invproptmpltid = municonv.saveinventoryproptmplt(proptmplt_chain, ctid, desc=proptmpltdesc_chain)
    
    ####################################
    # Read data in first before doing anything
    ####################################        
    data = __readdata('/'.join((fpath,chainedatafile)))
    startidx = 4
    
    ####################################
    # deal with data
    ####################################
    for i in range(len(devsn)):
        ####################################
        # Save inventory
        ####################################
        # check inventory entry first
        res = ()
        try:
            res = municonv.retrieveinventory(str(devsn[i]), devtype, vendor)
        except:
            pass
        if len(res) == 0:
            # save inventory
            invid = municonv.saveinventory(str(devsn[i]), devtype, vendor)
        elif len(res) == 1:
            invid = res[0][0]
        else:
            raise Exception("More than one inventory entity found for %s (SN: %s) at %s with component type %s" 
                            %(devname[i], str(devsn[i]), section, devtype))
#        print (invid)

        paramdict = {}
        
        line = startidx + i/2
        p1 = float(data[line][1])
        p2 = float(data[line][2])
        p3 = float(data[line][3])
        slope = p1*(1.0 - p3)
        offset = p2*(1.0 - p3)
        if offset < 0.0:
            paramdict['i2b'] = [0, '%s*input %s' %(slope, offset)]
        else:
            paramdict['i2b'] = [0, '%s*input + %s' %(slope, offset)]
        paramdict['raw'] = "(%s*I+%s)*(1-%s)"%(p1, p2, p3)

        jsondump = json.dumps({'standard':paramdict})
        try:
            municonv.saveinventoryprop(jsondump, invid, invproptmpltid)
        except:
            municonv.updateinventoryprop(jsondump, invid, invproptmpltid)

#        print(jsondump)
#    retrievedata = municonv.retrieveinventoryprop(invid, invproptmpltid)
#    if len(retrievedata) == 1:
#        print (retrievedata[0][0], retrievedata[0][2], retrievedata[0][3])
#        dump = retrievedata[0][1]
#        print (dump)
#        print (type(dump))
#        restoredata = json.loads(dump)
#        print (restoredata)
#        print (type(restoredata))
#    else:
#        raise ValueError('More than one entry found in inventory property table for municonv.')


def savelnqdp(fpath):
    '''save linac quadrupole data
    '''
    datafiles = ['hall_probe_LN-QDP-0000-0001_000.xls',
                 'hall_probe_LN-QDP-0000-0002_000.xls',
                 'hall_probe_LN-QDP-0000-0003_000.xls',
                 'hall_probe_LN-QDP-0000-0004_000.xls',
                 'hall_probe_LN-QDP-0000-0005_000.xls',
                 'hall_probe_LN-QDP-0000-0006_000.xls',
                 'hall_probe_LN-QDP-0000-0007_000.xls',
                 'hall_probe_LN-QDP-0000-0008_000.xls',
                 'hall_probe_LN-QDP-0000-0009_000.xls']
    devtype = 'LN Quadrupole'
    # the serial # are fake
    devsn = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    devname = ['LN-Q1', 'LN-Q2', 'LN-Q3',
               'LN-Q4', 'LN-Q5', 'LN-Q6',
               'LN-Q7', 'LN-Q8', 'LN-Q9']
    designlen = [0.10, 0.10, 0.10, 
                 0.10, 0.10, 0.10, 
                 0.10, 0.10, 0.10]
    section="Linac"
    vendor = "RI"

    ####################################
    # save component type
    ####################################
    cmpnttypeid = municonv.retrievecmpnttype(devtype, vendor=vendor)
    if len(cmpnttypeid) == 0:
        cmpnttypeid = municonv.savecmpnttype(devtype, "quadrupole magnet for linac", "RI")
        ctid = cmpnttypeid[0]
        #vndrid = cmpnttypeid[1]
    else:
        ctid = cmpnttypeid[0][0]
        #vndrid = cmpnttypeid[0][4]
    
    ####################################
    # save inventory property template
    # the key name for unit conversion is:
    #    "municonv"
    ####################################
    invproptmplt = municonv.retrieveinventoryproptmplt(proptmplt, ctid, desc=proptmpltdesc)
    if len(invproptmplt):
        invproptmpltid = invproptmplt[0][0]
    else:
        invproptmpltid = municonv.saveinventoryproptmplt(proptmplt, ctid, desc=proptmpltdesc)
    
    ####################################
    # deal with data
    ####################################
    length = len(datafiles)
    if length != len(devsn) or length != len(devname):
        raise ValueError('data length does not match each other.')
    for i in range(length):
        ####################################
        # Read data in first before doing anything
        ####################################        
        datafile = '/'.join((fpath,datafiles[i]))
        data = __readdata(datafile)

        if data[3][0] == 'Serial Number':
            # Raise an exception if the serial non does not match
            if devsn[i] != int(data[3][1]):
                raise ValueError("Serial no (%s) does not match that in spreadsheet file (%s)." %(devsn[i], int(data[3][1])))
        else:
            raise TypeError("Wrong spreadsheet format.")

        ####################################
        # Save inventory
        ####################################
        # check inventory entry first
        res = ()
        try:
            res = municonv.retrieveinventory(str(devsn[i]), devtype, vendor)
        except:
            pass
        if len(res) == 0:
            # save inventory
            invid = municonv.saveinventory(str(devsn[i]), devtype, vendor)
        elif len(res) == 1:
            invid = res[0][0]
        else:
            raise Exception("More than one inventory entity found for %s (SN: %s) at %s with component type %s" 
                            %(devname[i], str(devsn[i]), section, devtype))

        ####################################
        # Save installation
        ####################################
        # retrieve install to check whether it exists already.
        res = ()
        try:
            res = municonv.retrieveinstall(devname[i], ctypename=devtype, location=section)
        except:
            pass
        if len(res) == 0:
            # save install
            instid = municonv.saveinstall(devname[i], ctid, section, inventoryid=invid)
        elif len(res) == 1:
            instid = res[0][0]
        else:
            raise Exception("More than one install entity found for %s at %s with component type %s" 
                            %(devname[i], section, devtype))
        
        ####################################
        # Link inventory and installation
        ####################################
        municonv.inventory2install(instid, invid)

        ####################################
        # Create a parameter dictionary
        ####################################
        paramdict = {'elem_name': devname[i],
                     'device_name': devname[i],
                     'serial': devsn[i],
                     'magnetic_len_design': designlen[i],
                     'current_unit': 'A',
                     'field_unit': 'T'
                     }
        slope = None
        if data[0][10] == 'slope' and data[0][11] != '':
            slope = data[0][11]
        offset = None
        if data[2][10] == 'offset' and data[2][11] != '':
            offset = data[2][11]

        #print(slope, offset)
        if slope and offset:
            if offset < 0.0:
                paramdict['i2b'] = [0, '%s*input %s' %(slope, offset)]
            else:
                paramdict['i2b'] = [0, '%s*input + %s' %(slope, offset)]

        if data[4][10] == 'magnetic_len_meas' and data[4][11] != '':
            paramdict['magnetic_len_meas'] = data[4][11]
        
        if data[0][1] != "" and data[0][0] == 'Magnet Type':
            paramdict['ref_draw'] = data[0][1] 
        
        if data[5][1] != "" and data[5][0] == 'Reference_Radius':
            paramdict['ref_radius'] = float(data[5][1])/1000.00
        
        current=[]
        sig_current=[]
        field=[]
        sig_field=[]
        mag_len=[]
        direction=[]
        for vals in data[11:]:
            current.append(vals[3])
            sig_current.append(vals[4])
            direction.append(vals[5])
            field.append(vals[8])
            sig_field.append(vals[9])
            mag_len.append(vals[13])
        
        paramdict['current'] = current
        paramdict['sig_current'] = sig_current
        paramdict['field'] = field
        paramdict['sig_field'] = sig_field
        paramdict['direction'] = direction
        paramdict['magnetic_len'] = mag_len

        jsondump = json.dumps({'standard':paramdict})
        try:
            municonv.saveinventoryprop(jsondump, invid, invproptmpltid)
        except:
            municonv.updateinventoryprop(jsondump, invid, invproptmpltid)

#    retrievedata = municonv.retrieveinventoryprop(invid, invproptmpltid)
#    if len(retrievedata) == 1:
##        print (retrievedata[0][0], retrievedata[0][2], retrievedata[0][3])
#        dump = retrievedata[0][1]
#        print (dump)
##        print (type(dump))
#        restoredata = json.loads(dump)
##        print (restoredata)
##        print (type(restoredata))
#        print (restoredata['i2b'])
#    else:
#        raise ValueError('More than one entry found in inventory property table for municonv.')

def savelbtdpl(fpath):
    '''save linac to booster transport line dipole data

    since all dipole magnets share the same measurement data set
    save data into component type property table instead of inventory property.
    '''
    datafiles = 'hall_probe_LBT-DPL-4800-0003_000.xls'
    devtype = 'LBT Dipole'
    # the serial
    # refer to "magnet SN assignments.xlsx"
    devsn = [3, 2, 1, 4]
    devname = ['LB-B1', 'LB-B2', 'LB-B3', 'LB-B4']
    designlen = [0.35, 0.35, 0.35, 0.35]

    # use which measure data set 
    # dictionary device name: [reference draw, serial #]
#    use_meas_set = {'LB-B1': ['LBT-MG-DPL-4800', 3],
#                    'LB-B2': ['LBT-MG-DPL-4800', 3],
#                    'LB-B3': ['LBT-MG-DPL-4800', 3],
#                    'LB-B4': ['LBT-MG-DPL-4800', 3]
#                   }
    length = len(devsn)
    if length != len(devname) or length != len(designlen):
        raise ValueError('data length does not match each other.')
    
    section="LBT"
    vendor = "Stangenes, USA"

    ####################################
    # save component type
    ####################################
    cmpnttypeid = municonv.retrievecmpnttype(devtype, vendor=vendor)
    if len(cmpnttypeid) == 0:
        cmpnttypeid = municonv.savecmpnttype(devtype, "dipole magnet for linac to booster transport line", vendor)
        ctid = cmpnttypeid[0]
        #vndrid = cmpnttypeid[1]
    else:
        ctid = cmpnttypeid[0][0]
        #vndrid = cmpnttypeid[0][4]
    
    ####################################
    # save component property property type
    # the key name for unit conversion is:
    #    "municonv"
    ####################################
    # since all dipole magnets share the same measurement data set
    # save data into component type property instead of inventory property
    ctypeproptype = municonv.retrievecmpnttypeproptype(proptmplt, desc=proptmpltdesc)
    
    if len(ctypeproptype):
        ctypeproptypeid = ctypeproptype[0][0]
    else:
        ctypeproptypeid = municonv.savecmpnttypeproptype(proptmplt, desc=proptmpltdesc)
#    print (ctypeproptypeid)
    
    ####################################
    # deal with data
    ####################################
    ####################################
    # Read data in first before doing anything
    ####################################        
    datafile = '/'.join((fpath,datafiles))
    data = __readdata(datafile)
    serial = None
    if data[3][1] != '' and data[3][0] == 'Serial Number':
        serial = data[3][1]
    idx = None
    if serial:
        serial = int(serial)
        for i in range(length):
            if devsn[i] == serial:
                idx = i
                break
    if idx == None:
        raise ValueError("Cannot find the device in the list. Please check the serial number.")

    ####################################
    # Create a parameter dictionary
    ####################################
    paramdict = {'elem_name': devname[idx],
                 'device_name': devname[idx],
                 'serial': serial,
                 'energy_default': 0.2,
                 'current_unit': 'A',
                 'field_unit': 'T-m',
                 'magnetic_len_design': designlen[idx]
                 }
    slope = None
    if data[0][10] == 'slope' and data[0][11] != '':
        slope = data[0][11]
    offset = None
    if data[2][10] == 'offset' and data[2][11] != '':
        offset = data[2][11]

    #print(slope, offset)
    if slope and offset:
        if offset < 0.0:
            paramdict['i2b'] = [0, '%s*input %s' %(slope, offset)]
        else:
            paramdict['i2b'] = [0, '%s*input + %s' %(slope, offset)]

    if data[4][10] == 'magnetic_len_meas' and data[4][11] != '':
        paramdict['magnetic_len_meas'] = data[4][11]
    
    if data[0][1] != "" and data[0][0] == 'Magnet Type':
        paramdict['ref_draw'] = data[0][1] 
    
    if data[5][1] != "" and data[5][0] == 'Reference_Radius':
        paramdict['ref_radius'] = float(data[5][1])/1000.00
    
    if data[5][10] == 'brho' and data[5][11] != '':
        paramdict['brho'] = data[5][11]
    
    if data[6][10] == 'brho_unit' and data[6][11] != '':
        paramdict['brho_unit'] = data[6][11]

    current=[]
    sig_current=[]
    field=[]
    sig_field=[]
    mag_len=[]
    direction=[]
    run = []
    for vals in data[11:]:
        run.append(vals[1])
        current.append(vals[3])
        sig_current.append(vals[4])
        direction.append(vals[5])
        field.append(vals[8])
        sig_field.append(vals[9])
        mag_len.append(vals[13])
    
    paramdict['run_number'] = run
    paramdict['current'] = current
    paramdict['sig_current'] = sig_current
    paramdict['field'] = field
    paramdict['sig_field'] = sig_field
    paramdict['direction'] = direction
    paramdict['magnetic_len'] = mag_len

    jsondump = json.dumps({'standard':paramdict})
    try:
        municonv.savecmpnttypeprop(jsondump, ctid, ctypeproptypeid)
    except:
        municonv.updateinventoryprop(jsondump, ctid, ctypeproptypeid)

    ####################################
    # save inventory and installation
    ####################################
    for i in range(length):
        ####################################
        # Save inventory
        ####################################
        # check inventory entry first
        res = ()
        try:
            res = municonv.retrieveinventory(str(devsn[i]), devtype, vendor)
        except:
            pass
        if len(res) == 0:
            # save inventory
            invid = municonv.saveinventory(str(devsn[i]), devtype, vendor)
        elif len(res) == 1:
            invid = res[0][0]
        else:
            raise Exception("More than one inventory entity found for %s (SN: %s) at %s with component type %s" 
                            %(devname[i], str(devsn[i]), section, devtype))

        ####################################
        # Save installation
        ####################################
        # retrieve install to check whether it exists already.
        res = ()
        try:
            res = municonv.retrieveinstall(devname[i], ctypename=devtype, location=section)
        except:
            pass
        if len(res) == 0:
            # save install
            instid = municonv.saveinstall(devname[i], ctid, section, inventoryid=invid)
        elif len(res) == 1:
            instid = res[0][0]
        else:
            raise Exception("More than one install entity found for %s at %s with component type %s" 
                            %(devname[i], section, devtype))
        
        ####################################
        # Link inventory and installation
        ####################################
        municonv.inventory2install(instid, invid)

def savequad1340(fpath):
    '''save quadrupole with 134mm aperture.
    This type of quadrupole is used in linac to booster transport line with 2 installed only.

    since all dipole magnets share the same measurement data set
    save data into component type property table instead of inventory property.
    '''
    datafiles = 'rot_coil_LBT-QDP-1340-0001_000.xls'
    devtype = 'LBT Quadrupole 1340'
    # the serial
    # refer to "magnet SN assignments.xlsx"
    devsn = [2, 1]
    devname = ['LB-Q5', 'LB-Q6']
    designlen = [0.25, 0.25]

    # use which measure data set 
    # dictionary device name: [reference draw, serial #]
#    use_meas_set = {'LB-B1': ['LBT-MG-DPL-4800', 3],
#                    'LB-B2': ['LBT-MG-DPL-4800', 3],
#                    'LB-B3': ['LBT-MG-DPL-4800', 3],
#                    'LB-B4': ['LBT-MG-DPL-4800', 3]
#                   }
    length = len(devsn)
    if length != len(devname) or length != len(designlen):
        raise ValueError('data length does not match each other.')
    
    section="LBT"
    vendor = "Stangenes, USA"

    ####################################
    # save component type
    ####################################
    cmpnttypeid = municonv.retrievecmpnttype(devtype, vendor=vendor)
    if len(cmpnttypeid) == 0:
        cmpnttypeid = municonv.savecmpnttype(devtype, "quadrupole magnet with 134mm aperture.", vendor)
        ctid = cmpnttypeid[0]
    else:
        ctid = cmpnttypeid[0][0]
    
    ####################################
    # save component property property type
    # the key name for unit conversion is:
    #    "municonv"
    ####################################
    # since all 134mm quadrupole magnets share the same measurement data set
    # save data into component type property instead of inventory property
    ctypeproptype = municonv.retrievecmpnttypeproptype(proptmplt, desc=proptmpltdesc)
    
    if len(ctypeproptype):
        ctypeproptypeid = ctypeproptype[0][0]
    else:
        ctypeproptypeid = municonv.savecmpnttypeproptype(proptmplt, desc=proptmpltdesc)
#    print (ctypeproptypeid)
    
    ####################################
    # deal with data
    ####################################
    ####################################
    # Read data in first before doing anything
    ####################################        
    datafile = '/'.join((fpath,datafiles))
    data = __readdata(datafile)
    serial = None
    if data[3][1] != '' and data[3][0] == 'Serial Number':
        serial = data[3][1]
    idx = None
    if serial:
        serial = int(serial)
        for i in range(length):
            if devsn[i] == serial:
                idx = i
                break
    if idx == None:
        raise ValueError("Cannot find the device in the list. Please check the serial number.")

    ####################################
    # Create a parameter dictionary
    ####################################
    paramdict = {'elem_name': devname[idx],
                 'device_name': devname[idx],
                 'serial': serial,
                 'energy_default': 0.2,
                 'current_unit': 'A',
                 'field_unit': 'T',
                 'magnetic_len_design': designlen[idx]
                 }
    slope = None
    if data[0][10] == 'slope' and data[0][11] != '':
        slope = data[0][11]
    offset = None
    if data[2][10] == 'offset' and data[2][11] != '':
        offset = data[2][11]

#    #print(slope, offset)
    if slope and offset:
        if offset < 0.0:
            paramdict['i2b'] = [0, '%s*input %s' %(slope, offset)]
        else:
            paramdict['i2b'] = [0, '%s*input + %s' %(slope, offset)]

    if data[4][10] == 'magnetic_len_meas' and data[4][11] != '':
        paramdict['magnetic_len_meas'] = data[4][11]
    
    if data[0][1] != "" and data[0][0] == 'Magnet Type':
        paramdict['ref_draw'] = data[0][1] 
    
    if data[5][1] != "" and data[5][0] == 'Reference_Radius':
        paramdict['ref_radius'] = data[5][1]

    # need to confirm this function.
    # format: algorithm id, algorithm expression, field order (1: dipole; 2: Quad, K1; 3: Sext, K2)
    paramdict['b2k'] = [0, "input/(3.335646*energy)", 2]
    
    current=[]
    sig_current=[]
    field=[]
    sig_field=[]
    mag_len=[]
    direction=[]
    for vals in data[11:]:
        current.append(vals[3])
        sig_current.append(vals[4])
        direction.append(vals[5])
        field.append(vals[8])
        sig_field.append(vals[9])
        mag_len.append(vals[13])

    paramdict['current'] = current
    paramdict['sig_current'] = sig_current
    paramdict['field'] = field
    paramdict['sig_field'] = sig_field
    paramdict['direction'] = direction
    paramdict['magnetic_len'] = mag_len

    jsondump = json.dumps({'standard':paramdict})
    try:
        municonv.savecmpnttypeprop(jsondump, ctid, ctypeproptypeid)
    except:
        municonv.updateinventoryprop(jsondump, ctid, ctypeproptypeid)

    ####################################
    # save inventory and installation
    ####################################
    for i in range(length):
        ####################################
        # Save inventory
        ####################################
        # check inventory entry first
        res = ()
        try:
            res = municonv.retrieveinventory(str(devsn[i]), devtype, vendor)
        except:
            pass
        if len(res) == 0:
            # save inventory
            invid = municonv.saveinventory(str(devsn[i]), devtype, vendor)
        elif len(res) == 1:
            invid = res[0][0]
        else:
            raise Exception("More than one inventory entity found for %s (SN: %s) at %s with component type %s" 
                            %(devname[i], str(devsn[i]), section, devtype))

        ####################################
        # Save installation
        ####################################
        # retrieve install to check whether it exists already.
        res = ()
        try:
            res = municonv.retrieveinstall(devname[i], ctypename=devtype, location=section)
        except:
            pass
        if len(res) == 0:
            # save install
            instid = municonv.saveinstall(devname[i], ctid, section, inventoryid=invid)
        elif len(res) == 1:
            instid = res[0][0]
        else:
            raise Exception("More than one install entity found for %s at %s with component type %s" 
                            %(devname[i], section, devtype))
        
        ####################################
        # Link inventory and installation
        ####################################
        municonv.inventory2install(instid, invid)
    
def savequad5200(fpath, section):
    '''save linac to booster transport line quadrupole data

    This type of quadrupole is used in linac to booster transport line and booster to storage ring transport line.

    since all dipole magnets share the same measurement data set
    save data into component type property table instead of inventory property.
    '''
    devtype = '%s Quadrupole 5200'%(section)
    data_pattern = 'rot_coil_%s'%section
    data_pattern += '-QDP-%s-%s_%s.xls'

    if section == "BST":
        default_energy = 3.0
        # serial #
        # refer to "magnet SN assignments.xlsx"
        devsn = [1, 2, 3, 4, 
                 5, 6, 7, 10, 
                 11, 12, 13, 14,
                 15, 16,
                 8, 9]
        devname = ['BS-Q1', 'BS-Q2', 'BS-Q3', 'BS-Q4', 
                   'BS-Q5', 'BS-Q6', 'BS-Q7', 'BS-Q8',
                   'BS-Q9', 'BS-Q10','BS-Q11','BS-Q12',
                   'BS-Q13', 'BS-Q14',
                   'BS-Q1BD1', 'BS-Q2BD1']
        designlen = [0.35, 0.35, 0.35, 0.35,
                     0.35, 0.35, 0.35, 0.35,
                     0.35, 0.35, 0.35, 0.35,
                     0.35, 0.35,
                     0.35, 0.35]
        # the following mapping need to be update.
        # It is for development purpose only.
        # dict format: dev name: [reference draw, serial, run #
        use_meas_set = {'BS-Q1': ['BST-MG-QDP-5200', 1, 1],
                        'BS-Q2': ['BST-MG-QDP-5200', 2, 0],
                        'BS-Q3': ['BST-MG-QDP-5200', 3, 0],
                        'BS-Q4': ['BST-MG-QDP-5200', 4, 0],
                        'BS-Q5': ['BST-MG-QDP-5200', 5, 0],
                        'BS-Q6': ['BST-MG-QDP-5200', 6, 0],
                        'BS-Q7': ['BST-MG-QDP-5200', 7, 0],
                        'BS-Q8': ['BST-MG-QDP-5200', 10, 0],
                        'BS-Q9': ['BST-MG-QDP-5200', 11, 0],
                        'BS-Q10': ['BST-MG-QDP-5200',12, 0],
                        'BS-Q11': ['BST-MG-QDP-5200',13, 0],
                        'BS-Q12': ['BST-MG-QDP-5200',14, 1],
                        'BS-Q13': ['BST-MG-QDP-5200',15, 0],
                        'BS-Q14': ['BST-MG-QDP-5200',16, 0],
                        'BS-Q2BD1': ['BST-MG-QDP-5200',8, 0],
                        'BS-Q1BD1': ['BST-MG-QDP-5200',9, 0],                        
                        }
    elif section == "LBT":
        default_energy = 0.2
        # serial #
        # refer to "magnet SN assignments.xlsx"
        # LB-Q5 and LB-Q6 are 134mm quad, which is LBT-MG-QDP-1340
        devsn = [1, 2, 6, 5, 
                 4, 9, 13, 8, 
                 10, 11, 12, 14,
                 15, 7, 3]
        devname = ['LB-Q1', 'LB-Q2', 'LB-Q3', 'LB-Q4', 
                   'LB-Q7', 'LB-Q8', 'LB-Q9', 'LB-Q10',
                   'LB-Q11', 'LB-Q12', 'LB-Q13', 'LB-Q14', 'LB-Q15',
                   'LB-Q1BD1', 'LB-Q2BD1']
        designlen = [0.15, 0.15, 0.15, 0.15,
                     0.15, 0.15, 0.15, 0.15,
                     0.15, 0.15, 0.15, 0.15,
                     0.15, 0.15, 0.15]
        # the following mapping need to be update.
        # It is for development purpose only.
        # dict format: dev name: [reference draw, serial, run #
        # Measurement data not available for:
        # LBT-MG-QDP-5200: 1, 2, 4, 5, 6, 7
        #                  1, 2, 4, 5, 6 => use #8 data
        #                  7 => use #3 data
        use_meas_set = {'LB-Q1': ['LBT-MG-QDP-5200', 8, 0],
                        'LB-Q2': ['LBT-MG-QDP-5200', 8, 0],
                        'LB-Q3': ['LBT-MG-QDP-5200', 9, 0],
                        'LB-Q4': ['LBT-MG-QDP-5200', 8, 0],
                        'LB-Q7': ['LBT-MG-QDP-5200', 8, 0],
                        'LB-Q1BD1': ['LBT-MG-QDP-5200',3, 0],
                        
                        'LB-Q8': ['LBT-MG-QDP-5200', 9, 0],
                        'LB-Q9': ['LBT-MG-QDP-5200', 13, 0],
                        'LB-Q10': ['LBT-MG-QDP-5200',8, 0],
                        'LB-Q11': ['LBT-MG-QDP-5200',10, 0],
                        'LB-Q12': ['LBT-MG-QDP-5200',11, 0],
                        'LB-Q13': ['LBT-MG-QDP-5200',12, 0],
                        'LB-Q14': ['LBT-MG-QDP-5200',14, 0],
                        'LB-Q15': ['LBT-MG-QDP-5200',15, 0],
                        'LB-Q2BD1': ['LBT-MG-QDP-5200',3, 0]}
    else:
        raise ValueError("QDP 5200 only available in section LBT/BST.")
    
    vendor = "Stangenes, USA"

    ####################################
    # save component type
    ####################################
    cmpnttypeid = municonv.retrievecmpnttype(devtype, vendor=vendor)
    if len(cmpnttypeid) == 0:
        cmpnttypeid = municonv.savecmpnttype(devtype, "quadrupole magnet with 52mm aperture", vendor)
        ctid = cmpnttypeid[0]
    else:
        ctid = cmpnttypeid[0][0]

    ####################################
    # save inventory property template
    # the key name for unit conversion is:
    #    "municonv"
    ####################################
    invproptmplt = municonv.retrieveinventoryproptmplt(proptmplt, ctid, desc=proptmpltdesc)
    if len(invproptmplt):
        invproptmpltid = invproptmplt[0][0]
    else:
        invproptmpltid = municonv.saveinventoryproptmplt(proptmplt, ctid, desc=proptmpltdesc)
    
    ####################################
    # deal with data
    ####################################
    length = len(use_meas_set)
    if length != len(devsn) or length != len(devname) or length != len(designlen):
        raise ValueError('data length does not match each other.')
    for i in range(length):
        data_set = use_meas_set[devname[i]]
        mag_type = data_set[0].split('-')[3]
        sn = str(data_set[1]).zfill(4)
        runno = str(data_set[2]).zfill(3)
        # get data file name
        datafile = data_pattern%(mag_type, sn, runno)

        ####################################
        # Read data in first before doing anything
        ####################################
        # get full path of data file        
        datafile = '/'.join((fpath,datafile))
        data = __readdata(datafile)

        if data[3][0] == 'Serial Number':
            # Raise an exception if the serial non does not match
            if use_meas_set[devname[i]][1] != int(data[3][1]):
                raise ValueError("Serial no (%s) does not match that in spreadsheet file (%s)." %(devsn[i], int(data[3][1])))
        else:
            raise TypeError("Wrong spreadsheet format.")

        ####################################
        # Save inventory
        ####################################
        # check inventory entry first
        res = ()
        try:
            res = municonv.retrieveinventory(str(devsn[i]), devtype, vendor)
        except:
            pass
        if len(res) == 0:
            # save inventory
            invid = municonv.saveinventory(str(devsn[i]), devtype, vendor)
        elif len(res) == 1:
            invid = res[0][0]
        else:
            raise Exception("More than one inventory entity found for %s (SN: %s) at %s with component type %s" 
                            %(devname[i], str(devsn[i]), section, devtype))

        ####################################
        # Save installation
        ####################################
        # retrieve install to check whether it exists already.
        res = ()
        try:
            res = municonv.retrieveinstall(devname[i], ctypename=devtype, location=section)
        except:
            pass
        if len(res) == 0:
            # save install
            instid = municonv.saveinstall(devname[i], ctid, section, inventoryid=invid)
        elif len(res) == 1:
            instid = res[0][0]
        else:
            raise Exception("More than one install entity found for %s at %s with component type %s" 
                            %(devname[i], section, devtype))
        
        ####################################
        # Link inventory and installation
        ####################################
        municonv.inventory2install(instid, invid)

        ####################################
        # Create a parameter dictionary
        ####################################
        paramdict = {'elem_name': devname[i],
                     'device_name': devname[i],
                     'serial': devsn[i],
                     'energy_default': default_energy,
                     'magnetic_len_design': designlen[i],
                     'current_unit': 'A',
                     'field_unit': 'T-m'
                     }
        if section == "LBT":
            slope = None
            if data[0][10] == 'slope' and data[0][11] != '':
                slope = data[0][11]
            offset = None
            if data[2][10] == 'offset' and data[2][11] != '':
                offset = data[2][11]
    
            #print(slope, offset)
            if slope and offset:
                if offset < 0.0:
                    paramdict['i2b'] = [0, '%s*input %s' %(slope, offset)]
                else:
                    paramdict['i2b'] = [0, '%s*input + %s' %(slope, offset)]
        elif section == "BST":
            secondary = None
            if data[0][12] == '2nd order' and data[0][13] != '':
                secondary = data[0][13]
            slope = None
            if data[0][10] == 'slope' and data[0][11] != '':
                slope = data[0][11]
            offset = None
            if data[2][10] == 'offset' and data[2][11] != '':
                offset = data[2][11]
    
            function = ""
            if secondary:
                function = "%s*input**2" %(secondary)
            if slope:
                if slope < 0:
                    function += " %s*input " %slope
                else:
                    function += " + %s*input " %slope
            if offset:
                if offset < 0.0:
                    function += " %s " %offset
                else:
                    function += " + %s " %offset
            if function == "":
                raise ValueError("Cannot identofy function.")
            paramdict['i2b'] = [1, function]
        else:
            raise ValueError("QDP 5200 only available in section LBT/BST.")

        if data[4][10] == 'magnetic_len_meas' and data[4][11] != '':
            paramdict['magnetic_len_meas'] = data[4][11]

        if data[0][1] != "" and data[0][0] == 'Magnet Type':
            paramdict['ref_draw'] = data[0][1] 
        
        if data[5][1] != "" and data[5][0] == 'Reference_Radius':
            paramdict['ref_radius'] = float(data[5][1])/1000.0
            paramdict['b2k'] = [0, "input/(%s*3.335646*energy)"%(paramdict['ref_radius']), 2]
        
        current=[]
        field=[]
        direction=[]
        run = []
        for vals in data[11:]:
            if vals[3] == "":
                break
            run.append(vals[1])
            current.append(vals[3])
            direction.append(vals[6])
            field.append(vals[13])

        paramdict['run_number'] = run
        paramdict['current'] = current
        paramdict['field'] = field
        paramdict['direction'] = direction

        jsondump = json.dumps({'standard':paramdict})
        try:
            municonv.saveinventoryprop(jsondump, invid, invproptmpltid)
        except:
            municonv.updateinventoryprop(jsondump, invid, invproptmpltid)

#    retrievedata = municonv.retrieveinventoryprop(invid, invproptmpltid)
#    if len(retrievedata) == 1:
##        print (retrievedata[0][0], retrievedata[0][2], retrievedata[0][3])
#        dump = retrievedata[0][1]
##        import pprint
##        pprint.pprint (dump)
##        print (type(dump))
#        restoredata = json.loads(dump)
#        import pprint
#        pprint.pprint (restoredata)
##        print (type(restoredata))
#        print (restoredata['i2b'])
#    else:
#        raise ValueError('More than one entry found in inventory property table for municonv.')

def savedpl9035(fpath):
    '''save booster to storage ring transport line dipole data

    since all dipole magnets share the same measurement data set
    save data into component type property table instead of inventory property.
    
    The dipoles are all powered separately. All have trim coil, but not used currently.
    The data is not loaded into database therefore.
    '''
    datafiles = 'hall_probe_BST-DPL-9035-0001_000.xls'
    devtype = 'BST Dipole'

    #subdevtype = 'BST Dipole Trim'

    # the serial
    # refer to "magnet SN assignments.xlsx"
    devsn = [2, 1, 3, 4]
    devname = ['BS-B1', 'BS-B2', 'BS-B3', 'BS-B4']
    designlen = [1.40, 1.40, 1.40, 1.40]

    length = len(devsn)
    if length != len(devname) or length != len(designlen):
        raise ValueError('data length does not match each other.')
    
    section="BST"
    vendor = "Stangenes, USA"

    ####################################
    # save component type
    ####################################
    cmpnttypeid = municonv.retrievecmpnttype(devtype, vendor=vendor)
    if len(cmpnttypeid) == 0:
        cmpnttypeid = municonv.savecmpnttype(devtype, "dipole magnet for linac to booster transport line", vendor)
        ctid = cmpnttypeid[0]
    else:
        ctid = cmpnttypeid[0][0]
    
    ####################################
    # save component property property type
    # the key name for unit conversion is:
    #    "municonv"
    ####################################
    # since all dipole magnets share the same measurement data set
    # save data into component type property instead of inventory property
    ctypeproptype = municonv.retrievecmpnttypeproptype(proptmplt, desc=proptmpltdesc)
    
    if len(ctypeproptype):
        ctypeproptypeid = ctypeproptype[0][0]
    else:
        ctypeproptypeid = municonv.savecmpnttypeproptype(proptmplt, desc=proptmpltdesc)
#    print (ctypeproptypeid)
    
    ####################################
    # deal with data
    ####################################
    ####################################
    # Read data in first before doing anything
    ####################################
    datafile = '/'.join((fpath,datafiles))
    data = __readdata(datafile)
    serial = None
    if data[3][1] != '' and data[3][0] == 'Serial Number':
        serial = data[3][1]
    idx = None
    if serial:
        serial = int(serial)
        for i in range(length):
            if devsn[i] == serial:
                idx = i
                break
    if idx == None:
        raise ValueError("Cannot find the device in the list. Please check the serial number.")

    ####################################
    # Create a parameter dictionary
    ####################################
    paramdict = {'elem_name': devname[idx],
                 'device_name': devname[idx],
                 'serial': serial,
                 'energy_default': 3.0,
                 'current_unit': 'A',
                 'field_unit': 'T-m',
                 'magnetic_len_design': designlen[i]
                 }
    slope = None
    if data[0][10] == 'slope' and data[0][11] != '':
        slope = data[0][11]
    offset = None
    if data[2][10] == 'offset' and data[2][11] != '':
        offset = data[2][11]

    #print(slope, offset)
    if slope and offset:
        if offset < 0.0:
            paramdict['i2b'] = [0, '%s*input %s' %(slope, offset)]
        else:
            paramdict['i2b'] = [0, '%s*input + %s' %(slope, offset)]

    if data[4][10] == 'magnetic_len_meas' and data[4][11] != '':
        paramdict['magnetic_len_meas'] = data[4][11]
    
    if data[0][1] != "" and data[0][0] == 'Magnet Type':
        paramdict['ref_draw'] = data[0][1] 
    
    if data[5][1] != "" and data[5][0] == 'Reference_Radius':
        paramdict['ref_radius'] = data[5][1]
    
    if data[5][10] == 'brho' and data[5][11] != '':
        paramdict['brho'] = data[5][11]
    
    if data[6][10] == 'brho_unit' and data[6][11] != '':
        paramdict['brho_unit'] = data[6][11]

    current=[]
    field=[]
    for vals in data[11:]:
        current.append(vals[3])
        field.append(vals[8])
    
    paramdict['current'] = current
    paramdict['field'] = field

    jsondump = json.dumps({'standard':paramdict})
    try:
        municonv.savecmpnttypeprop(jsondump, ctid, ctypeproptypeid)
    except:
        municonv.updateinventoryprop(jsondump, ctid, ctypeproptypeid)

    ####################################
    # save inventory and installation
    ####################################
    for i in range(length):
        ####################################
        # Save inventory
        ####################################
        # check inventory entry first
        res = ()
        try:
            res = municonv.retrieveinventory(str(devsn[i]), devtype, vendor)
        except:
            pass
        if len(res) == 0:
            # save inventory
            invid = municonv.saveinventory(str(devsn[i]), devtype, vendor)
        elif len(res) == 1:
            invid = res[0][0]
        else:
            raise Exception("More than one inventory entity found for %s (SN: %s) at %s with component type %s" 
                            %(devname[i], str(devsn[i]), section, devtype))

        ####################################
        # Save installation
        ####################################
        # retrieve install to check whether it exists already.
        res = ()
        try:
            res = municonv.retrieveinstall(devname[i], ctypename=devtype, location=section)
        except:
            pass
        if len(res) == 0:
            # save install
            instid = municonv.saveinstall(devname[i], ctid, section, inventoryid=invid)
        elif len(res) == 1:
            instid = res[0][0]
        else:
            raise Exception("More than one install entity found for %s at %s with component type %s" 
                            %(devname[i], section, devtype))
        
        ####################################
        # Link inventory and installation
        ####################################
        municonv.inventory2install(instid, invid)

def saveboosterdata(devname, devsn, designlen, devtype, dtypedesc, paramdict):
    '''
    '''
    length = len(devsn)
    if length != len(devname) or length != len(designlen):
        raise ValueError('data length does not match each other.')
    
    section="Booster"
    vendor = "BINP, Russia"

    ####################################
    # save component type
    ####################################
    cmpnttypeid = municonv.retrievecmpnttype(devtype, vendor=vendor)
    if len(cmpnttypeid) == 0:
        cmpnttypeid = municonv.savecmpnttype(devtype, dtypedesc, vendor)
        ctid = cmpnttypeid[0]
    else:
        ctid = cmpnttypeid[0][0]
    
    ####################################
    # save component property property type
    # the key name for unit conversion is:
    #    "municonv"
    ####################################
    # since magnets share the same measurement data set for the same type
    # save data into component type property instead of inventory property
    ctypeproptype = municonv.retrievecmpnttypeproptype(proptmplt, desc=proptmpltdesc)
    
    if len(ctypeproptype):
        ctypeproptypeid = ctypeproptype[0][0]
    else:
        ctypeproptypeid = municonv.savecmpnttypeproptype(proptmplt, desc=proptmpltdesc)
#    print (ctypeproptypeid)
    
    jsondump = json.dumps(paramdict)
    try:
        municonv.savecmpnttypeprop(jsondump, ctid, ctypeproptypeid)
    except:
        municonv.updatecmpnttypeprop(jsondump, ctid, ctypeproptypeid)

    ####################################
    # save inventory and installation
    ####################################
    for i in range(length):
        ####################################
        # Save inventory
        ####################################
        # check inventory entry first
        res = ()
        try:
            res = municonv.retrieveinventory(str(devsn[i]), devtype, vendor)
        except:
            pass
        if len(res) == 0:
            # save inventory
            invid = municonv.saveinventory(str(devsn[i]), devtype, vendor)
        elif len(res) == 1:
            invid = res[0][0]
        else:
            raise Exception("More than one inventory entity found for %s (SN: %s) at %s with component type %s" 
                            %(devname[i], str(devsn[i]), section, devtype))

        ####################################
        # Save installation
        ####################################
        # retrieve install to check whether it exists already.
        res = ()
        try:
            res = municonv.retrieveinstall(devname[i], ctypename=devtype, location=section)
        except:
            pass
        if len(res) == 0:
            # save install
            instid = municonv.saveinstall(devname[i], ctid, section, inventoryid=invid)
        elif len(res) == 1:
            instid = res[0][0]
        else:
            raise Exception("More than one install entity found for %s at %s with component type %s" 
                            %(devname[i], section, devtype))
        
        ####################################
        # Link inventory and installation
        ####################################
        municonv.inventory2install(instid, invid)

def createfit(k):
    fitting = "%s*input**4" %k[0]
    if k[1] < 0:
        fitting += " %s*input**3" %k[1]
    else:
        fitting += " + %s*input**3" %k[1]
    if k[2] < 0:
        fitting += " %s*input**2" %k[2]
    else:
        fitting += " + %s*input**2" %k[2]
    if k[3] < 0:
        fitting += " %s*input" %k[3]
    else:
        fitting += " + %s*input" %k[3]
    if k[4] < 0:
        fitting += " %s" %k[4]
    else:
        fitting += " + %s" %k[4]
    
    return fitting

def savebooster(fpath):
    '''
    '''
    ####################################
    # deal with data
    ####################################
    ####################################
    # Read data in first before doing anything
    ####################################
    datafile = '/'.join((fpath,'../Bcoeff1.xlsx'))
    data = __readdata(datafile)

    ####################################
    # Booster dipole magnet
    ####################################
    #device name
    devbd1 = ['A1BD1', 'A1BD2', 'A1BD3', 'A1BD4', 'A1BD5', 'A1BD6', 'A1BD7', 'A1BD8',
              'A2BD1', 'A2BD2', 'A2BD3', 'A2BD4', 'A2BD5', 'A2BD6', 'A2BD7', 'A2BD8']
    #serial number
    devbd1sn = [24, 4, 5, 6, 25, 11, 12, 22,
                2 , 16, 10, 18, 15, 23, 33, 28]
    # device type
    devtype1 = 'BS Dipole BD1'
    # design length
    bd1len = [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 
              1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3]
    desc1 = 'Dipole type BD1 for booster ring'
    paramstandard = {}
    paramcomplex = {}
    paramdict={}
    idx = 2
    for i in range(4):
        subparam = {'current_unit': 'A'}
        k = []
        for j in range(5):
            k.append(data[idx][5*i+j+1])
        if i == 0:
            subparam['field_unit'] = 'T'
            subparam['i2b'] = [1, createfit(k)]
            subparam['description'] = 'Dipole field component for a combined funbction magnet'
            paramcomplex['1'] = subparam
        elif i ==1:
            subparam['field_unit'] = 'T/m'
            subparam['i2b'] = [1, createfit(k)]
            subparam['description'] = 'Quadrupole field component for a combined funbction magnet'
            paramcomplex['2'] = subparam
        elif i ==2:
            subparam['field_unit'] = 'T/m^2'
            subparam['i2b'] = [1, createfit(k)]
            subparam['description'] = 'Sextupole field component for a combined funbction magnet'
            paramcomplex['3'] = subparam
        elif i ==3:
            paramstandard['current_unit'] = 'A'
            paramstandard['field_unit'] = 'T'
            paramstandard['b2i'] = [1, createfit(k)]
    if paramstandard:
        paramdict['standard'] = paramstandard
    if paramcomplex:
        paramdict['complex']=paramcomplex
            
#    import pprint
#    pprint.pprint (paramdict)
    saveboosterdata(devbd1, devbd1sn, bd1len, devtype1, desc1, paramdict)
    idx += 1

    #device name
    devbd2 = ['A3BD1', 'A3BD2', 'A3BD3', 'A3BD4', 'A3BD5', 'A3BD6', 'A3BD7', 'A3BD8',
              'A4BD1', 'A4BD2', 'A4BD3', 'A4BD4', 'A4BD5', 'A4BD6', 'A4BD7','A4BD8']
    #serial number
    devbd2sn = [32, 26, 17, 8, 29, 34, 3, 21,
                31, 7, 14, 13, 19, 9, 30, 20]
    # device type
    devtype2 = 'BS Dipole BD2'
    # design length
    bd2len = [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 
              1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3]
    desc2 = 'Dipole type BD2 for booster ring'
    paramstandard.clear()
    paramcomplex.clear()
    paramdict.clear()
    for i in range(4):
        subparam = {'current_unit': 'A'}
        k = []
        for j in range(5):
            k.append(data[idx][5*i+j+1])
        if i == 0:
            subparam['field_unit'] = 'T'
            subparam['i2b'] = [1, createfit(k)]
            subparam['description'] = 'Dipole field component for a combined funbction magnet'
            paramcomplex['1'] = subparam
        elif i ==1:
            subparam['field_unit'] = 'T/m'
            subparam['i2b'] = [1, createfit(k)]
            subparam['description'] = 'Quadrupole field component for a combined funbction magnet'
            paramcomplex['2'] = subparam
        elif i ==2:
            subparam['field_unit'] = 'T/m^2'
            subparam['i2b'] = [1, createfit(k)]
            subparam['description'] = 'Sextupole field component for a combined funbction magnet'
            paramcomplex['3'] = subparam
        elif i ==3:
            paramstandard['current_unit'] = 'A'
            paramstandard['field_unit'] = 'T'
            paramstandard['b2i'] = [1, createfit(k)]
    if paramstandard:
        paramdict['standard'] = paramstandard
    if paramcomplex:
        paramdict['complex']=paramcomplex
    saveboosterdata(devbd2, devbd2sn, bd2len, devtype2, desc2, paramdict)
    idx += 1
    
    #device name
    devbf =['A1BF1', 'A1BF2', 'A1BF3', 'A1BF4', 'A1BF5', 'A1BF6', 'A1BF7', 
            'A2BF1', 'A2BF2', 'A2BF3', 'A2BF4', 'A2BF5', 'A2BF6', 'A2BF7',
            'A3BF1', 'A3BF2', 'A3BF3', 'A3BF4', 'A3BF5', 'A3BF6', 'A3BF7',
            'A4BF1', 'A4BF2', 'A4BF3', 'A4BF4', 'A4BF5', 'A4BF6', 'A4BF7']
    #serial number
    devbfsn = [26, 6, 9, 12, 25, 8, 13,
               16, 18, 7, 24, 10, 4, 2,
               29, 15, 14, 20, 21, 11, 3, 
               22, 5, 19, 17, 27, 30, 23]
    # device type
    devtype3 = 'BS Dipole BF'
    # design length
    bflen = [1.24, 1.24, 1.24, 1.24, 1.24, 1.24, 1.24,  
             1.24, 1.24, 1.24, 1.24, 1.24, 1.24, 1.24,
             1.24, 1.24, 1.24, 1.24, 1.24, 1.24, 1.24,
             1.24, 1.24, 1.24, 1.24, 1.24, 1.24, 1.24]
    desc3 = 'Dipole type BF for booster ring'
    paramstandard.clear()
    paramcomplex.clear()
    paramdict.clear()
    for i in range(4):
        subparam = {'current_unit': 'A'}
        k = []
        for j in range(5):
            k.append(data[idx][5*i+j+1])
        if i == 0:
            subparam['field_unit'] = 'T'
            subparam['i2b'] = [1, createfit(k)]
            subparam['description'] = 'Dipole field component for a combined funbction magnet'
            paramcomplex['1'] = subparam
        elif i ==1:
            subparam['field_unit'] = 'T/m'
            subparam['i2b'] = [1, createfit(k)]
            subparam['description'] = 'Quadrupole field component for a combined funbction magnet'
            paramcomplex['2'] = subparam
        elif i ==2:
            subparam['field_unit'] = 'T/m^2'
            subparam['i2b'] = [1, createfit(k)]
            subparam['description'] = 'Sextupole field component for a combined funbction magnet'
            paramcomplex['3'] = subparam
        elif i ==3:
            paramstandard['current_unit'] = 'A'
            paramstandard['field_unit'] = 'T'
            paramstandard['b2i'] = [1, createfit(k)]
    if paramstandard:
        paramdict['standard'] = paramstandard
    if paramcomplex:
        paramdict['complex']=paramcomplex
#    pprint.pprint (paramdict)
    saveboosterdata(devbf, devbfsn, bflen, devtype3, desc3, paramdict)
    idx += 2
    
    ####################################
    # Booster quadrupole magnet
    ####################################
    #device name
    devqf =['A1QF1', 'A1QF2', 
            'A2QF1', 'A2QF2',
            'A3QF1', 'A3QF2',
            'A4QF1', 'A4QF2',]
    #serial number
    devqfsn = [1, 2, 3, 4,
               5, 6, 7, 8]
    # device type
    devtypeqf = 'BS Quadrupole QF'
    # design length
    qflen = [0.3, 0.3, 0.3, 0.3, 
             0.3, 0.3, 0.3, 0.3]
    descqf = 'Quadrupole type QF for booster ring'
    paramdict.clear()
    paramdict['current_unit'] = 'A'
    paramdict['field_unit'] = 'T/m'
    for i in [1, 3]:
        k=[]
        for j in range(5):
            k.append(data[idx][5*i+j+1])
        if i == 1:
            paramdict['i2b'] = [1, createfit(k)]
        elif i == 3:
            paramdict['b2i'] = [1, createfit(k)]
#    pprint.pprint (paramdict)
    saveboosterdata(devqf, devqfsn, qflen, devtypeqf, descqf, {'standard':paramdict})
    idx += 1
    
    #device name
    devqd =['A1QD1', 'A1QD2', 
            'A2QD1', 'A2QD2',
            'A3QD1', 'A3QD2',
            'A4QD1', 'A4QD2',]
    #serial number
    devqdsn = [1, 2, 3, 4,
               5, 6, 7, 8]
    # device type
    devtypeqd = 'BS Quadrupole QD'
    # design length
    qdlen = [0.3, 0.3, 0.3, 0.3, 
             0.3, 0.3, 0.3, 0.3]
    descqd = 'Quadrupole type QD for booster ring'
    paramdict.clear()
    paramdict['current_unit'] = 'A'
    paramdict['field_unit'] = 'T/m'
    for i in [1, 3]:
        k=[]
        for j in range(5):
            k.append(data[idx][5*i+j+1])
        if i == 1:
            paramdict['i2b'] = [1, createfit(k)]
        elif i == 3:
            paramdict['b2i'] = [1, createfit(k)]
#    pprint.pprint (paramdict)
    saveboosterdata(devqd, devqdsn, qdlen, devtypeqd, descqd, {'standard':paramdict})
    idx += 1

    #device name
    devqg =['A1QG1', 'A1QG2', 
            'A2QG1', 'A2QG2',
            'A3QG1', 'A3QG2',
            'A4QG1', 'A4QG2',]
    #serial number
    devqgsn = [1, 2, 3, 4,
               5, 6, 7, 8]
    # device type
    devtypeqg = 'BS Quadrupole QG'
    # design length
    qglen = [0.3, 0.3, 0.3, 0.3, 
             0.3, 0.3, 0.3, 0.3]
    descqg = 'Quadrupole type QG for booster ring'
    paramdict.clear()
    paramdict['current_unit'] = 'A'
    paramdict['field_unit'] = 'T/m'
    for i in [1, 3]:
        k=[]
        for j in range(5):
            k.append(data[idx][5*i+j+1])
        if i == 1:
            paramdict['i2b'] = [1, createfit(k)]
        elif i == 3:
            paramdict['b2i'] = [1, createfit(k)]
#    pprint.pprint (paramdict)
    saveboosterdata(devqg, devqgsn, qglen, devtypeqg, descqg, {'standard':paramdict})
    idx += 2

    ####################################
    # Booster sextupole magnet
    ####################################
    #device name
    devsf =['A1SF1', 'A1SF2', 
            'A2SF1', 'A2SF2',
            'A3SF1', 'A3SF2',
            'A4SF1', 'A4SF2',]
    #serial number
    devsfsn = [1, 2, 3, 4,
               5, 6, 7, 8]
    # device type
    devtypesf = 'BS Sextupole SF'
    # design length
    sflen = [0.12, 0.12, 0.12, 0.12, 
             0.12, 0.12, 0.12, 0.12]
    descsf = 'Sextupole type SF for booster ring'
    paramdict.clear()
    paramdict['current_unit'] = 'A'
    paramdict['field_unit'] = 'T/m^2'
    for i in [2, 3]:
        k=[]
        for j in range(5):
            k.append(data[idx][5*i+j+1])
        if i == 2:
            paramdict['i2b'] = [1, createfit(k)]
        elif i == 3:
            paramdict['b2i'] = [1, createfit(k)]
#    pprint.pprint (paramdict)
    saveboosterdata(devsf, devsfsn, sflen, devtypesf, descsf, {'standard':paramdict})
    idx += 1

    #device name
    devsd =['A1SD1', 'A1SD2', 
            'A2SD1', 'A2SD2',
            'A3SD1', 'A3SD2',
            'A4SD1', 'A4SD2',]
    #serial number
    devsdsn = [1, 2, 3, 4,
               5, 6, 7, 8]
    # device type
    devtypesd = 'BS Sextupole SD'
    # design length
    sdlen = [0.12, 0.12, 0.12, 0.12, 
             0.12, 0.12, 0.12, 0.12]
    descsd = 'Sextupole type SF for booster ring'
    paramdict.clear()
    paramdict['current_unit'] = 'A'
    paramdict['field_unit'] = 'T/m^2'
    for i in [2, 3]:
        k=[]
        for j in range(5):
            k.append(data[idx][5*i+j+1])
        if i == 2:
            paramdict['i2b'] = [1, createfit(k)]
        elif i == 3:
            paramdict['b2i'] = [1, createfit(k)]
#    pprint.pprint (paramdict)
    saveboosterdata(devsd, devsdsn, sdlen, devtypesd, descsd, {'standard':paramdict})
    idx += 1
    
def main(fpath):
    '''
    '''
    ####################################
    # linac
    ####################################
    savesol(fpath)
    savesolavg(fpath)
    savelnqdp(fpath)

    ####################################
    # linac to booster transport line
    ####################################
    # linac tp booster transport line dipole
    savelbtdpl(fpath)
    # linac tp booster transport line quadrupole
    savequad1340(fpath)
    savequad5200(fpath, "LBT")

    ####################################
    # booster ring
    ####################################
    # all dipole, quadrupole, and sextupole
    savebooster(fpath)

    ####################################
    # booster to storage ring transport line
    ####################################
    # booster to storage ring transport line dipole
    savedpl9035(fpath)
    # booster to storage ring transport line quadrupole
    savequad5200(fpath, "BST")

if __name__ == '__main__':
    municonv = municonvdata()
    municonv.connectdb(host=host, user=user, pwd=pw, db=db)

    #/Users/shengb/Documents/Work/Magnetic.Measurement/NSLS2/MagnetMeasurements/injector/NewFormat
    rootpath = None
    if sys.version_info[:2] > (3,0):
        rootpath = input ('Please specify the path to the data file directory:')
    else:
        rootpath = raw_input('Please specify the path to the data file directory:')

    main (rootpath)
    print('Finish saving magnet measurement data.')

    
