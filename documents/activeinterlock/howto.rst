How to
==============================================

These tutorials are intended for administrators that are in charge of ActiveInterlock tools and have access to source code and ActiveInterlock database.

Make data column approvable
------------------------------

In the first few runs there might be some changes regarding which columns should be approved after they had been changed and which don't need approval. To quickly change this we should follow next few steps:

 * find property type that should be approvable in the **active_interlock_prop_type** table and set its description to **approvable**,
 * find existing properties of that type in the **active_interlock_prop** table and set their status to **2**

:NOTE: Some of the property types are not present in the **active_interlock_prop_type** e.g. name, logic, shape, ... These property types cannot be set as approvable following instructions above.