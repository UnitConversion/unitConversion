/**
 * Provide systems to controllers
 */
app.factory('systemService', function($resource){

	return $resource(serviceurl + 'magnets/system/', {}, {
		transform: {
			method:'GET',
			isArray:false,
			transformResponse: function(response) {
				l(response);

				var systemsObject = {};
				systemsObject.systems = JSON.parse(response);
				return systemsObject;
			}
		}
	});
});