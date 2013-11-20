#!/usr/bin/env python

import sys
import os.path


BASE_PATH = os.path.dirname(__file__)
#Add the pyirmis app to our django path
sys.path.append(os.path.join(BASE_PATH, '../../'))
#Add the pyirmis irmis dev packages
#sys.path.append(os.path.join(BASE_PATH, '../physics_dev_packages/lib/python2.7/site-packages/'))
#sys.path.append(os.path.join(BASE_PATH, '../physics_dev_packages/lib/python2.6/site-packages/'))
#sys.path.append(os.path.join(BASE_PATH, '../physics_dev_packages/lib64/python2.7/site-packages/'))
#sys.path.append(os.path.join(BASE_PATH, '../physics_dev_packages/lib64/python2.6/site-packages/'))
from django.core.management import execute_manager

try:
    import settings # Assumed to be in the same directory.
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings)
