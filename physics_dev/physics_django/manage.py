#!/usr/bin/env python

import sys
import os.path


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
#Add the pyirmis app to our django path
sys.path.append(os.path.join(BASE_PATH, '../../'))
#Add the pyirmis irmis dev packages
#sys.path.append(os.path.join(BASE_PATH, '../physics_dev_packages/lib/python2.7/site-packages/'))
#sys.path.append(os.path.join(BASE_PATH, '../physics_dev_packages/lib/python2.6/site-packages/'))
#sys.path.append(os.path.join(BASE_PATH, '../physics_dev_packages/lib64/python2.7/site-packages/'))
#sys.path.append(os.path.join(BASE_PATH, '../physics_dev_packages/lib64/python2.6/site-packages/'))

try:
    import settings # Assumed to be in the same directory.
except ImportError as exc:
    sys.stderr.write("Error: failed to import settings module ({})".format(exc))
    sys.exit(1)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
