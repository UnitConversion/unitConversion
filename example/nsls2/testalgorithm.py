'''
Created on Sep 19, 2012

@author: shengb
'''
import pprint
try:
    import simplejson as json
except ImportError:
    import json

def makei2b(expr, revert=False, y=0.0):
    f=None
    
    if revert:
        funcstr='''def f(input):
        return {e} - {y}
        '''.format(e=expr, y=y)        
    else:
        funcstr='''def f(input):
        return {e}
        '''.format(e=expr)
    exec(funcstr)
    return f

def makeb2k(expr, revert=False, y=0.0):
    f=None
    
    if revert:
        funcstr='''def f(input, energy=None):
        if(energy == None):
            raise ValueError("Cannnot get beam energy")
        return {e} - {y}
        '''.format(e=expr, y=y)        
    else:
        funcstr='''def f(input, energy=None):
        if(energy == None):
            raise ValueError("Cannnot get beam energy")
        return {e}
        '''.format(e=expr)
    exec(funcstr)
    return f

paramdict={'elem_name': 'LN-Q1',
           'device_name': 'LN-Q1',
           'serial': 001,
           'ref_draw': 'LBT-MG-QDP-5200',
           'energy_default': 0.2,
           'current': [5.000,4.000,3.000,2.000,1.000,0.000],
           'sig_current': None,
           'current_unit': 'A',
           'field': [0.523117117,0.423583722,0.3212263,0.217765243,0.113562683,0.007715707],
           'sig_field': None,
           'field_unit': 'T',
           'magnetic_len_meas': 0.1204868968,
           'magnetic_len_design': None,
           'ref_radius': 0.00575,
           'i2b': [0, '0.009933391 + 0.10315794*input'],
           'b2k': [0, 'input/(%s**2*3.335646*energy)'%(1.234), 3],
           }

jsondump = json.dumps(paramdict)
#print type(jsondump)
#pprint.pprint(jsondump)

paramsnew = json.loads(jsondump)
#print type(paramsnew)
#pprint.pprint(paramsnew)

fitting = paramsnew['i2b']
fid = fitting[0]
fitfunc = fitting[1]
func = makei2b(fitfunc)
print func(1.25)
#revertf = makei2b(fitting[1], revert=True, y = func(.4))

from scipy import optimize
print optimize.fsolve(makei2b(fitfunc, revert=True, y = 0.138880816), 0.0)

fitting = paramsnew['b2k']
fid = fitting[0]
fitfunc = fitting[1]
func = makeb2k(fitfunc)
print func(1.25, 3.0)
#revertf = makei2b(fitting[1], revert=True, y = func(.4))

#from scipy import optimize
print optimize.fsolve(makeb2k(fitfunc, revert=True, y = 0.138880816), 0.0, 2.8)
