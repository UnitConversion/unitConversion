/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 * List systems in the left pane
 */
app.controller('systemsListCtrl', function($scope, $routeParams, $http, systemService) {
	l("system controller");
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
		window.location = "#/system=" + search.system;
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
 * List devices in the middle pane
 */
app.controller('devicesListCtrl', function($scope, $routeParams, $http, systemService){
	l("devices controller");
	$scope.devices = [];
	$scope.systems = [];

	// Load Systems
	systemService.transform(function(data){
		$scope.systems = data.systems;
	});

	l($routeParams);

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
});