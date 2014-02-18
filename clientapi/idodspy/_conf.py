# -*- coding: utf-8 -*-
"""
Internal module

Used to read the idodsclient.conf file

Created on Feb 17, 2014
@author: dejan.dezman@cosylab.com

example file
cat ~/idodsclient.conf
[DEFAULT]
BaseURL=http://localhost:8080/id/device/
username=MyUserName
password=MyPassword
"""

def __loadConfig():
    import os.path
    import ConfigParser
    dflt={'BaseURL':'http://localhost:8000/id/device/'}
    config=ConfigParser.SafeConfigParser(defaults=dflt)
    config.read([
        '/etc/idodsclient.conf',
        os.path.expanduser('~/.idodsclient.conf'),
        'idodsclient.conf'
    ])
    return config

_conf=__loadConfig()