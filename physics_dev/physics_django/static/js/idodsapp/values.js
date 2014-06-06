/*
 * Values for insertion device online data service module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created: Feb 28, 2014
 */

app.value('EntityError', function(key, value){
	this.errorDict = {};
	this.num = 0;

	this.add = function(key, value) {
		this.errorDict[key] = value;
		this.num ++;
	};

	this.reset = function() {
		this.errorDict = {};
		this.num = 0;
	};

	if (key !== undefined && value !== undefined) {
		this.add(key, value);
		this.num ++;
	}
});

/*
 * Vendor object
 */
 app.value('Vendor', function(obj){
 	this.m = ["name"];
 	this.search_m = ["name"];
 	this.retrieve = ["id", "name", "description"];
 	this.list = ["name", "description"];
 	this.save = ["name", "description"];
 	this.update = ["old_name", "name", "description"];
 	this.display = {"name": "Name", "description": "Description", "id": "Id"};
 	this.id = "";
 	this.old_name = "";
 	this.name = "";
 	this.description = "";

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		if('id' in obj) {
 			this.id = obj.id;
 		}
 		this.name = obj.name;

 		if('old_name' in obj) {
 			this.old_name = obj.old_name;
 		}

 		this.description = obj.description;
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

/*
 * Component type info object
 */
app.value('CmpntTypeInfo', {
	'save_title': 'Save new Component type',
	'save_button': 'Save Component type',
	'retrieve_title': 'Component type',
	'retrieve_update_button': 'Update Component type',
	'update_title': 'Update Component type',
	'update_button': 'Update Component type',
	'search_button': 'Add Component type',
	'search_filter': 'Filter component types ...'
});

/*
 * Component type object
 */
 app.value('CmpntType', function(obj){
 	this.m = ["name"];
 	this.search_m = ["name"];
 	this.retrieve = ["id", "name", "description"];
 	this.list = ["name", "description", "all_cmpnt_types"];
 	this.save = ["name", "description", "props"];
 	this.save_show = ["name", "description"];
 	this.update = ["old_name", "name", "description", "props"];
 	this.display = {"name": "Name", "description": "Description", "id": "Id"};
 	this.id = "";
 	this.old_name = "";
 	this.name = "";
 	this.description = "";
 	this.props = {};
 	this.prop_keys = [];

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		if('id' in obj) {
 			this.id = obj.id;
 		}
 		this.name = obj.name;

 		if('old_name' in obj) {
 			this.old_name = obj.old_name;
 		}

 		if('props' in obj) {
 			this.props = obj.props;
 		}

 		if('prop_keys' in obj) {
 			//this.prop_keys = obj.prop_keys;

 			for(var i = 0; i<obj.prop_keys.length; i++) {
 				var key = obj.prop_keys[i];

 				this.prop_keys.push({'name':key, 'value':obj[key]});
 			}


 		}

 		this.description = obj.description;
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

/*
 * Component type property type info object
 */
app.value('CmpntTypeTypeInfo', {
	'save_title': 'Save new Component type property type',
	'save_button': 'Save Component type property type',
	'retrieve_title': 'Component type property type',
	'retrieve_update_button': 'Update Component type property type',
	'update_title': 'Update Component type property type',
	'update_button': 'Update Component type property type',
	'search_button': 'Add Component type property type',
	'search_filter': 'Filter property types ...'
});

/*
 * Component type property type object
 */
 app.value('CmpntTypeType', function(obj){
 	this.m = ["name"];
 	this.search_m = ["name"];
 	this.retrieve = ["id", "name", "description"];
 	this.list = ["name"];
 	this.save = ["name", "description"];
 	this.update = ["old_name", "name", "description"];
 	this.display = {"name": "Name", "description": "Description", "id": "Id"};

 	this.id = "";
 	this.old_name = "";
 	this.name = "";
 	this.description = "";

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		if('id' in obj) {
 			this.id = obj.id;
 		}
 		this.name = obj.name;

 		if('old_name' in obj) {
 			this.old_name = obj.old_name;
 		}

 		this.description = obj.description;
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

 /*
 * Inventory info object
 */
app.value('InventoryInfo', {
	'save_title': 'Save new Inventory',
	'save_button': 'Save Inventory',
	'retrieve_title': 'Inventory',
	'retrieve_update_button': 'Update Inventory',
	'update_title': 'Update Inventory',
	'update_button': 'Update Inventory',
	'search_button': 'Add Inventory',
	'search_filter': 'Filter Inventory items ...'
});

/*
 * Inventory object
 */
 app.value('Inventory', function(obj){

 	// Mandatory parameters that have to be set in the save form
 	this.m = ["name", "cmpnt_type", "vendor"];

 	// Mandatory parameters that have to be present in an URL when searching
 	this.search_m = ["name"];

 	// Parameters that are displayed when showing item details
 	this.retrieve = ["id", "name", "cmpnt_type", "vendor", "alias", "serialno"];

 	// Parameters that are displayed when showing item details
 	this.retrieve_show = ["id", "name"];

 	// Parameters that are displayed when showing item details
 	this.retrieve_hide = ["cmpnt_type", "vendor", "alias", "serialno"];

 	// Parameters that are checked before saving or updating
 	this.list = ["name", "cmpnt_type", "vendor", "alias", "serialno"];

 	// Parameters used for save URL
 	this.save = ["name", "cmpnt_type", "vendor", "alias", "serialno", "props"];

 	// Parameters that are displayed when saving new item
 	this.save_show = ["name", "cmpnt_type", "vendor", "alias", "serialno"];

 	// Parameters used as update URL parameters
 	this.update = ["old_name", "name", "cmpnt_type", "vendor", "alias", "serialno", "props"];

 	this.display = {
 		"serialno": "Serial number",
 		"alias": "Alias",
 		"vendor": "Vendor",
 		"name": "Name",
 		"cmpnt_type": "Component type",
 		"id": "Id"
 	};

 	this.id = "";
 	this.old_name = "";
 	this.name = "";
 	this.cmpnt_type = "";
 	this.vendor = "";
 	this.alias = "";
 	this.serialno = "";

 	this.props = {};
 	this.prop_keys = [];

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		if('id' in obj) {
 			this.id = obj.id;
 		}

 		this.name = obj.name;

 		if('old_name' in obj) {
 			this.old_name = obj.old_name;
 		}

 		if('props' in obj) {
 			this.props = obj.props;
 		}

 		if('prop_keys' in obj) {
 			//this.prop_keys = obj.prop_keys;

 			for(var i = 0; i<obj.prop_keys.length; i++) {
 				var key = obj.prop_keys[i];

 				this.prop_keys.push({'name':key, 'value':obj[key]});
 			}
 		}

 		this.cmpnt_type = obj.cmpnt_type;
 		this.vendor = obj.vendor;
 		this.alias = obj.alias;
 		this.serialno = obj.serialno;
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

 /*
 * Inventory property template info object
 */
app.value('InventoryTypeInfo', {
	'save_title': 'Save Inventory property template',
	'save_button': 'Save Inventory property template',
	'retrieve_title': 'Inventory property template',
	'retrieve_update_button': 'Update Inventory property template',
	'update_title': 'Update Inventory property template',
	'update_button': 'Update Inventory property template',
	'search_button': 'Add Inventory property template',
	'search_filter': 'Filter Inventory templates ...'
});

/*
 * Inventory property tempalte object
 */
 app.value('InventoryType', function(obj){

 	// Mandatory parameters that have to be set in the save form
 	this.m = ["name", "cmpnt_type"];

 	// Mandatory parameters that have to be present in an URL when searching
 	this.search_m = ["name"];

 	// Parameters that are displayed when showing item details
 	this.retrieve = ["id", "name", "cmpnt_type", "description", "default", "unit"];

 	// Parameters that are checked before saving or updating
 	this.list = ["name", "cmpnt_type", "description", "default", "unit"];

 	// Parameters used for save URL
 	this.save = ["name", "cmpnt_type", "description", "default", "unit"];

 	// Parameters that are displayed when saving new item
 	this.save_show = ["name", "cmpnt_type", "description", "default", "unit"];

 	// Parameters used as update URL parameters
 	this.update = ["tmplt_id", "name", "cmpnt_type", "description", "default", "unit"];

 	this.display = {
 		"id": "Id",
 		"name": "Name",
 		"cmpnt_type": "Component type",
 		"description": "Description",
 		"default": "Default",
 		"unit": "Unit"
 	};

 	this.id = "";
 	this.tmplt_id = "";
 	this.name = "";
 	this.cmpnt_type = "";
 	this.description = "";
 	this.default = "";
 	this.unit = "";

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		if('id' in obj) {
 			this.id = obj.id;
 			this.tmplt_id = obj.tmplt_id;
 		}

 		this.name = obj.name;
 		this.cmpnt_type = obj.cmpnt_type;
 		this.description = obj.description;
 		this.default = obj.default;
 		this.unit = obj.unit;
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

 /*
 * Install rel info object
 */
app.value('InstallRelInfo', {
	'save_title': 'Save Install relationship',
	'save_button': 'Save Install relationship',
	'retrieve_title': 'Install relationship',
	'retrieve_update_button': 'Update Install relationship',
	'retrieve_delete_button': 'Delete Install relationship',
	'update_title': 'Update Install relationship',
	'update_button': 'Update Install relationship',
	'search_button': 'Add Install relationship',
	'search_filter': 'Filter Install relationships ...'
});

/*
 * Install rel object
 */
 app.value('InstallRel', function(obj){

 	// Mandatory parameters that have to be set in the save form
 	this.m = ["description", "parent_install", "child_install"];

 	// Mandatory parameters that have to be present in an URL when searching
 	this.search_m = ["description"];

 	// Parameters that are displayed when showing item details
 	this.retrieve = ["id", "parentname", "childname", "description", "order", "date"];

 	// Parameters that are checked before saving or updating
 	this.list = ["parent_install", "child_install", "description", "order"];

 	// Parameters used for save URL
 	this.save = ["parent_install", "child_install", "description", "order", "props"];

 	// Parameters that are displayed when saving new item
 	this.save_show = ["parent_install", "child_install", "description", "order"];

 	// Parameters used as update URL parameters
 	this.update = ["parent_install", "child_install", "description", "order", "props"];

 	this.display = {
 		"id": "Id",
 		"parentname": "Parent name",
 		"parent_install": "Parent name",
 		"childname": "Child name",
 		"child_install": "Child name",
 		"description": "Description",
 		"order": "Order",
 		"date": "Date created"
 	};

 	this.id = "";
 	this.old_name = "";
 	this.install_name = "";
 	this.parentname = "";
 	this.childname = "";
 	this.order = undefined;
 	this.description = "";
 	this.date = "";
 	this.parent_install = "";
 	this.child_install = "";

 	this.props = {};
 	this.prop_keys = [];

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		if('id' in obj) {
 			this.id = obj.id;
 			this.old_name = obj.old_name;
 		}

 		if('props' in obj) {
 			this.props = obj.props;
 		}

 		if('prop_keys' in obj) {
 			//this.prop_keys = obj.prop_keys;

 			for(var i = 0; i<obj.prop_keys.length; i++) {
 				var key = obj.prop_keys[i];

 				this.prop_keys.push({'name':key, 'value':obj[key]});
 			}
 		}

 		this.install_name = obj.install_name;
 		this.description = obj.description;
 		this.date = obj.date;
 		this.order = obj.order;

 		if (this.order === null) {
 			this.order = undefined;
 		}

 		this.childname = obj.childname;
 		this.parentname = obj.parentname;
 		this.parent_install = obj.parent_install;
 		this.child_install = obj.child_install;
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

 /*
 * Install rel type info object
 */
app.value('InstallRelTypeInfo', {
	'save_title': 'Save Install relationship type',
	'save_button': 'Save Install relationship type',
	'retrieve_title': 'Install relationship type',
	'retrieve_update_button': 'Update Install relationship type',
	'update_title': 'Update Install relationship type',
	'update_button': 'Update Install relationship type',
	'search_button': 'Add Install relationship type',
	'search_filter': 'Filter Install relationships ...'
});

/*
 * Install rel type object
 */
 app.value('InstallRelType', function(obj){

 	// Mandatory parameters that have to be set in the save form
 	this.m = ["name"];

 	// Mandatory parameters that have to be present in an URL when searching
 	this.search_m = ["name"];

 	// Parameters that are displayed when showing item details
 	this.retrieve = ["id", "name", "description", "unit"];

 	// Parameters that are checked before saving or updating
 	this.list = ["name", "description", "unit"];

 	// Parameters used for save URL
 	this.save = ["name", "description", "unit"];

 	// Parameters that are displayed when saving new item
 	this.save_show = ["name", "description", "unit"];

 	// Parameters used as update URL parameters
 	this.update = ["old_name", "name", "description", "unit"];

 	this.display = {
 		"id": "Id",
 		"name": "Name",
 		"description": "Description",
 		"unit": "Unit"
 	};

 	this.id = "";
 	this.old_name = "";
 	this.name = "";
 	this.description = "";
 	this.unit = "";

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		if('id' in obj) {
 			this.id = obj.id;
 			this.old_name = obj.old_name;
 		}

 		this.name = obj.name;
 		this.description = obj.description;
 		this.unit = obj.unit;
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

 /*
 * Install info object
 */
app.value('InstallInfo', {
	'save_title': 'Save Install',
	'save_button': 'Save Install',
	'retrieve_title': 'Install',
	'retrieve_update_button': 'Update Install',
	'update_title': 'Update Install',
	'update_button': 'Update Install',
	'search_button': 'Add Install',
	'search_filter': 'Filter Install items ...'
});

/*
 * Install object
 */
 app.value('Install', function(obj){

 	// Mandatory parameters that have to be set in the save form
 	this.m = ["name", "cmpnt_type"];

 	// Mandatory parameters that have to be present in an URL when searching
 	this.search_m = ["name"];

 	// Parameters that are displayed when showing item details
 	this.retrieve = ["id", "name", "cmpnt_type", "description", "coordinatecenter"];

 	// Parameters that are displayed when showing item details
 	this.retrieve_show = ["id", "name"];

 	// Parameters that are displayed when showing item details
 	this.retrieve_hide = ["cmpnt_type", "description", "coordinatecenter"];

 	// Parameters that are checked before saving or updating
 	this.list = ["name", "cmpnt_type", "description", "coordinatecenter", "all_install"];

 	// Parameters used for save URL
 	this.save = ["name", "cmpnt_type", "description", "coordinatecenter"];

 	// Parameters that are displayed when saving new item
 	this.save_show = ["name", "cmpnt_type", "description", "coordinatecenter"];

 	// Parameters used as update URL parameters
 	this.update = ["old_name", "name", "cmpnt_type", "description", "coordinatecenter"];

 	this.display = {
 		"id": "Id",
 		"name": "Name",
 		"cmpnt_type": "Component type",
 		"description": "Description",
 		"coordinatecenter": "Coordinate center"
 	};

 	this.id = "";
 	this.name = "";
 	this.cmpnt_type = "";
 	this.description = "";
 	this.coordinatecenter = undefined;

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		if('id' in obj) {
 			this.id = obj.id;
 		}

 		if('old_name' in obj) {
 			this.old_name = obj.old_name;
 		}

 		this.name = obj.name;
 		this.cmpnt_type = obj.cmpnt_type;
 		this.description = obj.description;

 		if (obj.coordinatecenter === null) {
 			this.coordinatecenter = undefined;

 		} else {
 			this.coordinatecenter = obj.coordinatecenter;
 		}
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

 /*
 * Inventory to Install info object
 */
app.value('InventoryToInstallInfo', {
	'save_title': 'Save Inventory to Install',
	'save_button': 'Save Inventory to Install',
	'retrieve_title': 'Inventory to Install',
	'retrieve_update_button': 'Update Inventory to Install',
	'retrieve_delete_button': 'Uninstall device',
	'update_title': 'Update Inventory to Install',
	'update_button': 'Update Inventory to Install',
	'search_button': 'Add Inventory to Install',
	'search_filter': 'Filter Inventory to Install items ...'
});

/*
 * Inventory to Install object
 */
 app.value('InventoryToInstall', function(obj){

 	// Mandatory parameters that have to be set in the save form
 	this.m = ["install_name", "inv_name"];

 	// Mandatory parameters that have to be present in an URL when searching
 	this.search_m = ["install_name", "inv_name"];

 	// Parameters that are displayed when showing item details
 	this.retrieve = ["inventory_to_install_id", "install_name", "inv_name"];

 	// Parameters that are checked before saving or updating
 	this.list = ["install_name", "inv_name"];

 	// Parameters used for save URL
 	this.save = ["install_name", "inv_name"];

 	// Parameters that are displayed when saving new item
 	this.save_show = ["install_name", "inv_name"];

 	// Parameters used as update URL parameters
 	this.update = ["inventory_to_install_id", "install_name", "inv_name"];

 	// All parameters
 	this.all = ["inventory_to_install_id", "install_name", "inv_name"];

 	this.display = {
 		"inventory_to_install_id": "Id",
 		"install_name": "Install name",
 		"inv_name": "Inventory name"
 	};

 	this.id = "";
 	this.inventory_to_install_id = "";
 	this.install_name = "";
 	this.inv_name = "";

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		this.inventory_to_install_id = obj.id;
 		this.id = obj.id;
 		this.install_name = obj.installname;
 		this.inv_name = obj.inventoryname;

 		if(obj.install_name) {
 			this.install_name = obj.install_name;
 		}

 		if(obj.inv_name) {
 			this.inv_name = obj.inv_name;
 		}
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

 /*
 * Data method info object
 */
app.value('DataMethodInfo', {
	'save_title': 'Save Data method',
	'save_button': 'Save Data method',
	'retrieve_title': 'Data method',
	'retrieve_update_button': 'Update Data method',
	'update_title': 'Update Data method',
	'update_button': 'Update Data method',
	'search_button': 'Add Data method',
	'search_filter': 'Filter Data methods ...'
});

/*
 * Data method object
 */
 app.value('DataMethod', function(obj){

 	// Mandatory parameters that have to be set in the save form
 	this.m = ["name"];

 	// Mandatory parameters that have to be present in an URL when searching
 	this.search_m = ["name"];

 	// Parameters that are displayed when showing item details
 	this.retrieve = ["id", "name", "description"];

 	// Parameters that are checked before saving or updating
 	this.list = ["name", "description"];

 	// Parameters used for save URL
 	this.save = ["name", "description"];

 	// Parameters that are displayed when saving new item
 	this.save_show = ["name", "description"];

 	// Parameters used as update URL parameters
 	this.update = ["old_name", "name", "description"];

 	this.display = {
 		"id": "Id",
 		"name": "Name",
 		"description": "Description"
 	};

 	this.id = "";
 	this.name = "";
 	this.description = "";

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		if('id' in obj) {
 			this.id = obj.id;
 		}

 		if('old_name' in obj) {
 			this.old_name = obj.old_name;
 		}

 		this.name = obj.name;
 		this.description = obj.description;
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

 /*
 * Offline data info object
 */
app.value('OfflineDataInfo', {
	'save_title': 'Save Offline data',
	'save_button': 'Save Offline data',
	'retrieve_title': 'Offline data',
	'retrieve_update_button': 'Update Offline data',
	'retrieve_delete_button': 'Delete Offline data',
	'update_title': 'Update Offline data',
	'update_button': 'Update Offline data',
	'search_button': 'Add Offline data',
	'search_filter': 'Filter Offline data ...'
});

/*
 * Offline data object
 */
 app.value('OfflineData', function(obj){

 	// Mandatory parameters that have to be set in the save form
 	this.m = ["inventory_name", "data_id", "status"];

 	// Mandatory parameters that have to be present in an URL when searching
 	this.search_m = ["inventory_name"];

 	// Parameters that are displayed when showing item details
 	this.retrieve = ["id", "inventory_name", "description", "username", "date", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "status", "data_file_name", "script_name", "method_name", "methoddesc"];

 	// Parameters that are displayed when showing item details
 	this.retrieve_show = ["id", "status"];

 	// Parameters that are displayed when showing item details
 	this.retrieve_hide = ["inventory_name", "description", "username", "date", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "data_file_name", "script_name", "method_name", "methoddesc"];

 	// Parameters that are checked before saving or updating
 	this.list = ["inventory_name", "description", "date", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "status", "method_name"];

 	// Parameters used for save URL
 	this.save = ["inventory_name", "description", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "data_file_name", "data_id", "method_name", "status", "script_name", "script"];

 	// Parameters that are displayed when saving new item
 	this.save_show = ["inventory_name", "description", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "method_name", "script_name", "script", "status", "data_file_name"];

 	// Parameters used as update URL parameters
 	this.update = ["offline_data_id", "inventory_name", "description", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "data_file_name", "data_id", "method_name", "status", "script_name", "script"];

 	// All props
 	this.all = ["id", "offline_data_id", "inventory_name", "description", "date", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "data_file_name", "data_id", "method_name", "methoddesc", "status", "script_name", "script"];

 	// Parameters that are displayed in install details pane
 	this.install_display = ["date", "description", "status", "gap", "phase1"];

 	this.display = {
 		"id": "Id",
 		"inventory_name": "Inventory name",
 		"description": "Description",
 		"polarmode": "Polar mode",
 		"methoddesc": "Method description",
 		"phasemode": "Phase mode",
 		"data_file_name": "Data file name",
 		"method_name": "Method name",
 		"data_id": "Data id",
 		"date": "Date",
 		"gap": "Gap",
 		"phase1": "Phase 1",
 		"phase2": "Phase 2",
 		"phase3": "Phase 3",
 		"phase4": "Phase 4",
 		"script_name": "Script file name",
 		"script": "Script file content",
 		"status": "Data status"
 	};

 	this.id = "";
 	this.inventory_name = "";
 	this.description = "";
 	this.username = "";
 	this.date = "";
 	this.gap = undefined;
 	this.phase1 = undefined;
 	this.phase2 = undefined;
 	this.phase3 = undefined;
 	this.phase4 = undefined;
 	this.phasemode = "";
 	this.polarmode = "";
 	this.status = "";
 	this.data_file_name = "";
 	this.script_name = "";
 	this.script = "";
 	this.method_name = "";
 	this.methoddesc = "";
 	this.data_id = "";

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		for(i=0; i<this.all.length; i++) {

 			if(obj[this.all[i]] === null) {
 				this[this.all[i]] = undefined;

 			} else {
 				this[this.all[i]] = obj[this.all[i]];
 			}

  		}
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

 /*
 * Offline data (via install) info object
 */
app.value('OfflineDataInstallInfo', {
	'save_title': 'Save Offline data',
	'save_button': 'Save Offline data',
	'retrieve_title': 'Offline data',
	'retrieve_update_button': 'Update Offline data',
	'retrieve_delete_button': 'Delete Offline data',
	'update_title': 'Update Offline data',
	'update_button': 'Update Offline data',
	'search_button': 'Add Offline data',
	'search_filter': 'Filter Offline data ...'
});

/*
 * Offline data (via install) object
 */
 app.value('OfflineDataInstall', function(obj){

 	// Mandatory parameters that have to be set in the save form
 	this.m = ["inventory_name", "data_id", "status", "method_name"];

 	// Mandatory parameters that have to be present in an URL when searching
 	this.search_m = ["install_name"];

 	// Parameters that are displayed when showing item details
 	this.retrieve = ["id", "inventory_name", "install_name", "description", "username", "date", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "status", "data_file_name", "script_name", "method_name", "methoddesc"];

 	// Parameters that are displayed when showing item details
 	this.retrieve_show = ["id", "status"];

 	// Parameters that are displayed when showing item details
 	this.retrieve_hide = ["inventory_name", "install_name", "description", "username", "date", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "data_file_name", "script_name", "method_name", "methoddesc"];

 	// Parameters that are checked before saving or updating
 	this.list = ["install_name", "description", "date", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "status", "method_name"];

 	// Parameters used for save URL
 	this.save = ["inventory_name", "description", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "data_file_name", "data_id", "method_name", "status", "script_name", "script"];

 	// Parameters that are displayed when saving new item
 	this.save_show = ["inventory_name", "description", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "method_name", "script_name", "script", "status", "data_file_name"];

 	// Parameters used as update URL parameters
 	this.update = ["offline_data_id", "inventory_name", "description", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "data_file_name", "data_id", "method_name", "status", "script_name", "script"];

 	// All props
 	this.all = ["id", "offline_data_id", "install_name", "inventory_name", "description", "date", "gap", "phase1", "phase2", "phase3", "phase4", "phasemode", "polarmode", "data_file_name", "data_id", "method_name", "methoddesc", "status", "script_name", "script"];

 	this.display = {
 		"id": "Id",
 		"install_name": "Install name",
 		"inventory_name": "Inventory name",
 		"description": "Description",
 		"polarmode": "Polar mode",
 		"methoddesc": "Method description",
 		"phasemode": "Phase mode",
 		"data_file_name": "Data file name",
 		"method_name": "Method name",
 		"data_id": "Data id",
 		"gap": "Gap",
 		"phase1": "Phase 1",
 		"phase2": "Phase 2",
 		"phase3": "Phase 3",
 		"phase4": "Phase 4",
 		"script_name": "Script file name",
 		"script": "Script file content",
 		"status": "Data status"
 	};

 	this.id = "";
 	this.install_name = "";
 	this.inventory_name = "";
 	this.description = "";
 	this.username = "";
 	this.date = "";
 	this.gap = undefined;
 	this.phase1 = undefined;
 	this.phase2 = undefined;
 	this.phase3 = undefined;
 	this.phase4 = undefined;
 	this.phasemode = "";
 	this.polarmode = "";
 	this.status = "";
 	this.data_file_name = "";
 	this.script_name = "";
 	this.script = "";
 	this.method_name = "";
 	this.methoddesc = "";
 	this.data_id = "";

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		for(i=0; i<this.all.length; i++) {

 			if (obj[this.all[i]] === null) {
 				this[this.all[i]] = undefined;
 			}

 			this[this.all[i]] = obj[this.all[i]];
 		}
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });

 /*
 * Online data info object
 */
app.value('OnlineDataInfo', {
	'save_title': 'Save Online data',
	'save_button': 'Save Online data',
	'retrieve_title': 'Online data',
	'retrieve_update_button': 'Update Online data',
	'retrieve_delete_button': 'Delete Online data',
	'update_title': 'Update Online data',
	'update_button': 'Update Online data',
	'search_button': 'Add Online data',
	'search_filter': 'Filter Online data ...'
});

/*
 * Online data object
 */
 app.value('OnlineData', function(obj){

 	// Mandatory parameters that have to be set in the save form
 	this.m = ["install_name", "status", "file_name"];

 	// Mandatory parameters that have to be present in an URL when searching
 	this.search_m = ["install_name"];

 	// Parameters that are displayed when showing item details
 	this.retrieve = ["id", "install_name", "description", "username", "status", "url", "date"];

 	// Parameters that are displayed when showing item details
 	this.retrieve_show = ["id", "status"];

 	// Parameters that are displayed when showing item details
 	this.retrieve_hide = ["install_name", "description", "username", "url", "date"];

 	// Parameters that are checked before saving or updating
 	this.list = ["install_name", "description", "date", "status"];

 	// Parameters used for save URL
 	this.save = ["install_name", "description", "status", "url"];

 	// Parameters that are displayed when saving new item
 	this.save_show = ["install_name", "description", "status"];

 	// Parameters used as update URL parameters
 	this.update = ["online_data_id", "install_name", "description", "status", "url"];

 	// Parameters that are displayed in install details pane
 	this.install_display = ["date", "description", "status"];

 	this.display = {
 		"id": "Id",
 		"install_name": "Install name",
 		"description": "Description",
 		"status": "Status",
 		"date": "Date",
 		"url": "Data file",
 		"file_name": "Data file name"
 	};

 	this.id = "";
 	this.install_name = "";
 	this.description = "";
 	this.username = "";
 	this.date = "";
 	this.status = "";
 	this.url = "";
 	this.file_name = "";

 	this.set = function(obj) {

 		if(obj === undefined) {
 			return undefined;
 		}

 		if('id' in obj) {
 			this.id = obj.id;
 		}

 		if('online_data_id' in obj) {
 			this.online_data_id = obj.online_data_id;
 		}

 		this.install_name = obj.install_name;
 		this.description = obj.description;
 		this.username = obj.username;
 		this.date = obj.date;
 		this.status = obj.status;
 		this.url = obj.url;

 		if(this.url !== undefined && this.url !== "") {

	 		var urlParts = obj.url.split(/[\/\\]/);

	 		if (urlParts.length >= 1) {
	 			this.file_name = urlParts[urlParts.length-1];
	 		}

 		} else {
 			this.file_name = obj.file_name;
 		}
 	};

 	if(obj !== undefined) {
 		this.set(obj);
 	}
 });