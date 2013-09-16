
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
	l("main controller");

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
	l("search controller " + $routeParams.id);
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
app.controller('showDetailsCtrl', function($scope, $routeParams, $http){
	l("details controller");
	$scope.id = $routeParams.id;
	$scope.show = true;
	$scope.data = {};
	$scope.view = $routeParams.view;

	$scope.error = {};

	var query = serviceurl + 'magnets/conversion/?id=' + $routeParams.id;
	l(query);

	$http.get(query).success(function(data){
		showDetails(data, $routeParams.id);
		//var repairedData = removeColumnsFromObjects(data[$routeParams.id]);
		$scope.data = data[$routeParams.id];
	});

	$scope.result = "";

	$scope.convert = function() {
		var conversionQuery = serviceurl + 'magnets/conversion/?id=' + $routeParams.id + '&from=' + $scope.source_unit + '&to=' + $scope.destination_unit + '&value=' + $scope.initial_value;
		l(conversionQuery);

		$http.get(conversionQuery).success(function(data){
			$scope.result = data[$routeParams.id];
			l($scope.result);
			$scope.error.display = false;

		}).error(function(){
			$scope.error.display = true;
		});
	};
});