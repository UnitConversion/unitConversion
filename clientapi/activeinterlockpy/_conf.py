# -*- coding: utf-8 -*-
"""
Internal module

Used to read the activeinterlockclient.conf file

example file
cat ~/activeinterlockclient.conf
[DEFAULT]
BaseURL=http://localhost:8080/activeinterlock
username=MyUserName
password=MyPassword
"""

def __loadConfig():
    import os.path
    import ConfigParser
    dflt={'BaseURL':'http://localhost:8000/ai/'}
    config=ConfigParser.SafeConfigParser(defaults=dflt)
    config.read([
        '/etc/activeinterlock.conf',
        os.path.expanduser('~/.activeinterlock.conf'),
        'activeinterlock.conf'
    ])
    return config

_conf=__loadConfig()