/*
 * Services for conversion module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/*
 * Provide systems to controllers
 */
app.factory('systemService', function($resource){

	return $resource(serviceurl + 'magnets/system/', {}, {
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