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

	$scope.compareLattice = function() {
		var lattices = [];

		$.each($scope.comparison.data, function(i, lattice){

			if(lattice === true) {
				lattices.push(i);
			}
		});

		var location = createLatticeListQuery($routeParams, true) + "/id/" + lattices.join(",");
		//l(location);

		$window.location = location;

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
 * Show details in the right pane
 */
app.controller('showDetailsCtrl', function($scope, $routeParams, $http, $location, $sce, $q){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.raw = {};
	$scope.raw.data = [];
	$scope.raw.show = true;
	$scope.lattices = [];
	$scope.lattice = {};
	$scope.latticeModels = [];
	$scope.compare = {};
	$scope.compare.show = false;
	$scope.raw.id = $routeParams.id;

	// Check if we got complex id
	if($scope.raw.id.split(',').length > 1) {
		$scope.compare.show = true;
	}

	$scope.$watch('comparison', function(newValue, oldValue){
		l(newValue);
		l("comparison");
		l($scope.comparison);
	});

	l($scope.comparison);

	var query = "";

	var params = $routeParams.id.split('|||');
	var paramsObject = {};
	paramsObject.type = $routeParams.type;
	paramsObject.name = params[0];
	paramsObject.branch = params[1];
	paramsObject.version = params[2];
	l(params);

	// Show lattice info only if not comparing lattices
	if($scope.compare.show === false) {
		query = serviceurl + 'lattice/?function=retrieveLatticeInfo&' + createLatticeListQuery(paramsObject, false);
		l(query);

		$http.get(query).success(function(data){
			//l("got data");

			$.each(data, function(i, item){
				l(item);
				$scope.lattices.push(item);
			});

			$scope.lattice = $scope.lattices[0];
			//l($scope.lattices);
		});
	}

	// Show lattice model list if not comparing lattices
	if($scope.compare.show === false) {
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
	}

	// If not comparing data, show raw lattice in a table
	if($scope.compare.show === false) {
		query = serviceurl + 'lattice/?function=retrieveLattice&withdata=true&' + createLatticeListQuery(paramsObject, false);
		//l(query);

		var table = "";

		$http.get(query).success(function(data){
			//$('#raw').html(drawDataTree("", data));

			$.each(data, function(i, datum){
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
				l(header);

				$scope.raw.data.push({head: header});

				// Add header
				table = "<tr>";

				$.each(header, function(i, column){
					table += "<th>" + column.charAt(0).toUpperCase() + column.slice(1) + "</th>";
				});

				table += "</tr>";

				// Add data
				$.each(lattice, function(j, line){
					table += "<tr>";

					$.each(header, function(i, column){

						if(line[column] === undefined) {
							table += "<td></td>";

						} else {

							// Ckeck for file links
							if(column.indexOf("file") !== -1) {
								table += '<td><a href="#">' + line[column] + '</a></td>';

							} else {
								table += "<td>" + line[column] + "</td>";
							}
						}
					});

					table += "</tr>";
				});
			});

			$('#lattice_table').html(table);

			$scope.raw.show = false;
		});

	// Compare lattices
	} else {
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
				l(params);

				query = serviceurl + 'lattice/?function=retrieveLattice&withdata=true&' + createLatticeListQuery(paramsObject, false);

				gets.push($http.get(query));
			});

			// Return all results
			$q.all(gets).then(function(results) {
				var latticesData = {};

				if(!checkLatticeFormat(results)) {
					$scope.compare.message = "Selected lattices doens't have same formats. Comparison cannot continue.";

				} else {
					//l(results);

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

						latticesData[result.data[keys[0]].name] = {keys:header, data:latticeData};
					});

					//l(latticesData);

					// List devices
					var latticesKeys = Object.keys(latticesData);
					var html = "<tr><th>Device names</th>";

					$.each(latticesKeys, function(i, key){
						html += "<th>" + key + "</th>";
					});

					html += "<th>Diff</th>";

					html += "</tr>";

					$.each(latticesData[latticesKeys[0]].data, function(i, latticeLine) {
						html += "<tr><td>" + i + "</td>";

						var deviceKeys = [];

						$.each(latticesData, function(j, lattice) {

							var keys = [];

							$.each(lattice.keys, function(j, header) {

								if(latticeLine[header] === undefined) {
									keys.push(header + "=");

								} else {
									keys.push(header + "=" + latticeLine[header]);
								}
							});

							deviceKeys.push(keys);

							html += "<td>" + keys.join(", ") + "</td>";
						});

						var cssClass = checkDiff(deviceKeys);

						html += "<td class='" + cssClass + "'></td>";

						html += "</tr>";

					});

					$('#lattice_table2').html(html);
				}
			});
		}
	}

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