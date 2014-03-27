import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def createGroup(name):
    '''
    Create auth group
    '''
    try:
        Group.objects.create(name=name)
    except IntegrityError:
        sys.stderr.write("%s group already exists in the database\n" % name)

def addUserIntoGroup(username, groupname):
    '''
    Add user into group
    '''
    # Get user
    user = getuser(username)
    # Get group
    group = getgroup(groupname)
    
    try:
        user.groups.add(group)
    
    except IntegrityError:
        sys.stderr.write("user already in group\n")

def createContentType(name, label):
    '''
    Create new content type and return it
    '''
    try: 
        ContentType.objects.create(name=name, app_label=label, model='')
    except:
        pass

def getContentType(name):
    # Get content type
    return ContentType.objects.get(name=name)

def addPermissionToGroup(group, permission):
    '''
    Add permission to group
    '''
    try:
        group.permissions.add(permission)
    except IntegrityError:
        sys.stderr.write("permission already assigned to group\n")


def creategroup(groupname):
    '''
    add a new group to service.
    Groups for NSLS II project:
        - lattice_model
        - unit_conversion
        - insertion_device
        - active_interlock
    '''
    try:
        Group.objects.get(name=groupname)
    except:
        createGroup(groupname)

def getgroup(groupname):
    return Group.objects.get(name=groupname)
  
def createuser(username, email, passwd):
    '''
    '''
    # Create user user
    try:
        User.objects.create_user(username, email, passwd)
    except IntegrityError:
        sys.stderr.write("User user already exists in the database\n")

def getuser(username):
    return User.objects.get(username=username)    
    

def install(groupname, username, email, userpw, contenttype, contentlabel, codename, codedesc):
    creategroup(groupname)
    group = getgroup(groupname)
    createuser(username, email, userpw)

    # Add user into unit_conversion group
    addUserIntoGroup(username, groupname)
        
    # Create lattice content type
    createContentType(contenttype, contentlabel)
    
    contentType = getContentType(contenttype)
    
    # Create and get can_upload permission
    Permission.objects.get_or_create(codename=codename, name=codedesc, content_type=contentType)
    permission = Permission.objects.get(name=codedesc)
    
    # Add can_upload permission to lattice_model group
    addPermissionToGroup(group, permission)

if __name__ == "__main__":
    username = 'petr'
    email = 'pilinski@bnl.gov'
    userpw = 'petr'

#    groupname = 'lattice_model'
#    contenttype = 'lattice_type'
#    contentlabel = 'lattice'
#    codename ='can_upload'
#    codedesc ='Can Upload Lattice'
#    install(groupname, username, email, userpw, contenttype, contentlabel, codename, codedesc)

    groupname = 'active_interlock'
    contenttype = 'active_interlock_type'
    contentlabel = 'ai'
    codename ='can_modify_ai'
    codedesc ='Can Modify Active Interlock'
    install(groupname, username, email, userpw, contenttype, contentlabel, codename, codedesc)
    
#    groupname = 'insertion_device'
#    contenttype = 'insertion_device_type'
#    contentlabel = 'id'
#    codename ='can_modify_id'
#    codedesc ='Can Modify Insertion Device'
#    install(groupname, username, email, userpw, contenttype, contentlabel, codename, codedesc)
    
    