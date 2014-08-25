/*
 * Services for modules
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/*
 * Provide model code info to controllers
 */
app.factory('modelCodeInfoService', function($resource){

	return $resource(serviceurl + 'lattice/?function=retrieveModelCodeInfo&name=*&algorithm=*', {}, {
		transform: {
			method:'GET',
			isArray:false,
			transformResponse: function(response) {
				var returnData = {};
				returnData.data = JSON.parse(response);
				return returnData;
			}
		}
	});
});

/*
 * Provide a navigation factory to switch between views
 */
app.factory('navigationFactory', function($rootScope, masterTypes, dataTypes, mapMasterTypesToDataTypes) {
	var factory = {};
	factory.view = "";
	factory.nav = {};
	factory.nav.masterTypes = masterTypes;
	factory.nav.dataTypes = dataTypes;

	factory.setView = function(view) {
		this.view = view;
		this.broadcast();
	};

	factory.broadcast = function() {
		$rootScope.$broadcast('handleBroadcast');
	};

	return factory;
});

/*
 * Check if object has all mandatory properties set
 * @param item item we are checking
 * @param error error is filled in if mandatory property is not set
 */
function checkItem(item, error) {
	error.reset();

	$.each(item.m, function(i, property) {

		if(item[property] === undefined || item[property] === "") {
			error.add(property, item.display[property] + " is mandatory!");
		}
	});

	if(error.num === 0) {
		return true;

	} else {
		return error;
	}
}

/*
 * Retrieve item from the REST
 * @param url url for retrieving the item
 * @param obj item object that has the information about search parameters
 * @param Class name of the class we will create when we will get items
 */
function retrieveItem($q, $http, url, obj, Class) {
	var query = serviceurl + "/" + url + "/?";
	query += prepareUrlParameters(obj.list, obj, obj.search_m);

	var deffered = $q.defer();
	var promise = deffered.promise;

	$http.get(query).success(function(data){
		deffered.resolve(new Class(data[obj.id]));

	}).error(function(data, status, headers, config) {
		deffered.reject(data);
	});

	return promise;
}

/*
 * Retrieve all items from the REST
 * @param url url for retrieving the item
 * @param list array of parameters that can be present in the http request
 * @param params value of the parameters that can be present in the http request
 * @param mandatoryList array of mandatory parameters that should be present in the http request
 */
function retrieveItems($q, $http, url, list, params, mandatoryList) {
	var query = serviceurl + "/" + url + "/?";

	query += prepareUrlParameters(list, params, mandatoryList);

	var deffered = $q.defer();
	var promise = deffered.promise;

	$http.get(query).success(function(data){
		deffered.resolve(data);

	}).error(function(data, status, headers, config) {
		deffered.reject(data);
	});

	return promise;
}

/*
 * Save item in the database using REST
 * @param url url for saving the item
 * @param obj item we want to save
 */
function saveItem($q, $http, url, obj) {
	var query = serviceurl + "/" + url + "/";

	var params = prepareUrlParameters(obj.save, obj);

	var deffered = $q.defer();
	var promise = deffered.promise;

	$http.post(query, params).success(function(data){
		deffered.resolve(data);

	}).error(function(data, status, headers, config) {
		deffered.reject(data);
	});

	return promise;
}

/*
 * Update item using REST
 * @param url url for updating the item
 * @param obj item we want to update
 */
function updateItem($q, $http, url, obj) {
	var query = serviceurl + "/" + url + "/";

	var params = prepareUrlParameters(obj.update, obj);
	var deffered = $q.defer();
	var promise = deffered.promise;

	$http.post(query, params).success(function(data){
		deffered.resolve(data);

	}).error(function(data, status, headers, config) {
		deffered.reject(data);
	});

	return promise;
}

/*
 * Provide a factory for the vendor entity. Vendor can be checked, retrieved, saved and updated
 */
app.factory('vendorFactory', function($http, $q, Vendor, EntityError) {
	var factory = {};
	factory.eVendor = new Vendor();
	factory.error = new EntityError();

	// Set vendor object
	factory.setVendor = function(vendor) {
		this.eVendor.set(vendor);
	};

	// Check vendor before sending it to the server
	factory.checkVendor = function(vendor) {

		if(vendor !== undefined) {
			factory.setVendor(vendor);
		}

		return checkItem(factory.eVendor, factory.error);
	};

	// Get vendor from server
	factory.retrieveVendor = function(vendor) {

		if(vendor !== undefined) {
			this.setVendor(vendor);
		}

		return retrieveItem($q, $http, "vendor", this.eVendor, Vendor);
	};

	// Get vendors from server
	factory.retrieveVendors = function(params) {
		return retrieveItems($q, $http, "vendor", this.eVendor.list, params, this.eVendor.search_m);
	};

	// Save new vendor
	factory.saveVendor = function(vendor) {

		if(vendor !== undefined) {
			this.setVendor(vendor);
		}

		return saveItem($q, $http, "savevendor", this.eVendor);
	};

	// Update a vendor
	factory.updateVendor = function(vendor) {

		if(vendor !== undefined) {
			this.setVendor(vendor);
		}

		return updateItem($q, $http, "updatevendor", this.eVendor);
	};

	return factory;
});

/*
 * Provide a factory for the component type entity. Component type can be checked, retrieved, saved and updated
 */
app.factory('cmpntTypeFactory', function($http, $q, CmpntType, EntityError) {
	var factory = {};
	factory.eCmpntType = new CmpntType();
	factory.error = new EntityError();

	// Set component type object
	factory.setCmpntType = function(cmpntType) {
		this.eCmpntType.set(cmpntType);
	};

	// Check component type before sending it to the server
	factory.checkCmpntType = function(cmpntType) {

		if(cmpntType !== undefined) {
			this.setCmpntType(cmpntType);
		}

		return checkItem(this.eCmpntType, this.error);
	};

	// Get componet type from server
	factory.retrieveCmpntType = function(cmpntType) {

		if(cmpntType !== undefined) {
			this.setCmpntType(cmpntType);
		}

		return retrieveItem($q, $http, "cmpnttype", this.eCmpntType, CmpntType);
	};

	// Get component types from server
	factory.retrieveCompntTypes = function(params) {
		return retrieveItems($q, $http, "cmpnttype", this.eCmpntType.list, params, this.eCmpntType.search_m);
	};

	// Save new component type
	factory.saveCmpntType = function(cmpntType) {

		if(cmpntType !== undefined) {
			this.setCmpntType(cmpntType);
		}

		return saveItem($q, $http, "savecmpnttype", this.eCmpntType);
	};

	// Update component tpye
	factory.updateCmpntType = function(cmpntType) {

		if(cmpntType !== undefined) {
			this.setCmpntType(cmpntType);
		}

		return updateItem($q, $http, "updatecmpnttype", this.eCmpntType);
	};

	return factory;
});

/*
 * Provide a factory for the component type property type entity. Component type property type can be checked, retrieved, saved and updated
 */
app.factory('cmpntTypeTypeFactory', function($http, $q, CmpntTypeType, EntityError) {
	var factory = {};
	factory.eCmpntTypeType = new CmpntTypeType();
	factory.error = new EntityError();

	// Set component type property type object
	factory.setCmpntTypeType = function(cmpntTypeType) {
		this.eCmpntTypeType.set(cmpntTypeType);
	};

	// Check component type property type before sending it to the server
	factory.checkCmpntTypeType = function(cmpntTypeType) {

		if(cmpntTypeType !== undefined) {
			this.setCmpntTypeType(cmpntTypeType);
		}

		return checkItem(this.eCmpntTypeType, this.error);
	};

	// Get componet type property type from server
	factory.retrieveCmpntTypeType = function(cmpntTypeType) {

		if(cmpntTypeType !== undefined) {
			this.setCmpntTypeType(cmpntTypeType);
		}

		return retrieveItem($q, $http, "cmpnttypeproptype", this.eCmpntTypeType, CmpntTypeType);
	};

	// Get component type property types from server
	factory.retrieveCompntTypeTypes = function(params) {
		return retrieveItems($q, $http, "cmpnttypeproptype", this.eCmpntTypeType.list, params, this.eCmpntTypeType.search_m);
	};

	// Save new component type property type
	factory.saveCmpntTypeType = function(cmpntTypeType) {

		if(cmpntTypeType !== undefined) {
			this.setCmpntTypeType(cmpntTypeType);
		}

		return saveItem($q, $http, "savecmpnttypeproptype", this.eCmpntTypeType);
	};

	// Update component type property type
	factory.updateCmpntTypeType = function(cmpntTypeType) {

		if(cmpntTypeType !== undefined) {
			this.setCmpntTypeType(cmpntTypeType);
		}

		return updateItem($q, $http, "updatecmpnttypeproptype", this.eCmpntTypeType);
	};

	return factory;
});

/*
 * Provide a factory for the inventory entity. Inventory can be checked, retrieved, saved and updated
 */
app.factory('inventoryFactory', function($http, $q, Inventory, EntityError) {
	var factory = {};
	factory.entity = new Inventory();
	factory.error = new EntityError();

	// Set inventory object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check inventory before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}
		l(this.entity);

		return checkItem(this.entity, this.error);
	};

	// Get inventory from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "inventory", this.entity, Inventory);
	};

	// Get inventories from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "inventory", this.entity.list, params, this.entity.search_m);
	};

	// Save new inventory
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "saveinventory", this.entity);
	};

	// Update inventory
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return updateItem($q, $http, "updateinventory", this.entity);
	};

	return factory;
});

/*
 * Provide a factory for the inventory property template entity. Inventory property template can be checked, retrieved, saved and updated
 */
app.factory('inventoryTypeFactory', function($http, $q, InventoryType, EntityError) {
	var factory = {};
	factory.entity = new InventoryType();
	factory.error = new EntityError();

	// Set inventory property template object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check inventory property tempalte before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return checkItem(this.entity, this.error);
	};

	// Get inventory property template from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "inventoryproptmplt", this.entity, InventoryType);
	};

	// Get inventorie property templates from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "inventoryproptmplt", this.entity.list, params, this.entity.search_m);
	};

	// Save new inventory property template
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "saveinventoryproptmplt", this.entity);
	};

	// Update inventory property template
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return updateItem($q, $http, "updateinventoryproptmplt", this.entity);
	};

	return factory;
});

/*
 * Provide a factory for the install entity. Install can be checked, retrieved, saved and updated
 */
app.factory('installFactory', function($http, $q, Install, EntityError) {
	var factory = {};
	factory.entity = new Install();
	factory.error = new EntityError();

	// Set install object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check install before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return checkItem(this.entity, this.error);
	};

	// Get install from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "install", this.entity, Install);
	};

	// Get install from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "install", this.entity.list, params, this.entity.search_m);
	};

	// Save new install
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "saveinstall", this.entity);
	};

	// Update install
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return updateItem($q, $http, "updateinstall", this.entity);
	};

	return factory;
});

/*
 * Provide a factory for the install entity. Install can be checked, retrieved, saved and updated
 */
app.factory('inventoryToInstallFactory', function($http, $q, InventoryToInstall, EntityError) {
	var factory = {};
	factory.entity = new InventoryToInstall();
	factory.error = new EntityError();

	// Set inventory to install object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check inventory to install before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return checkItem(this.entity, this.error);
	};

	// Get inventory to install from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "inventorytoinstall", this.entity, InventoryToInstall);
	};

	// Get inventory to install from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "inventorytoinstall", this.entity.list, params, this.entity.search_m);
	};

	// Save new inventory to install
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "saveinventorytoinstall", this.entity);
	};

	// Update inventory to install
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return updateItem($q, $http, "updateinventorytoinstall", this.entity);
	};

	// Delete inventory to install
	factory.deleteItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		var query = serviceurl + "/deleteinventorytoinstall/";
		l(this.entity);
		var params = prepareUrlParameters(["inventory_to_install_id"], item);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);

		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	};

	return factory;
});

/*
 * Provide a factory for the install rel entity. Install rel can be checked, retrieved, saved and updated
 */
app.factory('installRelFactory', function($http, $q, InstallRel, EntityError) {
	var factory = {};
	factory.entity = new InstallRel();
	factory.error = new EntityError();

	// Set install rel type object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check install rel type before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return checkItem(this.entity, this.error);
	};

	// Get install rel tree from server
	factory.retrieveTree = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		var query = serviceurl + "/trees/?";
		query += prepareUrlParameters(["install_name"], this.entity);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.get(query).success(function(data){
			deffered.resolve(data);

		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	};

	// Get install from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "installrel", this.entity, InstallRel);
	};

	// Get install rel type from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "installrel", this.entity.list, params, this.entity.search_m);
	};

	// Save new install rel type
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "saveinstallrel", this.entity);
	};

	// Update install rel type
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return updateItem($q, $http, "updateinstallrel", this.entity);
	};

	// Delete install rel
	factory.deleteItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		var query = serviceurl + "/deleteinstallrel/";
		l(this.entity);
		var params = prepareUrlParameters(["parent_install", "child_install"], item);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);

		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	};

	return factory;
});

/*
 * Provide a factory for the install rel property entity. Install rel prop can be checked, retrieved, saved and updated
 */
app.factory('installRelPropFactory', function($http, $q, InstallRelProp, EntityError) {
	var factory = {};
	factory.entity = new InstallRelProp();
	factory.error = new EntityError();

	// Set install rel prop object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check install rel prop before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return checkItem(this.entity, this.error);
	};

	// Save new install rel prop
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "saveinstallrelprop", this.entity);
	};

	// Update install rel prop
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return updateItem($q, $http, "updateinstallrelprop", this.entity);
	};

	return factory;
});

/*
 * Provide a factory for the install rel type entity. Install rel type can be checked, retrieved, saved and updated
 */
app.factory('installRelTypeFactory', function($http, $q, InstallRelType, EntityError) {
	var factory = {};
	factory.entity = new InstallRelType();
	factory.error = new EntityError();

	// Set install rel type object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check install rel type before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return checkItem(this.entity, this.error);
	};

	// Get install rel type from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "installrelproptype", this.entity, InstallRelType);
	};

	// Get install rel type from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "installrelproptype", this.entity.list, params, this.entity.search_m);
	};

	// Save new install rel type
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "saveinstallrelproptype", this.entity);
	};

	// Update install rel type
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return updateItem($q, $http, "updateinstallrelproptype", this.entity);
	};

	return factory;
});

/*
 * Provide a factory for the data method entity. Data method can be checked, retrieved, saved and updated
 */
app.factory('dataMethodFactory', function($http, $q, DataMethod, EntityError) {
	var factory = {};
	factory.entity = new DataMethod();
	factory.error = new EntityError();

	// Set data method object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check data method before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return checkItem(this.entity, this.error);
	};

	// Get data method from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "datamethod", this.entity, DataMethod);
	};

	// Get data method from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "datamethod", this.entity.list, params, this.entity.search_m);
	};

	// Save new data method
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "savedatamethod", this.entity);
	};

	// Update data method
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return updateItem($q, $http, "updatedatamethod", this.entity);
	};

	return factory;
});

/*
 * Provide a factory for the offline data entity. Offline data can be checked, retrieved, saved and updated
 */
app.factory('offlineDataFactory', function($http, $q, OfflineData, EntityError) {
	var factory = {};
	factory.entity = new OfflineData();
	factory.error = new EntityError();

	// Set offline data object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check offline data before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return checkItem(this.entity, this.error);
	};

	// Get offline data from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "offlinedata", this.entity, OfflineData);
	};

	// Raw data file
	factory.retrieveRawFile = function(id) {
		var query = serviceurl + "/rawdata/?raw_data_id=" + id;

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.get(query).success(function(data){
			deffered.resolve(data);

		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	};

	// Get offline data from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "offlinedata", this.entity.list, params, this.entity.search_m);
	};

	// Save new offline data
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "saveofflinedata", this.entity);
	};

	// Update offline data
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return updateItem($q, $http, "updateofflinedata", this.entity);
	};

	// Delete offline data
	factory.deleteItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		var query = serviceurl + "/deleteofflinedata/";
		l(this.entity);
		var params = prepareUrlParameters(["offline_data_id"], item);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);

		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	};

	return factory;
});

/*
 * Provide a factory for the offline data (via install) entity. Offline data can be checked, retrieved, saved and updated
 */
app.factory('offlineDataInstallFactory', function($http, $q, OfflineDataInstall, EntityError) {
	var factory = {};
	factory.entity = new OfflineDataInstall();
	factory.error = new EntityError();

	// Set offline data install object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check offline data install before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return checkItem(this.entity, this.error);
	};

	// Get offline data install from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "offlinedatainstall", this.entity, OfflineDataInstall);
	};

	// Get offline data install from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "offlinedatainstall", this.entity.list, params, this.entity.search_m);
	};

	return factory;
});

/*
 * Provide a factory for the online data entity. Online data can be checked, retrieved, saved and updated
 */
app.factory('onlineDataFactory', function($http, $q, OnlineData, EntityError) {
	var factory = {};
	factory.entity = new OnlineData();
	factory.error = new EntityError();

	// Set online data object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check online data before sending it to the server
	factory.checkItem = function(item) {
		l(item);

		if(item !== undefined) {
			this.setItem(item);
		}
		l(this.entity);
		return checkItem(this.entity, this.error);
	};

	// Get online data from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "onlinedata", this.entity, OnlineData);
	};

	// Get online data from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "onlinedata", this.entity.list, params, this.entity.search_m);
	};

	// Save new online data
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "saveonlinedata", this.entity);
	};

	// Update online data
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return updateItem($q, $http, "updateonlinedata", this.entity);
	};

	// Delete online data
	factory.deleteItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		var query = serviceurl + "/deleteonlinedata/";
		l(this.entity);
		var params = prepareUrlParameters(["online_data_id"], item);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);

		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	};

	return factory;
});

/*
 * Provide a factory for the rot coil data entity. Rot coil data can be checked, retrieved, saved and updated
 */
app.factory('rotCoilDataFactory', function($http, $q, RotCoilData, EntityError) {
	var factory = {};
	factory.entity = new RotCoilData();
	factory.error = new EntityError();

	// Set rot coil data object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check rot coil data before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return checkItem(this.entity, this.error);
	};

	// Get rot coil data from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "rotcoildata", this.entity, RotCoilData);
	};

	// Get rot coil data from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "rotcoildata", this.entity.list, params, this.entity.search_m);
	};

	// Save new rot coil data
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "saverotcoildata", this.entity);
	};

	// Update rot coil data
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return updateItem($q, $http, "updaterotcoildata", this.entity);
	};

	// Delete rot coil data
	factory.deleteItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		var query = serviceurl + "/deleterotcoildata/";
		l(this.entity);
		var params = prepareUrlParameters(["inventory_name", "rot_coil_data_id"], item);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);

		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	};

	return factory;
});

/*
 * Provide a factory for the hall probe data entity. Hall probe data can be checked, retrieved, saved and updated
 */
app.factory('hallProbeDataFactory', function($http, $q, HallProbeData, EntityError) {
	var factory = {};
	factory.entity = new HallProbeData();
	factory.error = new EntityError();

	// Set rot hall probe object
	factory.setItem = function(item) {
		this.entity.set(item);
	};

	// Check rot hall probe before sending it to the server
	factory.checkItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return checkItem(this.entity, this.error);
	};

	// Get rot hall probe from server
	factory.retrieveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return retrieveItem($q, $http, "hallprobedata", this.entity, HallProbeData);
	};

	// Get rot hall probe from server
	factory.retrieveItems = function(params) {
		return retrieveItems($q, $http, "hallprobedata", this.entity.list, params, this.entity.search_m);
	};

	// Save new rot hall probe
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		return saveItem($q, $http, "savehallprobedata", this.entity);
	};

	// Update rot hall probe
	factory.updateItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}
		l(item);
		l(this.entity);

		return updateItem($q, $http, "updatehallprobedata", this.entity);
	};

	// Delete hall probe data
	factory.deleteItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		var query = serviceurl + "/deletehallprobedata/";
		l(this.entity);
		var params = prepareUrlParameters(["inventory_name", "hall_probe_id"], item);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);

		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	};

	return factory;
});