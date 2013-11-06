/*
 * Controllers for lattice module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

app.controller('indexCtrl', function($scope, $location, $anchorScroll) {

	$scope.top = function() {
		//l($location.hash());
		var id = $location.hash();

		// If no Log entry is selected, go to the top
		if(id === "" || id === "top") {
			$location.hash("top");
			$anchorScroll();

		// Scroll to the device
		} else {
			$location.hash("");
			var element = $('input[value=' + id + ']');
			//l(element.offset().top);

			$('html, body').animate({
				scrollTop: element.parent().offset().top
			}, 100);
		}
	};
});

/*
 * Main controller when we load the main page
 */
app.controller('mainCtrl', function($scope){
	$scope.version = version;
	$scope.style = {};
	$scope.style.middle_class = "container-scroll-middle";
	$scope.style.right_class = "container-scroll-last-one";
	$scope.statuses = statuses;
	$scope.modelStatuses = modelStatuses;
});

/*
 * Controller for the left/search pane
 */
app.controller('searchFormCtrl', function($scope, systemService, $window, $routeParams){
	$scope.search = {};
	$scope.systems = [];
	$scope.search.displayLattice = "display_block";
	$scope.search.displayModel = "display_none";
	$scope.search.type = "lattice";
	$scope.search.selected = "-";

	// Set search type
	if($routeParams.type !== undefined) {
		$scope.search.type = $routeParams.type;
	}

	// Lattice search button click
	$scope.searchForLattice = function(search) {
		search.search = new Date().getTime();
		var newLocation = createLatticeListQuery(search, true) + "/list";
		//l(newLocation);
		$window.location = newLocation;
	};

	// Model search button click
	$scope.searchForModel = function(search) {
		var newLocation = createModelListQuery(search, true) + "/list";
		//l(newLocation);
		$window.location = newLocation;
	};

	// Watch for search type change
	$scope.$watch('search.type', function(newValue, oldValue){

		if(newValue === "lattice") {
			$scope.search.displayLattice = "display_block";
			$scope.search.displayModel = "display_none";

		} else {
			$scope.search.displayLattice = "display_none";
			$scope.search.displayModel = "display_block";
		}
	});
});

/*
 * List lattice in the middle pane
 */
app.controller('listLatticeCtrl', function($scope, $routeParams, $http, $window) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;
	$scope.comparison = {};
	$scope.comparison.data = {};
	$scope.comparison.length = 0;
	$scope.comparison.show = 'false';

	$scope.lattices = [];
	var previousLattice = undefined;
	var query = "";

	$scope.setCompareData = function() {
		//comparison[latticeData.name + '|||' + latticeData.branch + '|||' + latticeData.version] = "compare";
		//l("comparison list");
		//l($scope.comparison);

		$scope.comparison.length = Object.keys($scope.comparison.data).length;
	};

	// Click on compare lattice button
	$scope.compareLattice = function() {
		var lattices = [];

		$.each($scope.comparison.data, function(i, lattice){

			if(lattice === true) {
				lattices.push(i);
			}
		});

		var location = createLatticeListQuery($routeParams, true) + "/ids/" + lattices.join(",");
		//l(location);

		$window.location = location;
	};

	$scope.clearSelection = function() {

		$.each($scope.comparison.data, function(i, lattice){
			$scope.comparison.data[i] = false;
		});

		$scope.comparison.length = 0;
	};

	query = serviceurl + 'lattice/?function=retrieveLatticeInfo&' + createLatticeListQuery($routeParams, false);
	//l(query);

	$http.get(query).success(function(data){

		$.each(data, function(i, item){

			// Build customized Log object
			var newItem = item;

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.lattices.push(newItem);
		});
	});

	// Show details when user selects the lattice from a list
	$scope.showDetails = function(lattice){
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousLattice !== undefined) {
			previousLattice.click = "";
		}

		previousLattice = lattice;
		lattice.click = "lattice_click";
		lattice.search = $routeParams.search;
		lattice.type = $routeParams.type;
		$routeParams.click = "lattice_click";

		var location = createLatticeListQuery($routeParams, true) + "/id/" + lattice.name + '|||' + lattice.branch + '|||' + lattice.version;
		//l(location);

		$window.location = location;
	};
});

/*
 * List models in the middle pane
 */
app.controller('listModelCtrl', function($scope, $routeParams, $http, $window) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;

	$scope.models = [];
	var previousModel = undefined;
	var query = "";

	query = serviceurl + 'lattice/?function=retrieveModel&' + createModelListQuery($routeParams, false);
	//l(query);


	$http.get(query).success(function(data){
		var index = 0;

		$.each(data, function(i, item){

			// Build customized Log object
			var newItem = item;
			newItem.name = i;

			// Alternate background colors
			if(index%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.models.push(newItem);

			index ++;
		});

		//l($scope.models);
	});

	// Show details when user selects the model from a list
	$scope.showDetails = function(model){
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousModel !== undefined) {
			previousModel.click = "";
		}

		previousModel = model;
		model.click = "lattice_click";
		model.search = $routeParams.search;
		model.type = $routeParams.type;

		var location = createModelListQuery(model, true) + "/id/" + model.id;
		//l(location);

		$window.location = location;
	};
});

/*
 * Show lattice details in the right pane
 */
app.controller('showLatticeDetailsCtrl', function($scope, $routeParams, $http, $location, $sce, $q){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.raw = {};
	$scope.raw.data = [];
	$scope.raw.show = true;
	$scope.latticeModels = [];
	$scope.compare = {};
	$scope.compare.show = false;
	$scope.raw.id = $routeParams.id;

	var query = "";

	var params = $routeParams.id.split('|||');
	var paramsObject = {};
	paramsObject.type = $routeParams.type;
	paramsObject.name = params[0];
	paramsObject.branch = params[1];
	paramsObject.version = params[2];
	l(params);

	// Show lattice model list
	query = serviceurl + 'lattice/?function=retrieveModelList&latticename=' + paramsObject.name + '&latticeversion=' + paramsObject.version + '&latticebranch=' + paramsObject.branch;
	//l(query);

	$http.get(query).success(function(data){
		l("got modeules");

		$.each(data, function(name, model){
			model.name = name;

			var route = {};
			route.name = name;
			route.id = model.id;
			route.type = "model";

			$.each(model, function(i, cell){
				model[i] = $sce.trustAsHtml(model[i].toString());
			});

			var location = createModelListQuery(route, true) + "/details";
			model.link = $sce.trustAsHtml('<a href="' + location + '">link to model</a>');
			$scope.latticeModels.push(model);
		});

		l($scope.latticeModels);
	});

	// Show raw lattice in a table
	query = serviceurl + 'lattice/?function=retrieveLattice&withdata=true&' + createLatticeListQuery(paramsObject, false);
	//l(query);

	var table = "";

	$http.get(query).success(function(data){

		$.each(data, function(i, datum){
			$scope.lattice = datum;
			l($scope.lattice);

			var lattice = datum.lattice;
			var header = [];

			header.push("id");
			header.push("name");
			header.push("type");
			header.push("length");
			header.push("position");

			// Get the rest of the columns
			if(lattice.columns !== undefined) {

				$.each(lattice.columns, function(i, column){
					header.push(column);
				});
			}

			$scope.raw.data.push({head: header});

			table = createLatticeTable(header, lattice);
		});

		$('#lattice_table').html(table);

		$scope.raw.show = false;
	});

	$scope.downloadFile = function() {

	};
});

/*
 * Show lattice compare view in the right pane
 */
app.controller('showLatticesDetailsCtrl', function($scope, $routeParams, $http, $location, $q, $anchorScroll){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.raw = {};
	$scope.raw.show = true;
	$scope.compare = {};
	$scope.compare.show = true;
	$scope.raw.id = $routeParams.ids;

	l($location.path());

	var query = "";
	var latticesData = {};
	$scope.raw.lattices = latticesData;
	$scope.raw.deviceName = "";
	var latticesKeys = [];

	// If comparing data
	var ids = $scope.raw.id.split(',');

	if(ids.length > 2) {
		$scope.compare.message = "Comparison of more than two lattices is not allowed!";

	} else {
		var gets = [];

		$.each(ids, function(i, id){

			var params = id.split('|||');
			var paramsObject = {};
			paramsObject.type = $routeParams.type;
			paramsObject.name = params[0];
			paramsObject.branch = params[1];
			paramsObject.version = params[2];
			//l(params);

			query = serviceurl + 'lattice/?function=retrieveLattice&withdata=true&' + createLatticeListQuery(paramsObject, false);

			gets.push($http.get(query));
		});

		// Return all results
		$q.all(gets).then(function(results) {

			if(!checkLatticeFormat(results)) {
				$scope.compare.message = "Selected lattices doens't have same formats. Comparison cannot continue.";

			} else {
				l(results);

				$.each(results, function(i, result){
					var latticeData = {};
					var keys = Object.keys(result.data);

					var header = [];

					header.push("id");
					header.push("name");
					header.push("type");
					header.push("length");
					header.push("position");

					// Get the rest of the columns
					if(result.data[keys[0]].lattice.columns !== undefined) {

						$.each(result.data[keys[0]].lattice.columns, function(i, column){
							header.push(column);
						});
					}

					$.each(result.data[keys[0]].lattice, function(j, line){
						var key = line["name"];

						var valueObject = {};

						$.each(header, function(k, headerEl){
							valueObject[headerEl] = line[headerEl];
						});

						latticeData[key] = valueObject;
					});

					// Add compared property
					latticeData['compared'] = false;

					latticesData[result.data[keys[0]].name] = {keys:header, data:latticeData};
				});

				// List devices
				latticesKeys = Object.keys(latticesData);
				var html = "<tr><th>Device names</th>";

				$.each(latticesKeys, function(i, key){
					html += "<th>" + key + "</th>";
				});

				html += "<th>Diff</th>";

				html += "</tr>";

				html += createLatticeComparinsonRows(latticesData, latticesKeys[0]);

				html += createLatticeComparinsonRows(latticesData, latticesKeys[1]);

//				$.each(latticesData[latticesKeys[0]].data, function(i, latticeLine) {
//					var deviceKeys = [];
//					var deviceName = latticeLine.name;
//
//					if(deviceName === undefined) {
//						return;
//					}
//
//					html += "<tr><td class='lattice_table2_row'>" + i + "</td>";
//
//					$.each(latticesData, function(j, lattice) {
//
//						var keys = [];
//
//						$.each(lattice.keys, function(j, header) {
//
//							if(header === "name" || header === "id") {
//								return;
//							}
//
//							if(lattice.data[deviceName] !== undefined) {
//								lattice.data[deviceName]['compared'] = true;
//
//								if(lattice.data[deviceName][header] === undefined) {
//									keys.push(header + "=");
//
//								} else {
//									keys.push(header + "=" + lattice.data[deviceName][header]);
//								}
//							}
//						});
//
//						deviceKeys.push(keys);
//
//						html += "<td>" + keys.join(", ") + "</td>";
//					});
//
//					var cssClass = checkDiff(deviceKeys);
//
//					html += "<td ng-click='diffDetails(\"" + deviceName + "\")' class='diff_details " + cssClass + "'><i class='icon-search'></i></td>";
//
//					html += "</tr>";
//
//				});

				$scope.raw.table = html;
			}
		});
	}

	$scope.diffDetails = function(device) {
		$scope.raw.deviceName = device;
		$location.hash("details");
		$anchorScroll();
		l(latticesKeys);
		l(latticesData);

		var firstLatticeProperties = latticesData[latticesKeys[0]].keys;
		var firstLatticeDeviceData = latticesData[latticesKeys[0]].data[device];
		var secondLatticeDeviceData = latticesData[latticesKeys[1]].data[device];
		var detailsData = [];
		l(secondLatticeDeviceData);

		// Go through properties from the first lattice
		if(firstLatticeDeviceData !== undefined) {

			$.each(firstLatticeProperties, function(i, property) {
				var firstLatticeDeviceDataValue = firstLatticeDeviceData[property];
				var secondLatticeDeviceDataValue = "";

				if(secondLatticeDeviceData !== undefined && secondLatticeDeviceData[property] !== undefined) {
					secondLatticeDeviceDataValue = secondLatticeDeviceData[property];
				}

				var detailsDataEntry = {};
				detailsDataEntry["property"] = property;
				detailsDataEntry[latticesKeys[0]] = firstLatticeDeviceDataValue;
				detailsDataEntry[latticesKeys[1]] = secondLatticeDeviceDataValue;
				detailsData.push(detailsDataEntry);
			});
		}

		// Go through properties that are in the second lattice but not in the first one
		l(secondLatticeDeviceData);
		if(secondLatticeDeviceData !== undefined) {

			$.each(Object.keys(secondLatticeDeviceData), function(property, value) {
				var firstLatticeDeviceDataValue = "";
				var secondLatticeDeviceDataValue = "";

				// Set value of the first lattice
				if(firstLatticeDeviceData !== undefined && firstLatticeDeviceData[value] !== undefined) {
					firstLatticeDeviceDataValue = firstLatticeDeviceData[value];
				}

				// Set value of the second lattice
				if(secondLatticeDeviceData[value] !== undefined) {
					secondLatticeDeviceDataValue = secondLatticeDeviceData[value];
				}

				var detailsDataEntry = {};
				detailsDataEntry["property"] = value;
				detailsDataEntry[latticesKeys[0]] = firstLatticeDeviceDataValue;
				detailsDataEntry[latticesKeys[1]] = secondLatticeDeviceDataValue;
				detailsData.push(detailsDataEntry);
			});
		}

		l(detailsData);
		$scope.raw.latticeDetails = detailsData;
	};

	$scope.filterLattice = function() {
		filterTableItems("#lattice_table2_filter", ".lattice_table2_row", "#lattice_table2");
	};

	$scope.downloadFile = function() {

	};
});

/*
 * Show details in the right pane
 */
app.controller('showModelDetailsCtrl', function($scope, $routeParams, $http, $location, $sce){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.raw = {};
	$scope.raw.data = [];
	$scope.raw.show = true;
	$scope.models = {};

	var query = "";

	query = serviceurl + 'lattice/?function=retrieveModel&' + createModelListQuery($routeParams, false);
	l(query);

	$http.get(query).success(function(data){
		l("got models");

		$.each(data, function(name, model){
			model.name = name;

			if(model.simulationControl !== undefined) {
				model.simulationControlParsed = JSON.parse(model.simulationControl);
				l(model.simulationControlParsed);
			}
			$scope.models = model;
		});

		l($scope.models);
	});

	$scope.trim = function(input) {
		var output = input.replace(/^\s+|\s+$|\r\n/g, '');
		l(output);

		return output;
	};

//	query = serviceurl + 'lattice/?function=retrieveModelList&latticename=' + $routeParams.name + '&latticeversion=' + $routeParams.version + '&latticebranch=' + $routeParams.branch;
//	l(query);
//
//	$http.get(query).success(function(data){
//		l("got modeules");
//
//		$scope.models.data = data;
//		l($scope.models.data);
//	});

	$scope.downloadFile = function() {

	};

});

/*
 * Modal window example
 */
app.controller('modalCtrl', function($scope, $modalInstance) {
	$scope.ok = function() {
		$modalInstance.close();
	};

	$scope.cancel = function () {
		$modalInstance.dismiss('cancel');
	};
});