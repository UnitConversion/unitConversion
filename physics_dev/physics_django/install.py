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
        
    # Create insertion_device group
    try:
        idGroup = Group.objects.create(name='insertion_device')
    
    except IntegrityError:
        sys.stderr.write("insertion_device group already exists in the database\n")
    
    # Get user
    user = User.objects.get(username='user')
    
    # Get lattice_model group
    latticeModelGroup = Group.objects.get(name='lattice_model')
    
    # Get unit_conversion group
    unitConversionGroup = Group.objects.get(name='unit_conversion')
	    
    # Get insertion_device group
    idGroup = Group.objects.get(name='insertion_device')
    
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
		        
    # Add user into insertion_device group
    try:
        user.groups.add(idGroup)
    
    except IntegrityError:
        sys.stderr.write("user already in insertion_device group\n")
        
    # Create lattice content type
    #if(contentType == None):
    try: 
        ContentType.objects.create(name='lattice_type', app_label='lattice', model='')
    except:
        pass
    #contentType = ContentType.objects.get(name='lattice_type')
    # Get lattice content type
    contentType = ContentType.objects.get(name='lattice_type')
	
	# Create id content type
    try: 
        ContentType.objects.create(name='insertion_device_type', app_label='id', model='')
    except:
        pass

    # Get insertion device content type
    contentTypeId = ContentType.objects.get(name='insertion_device_type')
    
    # Create and get can_upload permission
    Permission.objects.get_or_create(codename='can_upload', name='Can Upload Lattice', content_type=contentType)
    permission = Permission.objects.get(name='Can Upload Lattice')
	    
    # Create and get can_modify_id permission
    Permission.objects.get_or_create(codename='can_modify_id', name='Can Modify Insertion Device', content_type=contentTypeId)
    permissionId = Permission.objects.get(name='Can Modify Insertion Device')
    
    # Add can_upload permission to lattice_model group
    try:
        latticeModelGroup.permissions.add(permission)
    except IntegrityError:
        sys.stderr.write("can_upload permission already assigned to lattice_model grop\n")
		
    # Add can_modify_id permission to insertion_device group
    try:
        idGroup.permissions.add(permissionId)
    except IntegrityError:
        sys.stderr.write("can_modify_id permission already assigned to insertion_device grop\n")

install()
