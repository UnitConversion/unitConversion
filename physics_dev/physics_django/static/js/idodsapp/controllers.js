/*
 * Controllers for insertion device online data service module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created: Feb 26, 2014
 */

app.controller('indexCtrl', function($scope, $location, $anchorScroll) {

	$scope.top = function() {
		//l($location.hash());
		var id = $location.hash();

		// If no Log entry is selected, go to the top
		if(id === "" || id === "top") {
			$location.hash("top");
			$anchorScroll();

		// Scroll to the device
		} else {
			$location.hash("");
			var element = $('input[value=' + id + ']');

			$('html, body').animate({
				scrollTop: element.parent().offset().top
			}, 100);
		}
	};
});

/*
 * Main controller when we load the main page
 */
app.controller('mainCtrl', function($scope, $window, $modal){
	$scope.version = version;
	$scope.style = {};
	$scope.style.middle_class = "container-scroll-middle";
	$scope.style.right_class = "container-scroll-last-one";
	setUpLoginForm();

	$scope.session = {};
	$scope.authenticated = {};
	$scope.authenticated.error = false;

	$scope.login = function() {

		$.ajax({
			url: serviceurlraw + "user/login/",
			method: "POST",
			data: "username=" + $scope.session.username + "&password=" + $scope.session.password
		}).success(function(data, status, headers, config) {
			$scope.authenticated.error = false;
			$scope.$apply();
			$window.location.reload();

		}).error(function(data, status, headers, config) {
			$scope.authenticated.error = true;
			$scope.$apply();
		});
	};

	$scope.logout = function() {

		$.ajax({
			url: serviceurlraw + "user/logout/",
			method: "POST"
		}).success(function(data, status, headers, config) {
			$window.location.reload();

		}).error(function(data, status, headers, config) {

		});
	};
});

/*
 * Controller for the left/search pane
 */
app.controller('searchVendorCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[0];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		$window.location = newLocation;
	};

	// Vendor search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "vendor", ["name", "description"]) + "/list";
		$window.location = newLocation;
	};
});

/*
 * List vendor in the middle pane
 */
app.controller('listVendorCtrl', function($scope, $routeParams, $http, $window, Vendor, vendorFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;

	$scope.vendors = [];
	var previousItem = undefined;

	vendorFactory.retrieveVendors($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new Vendor(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.vendors.push(newItem);
		});
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, "vendor", ["name", "description"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.name = item.name;
		$routeParams.description = item.description;

		var location = createRouteUrl($routeParams, "vendor", ["name", "description"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showVendorCtrl', function($scope, $routeParams, $http, $window, Vendor, vendorFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new Vendor();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	
	// Get vendor from the factory
	// Get inventory from the factory if updating
	if($routeParams.action != "save") {
		vendorFactory.retrieveVendor($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.old_name = result.name;
		});
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, "vendor", ["name", "description"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(newItem, action) {
		$scope.alert.show = false;
		var vendor = new Vendor(newItem);
		l(vendor);
		var result = vendorFactory.checkVendor(vendor);
		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {
			delete $scope.error;
			var promise;
			l($scope.element);
			
			if(action === "update") {
				promise = vendorFactory.updateVendor($scope.element);

			} else if(action == "save") {
				promise = vendorFactory.saveVendor($scope.new);
			}
			
			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Vendor successfully saved!";
			
			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});
		}
	}
});

/*
 * Controller for the left/search pane
 */
app.controller('searchCmpntTypeCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[1];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "cmpnt_type", ["name", "description"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listCmpntTypeCtrl', function($scope, $routeParams, $http, $window, CmpntTypeInfo, CmpntType, cmpntTypeFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = CmpntTypeInfo;

	$scope.types = [];
	var previousItem = undefined;

	cmpntTypeFactory.retrieveCompntTypes($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new CmpntType(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.types.push(newItem);
		});
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, "cmpnt_type", ["name", "description"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.name = item.name;
		$routeParams.description = item.description;

		var location = createRouteUrl($routeParams, "cmpnt_type", ["name", "description"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showCmpntTypeCtrl', function($scope, $routeParams, $http, $window, CmpntTypeInfo, CmpntType, CmpntTypeType, cmpntTypeFactory, cmpntTypeTypeFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new CmpntType();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = CmpntTypeInfo;

	$scope.types = [];
	$scope.new.prop_keys = [];

	// Retrieve all Componet type property types
	cmpntTypeTypeFactory.retrieveCompntTypeTypes({}).then(function(result) {

		$.each(result, function(i, item){
			$scope.types.push(item.name);
		});
	});
	
	// Append new property
	$scope.appendProperty = function() {

		if($routeParams.action === "save"){
			$scope.new.prop_keys.push({'name': '', 'value': ''});
		
		} else {
			$scope.element.prop_keys.push({'name': '', 'value': ''});
		}
		l($scope.props);
	}

	// Property name dropdown has changed
	$scope.changePropertyName = function() {
		l($scope.props);
	}
	
	// Get component type from the factory
	if($routeParams.action != "save") {
		cmpntTypeFactory.retrieveCmpntType($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.old_name = result.name;
			l($scope.element);
		});
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, "cmpnt_type", ["name", "description"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(newItem, action) {
		$scope.alert.show = false;
		var item = new CmpntType(newItem);
		l(item);
		var result = cmpntTypeFactory.checkCmpntType(item);
		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {
			var propsObject = {};

			delete $scope.error;
			var promise;
			
			if(action === "update") {

				$.each($scope.element.prop_keys, function(i, prop) {
					propsObject[prop.name] = prop.value;
				});

				$scope.element.props = JSON.stringify(propsObject);

				promise = cmpntTypeFactory.updateCmpntType($scope.element);

			} else if(action == "save") {

				$.each($scope.new.prop_keys, function(i, prop) {
					propsObject[prop.name] = prop.value;
				});

				$scope.new.props = JSON.stringify(propsObject);
				promise = cmpntTypeFactory.saveCmpntType($scope.new);
			}
			
			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Component type successfully saved!";
			
			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});
		}
	}
});

/*
 * Controller for the left/search pane
 */
app.controller('searchCmpntTypeTypeCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[2];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "cmpnt_type_type", ["name", "description"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listCmpntTypeTypeCtrl', function($scope, $routeParams, $http, $window, CmpntTypeType, CmpntTypeTypeInfo, cmpntTypeTypeFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = CmpntTypeTypeInfo;

	$scope.types = [];
	var previousItem = undefined;

	cmpntTypeTypeFactory.retrieveCompntTypeTypes($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new CmpntTypeType(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.types.push(newItem);
		});
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, "cmpnt_type_type", ["name", "description"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.name = item.name;
		$routeParams.description = item.description;

		var location = createRouteUrl($routeParams, "cmpnt_type_type", ["name", "description"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showCmpntTypeTypeCtrl', function($scope, $routeParams, $http, $window, CmpntTypeType, CmpntTypeTypeInfo, cmpntTypeTypeFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new CmpntTypeType();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = CmpntTypeTypeInfo;

	// Get component type from the factory 
	if($routeParams.action != "save") {
		cmpntTypeTypeFactory.retrieveCmpntTypeType($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.old_name = result.name;
		});
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, "cmpnt_type_type", ["name", "description"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	// Save item into database
	$scope.saveItem = function(newItem, action) {
		$scope.alert.show = false;
		var item = new CmpntTypeType(newItem);
		l(item);
		var result = cmpntTypeTypeFactory.checkCmpntTypeType(item);
		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {
			delete $scope.error;
			var promise;
			
			if(action === "update") {
				promise = cmpntTypeTypeFactory.updateCmpntTypeType($scope.element);

			} else if(action == "save") {
				promise = cmpntTypeTypeFactory.saveCmpntTypeType($scope.new);
			}
			
			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Component type property type successfully saved!";
			
			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});
		}
	}
});

/*
 * Controller for the left/search pane
 */
app.controller('searchInventoryCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[3];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "inventory", ["name"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listInventoryCtrl', function($scope, $routeParams, $http, $window, InventoryInfo, Inventory, inventoryFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = InventoryInfo;

	$scope.items = [];
	var previousItem = undefined;

	inventoryFactory.retrieveItems($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new Inventory(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.items.push(newItem);
		});
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, "inventory", ["name"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.name = item.name;

		var location = createRouteUrl($routeParams, "inventory", ["name"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showInventoryCtrl', function($scope, $routeParams, $http, $window, InventoryInfo, CmpntType, Inventory, cmpntTypeFactory, inventoryTypeFactory, inventoryFactory, vendorFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new Inventory();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = InventoryInfo;

	$scope.types = [];
	$scope.props = [];
	$scope.vendors = [];
	$scope.new.prop_keys = [];

	// Retrieve all Component types
	cmpntTypeFactory.retrieveCompntTypes({}).then(function(result) {

		$.each(result, function(i, item){
			$scope.types.push(item.name);
		});
	});

	// Retrieve all Inventory property templates
	inventoryTypeFactory.retrieveItems({}).then(function(result) {

		$.each(result, function(i, item){
			$scope.props.push(item.name);
		});
	});

	// Retrieve all vendors
	vendorFactory.retrieveVendors({}).then(function(result) {

		$.each(result, function(i, item){
			$scope.vendors.push(item.name);
		});
	});
	
	// Append new property
	$scope.appendProperty = function() {

		if($routeParams.action === "save"){
			$scope.new.prop_keys.push({'name': '', 'value': ''});
		
		} else {
			$scope.element.prop_keys.push({'name': '', 'value': ''});
		}
	}

	// Property name dropdown has changed
	$scope.changePropertyName = function() {
		l($scope.props);
	}
	
	// Get inventory from the factory if updating
	if($routeParams.action != "save") {
		
		inventoryFactory.retrieveItem($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.old_name = result.name;
			l($scope.element);
		});
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, "inventory", ["name"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(newItem, action) {
		$scope.alert.show = false;
		var item = new Inventory(newItem);
		var result = inventoryFactory.checkItem(item);
		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {
			var propsObject = {};

			delete $scope.error;
			var promise;
			
			if(action === "update") {

				$.each($scope.element.prop_keys, function(i, prop) {
					propsObject[prop.name] = prop.value;
				});

				$scope.element.props = JSON.stringify(propsObject);

				promise = inventoryFactory.updateItem($scope.element);

			} else if(action == "save") {

				$.each($scope.new.prop_keys, function(i, prop) {
					propsObject[prop.name] = prop.value;
				});

				$scope.new.props = JSON.stringify(propsObject);
				
				promise = inventoryFactory.saveItem($scope.new);
			}
			
			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Inventory successfully saved!";
			
			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});
		}
	}
});

/*
 * Controller for the left/search pane
 */
app.controller('searchInventoryTypeCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[4];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "inventory_type", ["name"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listInventoryTypeCtrl', function($scope, $routeParams, $http, $window, InventoryTypeInfo, InventoryType, inventoryTypeFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = InventoryTypeInfo;

	$scope.items = [];
	var previousItem = undefined;

	inventoryTypeFactory.retrieveItems($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new InventoryType(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.items.push(newItem);
		});
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, "inventory_type", ["name"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.name = item.name;

		var location = createRouteUrl($routeParams, "inventory_type", ["name"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showInventoryTypeCtrl', function($scope, $routeParams, $http, $window, InventoryTypeInfo, InventoryType, inventoryTypeFactory, cmpntTypeFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new InventoryType();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = InventoryTypeInfo;

	$scope.types = [];

	// Retrieve all Component types
	cmpntTypeFactory.retrieveCompntTypes({}).then(function(result) {

		$.each(result, function(i, item){
			$scope.types.push(item.name);
		});
	});

	// Get inventory from the factory if updating
	if($routeParams.action != "save") {
		
		inventoryTypeFactory.retrieveItem($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.tmplt_id = result.id;
			l($scope.element);
		});
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, "inventory_type", ["name"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(newItem, action) {
		$scope.alert.show = false;
		var item = new InventoryType(newItem);
		var result = inventoryTypeFactory.checkItem(item);
		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {
			var propsObject = {};

			delete $scope.error;
			var promise;
			
			if(action === "update") {
				promise = inventoryTypeFactory.updateItem($scope.element);

			} else if(action == "save") {
				promise = inventoryTypeFactory.saveItem($scope.new);
			}
			
			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Inventory property template successfully saved!";
			
			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});
		}
	}
});

/*
 * Controller for the left/search pane
 */
app.controller('searchInstallCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[5];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "install", ["name", "cmpnt_type", "description", "coordinatecenter"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listInstallCtrl', function($scope, $routeParams, $http, $window, InstallInfo, Install, installFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = InstallInfo;

	$scope.items = [];
	var previousItem = undefined;

	installFactory.retrieveItems($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new Install(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.items.push(newItem);
		});
		$scope.items.reverse();
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, "install", ["name", "cmpnt_type", "description", "coordinatecenter"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}
		l(item);

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.name = item.name;
		$routeParams.description = item.description;
		$routeParams.cmpnt_type = item.cmpnt_type;
		$routeParams.coordinatecenter = item.coordinatecenter;

		var location = createRouteUrl($routeParams, "install", ["name", "cmpnt_type", "description", "coordinatecenter"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showInstallCtrl', function($scope, $routeParams, $http, $window, InstallInfo, Install, installFactory, cmpntTypeFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new Install();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = InstallInfo;

	$scope.types = [];

	// Retrieve all Component types
	cmpntTypeFactory.retrieveCompntTypes({'all_cmpnt_types': true}).then(function(result) {

		$.each(result, function(i, item){
			$scope.types.push(item.name);
		});
	});

	// Get inventory from the factory if updating
	if($routeParams.action != "save") {
		l($routeParams);
		
		installFactory.retrieveItem($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.old_name = result.name;
			l($scope.element);
		});
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, "install", ["name", "cmpnt_type", "description", "coordinatecenter"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(newItem, action) {
		$scope.alert.show = false;
		var item = new Install(newItem);
		var result = installFactory.checkItem(item);
		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {
			var propsObject = {};

			delete $scope.error;
			var promise;
			
			if(action === "update") {
				promise = installFactory.updateItem($scope.element);

			} else if(action == "save") {
				promise = installFactory.saveItem($scope.new);
			}
			
			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Install item successfully saved!";
			
			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});
		}
	}
});

/*
 * Controller for the left/search pane
 */
app.controller('searchInventoryToInstallCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[6];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "inventory_to_install", ["inv_name", "install_name"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listInventoryToInstallCtrl', function($scope, $routeParams, $http, $window, InventoryToInstallInfo, InventoryToInstall, inventoryToInstallFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = InventoryToInstallInfo;

	$scope.items = [];
	var previousItem = undefined;

	inventoryToInstallFactory.retrieveItems($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new InventoryToInstall(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.items.push(newItem);
		});
		$scope.items.reverse();
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, "inventory_to_install", ["inv_name", "install_name"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.inv_name = item.inv_name;
		$routeParams.install_name = item.install_name;

		var location = createRouteUrl($routeParams, "inventory_to_install", ["inv_name", "install_name"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showInventoryToInstallCtrl', function($scope, $routeParams, $http, $window, InventoryToInstallInfo, InventoryToInstall, inventoryToInstallFactory, installFactory, inventoryFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new InventoryToInstall();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = InventoryToInstallInfo;

	$scope.inv = [];
	$scope.inst = [];

	// Retrieve all Inventory items
	inventoryFactory.retrieveItems({'name': '*'}).then(function(result) {

		$.each(result, function(i, item){
			$scope.inv.push(item.name);
		});
	});
	// Retrieve all Install items
	installFactory.retrieveItems({'name': '*'}).then(function(result) {

		$.each(result, function(i, item){
			$scope.inst.push(item.name);
		});
	});

	// Get inventory to install from the factory if updating
	if($routeParams.action != "save") {
		
		inventoryToInstallFactory.retrieveItem($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.old_name = result.name;
			l($scope.element);
		});
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, "inventory_to_install", ["inv_name", "install_name"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(newItem, action) {
		$scope.alert.show = false;
		var item = new InventoryToInstall(newItem);
		l(item);
		var result = inventoryToInstallFactory.checkItem(item);
		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {
			var propsObject = {};

			delete $scope.error;
			var promise;
			
			if(action === "update") {
				promise = inventoryToInstallFactory.updateItem($scope.element);

			} else if(action == "save") {
				promise = inventoryToInstallFactory.saveItem($scope.new);
			}
			
			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Install item successfully saved!";
			
			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});
		}
	}
});

/*
 * Controller for the left/search pane
 */
app.controller('searchInstallRelCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[7];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {

		// Set description if is not set
		if (search.description === undefined || search.description === "") {
			search.description = "*";
		}

		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "install_rel", ["description", "parent_install"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.showTree = function(search) {
		search.description = "";
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "install_rel", ["description", "parent_install"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listInstallRelCtrl', function($scope, $routeParams, $http, $window, $sce, InstallRelInfo, InstallRel, installRelFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = InstallRelInfo;

	$scope.items = [];

	var previousItem = undefined;
	$scope.tree = {};
	$scope.showTree = false;

	if ($routeParams.description === undefined) {
		$scope.showTree = true;

		installRelFactory.retrieveTree({'install_name': 'Trees'}).then(function(result) {

			l(result);
			//$scope.tree = $sce.trustAsHtml(drawDataTree("", result, 0));
			$scope.tree = drawDataTree("", result, 0);
			//$("#tree").html(drawDataTree("", result, 0));
		});
	
	} else {

		installRelFactory.retrieveItems($routeParams).then(function(result) {

			l(result);

			$.each(result, function(i, item){

				// Build customized object
				var newItem = new InstallRel(item);

				// Alternate background colors
				if(i%2 === 0) {
					newItem.color = "bg_dark";

				} else {
					newItem.color = "bg_light";
				}

				$scope.items.push(newItem);
			});
			$scope.items.reverse();
		});
	}
	
	// Show add form in the right pane
	$scope.addItem = function(parent) {

		if (parent !== undefined) {
			$routeParams.parent_install = parent;
		}

		l(parent);

		var location = createRouteUrl($routeParams, "install_rel", ["description", "parent_install"]) + "/id/new/action/save";
		l(location);
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.name = item.name;

		var location = createRouteUrl($routeParams, "install_rel", ["description", "parent_install"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};

	// Show details when user selects item from a list
	$scope.showTreeNodeDetails = function(id) {

		var location = createRouteUrl($routeParams, "install_rel", ["description", "parent_install"]) + "/id/" + id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showInstallRelCtrl', function($scope, $modal, $routeParams, $http, $window, InstallRelInfo, InstallRel, installRelFactory, installRelTypeFactory, EntityError, installFactory){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new InstallRel();
	$scope.new.prop_keys = [];
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = InstallRelInfo;
	$scope.installs = [];
	$scope.parentDisabled = false;

	$scope.types = [];
	$scope.props = [];

	// Get install
	installFactory.retrieveItems({'name': '*', 'all_install': 'True'}).then(function(result) {
		$.each(result, function(i, item){

			$scope.installs.push(item.name);
		});

		l($scope.isntalls);
	});

	installRelTypeFactory.retrieveItems({}).then(function(result) {

		$.each(result, function(i, item) {
			$scope.props.push(item.name);
		});
	});

	// Append new property
	$scope.appendProperty = function() {

		if($routeParams.action === "save"){
			$scope.new.prop_keys.push({'name': '', 'value': ''});
		
		} else {
			$scope.element.prop_keys.push({'name': '', 'value': ''});
		}
	}

	// Property name dropdown has changed
	$scope.changePropertyName = function() {
		l($scope.props);
	}

	// Get install rel type from the factory if updating
	if($routeParams.action != "save") {
		
		installRelFactory.retrieveItem($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.child_install = result.childname;
			$scope.element.parent_install = result.parentname;
			l($scope.element);
		});
	
	} else {
		$scope.new.parent_install = $routeParams.parent_install;
		$scope.new.parentname = $routeParams.parent_install;
	}

	// Disable parent if parent is set in url
	if ($routeParams.parent_install !== undefined && $routeParams.parent_install != "") {
		$scope.parentDisabled = true;
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, "install_rel", ["description", "parent_install"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}

	$scope.deleteItem = function(localParent, localChild) {
		var modalInstance = $modal.open({
			templateUrl: 'modal/delete_install_rel.html',
			controller: 'deleteInstallRelCtrl',
			resolve: {
				parent: function() {
					return localParent;
				},
				child: function() {
					return localChild;
				}
			}
		});
	}
	
	$scope.saveItem = function(newItem, action) {
		$scope.alert.show = false;
		var item = new InstallRel(newItem);
		var result = installRelFactory.checkItem(item);
		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {
			var propsObject = {};

			delete $scope.error;
			var promise;
			
			if(action === "update") {

				$.each($scope.element.prop_keys, function(i, prop) {
					propsObject[prop.name] = prop.value;
				});

				$scope.element.props = JSON.stringify(propsObject);

				promise = installRelFactory.updateItem($scope.element);

			} else if(action == "save") {

				$.each($scope.new.prop_keys, function(i, prop) {
					propsObject[prop.name] = prop.value;
				});

				$scope.new.props = JSON.stringify(propsObject);

				promise = installRelFactory.saveItem($scope.new);
			}
			
			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Install rel type successfully saved!";
			
			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});
		}
	}
});

/*
 * Delete install rel
 */
app.controller('deleteInstallRelCtrl', function($scope, $routeParams, $modalInstance, installRelFactory, $window, parent, child) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;
	var types = [];
	$scope.message = "This relationship and all its children will be deleted. Are you sure you want to continue?";

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		installRelFactory.deleteItem({'parent_install': parent, 'child_install': child}).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Install rel successfully deleted!";
			$scope.showYesButton = false;
			$scope.showCancelButton = false;
			$scope.showFinishButton = true;

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
		});
	};

	$scope.cancel = function() {
		$modalInstance.dismiss('cancel');
	};

	$scope.finish = function() {
		var newLocation = createRouteUrl($routeParams, "install_rel", ["description", "parent_install"]) + "/list";
		$window.location = newLocation;
		$modalInstance.dismiss('cancel');
	};
});

/*
 * Controller for the left/search pane
 */
app.controller('searchInstallRelTypeCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[8];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "install_rel_type", ["name"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listInstallRelTypeCtrl', function($scope, $routeParams, $http, $window, InstallRelTypeInfo, InstallRelType, installRelTypeFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = InstallRelTypeInfo;

	$scope.items = [];
	var previousItem = undefined;

	installRelTypeFactory.retrieveItems($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new InstallRelType(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.items.push(newItem);
		});
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, "install_rel_type", ["name"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.name = item.name;

		var location = createRouteUrl($routeParams, "install_rel_type", ["name"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showInstallRelTypeCtrl', function($scope, $routeParams, $http, $window, InstallRelTypeInfo, InstallRelType, installRelTypeFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new InstallRelType();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = InstallRelTypeInfo;

	// Get install rel type from the factory if updating
	if($routeParams.action != "save") {
		
		installRelTypeFactory.retrieveItem($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.old_name = result.name;
			l($scope.element);
		});
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, "install_rel_type", ["name"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(newItem, action) {
		$scope.alert.show = false;
		var item = new InstallRelType(newItem);
		var result = installRelTypeFactory.checkItem(item);
		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {
			var propsObject = {};

			delete $scope.error;
			var promise;
			
			if(action === "update") {
				promise = installRelTypeFactory.updateItem($scope.element);

			} else if(action == "save") {
				promise = installRelTypeFactory.saveItem($scope.new);
			}
			
			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Install rel type successfully saved!";
			
			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});
		}
	}
});

/*
 * Controller for the left/search pane
 */
app.controller('searchDataMethodCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[9];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "data_method", ["name", "description"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listDataMethodCtrl', function($scope, $routeParams, $http, $window, DataMethodInfo, DataMethod, dataMethodFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = DataMethodInfo;

	$scope.items = [];
	var previousItem = undefined;

	dataMethodFactory.retrieveItems($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new DataMethod(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.items.push(newItem);
		});
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, "data_method", ["name", "description"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.name = item.name;
		$routeParams.description = item.description;

		var location = createRouteUrl($routeParams, "data_method", ["name", "description"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showDataMethodCtrl', function($scope, $routeParams, $http, $window, DataMethodInfo, DataMethod, dataMethodFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new DataMethod();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = DataMethodInfo;

	// Get inventory from the factory if updating
	if($routeParams.action != "save") {
		
		dataMethodFactory.retrieveItem($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.old_name = result.name;
			l($scope.element);
		});
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, "data_method", ["name", "description"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(newItem, action) {
		$scope.alert.show = false;
		var item = new DataMethod(newItem);
		var result = dataMethodFactory.checkItem(item);
		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {
			var propsObject = {};

			delete $scope.error;
			var promise;
			
			if(action === "update") {
				promise = dataMethodFactory.updateItem($scope.element);

			} else if(action == "save") {
				promise = dataMethodFactory.saveItem($scope.new);
			}
			
			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Data method item successfully saved!";
			
			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});
		}
	}
});

/*
 * Controller for the left/search pane
 */
app.controller('searchOfflineDataCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[10];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "offline_data", ["inventory_name", "description"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listOfflineDataCtrl', function($scope, $routeParams, $http, $window, OfflineDataInfo, OfflineData, offlineDataFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = OfflineDataInfo;

	$scope.items = [];
	var previousItem = undefined;

	offlineDataFactory.retrieveItems($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new OfflineData(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.items.push(newItem);
		});
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, "offline_data", ["inventory_name", "description"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.inventory_name = item.inventory_name;
		$routeParams.description = item.description;

		var location = createRouteUrl($routeParams, "offline_data", ["inventory_name", "description"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showOfflineDataCtrl', function($scope, $routeParams, $http, $window, OfflineDataInfo, OfflineData, offlineDataFactory, inventoryFactory, dataMethodFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new OfflineData();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = OfflineDataInfo;
	var uploadData = undefined;
	$scope.uploadFileName = "";
	
	$scope.inventories = [];
	$scope.methods = [];

	// Retrieve all Inventories
	inventoryFactory.retrieveItems({}).then(function(result) {

		$.each(result, function(i, item){
			$scope.inventories.push(item.name);
		});
	});

	// Retrieve all Component types
	dataMethodFactory.retrieveItems({}).then(function(result) {

		$.each(result, function(i, item){
			$scope.methods.push(item.name);
		});
	});

	$scope.options = {
		url: serviceurl + "/saverawdata/",
		maxFileSize: 5000000,
		acceptFileTypes: /(\.|\/)(gif|jpe?g|png|txt)$/i
	};

	$scope.$on('fileuploadadd', function(e, data) {
		var id = data.fileInput.context.id;
		$scope.uploadFileName = data.files[0].name;

		uploadData = data;
		delete $scope.error.data_id;
	});

	$scope.$on('fileuploaddone', function(e, data) {
		l(data.jqXHR.responseText);
		var response = data.jqXHR.responseText;
		l(e);

		if($scope.action === "update") {
			$scope.element.data_id = JSON.parse(response)["id"];

		} else if($scope.action == "save") {
			$scope.new.data_id = JSON.parse(response)["id"];
		}

		saveData($scope, offlineDataFactory);
	});

	$scope.$on('fileuploadfail', function(e, data) {
		l(data);
	});

	// Get inventory from the factory if updating
	if($routeParams.action != "save") {
		
		offlineDataFactory.retrieveItem($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.offline_data_id = result.id;
			l($scope.element);
		});
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, "offline_data", ["inventory_name", "description"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(action) {

		if (uploadData === undefined && action === "save") {
			$scope.error['data_id'] = "Raw data field is mandatory!";

		} else if (uploadData === undefined && action !== "save") {
			saveData($scope, offlineDataFactory);

		} else {
			uploadData.submit();
		}
	}

	$scope.downloadScript = function(element) {
		download(element.script_name, element.script);
	}

	$scope.downloadRawData = function(element) {
		// Retrieve raw file
		offlineDataFactory.retrieveRawFile(element.data_id).then(function(result) {
			l(result);
			download(element.data_file_name, result[element.data_id]['data']);
		});
	}
});


/*
 * Controller for the left/search pane
 */
app.controller('searchOfflineDataInstallCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[11];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "offline_data_install", ["install_name", "description"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listOfflineDataInstallCtrl', function($scope, $routeParams, $http, $window, $location, OfflineDataInstallInfo, OfflineDataInstall, offlineDataInstallFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = OfflineDataInstallInfo;

	$scope.items = [];
	var previousItem = undefined;

	var pathParts = $location.path().split('/');
	var type = pathParts[1];

	// Append second part of the path
	if (type === "beamline" || type === "installation") {
		type += "/" + pathParts[2];
	}

	offlineDataInstallFactory.retrieveItems($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new OfflineDataInstall(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.items.push(newItem);
		});
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, type, ["install_name", "description"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.install_name = item.install_name;
		$routeParams.description = item.description;

		var location = createRouteUrl($routeParams, type, ["install_name", "description"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showOfflineDataInstallCtrl', function($scope, $routeParams, $location, $http, $window, OfflineDataInstallInfo, OfflineDataInstall, offlineDataInstallFactory, offlineDataFactory, inventoryFactory, dataMethodFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new OfflineDataInstall();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = OfflineDataInstallInfo;
	var uploadData = undefined;
	$scope.uploadFileName = "";
	
	$scope.inventories = [];
	$scope.methods = [];

	var pathParts = $location.path().split('/');
	var type = pathParts[1];

	// Append second part of the path
	if (type === "beamline" || type === "installation") {
		type += "/" + pathParts[2];
	}

	// Retrieve all Inventories
	inventoryFactory.retrieveItems({}).then(function(result) {

		$.each(result, function(i, item){
			$scope.inventories.push(item.name);
		});
	});

	// Retrieve all Component types
	dataMethodFactory.retrieveItems({}).then(function(result) {

		$.each(result, function(i, item){
			$scope.methods.push(item.name);
		});
	});

	$scope.options = {
		url: serviceurl + "/saverawdata/",
		maxFileSize: 5000000,
		acceptFileTypes: /(\.|\/)(gif|jpe?g|png|txt)$/i
	};

	$scope.$on('fileuploadadd', function(e, data) {
		var id = data.fileInput.context.id;
		$scope.uploadFileName = data.files[0].name;

		uploadData = data;
		delete $scope.error.data_id;
	});

	$scope.$on('fileuploaddone', function(e, data) {
		l(data.jqXHR.responseText);
		var response = data.jqXHR.responseText;
		l(e);

		if($scope.action === "update") {
			$scope.element.data_id = JSON.parse(response)["id"];

		} else if($scope.action == "save") {
			$scope.new.data_id = JSON.parse(response)["id"];
		}

		saveData($scope, offlineDataFactory);
	});

	$scope.$on('fileuploadfail', function(e, data) {
		l(data);
	});

	// Get inventory from the factory if updating
	if($routeParams.action != "save") {
		
		offlineDataInstallFactory.retrieveItem($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.offline_data_id = result.id;
			l($scope.element);
		});
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, type, ["install_name", "description"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(action) {

		if (uploadData === undefined && action === "save") {
			$scope.error['data_id'] = "Raw data field is mandatory!";

		} else if (uploadData === undefined && action !== "save") {
			saveData($scope, offlineDataFactory);

		} else {
			uploadData.submit();
		}
	}

	$scope.downloadScript = function(element) {
		download(element.script_name, element.script);
	}

	$scope.downloadRawData = function(element) {
		// Retrieve raw file
		offlineDataFactory.retrieveRawFile(element.data_id).then(function(result) {
			l(result);
			download(element.data_file_name, result[element.data_id]['data']);
		});
	}
});

/*
 * Controller for the left/search pane
 */
app.controller('searchOnlineDataCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[12];

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		var newLocation = createRouteUrl(search, "online_data", ["install_name", "description"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List items in the middle pane
 */
app.controller('listOnlineDataCtrl', function($scope, $location, $routeParams, $http, $window, OnlineDataInfo, OnlineData, onlineDataFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.info = OnlineDataInfo;

	$scope.items = [];
	var previousItem = undefined;

	var pathParts = $location.path().split('/');
	var type = pathParts[1];

	// Append second part of the path
	if (type === "beamline" || type === "installation") {
		type += "/" + pathParts[2];
	}

	onlineDataFactory.retrieveItems($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new OnlineData(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.items.push(newItem);
		});
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createRouteUrl($routeParams, type, ["install_name", "description"]) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.install_name = item.install_name;
		$routeParams.description = item.description;

		var location = createRouteUrl($routeParams, type, ["install_name", "description"]) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showOnlineDataCtrl', function($scope, $routeParams, $http, $window, $location, OnlineDataInfo, OnlineData, onlineDataFactory, EntityError, installFactory){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new OnlineData();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	$scope.info = OnlineDataInfo;
	$scope.installs = [];
	var uploadData = undefined;
	$scope.uploadFileName = "";

	var pathParts = $location.path().split('/');
	var type = pathParts[1];

	// Append second part of the path
	if (type === "beamline" || type === "installation") {
		type += "/" + pathParts[2];
	}

	// Get inventory from the factory if updating
	if($routeParams.action != "save") {
		
		onlineDataFactory.retrieveItem($routeParams).then(function(result) {
			$scope.element = result;
			$scope.element.online_data_id = result.id;
			l($scope.element);
		});
	}

	// Retrieve all Installs
	installFactory.retrieveItems({}).then(function(result) {

		$.each(result, function(i, item){
			$scope.installs.push(item.name);
		});
	});

	$scope.options = {
		url: serviceurl + "/file/",
		maxFileSize: 5000000,
		acceptFileTypes: /(\.|\/)(gif|jpe?g|png|txt)$/i
	};

	$scope.$on('fileuploadadd', function(e, data) {
		l("add");
		var id = data.fileInput.context.id;
		$scope.uploadFileName = data.files[0].name;

		uploadData = data;
		delete $scope.error.url;
	});

	$scope.$on('fileuploaddone', function(e, data) {
		l(data.jqXHR.responseText);
		var response = data.jqXHR.responseText;
		l(e);

		if($scope.action === "update") {
			$scope.element.url = JSON.parse(response)["path"];

		} else if($scope.action == "save") {
			$scope.new.url = JSON.parse(response)["path"];
		}

		saveData($scope, onlineDataFactory);
	});

	$scope.$on('fileuploadfail', function(e, data) {
		l(data);
	});

	$scope.download = function(url) {
		$window.location.href = serviceurlraw + url;
	}
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createRouteUrl($routeParams, type, ["install_name", "description"]) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(action) {

		if($scope.action === "update") {
			result = onlineDataFactory.checkItem($scope.element);

		} else if($scope.action == "save") {
			l($scope.new);
			result = onlineDataFactory.checkItem($scope.new);
		}

		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {

			if (uploadData === undefined && action === "save") {
				$scope.error['url'] = "Data file field is mandatory!";

			} else if (uploadData === undefined && action !== "save") {
				saveData($scope, onlineDataFactory);

			} else {
				l(uploadData);
				uploadData.submit();
			}
		}
	}
});

/*
 * Controller for the left/search pane
 */
app.controller('searchBeamlineCtrl', function($scope, $location, $window, $routeParams, installRelFactory){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[13];
	$scope.display = "online_data";

	var pathParts = $location.path().split('/');

	if (pathParts.length > 2) {
		$scope.display = pathParts[2];
	}

	installRelFactory.retrieveTree({'install_name': 'beamline'}).then(function(result) {

		l(result);
		$scope.tree = drawDataTree2("", result, 0);
	});

	$scope.listData = function(install_name) {
		l(install_name);
		$scope.searchForItem({'install_name': install_name});
	};

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		search.description = "*";
		var newLocation = createRouteUrl(search, "beamline/" + $scope.display, ["install_name", "description"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * Controller for the left/search pane
 */
app.controller('searchInstallationCtrl', function($scope, $location, $window, $routeParams, installRelFactory){
	$scope.search = {};
	$scope.dataTypes = dataTypes;
	$scope.search.type = dataTypes[14];
	$scope.display = "online_data";

	var pathParts = $location.path().split('/');

	if (pathParts.length > 2) {
		$scope.display = pathParts[2];
	}

	installRelFactory.retrieveTree({'install_name': 'installation'}).then(function(result) {

		l(result);
		$scope.tree = drawDataTree2("", result, 0);
	});

	$scope.listData = function(install_name) {
		l(install_name);
		$scope.searchForItem({'install_name': install_name});
	};

	// Change entity
	$scope.changeEntity = function() {
		var newLocation = createRouteUrl(undefined, $scope.search.type.name, []);
		l(newLocation);
		$window.location = newLocation;
	};

	// Item search button click
	$scope.searchForItem = function(search) {
		search.search = new Date().getTime();
		search.description = "*";
		var newLocation = createRouteUrl(search, "installation/" + $scope.display, ["install_name", "description"]) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});