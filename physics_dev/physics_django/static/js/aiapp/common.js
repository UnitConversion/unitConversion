/*
 * Helper functions for active interlock client
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created: Mar 6, 2014
 */

/**
 * Write logs to Chrome or Firefox console
 * @param input input string
 */
function l(input) {

	if(writeLogs === true) {
		console.log(input);
	}
}

/**
 * Prepare url post parameter. This function us used to avoid problems when using $http.post function.
 * @param dictOfValues dictionary of key and value of parameters
 */
function prepareUrlParameters(listOfKeys, dictOfValues, listOfMandatoryKeys) {
	var params = [];

	$.each(listOfKeys, function(i, key) {

		if(key in dictOfValues) {
			params.push(key + "=" + dictOfValues[key]);
		
		} else if(listOfMandatoryKeys && listOfMandatoryKeys.indexOf(key) >= 0) {
			params.push(key + "=*");
		}
	});
	
	return params.join("&");
}