/*
 * Controllers for conversion module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/*
 * Controller is used for controlling the index page
 */
app.controller('indexCtrl', function($scope, $location, $anchorScroll) {

	$scope.top = function() {
		l($location.hash());
		var id = $location.hash();

		// If no Log entry is selected, go to the top
		if(id === "" || id === "top") {
			$location.hash("top");
			$anchorScroll();

		// Scroll to the device
		} else {
			$location.hash("");
			var element = $('input[value=' + id + ']');
			l(element.offset().top);

			$('html, body').animate({
				scrollTop: element.parent().offset().top
			}, 100);
		}
	};
});

/*
 * Main controller when we load the main page
 */
app.controller('mainCtrl', function($scope, $window){
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
			url: ucserviceurl + "user/login/",
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
			url: ucserviceurl + "user/logout/",
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
app.controller('searchFormCtrl', function($scope, systemService, $window, $routeParams){
	$scope.search = {};
	$scope.systems = [];
	$scope.search.displayName = "display_search_filter";
	$scope.search.displaySystem = "display_search_filter";
	$scope.search.type = "install";
	l("Show search form!!!");

	// Set search type
	if($routeParams.type !== undefined) {
		$scope.search.type = $routeParams.type;
	}

	// Load Systems
	systemService.transform(function(data){
		$scope.systems = data.systems;
	});

	// Search button click
	$scope.searchForDevices = function(search) {
		var newLocation = createDeviceListQuery(search, true) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};

	// Watch for search type change
	$scope.$watch('search.type', function(newValue, oldValue){

		if(newValue === "install") {
			$scope.search.displayName = "display_search_filter";
			$scope.search.displaySystem = "display_search_filter";

		} else {
			$scope.search.displayName = "hide_display_filter";
			$scope.search.displaySystem = "hide_display_filter";
		}
	});
});

/*
 * List devices in the middle pane
 */
app.controller('listDevicesCtrl', function($scope, $routeParams, $http, $window) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;

	$scope.devices = [];
	var previousDevice;
	l("Show list!!!");

	var query = ucserviceurl + 'magnets/' + createDeviceListQuery($routeParams, false);

	$http.get(query).success(function(data){

		$.each(data, function(i, item){

			// Build customized Log object
			var newItem = item;

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			// Add create device id and add it to device
			newItem.id = item.inventoryId;

			if($routeParams.type === "install" && item.name !== undefined) {
				newItem.id = item.name;
			}

			$scope.devices.push(newItem);
		});
	});

	// Show details when user selects the device from a list
	$scope.showDetails = function(device){
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousDevice !== undefined) {
			previousDevice.click = "";
			//$scope.id = undefined;
		}

		previousDevice = device;
		device.click = "device_click";

		var id = device.inventoryId;

		if($routeParams.type === "install") {
			id = device.name;
		}

		$window.location = createDeviceListQuery($routeParams, true) + "/id/" + id + "/view/0/subview/results#" + id;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showDetailsCtrl', function($scope, $routeParams, $http, $window, detailsService, $location){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";

	$scope.id = $routeParams.id;
	$scope.data = {};
	$scope.view = $routeParams.view;
	$scope.subview = $routeParams.subview;
	$scope.result = {};
	$scope.detailsTabs = [];
	var detailsTabsIndex = 0;
	$scope.tabs = [];
	$scope.url = createDeviceListQuery($routeParams, true) + "/id/" + $routeParams.id + '/';
	$scope.inst_url = createDeviceListQuery($routeParams, true) + "/inst/" + $routeParams.id + '/';
	$scope.view = $routeParams.view;
	$scope.properties = {};

	$scope.error = {};
	$scope.error.message = "";

	var algorithms = {};
	$scope.results = {};
	$scope.results.convertedResult = [];
	$scope.results.series = [];

	$scope.scroll = {};
	$scope.scroll.scroll = $routeParams.id;

	$scope.goToMuniconvDetails = function() {
		var url = $scope.inst_url + 'step/' + new Date().getTime() + '/mt/m';
		$window.location = url;
	};

	$scope.goToMeasurementDataDetails = function() {
		var url = $scope.inst_url + 'step/' + new Date().getTime() + '/md';
		$window.location = url;
	};

	l("hash: " + $location.hash());
	l("Show details!!!");

	detailsService.getDetails($routeParams).then(function(data) {
		$scope.data = data[$routeParams.id];

		for(var first in $scope.data) {
			$scope.properties[first] = {};

			for(var second in $scope.data[first]) {
				$scope.detailsTabs.push({first: first, second: second, index: detailsTabsIndex});
				detailsTabsIndex ++;
				$scope.properties[first][second] = {};

				// Save all axcept the algorithms in an array
				for(var third in $scope.data[first][second]) {

					if(third !== "algorithms" && third !== "measurementData") {
						$scope.properties[first][second][third] = $scope.data[first][second][third];
					}
				}

				// Save all algorithms into an array
				for(var algorithm in $scope.data[first][second].algorithms) {
					var algorithmParts = algorithm.split("2");
					algorithms[algorithm] = $scope.data[first][second].algorithms[algorithm];
					algorithms[algorithmParts[0]] = $scope.data[first][second].algorithms[algorithm];
				}
			}
		}
	});

	/*
	 * When user clicks on convert button, fire this function
	 */
	$scope.convert = function() {
		$scope.tabs = [];

		var idParameter = "id";

		if($routeParams.type === "install") {
			idParameter = "name";
		}

		var conversionQuery = ucserviceurl
				+ 'magnets/conversion/?' + idParameter
				+ '=' + $routeParams.id
				+ '&from=' + $scope.source_unit
				+ '&to=' + $scope.destination_unit
				+ '&value=' + $scope.initial_value
				+ '&complex=' + $scope.detailsTabs[$routeParams.view]['second'];

		if($scope.energy !== undefined && $scope.energy !== "") {
			conversionQuery += '&energy=' + $scope.energy;
		}

		l(conversionQuery);

		// Execute conversion query
		$http.get(conversionQuery).success(function(data){
			l(data[$routeParams.id]);
			var details = data[$routeParams.id];
			var results = {};
			$scope.result = details;
			$scope.error.display = false;

			if(details[$scope.detailsTabs[$routeParams.view]['first']] !== undefined) {
				results = details[$scope.detailsTabs[$routeParams.view]['first']][$scope.detailsTabs[$routeParams.view]['second']];
				l(results);

				// Go through returned data and save needed values
				if(results.conversionResult.value === null && results.conversionResult.unit === "") {
					$scope.error.message = results.conversionResult.message;
					$scope.error.display = true;
					return;
				}

				// Get the initial unit from algorithms data
				var initialUnit = "";
				var algKey = $scope.source_unit + '2' + $scope.destination_unit;

				// Algorithm in a table
				if(algKey in algorithms) {
					initialUnit = algorithms[algKey].initialUnit;

				// Initial unit of algorithm in a table
				} else if ($scope.source_unit in algorithms) {
					initialUnit = algorithms[$scope.source_unit].initialUnit;

				// Nothing in a table, initial unit should be an empty string
				} else {
					initialUnit = "";
				}

				// Push conversion result to conversion result table
				$scope.results.convertedResult.push({
					init_value: $scope.initial_value,
					init_unit: initialUnit,
					conv_value: results.conversionResult.value,
					conv_unit: results.conversionResult.unit,
					from: $scope.source_unit,
					to: $scope.destination_unit,
					id: $routeParams.id
				});
			}

		}).error(function(){
			$scope.error.display = true;
		});
	};
});

/*
 * Show details in the right pane
 */
app.controller('showWizardCtrl', function($scope, $modal, $routeParams, $http, $window, detailsService, inventoryTypeFactory, InventoryType, inventoryPropFactory, InventoryProp, $location){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	l("Show wizard!");
	l($routeParams);

	$routeParams.id = $routeParams.inst;
	$scope.id = $routeParams.id;
	$scope.data = {};
	$scope.rawData = {};
	$scope.device = {};
	$scope.view = $routeParams.view;
	$scope.subview = $routeParams.subview;
	$scope.result = {};
	$scope.detailsTabs = [];
	var detailsTabsIndex = 0;
	$scope.tabs = [];
	$scope.inst_url = createDeviceListQuery($routeParams, true) + "/inst/" + $routeParams.inst + '/';
	$scope.url = createDeviceListQuery($routeParams, true) + "/id/" + $routeParams.inst + '/';
	$scope.view = $routeParams.view;
	$scope.properties = {};

	$scope.error = {};
	$scope.error.message = "";

	var algorithms = {};
	$scope.results = {};
	$scope.results.convertedResult = [];
	$scope.results.series = [];

	$scope.scroll = {};
	$scope.scroll.scroll = $routeParams.id;

	//l("hash: " + $location.hash());

	$scope.municonv = {
		'standard': {},
		'complex:1': {},
		'complex:2': {},
		'complex:3': {}
	};
	$scope.municonvChain = {
		'standard': {},
		'complex:1': {},
		'complex:2': {},
		'complex:3': {}
	};

	$scope.goToMuniconv = function() {
		var url = $scope.inst_url + 'step/' + $routeParams.si + '/mt/m';
		$window.location = url;
	};

	$scope.goToMuniconvChain = function() {
		var url = $scope.inst_url + 'step/' + $routeParams.si + '/mt/mc';
		$window.location = url;
	};

	$scope.goToMeasurementData = function() {
		var url = $scope.inst_url + 'step/' + new Date().getTime() + '/md';
		$window.location = url;
	};

	$scope.goToDetails = function() {
		var url = $scope.url + "view/0/subview/results#" + $routeParams.inst;

		var installs = Object.keys($scope.rawData);

		$.each($scope.rawData[installs[0]], function(i, type) {

			inventoryTypeFactory.retrieveItems({name: i, cmpnt_type_name: $scope.device.componentType}).then(function(data) {
				l(Object.keys(data).length);

				if(Object.keys(data).length < 1) {

					inventoryTypeFactory.saveItems({name: i, cmpnt_type_name: $scope.device.componentType}).then(function(saveTmpltResult) {
						// TODO: Save or update property
						l(saveTmpltResult);
					});

				} else {

					inventoryPropFactory.retrieveItems({inventory_id: $scope.device.inventoryId, inventory_property_template_name: i, cmpnt_type_name: $scope.device.componentType}).then(function(data) {
						l(data);

						if(Object.keys(data).length < 1) {

							inventoryPropFactory.saveItem({inventory_id: $scope.device.inventoryId, inventory_property_template_name: i, cmpnt_type_name: $scope.device.componentType, value: JSON.stringify($scope.rawData[installs[0]][i])}).then(function(result) {
								l(result);
							});

						} else {

							inventoryPropFactory.updateItem({inventory_id: $scope.device.inventoryId, inventory_property_template_name: i, cmpnt_type_name: $scope.device.componentType, value: JSON.stringify($scope.rawData[installs[0]][i])}).then(function(result) {
								l(result);
							});
						}
					});
				}
			});
		});

		//$window.location = url;
	};

	var query = ucserviceurl + 'magnets/install/?name=' + $scope.id;

	$http.get(query).success(function(deviceData){
		l(deviceData[0]);
		$scope.device = deviceData[0];
	});

	detailsService.getDetails($routeParams).then(function(data) {

		$scope.rawData = data;
		l(data);
		$scope.data = data[$routeParams.id];

		for(var first in $scope.data) {
			$scope.properties[first] = {};

			for(var second in $scope.data[first]) {
				$scope.detailsTabs.push({first: first, second: second, index: detailsTabsIndex});
				detailsTabsIndex ++;
				$scope.properties[first][second] = {};

				// Save all axcept the algorithms in an array
				for(var third in $scope.data[first][second]) {

					if(third !== "algorithms" && third !== "measurementData") {
						$scope.properties[first][second][third] = $scope.data[first][second][third];
					}
				}

				// Save all algorithms into an array
				for(var algorithm in $scope.data[first][second].algorithms) {
					var algorithmParts = algorithm.split("2");
					algorithms[algorithm] = $scope.data[first][second].algorithms[algorithm];
					algorithms[algorithmParts[0]] = $scope.data[first][second].algorithms[algorithm];
				}
			}
		}
	});

	$scope.toggleData = function(id, type, key) {
		l($scope.rawData[id]);

		// Init type
		if(!$scope.rawData[id][type]) {
			$scope.rawData[id][type] = {};
		}

		if($scope.rawData[id][type][key] || ($scope.rawData[id][type][key] && $scope.rawData[id][type][key].display && $scope.rawData[id][type][key].display === true)) {

			var modalInstance = $modal.open({
				templateUrl: 'modal/warning.html',
				controller: 'warningCtrl',
				resolve: {
					reason: function() {
						return "Data will be lost. Do you want to continue?";
					}
				}
			});

			modalInstance.result.then(function() {
				delete $scope.rawData[id][type][key];

			}, function() {
				l("cancel");
				l($('input#' + type + '_' + key));
				$('#' + type + '_' + key).prop('checked', true);
			});


		} else if(!$scope.rawData[id][type][key]) {

			$scope.rawData[id][type][key] = {
				display: true,
				description: "",
				defaultEnergy: "",
				algorithms: {}
			};

		} else {
			$scope.rawData[id][type][key].display = true;
		}
	};

	$scope.addAlgorithm = function(type, subtype) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/add_alg.html',
			controller: 'addAlgorithmCtrl',
			resolve: {
				data: function() {
					return $scope.rawData[$scope.id];
				},
				type: function() {
					return type;
				},
				subtype: function() {
					return subtype;
				},
				inventoryId: function() {
					return $scope.device.inventoryId;
				},
				cmpntTypeName: function() {
					return $scope.device.componentType;
				},
				existingAlg: function() {
					return undefined;
				},
				existingAlgId: function() {
					return undefined;
				}
			}
		});
	};

	$scope.editAlgorithm = function(type, subtype, existing, existingId) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/edit_alg.html',
			controller: 'addAlgorithmCtrl',
			resolve: {
				data: function() {
					return $scope.rawData[$scope.id];
				},
				type: function() {
					return type;
				},
				subtype: function() {
					return subtype;
				},
				inventoryId: function() {
					return $scope.device.inventoryId;
				},
				cmpntTypeName: function() {
					return $scope.device.componentType;
				},
				existingAlg: function() {
					return existing;
				},
				existingAlgId: function() {
					return existingId;
				}
			}
		});
	};

	$scope.deleteAlgorithm = function(type, subtype, id) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/delete_alg.html',
			controller: 'deleteAlgorithmCtrl',
			resolve: {
				data: function() {
					return $scope.rawData[$scope.id];
				},
				type: function() {
					return type;
				},
				subtype: function() {
					return subtype;
				},
				algId: function() {
					return id;
				},
				inventoryId: function() {
					return $scope.device.inventoryId;
				},
				cmpntTypeName: function() {
					return $scope.device.componentType;
				}
			}
		});
	};
});

app.controller('showMdCtrl', function($scope, $routeParams, $window){
	$scope.mdType = "inventory_id";

	$scope.manageMeasurementData = function() {
		var deviceId = $scope.device.inventoryId;

		if($scope.mdType === "cmpnt_type_name") {
			deviceId = $scope.device.componentType;
		}

		var newWindowUrl = ucserviceurl + "id/measurement/#/" + $scope.mdType + "/" + deviceId + "/view/readwrite";


		$window.open(newWindowUrl);
	};
});

app.controller('showMtCtrl', function($scope){
});

app.controller('showMtMCtrl', function($scope, $routeParams){
});

app.controller('showMtMcCtrl', function($scope, $routeParams){
});

/*
 * Show conversion results in tabs
 */
app.controller('showResultsCtrl', function($scope, $http, $routeParams, $window, detailsService, $location, $anchorScroll){
	$scope.view = $routeParams.view;
	$scope.subview = $routeParams.subview;
	$scope.plot = {};
	$scope.plot.x_axis = "current";
	$scope.plot.y_axis = "field";
	$scope.plot.direction_plot = "true";
	$scope.data = undefined;
	l("Show results!!!");
	l($routeParams);
	$scope.mdType = "inventory_id";

	if ($routeParams.subview === undefined) {
		l("return");
		return;
	}

	l("did not reutrn");

	$scope.viewMeasurementData = function(mdType) {
		var deviceId = $scope.device.inventoryId;

		if(mdType === "cmpnt_type_name") {
			deviceId = $scope.device.componentType;
		}

		var newWindowUrl = ucserviceurl + "id/measurement/#/" + mdType + "/" + deviceId + "/view/readonly";
		$window.open(newWindowUrl);
	};

	var detailsTabsIndex = 0;
	$scope.scroll.scroll = $routeParams.id;

	var query = ucserviceurl + 'magnets/install/?name=' + $routeParams.id;

	$http.get(query).success(function(deviceData){
		l(deviceData[0]);
		$scope.device = deviceData[0];
	});

	// Get and parse device details
	detailsService.getDetails($routeParams).then(function(data) {
		$scope.data = {};
		$scope.data.detailsTabs = [];
		$scope.data.details = data[$routeParams.id];

		for(var first in $scope.data.details) {

			for(var second in $scope.data.details[first]) {
				$scope.data.detailsTabs.push({first: first, second: second, index: detailsTabsIndex});
				detailsTabsIndex ++;
			}
		}

		// Only try to draw plot if in result subview
		if($scope.subview === "results") {
			drawPlot($scope.data.details[$scope.data.detailsTabs[$routeParams.view].first][$scope.data.detailsTabs[$routeParams.view].second].measurementData, $scope.plot.x_axis, $scope.plot.y_axis, $scope.results.series, $scope);
		}

		$anchorScroll();
	});

	// Clear results table
	$scope.clearTable = function() {
		l("clear");
		$scope.results.convertedResult = [];
	};

	// Redraw plot
	$scope.redraw = function() {
		l("redraw");
		drawPlot($scope.data.details[$scope.data.detailsTabs[$routeParams.view]['first']][$scope.data.detailsTabs[$routeParams.view]['second']].measurementData, $scope.plot.x_axis, $scope.plot.y_axis, $scope.results.series, $scope);
	};

	// Show conversion point on a plot
	$scope.showPoint = function(results) {
		$scope.results.series = [];

		for(var result in results) {

			if(results[result].show !== undefined && results[result].show === true) {
				$scope.results.series.push([results[result].init_value, results[result].conv_value]);
			}
		}

		drawPlot($scope.data.details[$scope.data.detailsTabs[$routeParams.view]['first']][$scope.data.detailsTabs[$routeParams.view]['second']].measurementData, $scope.plot.x_axis, $scope.plot.y_axis, $scope.results.series, $scope);
	};

	// Open new windows with measurement data
	$scope.openNewVindow = function() {
		var newWindowUrl = "measurement_data.html#?"
		+ "type=" + $routeParams.type
		+ "&id=" + $routeParams.id
		+ "&view=" + $scope.data.detailsTabs[$routeParams.view]['first'] + "_" + $scope.data.detailsTabs[$routeParams.view]['second'];

		$window.open(newWindowUrl);
	};
});

/*
 * Add algorithm controller
 */
app.controller('addAlgorithmCtrl', function($scope, $modalInstance, $window, inventoryPropFactory, InventoryProp, inventoryId, cmpntTypeName, data, type, subtype, algorithmId, algorithmType, unitTypes, mdTypes, RotCoilData, HallProbeData, existingAlg, existingAlgId) {
	$scope.upload = {};
	$scope.upload.description = "";
	$scope.alert = {};
	$scope.showSaveButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;

	$scope.algorithmId = algorithmId;
	$scope.algorithmType = algorithmType;
	$scope.unitTypes = unitTypes;

	$scope.mdTypes = mdTypes;

	var rotCoilDataColumns = new RotCoilData().tableColumns;
	var hallProbeDataColumns = new HallProbeData().tableColumns;

	$scope.mdData = {"rot_coil_data": rotCoilDataColumns, "hall_probe_data": hallProbeDataColumns};
	l($scope.mdData);

	$scope.form = {};
	$scope.form.type = type;
	$scope.form.mdType = "rot_coil_data";
	$scope.form.subtype = subtype;

	// Fill in data into form
	if(existingAlg) {
		$scope.form = parseAlgFunction(existingAlg.function);
		$scope.form.id = existingAlgId;
		$scope.form.init_unit = existingAlg.initialUnit;
		$scope.form.dest_unit = existingAlg.resultUnit;
	}

	l($scope.form);

	$scope.rawData = data;

	$scope.error = {};

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.error.exists = false;
		$scope.error.messages = {};
		l($scope.form);

		// Check id
		if(!$scope.form.id) {
			$scope.error.exists = true;
			$scope.error.messages.id = "Id must be set!";
		}

		// Check type
		if(!$scope.form.alg_type) {
			$scope.error.exists = true;
			$scope.error.messages.alg_type = "Type must be set!";
		}

		// Check parameters
		if($scope.form.alg_type === "1") {

			if(!$scope.form.a0 || !$scope.form.a1) {
				$scope.error.exists = true;
				$scope.error.messages.params = "Parameters must be set!";
			}

		} else if ($scope.form.alg_type === "2") {

			if(!$scope.form.a0 || !$scope.form.a1 || !$scope.form.a2) {
				$scope.error.exists = true;
				$scope.error.messages.params = "Parameters must be set!";
			}

		} else if ($scope.form.alg_type === "3") {

			if(!$scope.form.current || !$scope.form.field) {
				$scope.error.exists = true;
				$scope.error.messages.params = "Parameters must be set!";
			}
		}

		// Check initial unit
		if(!$scope.form.init_unit) {
			$scope.error.exists = true;
			$scope.error.messages.init = "Initial unit must be set!";
		}

		// Check destination unit
		if(!$scope.form.dest_unit) {
			$scope.error.exists = true;
			$scope.error.messages.dest = "Destination unit must be set!";
		}

		// If no error, continue
		if(!$scope.error.exists) {

			var functionString = "";

			// 1. order
			if($scope.form.alg_type === "1") {
				functionString = $scope.form.a1 + "*input" + returnSign($scope.form.a0) + $scope.form.a0;

			// 2. order
			} else if($scope.form.alg_type === "2") {
				functionString = $scope.form.a2 + "*input^2" + returnSign($scope.form.a1) + $scope.form.a1 + "*input" + returnSign($scope.form.a0) + $scope.form.a0;

			// md
			} else if($scope.form.alg_type === "3") {
				functionString = $scope.form.current + ", " + $scope.form.field;
			}

			// Push data into json
			$scope.rawData[type][subtype]['algorithms'][$scope.form.id] = {
				algorithmId: 0,
				auxInfo: 0,
				function: functionString,
				initialUnit: $scope.form.init_unit,
				resultUnit: $scope.form.dest_unit
			};

			$scope.alert.show = false;

			var promise = inventoryPropFactory.updateItem({inventory_id: inventoryId, inventory_property_template_name: type, cmpnt_type_name: cmpntTypeName, value: encodeURIComponent(JSON.stringify($scope.rawData[type]))});

			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Algorithm successfully added!";
				$scope.showSaveButton = false;
				$scope.showCancelButton = false;
				$scope.showFinishButton = true;

			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});

		} else {
			l($scope.error);
		}
	};

	$scope.cancel = function() {
		$modalInstance.dismiss('cancel');
	};

	$scope.finish = function() {
		//$window.location.reload();
		$modalInstance.dismiss('cancel');
	};
});

/*
 * Delete algorithm controller
 */
app.controller('deleteAlgorithmCtrl', function($scope, $modalInstance, $window, inventoryPropFactory, InventoryProp, inventoryId, cmpntTypeName, data, type, subtype, algId, algorithmId, algorithmType, unitTypes, mdTypes, RotCoilData, HallProbeData) {
	$scope.upload = {};
	$scope.upload.description = "";
	$scope.alert = {};
	$scope.showSaveButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;
	$scope.rawData = data;

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		// Delete data from json
		delete $scope.rawData[type][subtype]['algorithms'][algId];

		var promise = inventoryPropFactory.updateItem({inventory_id: inventoryId, inventory_property_template_name: type, cmpnt_type_name: cmpntTypeName, value: JSON.stringify($scope.rawData[type])});

		promise.then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Algorithm successfully deleted!";
			$scope.showSaveButton = false;
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
		//$window.location.reload();
		$modalInstance.dismiss('cancel');
	};
});

/*
 * Warning controller
 */
app.controller('warningCtrl', function($scope, $modalInstance, reason) {
	$scope.alert = {};
	$scope.showSaveButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;
	$scope.alert.body = reason;

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$modalInstance.close();
	};

	$scope.cancel = function() {
		$modalInstance.dismiss('cancel');
	};
});