How to...
==============================================

These tutorials are intended for administrators that are responsible for ActiveInterlock tools and have access to the source code and the ActiveInterlock database.

Make Data Column Approvable
------------------------------

In the first few runs there might be some changes regarding which columns should be approved, after they have been changed, and which don't need approval. To quickly change this:

 * Find the property type that should be approvable in the **active_interlock_prop_type** table and set its description to **approvable**,
 * Find existing properties of that type in the **active_interlock_prop** table and set their status to **2**

:NOTE: Some of the property types are not present in the **active_interlock_prop_type** e.g. name, logic, shape, etc.  These property types cannot be set as approvable.