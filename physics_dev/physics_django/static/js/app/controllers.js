app.controller('mainCtrl', function($scope, $http, systemService, $routeParams){

});

app.controller('searchFormCtrl', function($scope, systemService){
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
		window.location = "#/system=" + search.system + '&name=' + search.name;
		//searchForLogs(search.system, true);
	};

	// Watch for search type change
	$scope.$watch('search.type', function(newValue, oldValue){
		l(newValue);

		if(newValue === "installation") {
			$scope.search.displayName = "display_search_filter";
			$scope.search.displaySystem = "display_search_filter";

		} else {
			$scope.search.displayName = "hide_display_filter";
			$scope.search.displaySystem = "hide_display_filter";
		}
	});
});

/**
 * List systems in the left pane
 */
app.controller('listDevicesCtrl', function($scope, systemService, $routeParams, $http) {
	l("search controller");

	l($routeParams);
	$scope.devices = [];

	$http.get(serviceurl + 'magnets/devices/?system=' + $routeParams.systemName).success(function(data){

		$.each(data, function(i, item){

			// Build customized Log object
			var newItem = {
				name: item.name,
				serialNumber: item.serialNumber,
				typeDescription: item.typeDescription,
			};

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
		l(device);
		device.click = "device_click";
		//$scope.devices[1].click = "device_click";
		window.location = "#/query/id=3";
	};
});

/**
 * List devices in the middle pane
 */
app.controller('showDetailsCtrl', function($scope, $routeParams, $http, systemService){
	l("details controller");
	$('#load_details').show("fast");
	$scope.data = "bla";
});