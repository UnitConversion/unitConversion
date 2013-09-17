/*
 * Controllers for conversion module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/*
 * Main controller when we load the main page
 */
app.controller('mainCtrl', function($scope, $http, systemService, $routeParams){
	$scope.version = version;
});

/*
 * Controller for the left/search pane
 */
app.controller('searchFormCtrl', function($scope, systemService, $window){
	$scope.search = {};
	$scope.systems = [];
	$scope.search.displayName = "display_search_filter";
	$scope.search.displaySystem = "display_search_filter";
	$scope.search.type = "installation";

	// Load Systems
	systemService.transform(function(data){
		$scope.systems = data.systems;
	});

	// Search button click
	$scope.searchForDevices = function(search) {
		$window.location = createDeviceListQuery(search, true) + "/list";
	};

	// Watch for search type change
	$scope.$watch('search.type', function(newValue, oldValue){

		if(newValue === "installation") {
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
	$scope.id = $routeParams.id;

	$scope.devices = [];
	var previousDevice = undefined;

	var query = serviceurl + 'magnets/devices/?' + createDeviceListQuery($routeParams, false);
	l(query);

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
		$window.location = createDeviceListQuery($routeParams, true) + "/id/" + device.serialNumber;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showDetailsCtrl', function($scope, $routeParams, $http, $window){
	$scope.id = $routeParams.id;
	$scope.show = true;
	$scope.data = {};
	$scope.view = $routeParams.view;
	$scope.result = {};
	$scope.tabs = [];

	$scope.error = {};
	$scope.error.message = "";

	var algorithms = {};
	$scope.convertedResult = {};

	// Retrieve the details
	var query = serviceurl + 'magnets/conversion/?id=' + $routeParams.id;
	//l(query);

	$http.get(query).success(function(data){
		showDetails(data, $routeParams.id);
		$scope.data = data[$routeParams.id];

		for(var first in $scope.data) {
			for(var second in $scope.data[first]) {
				for(var algorithm in $scope.data[first][second].algorithms)
				algorithms[algorithm] = $scope.data[first][second].algorithms[algorithm];
			}
		}

		l(algorithms);
	});

	/*
	 * When user clicks on convert button, fire this function
	 */
	$scope.convert = function() {
		$scope.tabs = [];

		var conversionQuery = serviceurl + 'magnets/conversion/?id=' + $routeParams.id + '&from=' + $scope.source_unit + '&to=' + $scope.destination_unit + '&value=' + $scope.initial_value;
		l(conversionQuery);

		$http.get(conversionQuery).success(function(data){
			var details = data[$routeParams.id];
			$scope.result = details;
			$scope.error.display = false;

			// Go through returned data and save needed values
			for(var first in details) {

				for(var second in details[first]){
					$scope.tabs.push({first: first, second: second});
					var key = first + "_" + second;

					if(details[first][second].conversionResult.value === null && details[first][second].conversionResult.unit === "") {
						$scope.error.message = details[first][second].conversionResult.message;
						$scope.error.display = true;
						return;
					}

					// Create array of result objects
					if(!(key in $scope.convertedResult)) {
						$scope.convertedResult[key] = [];
					}

					// Get the initial unit from algorithms data
					var initialUnit = "";
					var algKey = $scope.source_unit + '2' + $scope.destination_unit;
					var algKeyRev = $scope.destination_unit + '2' + $scope.source_unit;

					if(algKey in algorithms) {
						initialUnit = algorithms[algKey].initialUnit;

					} else if(!(algKeyRev in algorithms)) {
						initialUnit = algorithms[algKey].resultUnit;
					}

					$scope.convertedResult[key].push({init_value: $scope.initial_value, init_unit: initialUnit, conv_value: details[first][second].conversionResult.value, conv_unit: details[first][second].conversionResult.unit});
				}
			}

			var urlPart = $scope.tabs[0].first + '_' + $scope.tabs[0].second;

			$window.location = createDeviceListQuery($routeParams, true) + "/id/" + $routeParams.id + '/' + urlPart;

		}).error(function(){
			$scope.error.display = true;
		});
	};
});

/*
 * Show conversion results in tabs
 */
app.controller('showResultsCtrl', function($scope, $routeParams){
	$scope.view = $routeParams.view;
	$scope.url = createDeviceListQuery($routeParams, true) + "/id/" + $routeParams.id + '/';
});

app.controller('modalCtrl', function($scope, $modalInstance) {
	$scope.ok = function() {
		$modalInstance.close();
	};

	$scope.cancel = function () {
		$modalInstance.dismiss('cancel');
	};
});