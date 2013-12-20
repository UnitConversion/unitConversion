/*
 * Services for modules
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/*
 * Provide model code info to controllers
 */
app.factory('modelCodeInfoService', function($resource){

	return $resource(serviceurl + 'lattice/?function=retrieveModelCodeInfo&name=*&algorithm=*', {}, {
		transform: {
			method:'GET',
			isArray:false,
			transformResponse: function(response) {
				var returnData = {};
				returnData.data = JSON.parse(response);
				return returnData;
			}
		}
	});
});