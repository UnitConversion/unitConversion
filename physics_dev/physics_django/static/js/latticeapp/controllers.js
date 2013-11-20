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
app.controller('mainCtrl', function($scope, $http, $route, $modal){
	$scope.version = version;
	$scope.style = {};
	$scope.style.middle_class = "container-scroll-middle";
	$scope.style.right_class = "container-scroll-last-one";
	$scope.statuses = statuses;
	$scope.modelStatuses = modelStatuses;
	setUpLoginForm();

	$scope.loginData = {};

	$scope.login = function() {
		l($scope.loginData);

		$.ajax({
			url: serviceurl + "user/login/",
			method: "POST",
			data: "username=" + $scope.loginData.username + "&password=" + $scope.loginData.password
		}).success(function(data, status, headers, config) {
			l(data);
			location.reload();

		}).error(function(data, status, headers, config) {

		});
	};

	$scope.logout = function() {

		$.ajax({
			url: serviceurl + "user/logout/",
			method: "POST"
		}).success(function(data, status, headers, config) {
			l(data);
			location.reload();

		}).error(function(data, status, headers, config) {

		});
	};

	$scope.uploadLattice = function() {
		var modalInstance = $modal.open({
			template: '\
				<div class="modal-header">\
					<button type="button" class="close" ng-click="cancel()">&times;</button>\
					<h3>Upload lattice</h3>\
				</div>\
				<div class="modal-body">\
					<div class="alert alert-error" ng-show="modal.error.show">\
						<button type="button" class="close" ng-click="closeAlert()">&times;</button>\
						<strong>Warning!</strong> Best check yo self, you not looking too good.\
					</div>\
					{{modal.error.show}}\
					<fieldset>\
						<label>Name</label>\
						<input ng-model="upload.name" type="text">\
						<label>Version</label>\
						<input ng-model="upload.version" type="text">\
						<label>Branch</label>\
						<input ng-model="upload.branch" type="text">\
						<label>File</label>\
						<input type="file">\
					</fieldset>\
				</div>\
				<div class="modal-footer">\
					<button class="btn btn-primary" ng-click="ok()">Upload</button>\
					<button class="btn btn-primary" ng-click="cancel()">Cancel</button>\
				</div>',
			controller: 'uploadLatticeModalCtrl'
		});
	};
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

	$scope.models = {};
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

			$scope.models[i] = newItem;

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
			var id = i + "||" + $scope.models[i].id;

			if(model === true) {
				models.push(id);
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

	// Get id parameter from the URL and split it by |||
	var params = $routeParams.id.split('|||');
	var paramsObject = {};
	paramsObject.type = $routeParams.type;
	paramsObject.name = params[0];
	paramsObject.branch = params[1];
	paramsObject.version = params[2];

	// Show lattice model list
	var query = serviceurl + 'lattice/?function=retrieveModelList&latticename=' + paramsObject.name + '&latticeversion=' + paramsObject.version + '&latticebranch=' + paramsObject.branch;

	// Get model list data and create appropriate object
	$http.get(query).success(function(data){

		$.each(data, function(name, model){
			model.name = name;

			var route = {};
			route.id = model.id;
			route.type = "model";

			$.each(model, function(i, cell){
				model[i] = $sce.trustAsHtml(model[i].toString());
			});

			var location = createModelListQuery(route, true) + "/id/" + name;
			model.link = $sce.trustAsHtml('<a href="' + location + '">link to model</a>');
			$scope.latticeModels.push(model);
		});
	});

	// Show raw lattice in a table
	query = serviceurl + 'lattice/?function=retrieveLattice&rawdata=true&withdata=true&' + createLatticeListQuery(paramsObject, false);

	var lattice = {};
	var header = [];

	// Get lattice data and generate appropriate objects
	$http.get(query).success(function(data){
		var latticeKeys = Object.keys(data);
		lattice = data[latticeKeys[0]].lattice;
		$scope.raw.url = serviceurl + data[latticeKeys[0]].rawlattice.name;
		$scope.lattice = data[latticeKeys[0]];
		$scope.lattice.latticeid = latticeKeys[0];

		// Create array of header columns
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

	// Show data by clicking on Show data in a table button
	$scope.showData = function() {
		$scope.raw.table =  createLatticeTable(header, lattice, $scope.raw.url);
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
	$scope.filter = {};
	$scope.filter.deviceName = "";

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
		filterTableItems($scope.filter, ".lattice_table2_row", "#lattice_table2");
	};

	$scope.downloadFile = function() {

	};
});

/*
 * Show model details in the right pane
 */
app.controller('showModelDetailsCtrl', function($scope, $routeParams, $http, $location, $sce){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.raw = {};
	$scope.raw.search = {};
	$scope.raw.data = {};
	$scope.raw.header = {};
	$scope.raw.show = true;
	$scope.models = {};
	$scope.raw.modelDetails = modelDetails;
	$scope.raw.showMatrices = false;
	$scope.raw.selection = {};
	$scope.raw.selectionCount = 0;

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
		$scope.raw.showMatrices = false;
		query = createModelDetailsUrl($scope.raw.search, $routeParams.id);
		l(query);

		$http.get(query).success(function(data){

			var transform = transformModelDetails(data);
			var name = transform[0];
			$scope.raw.header[transform[0]] = transform[1];
			$scope.raw.data[transform[0]] = transform[2];
			$scope.raw.selection = createPropertySelectionTable(transform[1], transform[0], $scope.raw.selection);
			$scope.raw.selectionCount = Object.keys($scope.raw.selection).length;

			l($scope.raw.data);
			l($scope.raw.header);
			l(name);

			if($scope.raw.data[transform[0]].transferMatrix !== undefined) {
				$scope.raw.transferMatrix = data[name].transferMatrix;
			}

			l($scope.raw.transferMatrix);
		});
	};

	$scope.showMatrices = function() {
		$scope.raw.showMatrices = true;
	};

	$scope.plotData = function() {
		l($scope.compare.selection);
		drawPlot(".placeholder", $scope.raw.selection, $scope.raw.data, undefined, "Position", "Property");
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
	$scope.models = {};
	$scope.compare = {};
	$scope.compare.show = true;
	$scope.raw.modelDetails = modelDetails;

	var query = "";
	var ids = $routeParams.ids.split("|||");
	var nameToIdMap = {};

	$scope.searchForModelDetails = function() {
		var gets = [];
		$scope.compare.names = [];
		$scope.compare.ids = [];
		$scope.compare.selection = {};
		$scope.compare.selectionCount = 0;
		$scope.compare.data = {};

		$.each(ids, function(i, id){
			var idParts = id.split("||");
			nameToIdMap[idParts[0]] = idParts[1];

			query = createModelDetailsUrl($scope.raw.search, idParts[0]);
			l(query);

			gets.push($http.get(query));
		});

		// Return all results
		$q.all(gets).then(function(results) {

			$.each(results, function(i, result) {
				var transform = transformModelDetails(result.data);
				//l(transform);

				$scope.compare.names.push(transform[0]);
				$scope.compare.ids.push(nameToIdMap[transform[0]]);
				$scope.compare.data[transform[0]] = transform[2];

				$scope.compare.selection = createPropertySelectionTable(transform[1], transform[0], $scope.compare.selection);

				$scope.compare.selectionCount = Object.keys($scope.compare.selection).length;
			});

			l($scope.compare.selection);
			l($scope.compare.names);
			l($scope.compare.data);
		});

	};

	$scope.plotData = function() {
		l($scope.compare.selection);
		drawPlot(".placeholder", $scope.compare.selection, $scope.compare.data, nameToIdMap, "Position", "Property");
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
 * Upload lattice controller
 */
app.controller('uploadLatticeModalCtrl', function($scope, $modalInstance) {
	$scope.upload = {};
	$scope.modal = {};
	$scope.modal.error = {};
	$scope.modal.error.show = false;

	$scope.closeAlert = function() {
		$scope.modal.error.show = false;
	};

	$scope.ok = function() {
		l(JSON.stringify($scope.upload));

		$.ajax({
			url: serviceurl + "lattice/upload",
			method: "POST",
			contentType: 'application/json; charset=utf-8',
			data: JSON.stringify($scope.upload)
		}).success(function(data, status, headers, config) {
			l(data);

			if(data.result === "error") {
				$scope.modal.error.show = true;
			}

		}).error(function(data, status, headers, config) {
			$scope.modal.error.show = true;
		});

		//$modalInstance.close();
	};

	$scope.cancel = function () {
		$modalInstance.dismiss('cancel');
	};
});