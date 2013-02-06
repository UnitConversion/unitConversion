'''
Created on Jan 30, 2013

@author: shengb
'''
from __future__ import print_function
import sys

import xlrd
# http://pypi.python.org/pypi/xlutils
from xlutils.copy import copy

def __readdata(xlname, sheetno=0, sheetname=None, writable=False):
    '''Read data from Excel spreadsheet file using xlrd library.
    '''
    # the working spreadsheet will be close by open_workbook() method automatically when returning
    # unless using on_demand=True. If on_demand is turned True, the file is not closed, even if the workbook is collected.
    # Should be careful to call release_resources() before letting the workbook go away..
    rb = xlrd.open_workbook(xlname)
    # read only copy to introspect the file
    sh = rb.sheet_by_index(sheetno) 
    
    raw_data = []
    for rownum in range(sh.nrows):
        raw_data.append(sh.row_values(rownum))
    
    if writable:
        # a writable copy (I can't read values out of this, only write to it)
        wb = copy(rb)
        return (raw_data, wb)
    else:
        return raw_data

if __name__ == '__main__':
    root = None
    if sys.version_info[:2] > (3,0):
        root = input ('Please specify the path to the data file:')
    else:
        root = raw_input('Please specify the path to the data file:')

    datasheet = 'Alignment Error Summary ER 02-01-2013.xls'
    target = 'SR-MG-INSTALL.xlsx'
    
    rawdata = __readdata("/".join((root, datasheet)))
    targetdata, wb = __readdata("/".join((root, target)), writable=True)
#    for i in range(15):
#        print (rawdata[i])

    order=0
    datadict = {}
    subdata = []
    key = ''
    for data in rawdata[2:]:
        if data[0] != '':
            if subdata:
                datadict[key] = subdata
                subdata = []
            order = int(data[0])
            key = data[1]
        subdata.append(data[2:])
    datadict[key] = subdata

    w_sheet = wb.get_sheet(0) 
    currentkey = ''
    newkey = ''
    newdata = []
    for i in range(1,len(targetdata)):
        if targetdata[i][1] in [2, 4, 6] and targetdata[i][4].split()[0] in ['Quad', 'Sext']:
            newkey="C%sG%s"%(targetdata[i][2], int(targetdata[i][1]))
            if newkey != currentkey:
                newdata = datadict[newkey]
                currentkey = newkey
                elemidx = 0
            alias_sn = newdata[elemidx][1].split("_")
            print(i, elemidx, alias_sn, currentkey)
            try:
                w_sheet.write(i, 7, alias_sn[1].strip())
                w_sheet.write(i, 8, alias_sn[0].strip())
            except:
                alias_sn = newdata[elemidx][1].split()
                w_sheet.write(i, 7, alias_sn[1].strip())
                w_sheet.write(i, 8, alias_sn[0].strip())
            elemidx +=1
    
    wb.save("/".join((root, target[:-5]+'-SN.xls')))

