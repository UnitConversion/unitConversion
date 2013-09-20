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
	$scope.style = {};
	$scope.style.middle_class = "container-scroll-middle";
	$scope.style.right_class = "container-scroll-last-one";
});

/*
 * Controller for the left/search pane
 */
app.controller('searchFormCtrl', function($scope, systemService, $window){
	$scope.search = {};
	$scope.systems = [];
	$scope.search.displayName = "display_search_filter";
	$scope.search.displaySystem = "display_search_filter";
	$scope.search.type = "install";

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
	var previousDevice = undefined;

	var query = serviceurl + 'magnets/' + createDeviceListQuery($routeParams, false);
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

		var id = device.inventoryId;

		if($routeParams.type === "install") {
			id = device.name;
		}

		$window.location = createDeviceListQuery($routeParams, true) + "/id/" + id + "/0/results";
	};
});

/*
 * Show details in the right pane
 */
app.controller('showDetailsCtrl', function($scope, $routeParams, $http, $window){
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
	$scope.view = $routeParams.view;

	$scope.error = {};
	$scope.error.message = "";

	var algorithms = {};
	$scope.convertedResult = [];

	// Retrieve the details
	var query = serviceurl + 'magnets/conversion/?id=' + $routeParams.id;

	if($routeParams.type === "install") {
		query = serviceurl + 'magnets/conversion/?name=' + $routeParams.id;
	}

	l(query);

	$http.get(query).success(function(data){
		//showDetails(data, $routeParams.id);
		$scope.data = data[$routeParams.id];

		for(var first in $scope.data) {
			for(var second in $scope.data[first]) {
				$scope.detailsTabs.push({first: first, second: second, index: detailsTabsIndex});
				detailsTabsIndex ++;

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

		var idParameter = "id";

		if($routeParams.type === "install") {
			idParameter = "name";
		}

		var conversionQuery = serviceurl
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
				var algKeyRev = $scope.destination_unit + '2' + $scope.source_unit;

				if(algKey in algorithms) {
					initialUnit = algorithms[algKey].initialUnit;

				} else if(!(algKeyRev in algorithms)) {
					initialUnit = algorithms[algKey].resultUnit;
				}

				$scope.convertedResult.push({
					init_value: $scope.initial_value,
					init_unit: initialUnit,
					conv_value: results.conversionResult.value,
					conv_unit: results.conversionResult.unit
				});
			}

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
	$scope.subview = $routeParams.subview;

	if($scope.subview === "plot"){

//		$scope.$watch('data', function(newData, oldData){
//			showDetails(newData[$scope.detailsTabs[$routeParams.view]['first']][$scope.detailsTabs[$routeParams.view]['second']].measurementData);
//		});
	}
});

app.controller('modalCtrl', function($scope, $modalInstance) {
	$scope.ok = function() {
		$modalInstance.close();
	};

	$scope.cancel = function () {
		$modalInstance.dismiss('cancel');
	};
});