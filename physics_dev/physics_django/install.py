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
    
    # Create user user
    try:
        user = User.objects.create_user('user', 'admin@gmail.com', 'user')

    except IntegrityError:
        sys.stderr.write("User user already exists in the database\n")
    
    # Create lattice_model group
    try:
        latticeGroup = Group.objects.create(name='lattice_model')
    
    except IntegrityError:
        sys.stderr.write("lattice_model group already exists in the database\n")
        
    # Create unit_conversion group
    try:
        unitConversionGroup = Group.objects.create(name='unit_conversion')
    
    except IntegrityError:
        sys.stderr.write("unit_conversion group already exists in the database\n")
    
    # Get user
    user = User.objects.get(username='user')
    
    # Get lattice_model group
    latticeModelGroup = Group.objects.get(name='lattice_model')
    
    # Get unit_conversion group
    unitConversionGroup = Group.objects.get(name='unit_conversion')
    
    # Add user into lattice_model group
    try:
        user.groups.add(latticeModelGroup)
    
    except IntegrityError:
        sys.stderr.write("user already in lattice_model group\n")
        
    # Add user into unit_conversion group
    try:
        user.groups.add(unitConversionGroup)
    
    except IntegrityError:
        sys.stderr.write("user already in unit_conversion group\n")
        
    # Create lattice content type
    contentType = ContentType.objects.get(name='lattice_type')
    
    if(contentType == None):
        ContentType.objects.create(name='lattice_type', app_label='lattice', model='')
    
    # Get lattice content type
    contentType = ContentType.objects.get(name='lattice_type')
    
    # Create and get can_upload permission
    Permission.objects.get_or_create(codename='can_upload', name='Can Upload Lattice', content_type=contentType)
    permission = Permission.objects.get(name='Can Upload Lattice')
    
    # Add can_upload permission to lattice_model group
    try:
        latticeModelGroup.permissions.add(permission)
    except IntegrityError:
        sys.stderr.write("can_upload permission already assigned to lattice_model grop\n")

install()