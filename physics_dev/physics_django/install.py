import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

'''
Create auth group
'''
def createGroup(name):

    try:
        Group.objects.create(name=name)
    
    except IntegrityError:
        sys.stderr.write("%s group already exists in the database\n" % name)

'''
Add user into group
'''
def addUserIntoGroup(user, group):
    
    try:
        user.groups.add(group)
    
    except IntegrityError:
        sys.stderr.write("user already in group\n")

'''
Create new content type and return it
'''
def createAndReturnContentType(name, label):
    
    # Create content type
    try: 
        ContentType.objects.create(name=name, app_label=label, model='')
    except:
        pass

    # Get content type
    return ContentType.objects.get(name=name)

'''
Add permission to group
'''
def addPermissionToGroup(group, permission):
    
    try:
        group.permissions.add(permission)
    except IntegrityError:
        sys.stderr.write("permission already assigned to group\n")

"""
    Create users, groups and permissions
"""
def install():
    
    # Create user user
    try:
        User.objects.create_user('user', 'admin@gmail.com', 'user')

    except IntegrityError:
        sys.stderr.write("User user already exists in the database\n")
    
    # Create lattice_model group
    createGroup('lattice_model')
        
    # Create unit_conversion group
    createGroup('unit_conversion')
        
    # Create insertion_device group
    createGroup('insertion_device')
    
    # Create active interlock group
    createGroup('active_interlock')
    
    # Get user
    user = User.objects.get(username='user')
    
    # Get lattice_model group
    latticeModelGroup = Group.objects.get(name='lattice_model')
    
    # Get unit_conversion group
    unitConversionGroup = Group.objects.get(name='unit_conversion')
    
    # Get insertion_device group
    idGroup = Group.objects.get(name='insertion_device')
    
    # Get active_interlock group
    aiGroup = Group.objects.get(name='active_interlock')
    
    
    # Add user into lattice_model group
    addUserIntoGroup(user, latticeModelGroup)
        
    # Add user into unit_conversion group
    addUserIntoGroup(user, unitConversionGroup)
        
    # Add user into insertion_device group
    addUserIntoGroup(user, idGroup)
    
    # Add user into active_interlock group
    addUserIntoGroup(user, aiGroup)
        
    # Create lattice content type
    contentType = createAndReturnContentType('lattice_type', 'lattice')

    # Create id content type
    contentTypeId = createAndReturnContentType('insertion_device_type', 'id')

    # Create ai content type
    contentTypeAi = createAndReturnContentType('active_interlock_type', 'ai')
    
    # Create and get can_upload permission
    Permission.objects.get_or_create(codename='can_upload', name='Can Upload Lattice', content_type=contentType)
    permission = Permission.objects.get(name='Can Upload Lattice')
    
    # Create and get can_modify_id permission
    Permission.objects.get_or_create(codename='can_modify_id', name='Can Modify Insertion Device', content_type=contentTypeId)
    permissionId = Permission.objects.get(name='Can Modify Insertion Device')
    
    # Create and get can_modify_ai permission
    Permission.objects.get_or_create(codename='can_modify_ai', name='Can Modify Active Interlock', content_type=contentTypeAi)
    permissionAi = Permission.objects.get(name='Can Modify Active Interlock')
    
    # Add can_upload permission to lattice_model group
    addPermissionToGroup(latticeModelGroup, permission)

    # Add can_modify_id permission to insertion_device group
    addPermissionToGroup(idGroup, permissionId)
    
    # Add can_modify_ai permission to active_interlock group
    addPermissionToGroup(aiGroup, permissionAi)

install()
