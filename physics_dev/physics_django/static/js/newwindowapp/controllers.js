/*
 * Controllers for new window module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */


measurementDataApp.controller('measurementDataCtrl', function($scope, $location, $http) {
	$scope.data = {};
	$scope.convertedData = [];
	var parameters = $location.search();
	var view = parameters.view.split("_");

	var idParameter = "id";

	if(parameters.type === "install") {
		idParameter = "name";
	}

	var query = serviceurl + 'magnets/conversion/?' + idParameter + '=' + parameters.id;

	l(query);

	$http.get(query).success(function(data){
		//showDetails(data, $routeParams.id);
		$scope.data = data[parameters.id][view[0]][view[1]]['measurementData'];
		l($scope.data);
		var length = 1;

		if($scope.data.current !== undefined) {
			length = $scope.data.current.length;
		}

		for(var i=0; i<length; i++) {
			var rowObject = {};

			for(var key in $scope.data) {
				var column = key;
				var row = $scope.data[key];


				if($.type(row) === 'array') {
					rowObject[key] = row[i];

				} else {

					if(i === 0) {
						rowObject[key] = row;

					} else {
						rowObject[key] = "";
					}
				}
			}

			$scope.convertedData.push(rowObject);
		}
	});
});