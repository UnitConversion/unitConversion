# -*- coding: utf-8 -*-
"""
Internal module

Used to read the latticepy.conf file

example file
cat ~/latticepy.conf
[DEFAULT]
BaseURL=http://localhost:8000/lattice
"""

def __loadConfig():
    import os.path
    import ConfigParser
    dflt={'url':'http://localhost:8000/lattice'}
    cf=ConfigParser.SafeConfigParser(defaults=dflt)
    cf.read([
        '/etc/latticepy.conf',
        os.path.expanduser('~/.latticepy.conf'),
        'latticepy.conf'
    ])
    return cf

_conf=__loadConfig()