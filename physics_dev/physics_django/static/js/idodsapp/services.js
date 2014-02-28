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

/*
 * Provide a factory for the vendor entity. Vendor can be checked, retrieved, saved and updated
 */
app.factory('vendorFactory', function($http, $q, Vendor, EntityError) {
	var factory = {};
	factory.eVendor = new Vendor();
	factory.error = new EntityError();

	// Set vendor object
	factory.setVendor = function(vendor) {
		this.eVendor.set(vendor);
	}

	// Check vendor before sending it to the server
	factory.checkVendor = function(vendor) {

		if(vendor !== undefined) {
			this.setVendor(vendor);
		}

		this.error.reset();

		l(this.eVendor.m);

		$.each(this.eVendor.m, function(i, property) {

			if(factory.eVendor[property] === undefined || factory.eVendor[property] === "") {
				factory.error.add(property, property + " is mandatory!");
			}
		});

		if(this.error.num === 0) {
			return true;
		
		} else {
			return this.error;
		}
	}

	// Get vendor from server
	factory.retrieveVendor = function(vendor) {
		var query = serviceurl + "/vendor/?";

		if(vendor !== undefined) {
			this.setVendor(vendor);
		}

		query += prepareUrlParameters(this.eVendor.list, this.eVendor);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.get(query).success(function(data){
			deffered.resolve(new Vendor(data[factory.eVendor.id]));
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	// Get vendors from server
	factory.retrieveVendors = function(params) {
		var query = serviceurl + "/vendor/?";
		l(this.eVendor);
		l(this.eVendor.m);

		query += prepareUrlParameters(this.eVendor.list, params, this.eVendor.m);
		l(query);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.get(query).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	// Save new vendor
	factory.saveVendor = function(vendor) {
		var query = serviceurl + "/savevendor/";

		if(vendor !== undefined) {
			this.setVendor(vendor);
		}

		var params = prepareUrlParameters(this.eVendor.save, this.eVendor);

		var deffered = $q.defer();
		var promise = deffered.promise;

		$http.post(query, params).success(function(data){
			deffered.resolve(data);
		
		}).error(function(data, status, headers, config) {
			deffered.reject(data);
		});

		return promise;
	}

	// Update a vendor
	factory.updateVendor = function(vendor) {
		var query = serviceurl + "/updatevendor/";

		if(vendor !== undefined) {
			this.setVendor(vendor);
		}

		var params = prepareUrlParameters(this.eVendor.update, this.eVendor);

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