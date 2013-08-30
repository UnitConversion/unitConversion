'''
Created on May 9, 2013

@author: shengb
'''
from django.db import connection, transaction
try:
    from django.utils import simplejson as json
except ImportError:
    import json

from pyactiveinterlock.epsai import epsai

epsaiinst = epsai(connection, transaction=transaction)

def retrieveactiveinterlock(status, datefrom=None, dateto=None, withdata=True, rawdata=False):
    ''''''
def saveactiveinterlock(data, description=None, rawdata=None, active=True, author=None):
    ''''''
def updateactiveinterlockstatus(aiid, status, author=None):
    ''''''
def retrieveactiveinterlockproptype(name, unit=None, description=None):
    ''''''
def saveactiveinterlockproptype(name, unit=None, description=None):
    ''''''
def retrieveactiveinterlocklogic(name, shape=None, logic=None):
    ''''''
def saveactiveinterlocklogic(name, shape, logic, logiccode, author=None):
    ''''''
