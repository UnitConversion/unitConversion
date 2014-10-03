/*
 * Services for conversion module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/*
 * Provide systems to controllers
 */
app.factory('systemService', function($resource){

	return $resource(ucserviceurl + 'magnets/system/', {}, {
		transform: {
			method:'GET',
			isArray:false,
			transformResponse: function(response) {
				var systemsObject = {};
				systemsObject.systems = JSON.parse(response);
				return systemsObject;
			}
		}
	});
});

/*
 * Provide device's details to controllers
 */
app.factory('detailsService', function($q, $http) {

	var getDetails = function(params) {
		var deferred = $q.defer();

		// Create query string
		var query = ucserviceurl + 'magnets/conversion/?id=' + params.id;

		if(params.type === "install") {
			query = ucserviceurl + 'magnets/conversion/?name=' + params.id;
		}

		$http.get(query).success(function(data){
			deferred.resolve(data);
		});

		return deferred.promise;
	};

	return {
		getDetails: getDetails
	};
});