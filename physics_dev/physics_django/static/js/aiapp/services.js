/*
 * Services for modules
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created: Mar 7, 2014
 */

app.factory('statusFactory', function($http, $q){
	var factory = {};
	factory.update = ["status", "new_status", "modified_by", "definition"];

	// Return statuses
	factory.retrieveStatuses = function() {
		var query = serviceurl + "/statuses/";

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.get(query).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	factory.updateStatus = function(params) {
		var query = serviceurl + "/updatestatus/";
		
		var payload = prepareUrlParameters(factory.update, params);
		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, payload).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	return factory;
})

/*
 * Provide header factory. Active interlock header can be retrieved and saved.
 */
app.factory('headerFactory', function($http, $q){
	var factory = {};

	factory.saveHeader = function(description) {
		var query = serviceurl + "/saveactiveinterlockheader/";

		var params = "description=" + description + "&created_by=admin";
		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	factory.retrieveHeader = function(){
		var query = serviceurl + "/activeinterlockheader/?status=" + aiStatusMap['history'];

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.get(query).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	return factory;
});

/*
 * Provide bending magnet factory. Banging magnet data can be retrieved and saved.
 */
app.factory('bmFactory', function($http, $q, BendingMagnet){
	var factory = {};
	factory.bm = new BendingMagnet();

	// Set item
	factory.setItem = function(item) {
		factory.bm.set(item);
	}

	// Check if all mandatory parameters are set
	factory.checkItem = function(item) {
		var errors = {};

		$.each(item.save_m, function(i, property) {

			if(item[property] === undefined || item[property] === "") {
				errors[property] = '*';
			}
		});

		return errors;
	}

	// Return all items
	factory.retrieveItems = function(params) {
		var query = serviceurl + "/device/?";
		params['definition'] = 'bm';
		query += prepareUrlParameters(factory.bm.retrieve, params, factory.bm.retrieve_m);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.get(query).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	// Save item
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		var query = serviceurl + "/savedevice/";
		factory.bm.definition = "bm";

		l(factory.bm);

		var params = prepareUrlParameters(factory.bm.save, factory.bm);
		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	// Update item
	factory.updateItem = function(params) {

		var query = serviceurl + "/updateprop/";

		var params = prepareUrlParameters(factory.bm.update, params);
		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	// Update device
	factory.updateDevice = function(params) {
		l(params);

		var query = serviceurl + "/updatedevice/";

		var params = prepareUrlParameters(factory.bm.update_device, params);
		l(params);
		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	// Approve item
	factory.approveItem = function(params) {
		var query = serviceurl + "/approve/";

		var params = prepareUrlParameters(factory.bm.approve, params);
		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	return factory;
});

/*
 * Provide logic factory. Logic can be retrieved and saved.
 */
app.factory('logicFactory', function($http, $q, Logic){
	var factory = {};
	factory.logic = new Logic();

	// Set item
	factory.setItem = function(item) {
		factory.logic.set(item);
	}

	// Check if all mandatory parameters are set
	factory.checkItem = function(item) {
		var errors = {};

		$.each(item.save_m, function(i, property) {

			if(item[property] === undefined || item[property] === "") {
				errors[property] = '*';
			}
		});

		return errors;
	}

	// Return all items
	factory.retrieveItems = function(params) {
		var query = serviceurl + "/logic/?";
		query += prepareUrlParameters(factory.logic.retrieve, params, factory.logic.retrieve_m);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.get(query).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	// Save item
	factory.saveItem = function(item) {

		if(item !== undefined) {
			this.setItem(item);
		}

		var query = serviceurl + "/savelogic/";

		var params = prepareUrlParameters(factory.logic.save, factory.logic);
		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	return factory;
});