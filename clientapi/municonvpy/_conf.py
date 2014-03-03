# -*- coding: utf-8 -*-
"""
Internal module

Used to read the municonvpy.conf file

example file
cat ~/municonvpy.conf
[DEFAULT]
BaseURL=http://localhost:8000/magnets
"""

def __loadConfig():
    import os.path
    import ConfigParser
    dflt={'url':'http://localhost:8000/magnets'}
    cf=ConfigParser.SafeConfigParser(defaults=dflt)
    cf.read([
        '/etc/municonvpy.conf',
        os.path.expanduser('~/.municonvpy.conf'),
        'municonvpy.conf'
    ])
    return cf

_conf=__loadConfig()