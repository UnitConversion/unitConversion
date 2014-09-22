Installation Instructions
===========================

The project is published on http://github.com. To get the project, you can clone it or download a zip file available at https://github.com/UnitConversion/unitConversion.

Authentication
---------------

User accounts, groups and permissions are all managed via Django's admin interface. Django admin is already enabled in the project and all that you need to do is to run ``syncdb``. After that you can access the Django admin interface from http://localhost:8000/admin.

To create a demo user with the permissions needed to access the web services, modify and run the ``install.py`` file which can be found in the  ``unitConversion/physics_dev/physics_django/`` directory.

In order to make modifications (save, update and delete) to IDODS, a user must have the permission named: **id.can_modify_id**.

Integration with LDAP
+++++++++++++++++++++++

To enable authentication integration with LDAP, first install two python modules: ``python-ldap`` and ``django-auth-ldap``. After that, make sure that lines: 3, 4 and all lines between *LDAP configuration START* and *LDAP configuration END* comments are uncommented. Then modify this LDAP configuration to reflect your LDAP server configuration and LDAP hierarchy.

First, set the LDAP server URL::

 AUTH_LDAP_SERVER_URI = "ldap://localhost"

Then, set group parameters that will alow Django to search for the groups that users must belong to, to be successfully authenticated using LDAP. At present, this part has not yet been implemented so it should be left as it is. The only important thing is that the **AUTH_LDAP_FIND_GROUP_PERMS** property is set to ``True``::

 AUTH_LDAP_FIND_GROUP_PERMS = True

This line will allow Django to map LDAP user groups and users to Django permissions. For LDAP to authenticate the user, ensure that the following line is correctly modified ::

 AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=people,dc=olog,dc=com"

This property holds the template string for direct binding of the user. Replace *user* with the relevant username when Django will be in the authentication phase.

After the first time user logs into IDODS, he/she will still not be able to make modifications to the database because the permissions haven't yet been set. When this happens, the user must send his username to the administrator, who can then put this user into the appropriate groups with the  appropriate permissions.