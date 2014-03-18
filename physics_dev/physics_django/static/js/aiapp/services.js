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
		var query = serviceurl + "/ai/statuses/";

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
		var query = serviceurl + "/ai/updatestatus/";
		
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
		var query = serviceurl + "/ai/saveactiveinterlockheader/";

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
		var query = serviceurl + "/ai/activeinterlockheader/?status=" + aiStatusMap['history'];

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
		var query = serviceurl + "/ai/device/?";
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

		var query = serviceurl + "/ai/savedevice/";
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

		var query = serviceurl + "/ai/updateprop/";

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

		var query = serviceurl + "/ai/updatedevice/";

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
		var query = serviceurl + "/ai/approve/";

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
 * Provide insertion device factory. Insertion device data can be retrieved and saved.
 */
app.factory('idFactory', function($http, $q, InsertionDevice){
	var factory = {};
	factory.id = new InsertionDevice();

	// Set item
	factory.setItem = function(item) {
		factory.id.set(item);
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
		var query = serviceurl + "/ai/device/?";
		params['definition'] = 'id';
		query += prepareUrlParameters(factory.id.retrieve, params, factory.id.retrieve_m);

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

		var query = serviceurl + "/ai/savedevice/";
		factory.id.definition = "id";

		l(factory.id);

		var params = prepareUrlParameters(factory.id.save, factory.id);
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

		var query = serviceurl + "/ai/updateprop/";

		var params = prepareUrlParameters(factory.id.update, params);
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

		var query = serviceurl + "/ai/updatedevice/";

		var params = prepareUrlParameters(factory.id.update_device, params);
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
		var query = serviceurl + "/ai/approve/";

		var params = prepareUrlParameters(factory.id.approve, params);
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

app.factory('authFactory', function($http, $q) {
	var factory = {};

	factory.login = function(username, password) {
		var query = serviceurl + "/user/login/";

		var params = 'username=' + username + '&password=' + password;
		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	factory.logout = function(username, password) {
		var query = serviceurl + "/user/logout/";

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query).success(function(data){
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
		var query = serviceurl + "/ai/logic/?";
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

		var query = serviceurl + "/ai/savelogic/";

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

	// Update item
	factory.updateItem = function(params) {

		var query = serviceurl + "/ai/updatelogic/";
		l(params);

		var params = prepareUrlParameters(factory.logic.update, params);
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