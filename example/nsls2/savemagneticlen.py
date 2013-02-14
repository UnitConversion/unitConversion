'''
Created on Feb 14, 2013

@author: shengb
'''
from pymuniconv.municonvdata import municonvdata
from pymuniconv.municonvprop import (magneticlen, magneticlendesc)

from rdbinfo import (host, user, pw, db)
from devicelist import magneticleninst

if __name__ == '__main__':
    municonv = municonvdata()
    municonv.connectdb(host=host, user=user, pwd=pw, db=db)

    res = municonv.retrievecmpnttypeproptype(magneticlen, magneticlendesc)
    if len(res) == 0:
        ctptid = municonv.savecmpnttypeproptype(magneticlen, magneticlendesc)
    else:
        ctptid=res[0][0]

    for k, v in magneticleninst.iteritems():
        res = municonv.retrievecmpnttype(k)
        if len(res) != 1:
            raise ValueError ("Given component type does (%s) not exist or not unique"%(v))
        ctid = res[0][0]
        try:
            municonv.savecmpnttypeprop(str(v), ctid, ctptid)
        except ValueError:
            municonv.updatecmpnttypeprop(str(v), ctid, ctptid)
    
    print('finish saving design magnetic length.')