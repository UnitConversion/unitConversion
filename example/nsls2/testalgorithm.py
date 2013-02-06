'''
Created on Sep 19, 2012

@author: shengb
'''
import pprint
try:
    import simplejson as json
except ImportError:
    import json

def make_func(expr, revert=False, y=0.0):
    f=None
    
    if revert:
        funcstr='''def f(i):
        return {e} - {y}
        '''.format(e=expr, y=y)        
    else:
        funcstr='''def f(i):
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
           'fitting_i2b': 'i2b:0.009933391 + 0.10315794*input:Integrated Gradient (T)',
           'fitting_b2k': 'b2k:input/radius_ref/(3.335646*energy):input has to be in the unit Tesla-m'
           }

jsondump = json.dumps(paramdict)
print type(jsondump)
pprint.pprint(jsondump)

paramsnew = json.loads(jsondump)
print type(paramsnew)
pprint.pprint(paramsnew)

fitting = paramsnew['fitting'].split(':')
fitting = [i.strip() for i in fitting]
expr = fitting[1]
func = make_func(expr)
print func(1.25)
#revertf = make_func(fitting[1], revert=True, y = func(.4))

from scipy import optimize
print optimize.fsolve(make_func(expr, revert=True, y = 0.138880816), 0.0)

#if __name__ == '__main__':
#    pass