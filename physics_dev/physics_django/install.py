import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

"""
    Create users, groups and permissions
"""
def install():
    
    try:
        # Create user
        user = User.objects.create_user('user', 'admin@gmail.com', 'user')
        latticeGroup = Group.objects.create(name='lattice_model')
        unitConversionGroup = Group.objects.create(name='unit_conversion')
        user.groups.add(name='lattice_model')
        user.groups.add(name='unit_conversion')
        
        ContentType.objects.create(name='lattice_type', app_label='lattice', model='')
        contentType = ContentType.objects.get(name='lattice_type')
        permission = Permission.objects.get_or_create(codename='can_upload', name='Can Upload Lattice', content_type=contentType)
        
        print "Objects created"

    except IntegrityError:
        sys.stderr.write("One of the objects already exists in the database")

install()