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
		var newLocation = createLatticeListQuery(search, true) + "/list";
		$window.location = newLocation;
	};

	// Model search button click
	$scope.searchForModel = function(search) {
		var newLocation = createModelListQuery(search, true) + "/list";
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
			newItem.latticeid = i;

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
	$scope.comparison = {};
	$scope.comparison.data = {};
	$scope.comparison.length = 0;
	$scope.comparison.show = 'false';

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

	$scope.setCompareData = function() {
		$scope.comparison.length = Object.keys($scope.comparison.data).length;
	};

	// Click on compare lattice button
	$scope.compareModel = function() {
		var models = [];

		$.each($scope.comparison.data, function(i, model){

			if(model === true) {
				models.push(i);
			}
		});

		var location = createModelListQuery($routeParams, true) + "/ids/" + models.join("|||");
		//l(location);

		$window.location = location;
	};

	$scope.clearSelection = function() {

		$.each($scope.comparison.data, function(i, model){
			$scope.comparison.data[i] = false;
		});

		$scope.comparison.length = 0;
	};

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
		$routeParams.click = "lattice_click";

		var location = createModelListQuery($routeParams, true) + "/id/" + model.name;
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
	$scope.latticeModels = [];
	$scope.compare = {};
	$scope.compare.show = false;
	$scope.raw.id = $routeParams.id;

	var params = $routeParams.id.split('|||');
	var paramsObject = {};
	paramsObject.type = $routeParams.type;
	paramsObject.name = params[0];
	paramsObject.branch = params[1];
	paramsObject.version = params[2];
	l(params);

	// Show lattice model list
	var query = serviceurl + 'lattice/?function=retrieveModelList&latticename=' + paramsObject.name + '&latticeversion=' + paramsObject.version + '&latticebranch=' + paramsObject.branch;
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

	var lattice = {};
	var header = [];

	$http.get(query).success(function(data){
		l(data);

		var latticeKeys = Object.keys(data);
		lattice = data[latticeKeys[0]].lattice;
		$scope.lattice = data[latticeKeys[0]];
		$scope.lattice.latticeid = latticeKeys[0];

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
	});

	$scope.showData = function() {
		$scope.raw.table =  createLatticeTable(header, lattice);
	};

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
	$scope.raw.ids = ids;

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

		var detailsData = createLatticeComparisonDetails(latticesData, latticesKeys, latticesKeys[0], device);
		l(latticesData[latticesKeys[0]].data[device]);
		l(latticesData[latticesKeys[1]].data[device]);
		detailsData = detailsData.concat(createLatticeComparisonDetails(latticesData, latticesKeys, latticesKeys[1], device));

		//l(detailsData);
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
	$scope.raw.search = {};
	$scope.raw.data = {};
	$scope.raw.show = true;
	$scope.models = {};
	$scope.raw.modelDetails = modelDetails;

	$scope.compare = {};
	$scope.compare.show = false;

	var keys = [];
	var privateModel = {};

	var query = serviceurl + 'lattice/?function=retrieveModel&name=' + $routeParams.id;

	$http.get(query).success(function(data){
		keys = Object.keys(data);
		privateModel = data[keys[0]];
		privateModel.name = keys[0];
		$scope.models = privateModel;
		l($scope.models);
	});

	$scope.trim = function(input) {
		var output = input.replace(/^\s+|\s+$|\r\n/g, '');
		l(output);

		return output;
	};

	$scope.showSimulationControlData = function() {
		if(privateModel.simulationControl !== undefined) {
			privateModel.simulationControlParsed = JSON.parse(privateModel.simulationControl);
			l(privateModel.simulationControlParsed);
		}
	};

	$scope.downloadFile = function() {

	};

	$scope.searchForModelDetails = function() {
		query = createModelDetailsUrl($scope.raw.search, $routeParams.id);
		l(query);

		$http.get(query).success(function(data){

			var transform = transformModelDetails(data);
			var name = transform[0];
			$scope.raw.header = transform[1];
			$scope.raw.data = transform[2];

			l($scope.raw.data);
			l($scope.raw.header);
			l(name);

			if($scope.raw.data.transferMatrix !== undefined) {
				$scope.raw.transferMatrix = data[name].transferMatrix;
			}

			l($scope.raw.transferMatrix);
		});
	};

});

/*
 * Show details in the right pane
 */
app.controller('showModelsDetailsCtrl', function($scope, $routeParams, $http, $location, $q){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.raw = {};
	$scope.raw.search = {};
	$scope.raw.data = [];
	$scope.models = {};
	$scope.compare = {};
	$scope.compare.show = true;
	$scope.raw.modelDetails = modelDetails;

	var query = serviceurl + 'lattice/?function=retrieveModel&' + createModelListQuery($routeParams, false);
	l(query);

	var ids = $routeParams.ids.split("|||");

	$scope.searchForModelDetails = function() {
		var gets = [];
		$scope.compare.names = [];
		$scope.compare.selection = {};
		$scope.compare.data = {};

		$.each(ids, function(i, id){
			query = createModelDetailsUrl($scope.raw.search, id);
			l(query);

			gets.push($http.get(query));
		});

		// Return all results
		$q.all(gets).then(function(results) {

			$.each(results, function(i, result) {
				var transform = transformModelDetails(result.data);
				//l(transform);

				$scope.compare.names.push(transform[0]);
				$scope.compare.data[transform[0]] = transform[2];

				$.each(transform[1], function(i, head) {

					if(head === "index" || head === "position" || head === "name") {
						return;
					}

					if(head in $scope.compare.selection) {
						$scope.compare.selection[head][transform[0]] = false;

					} else {
						$scope.compare.selection[head] = {};
						$scope.compare.selection[head][transform[0]] = false;
					}

				});
			});

			l($scope.compare.selection);
			l($scope.compare.names);
			l($scope.compare.data);
		});

	};

	$scope.plotData = function() {
		l($scope.compare.selection);
		drawPlot($scope.compare.selection, $scope.compare.data, "direction", "cos");
	};

	$scope.trim = function(input) {
		var output = input.replace(/^\s+|\s+$|\r\n/g, '');
		l(output);

		return output;
	};

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