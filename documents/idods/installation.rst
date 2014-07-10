Installation instructions
===========================

Project is published on a github.com. To get it you can clone it or download a zip file available at https://github.com/UnitConversion/unitConversion.

Authentication
---------------

User accounts, groups and permissions are all managed in Django administration. Django administration is already enabled in a project and what you have to do it to run *syncdb*. After that you can access Django administration by going to the http://localhost:8000/admin.

To set up a demo user with permissions needed to access web services user can modify and run *install.py* that can be found in *unitConversion/physics_dev/physics_django/* directory.

User has to have permission named: **id.can_modify_id** to make modifications (save, update and delete) to IDODS.

Integration with LDAP
+++++++++++++++++++++++

To enable authentication integration with LDAP user has to first install two python modules: *python-ldap* and *django-auth-ldap*. After that user has to make sure that lines: 3, 4 and all lines between *LDAP configuration START* and *LDAP configuration END* comments are uncommented. In these lines there is a LDAP configuration that has to be modified to reflect you LDAP server configuration and LDAP hierarchy.

First thing you have to do is to set LDAP server URL::

 AUTH_LDAP_SERVER_URI = "ldap://localhost"

After that you have to set group parameters that will alow Django to search for groups your users have to belong to to be successfully authenticated using LDAP. For now this part is not yet implemented so you can leave it as it is. The only important thing is that *AUTH_LDAP_FIND_GROUP_PERMS* property is set to *True*::

 AUTH_LDAP_FIND_GROUP_PERMS = True

This line will allow Django to map LDAP user groups and users to Django permissions. For LDAP to authenticate user one more line has to be modified ::

 AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=people,dc=olog,dc=com"

This property holds the template string for direct binding of the user. Placeholder *user* will be replaced by the provided username when Django will be in the authentication phase.

The first time user will want to log into IDODS and e.g. modify a vendor, he will not be able to do that because his permissions are not yet set. When this happens, user has to notify the administrator and trust him with his username. When administrator will log into Django administration console he will see new user has been added into the database and now administrator has to put this user into appropriate groups with appropriate permissions.