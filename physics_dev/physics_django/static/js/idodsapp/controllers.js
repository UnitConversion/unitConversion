/*
 * Controllers for insertion device online data service module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created: Feb 26, 2014
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

			$('html, body').animate({
				scrollTop: element.parent().offset().top
			}, 100);
		}
	};
});

/*
 * Main controller when we load the main page
 */
app.controller('mainCtrl', function($scope, $modal){
	$scope.version = version;
	$scope.style = {};
	$scope.style.middle_class = "container-scroll-middle";
	$scope.style.right_class = "container-scroll-last-one";
	setUpLoginForm();

	$scope.session = {};
	$scope.authenticated = {};
	$scope.authenticated.error = false;

	$scope.login = function() {
		l($scope.loginData);

		$.ajax({
			url: serviceurl + "user/login/",
			method: "POST",
			data: "username=" + $scope.session.username + "&password=" + $scope.session.password
		}).success(function(data, status, headers, config) {
			$scope.authenticated.error = false;
			$scope.$apply();
			location.reload();

		}).error(function(data, status, headers, config) {
			$scope.authenticated.error = true;
			$scope.$apply();
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
			templateUrl: 'modal/save_lattice.html',
			controller: 'uploadLatticeModalCtrl'
		});
	};

	$scope.uploadModel = function() {
		var modalInstance = $modal.open({
			templateUrl: 'modal/save_model.html',
			controller: 'uploadModelModalCtrl'
		});
	};
});

/*
 * Controller for the left/search pane
 */
app.controller('searchVendorCtrl', function($scope, $window, $routeParams){
	$scope.search = {};
	$scope.dataTypes = dataTypes;

	// Vendor search button click
	$scope.searchForVendor = function(search) {
		search.search = new Date().getTime();
		var newLocation = createUrlAndQuery(search, "vendor", true) + "/list";
		l(newLocation);
		$window.location = newLocation;
	};
});

/*
 * List vendor in the middle pane
 */
app.controller('listVendorCtrl', function($scope, $routeParams, $http, $window, Vendor, vendorFactory) {
	// Remove image from the middle pane if there is something to show
	$scope.style.middle_class = "container-scroll-middle-no-img";

	$scope.id = $routeParams.id;

	$scope.vendors = [];
	var previousItem = undefined;

	vendorFactory.retrieveVendors($routeParams).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new Vendor(item);

			// Alternate background colors
			if(i%2 === 0) {
				newItem.color = "bg_dark";

			} else {
				newItem.color = "bg_light";
			}

			$scope.vendors.push(newItem);
		});
	});
	
	// Show add form in the right pane
	$scope.addItem = function() {
		var location = createUrlAndQuery($routeParams, "vendor", true) + "/id/new/action/save";
		$window.location = location;
	}

	// Show details when user selects item from a list
	$scope.showDetails = function(item) {
		$scope.id = undefined;

		// Clear click style from previously selected element
		if(previousItem !== undefined) {
			previousItem.click = "";
		}

		previousItem = item;
		item.click = "item_click";
		item.search = $routeParams.search;
		$routeParams.click = "item_click";
		$routeParams.name = item.name;
		$routeParams.description = item.description;

		var location = createUrlAndQuery($routeParams, "vendor", true) + "/id/" + item.id + "/action/retrieve";
		$window.location = location;
	};
});

/*
 * Show details in the right pane
 */
app.controller('showVendorCtrl', function($scope, $routeParams, $http, $window, Vendor, vendorFactory, EntityError){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.action = $routeParams.action;
	$scope.new = new Vendor();
	$scope.error = {};
	$scope.alert = {};
	$scope.alert.show = false;
	
	// Get vendor from the factory
	vendorFactory.retrieveVendor($routeParams).then(function(result) {
		$scope.element = result;
	});
	
	// Show update form in the right pane
	$scope.updateItem = function() {
		var location = createUrlAndQuery($routeParams, "vendor", true) + "/id/" + $routeParams["id"] + "/action/update";
		$window.location = location;
	}
	
	$scope.saveItem = function(newItem, action) {
		$scope.alert.show = false;
		var vendor = new Vendor(newItem);
		l(vendor);
		var result = vendorFactory.checkVendor(vendor);
		l(result);

		if(result !== true) {
			$scope.error = result.errorDict;
		
		} else {
			var promise;
			
			if(action === "update") {
				promise = vendorFactory.updateVendor($scope.element);

			} else if(action == "save") {
				promise = vendorFactory.saveVendor($scope.new);
			}
			
			promise.then(function(data) {
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Vendor successfully saved!";
			
			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});
		}
	}
});

/*
 * Show lattice compare view in the right pane
 */
app.controller('showLatticesDetailsCtrl', function($scope, $routeParams, $http, $q){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.raw = {};
	$scope.raw.show = true;
	$scope.compare = {};
	$scope.compare.show = true;
	$scope.raw.id = $routeParams.ids;
	$scope.filter = {};
	$scope.filter.deviceName = "";

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
		var parent = $('.parent_' + device);
		var children = $('.children_' + device);

		children.toggle();

		if(parent.hasClass('icon-chevron-up')) {
			parent.removeClass('icon-chevron-up');
			parent.addClass('icon-chevron-down');

		} else {
			parent.removeClass('icon-chevron-down');
			parent.addClass('icon-chevron-up');
		}
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
app.controller('showModelDetailsCtrl', function($scope, $routeParams, $http, $window, $modal){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.raw = {};
	$scope.raw.search = {};
	$scope.raw.search.precision = 4;
	$scope.raw.data = {};
	$scope.raw.header = {};
	$scope.raw.show = true;
	$scope.models = {};
	$scope.raw.modelDetails = modelDetails;
	$scope.raw.showMatrices = false;
	$scope.raw.selection = {};
	$scope.raw.selectionCount = 0;
	$scope.raw.factor = {};

	$scope.compare = {};
	$scope.compare.show = false;

	$scope.plotPlaceholder = {};
	$scope.plotPlaceholder.show = false;

	var keys = [];
	var privateModel = {};

	var query = serviceurl + 'lattice/?function=retrieveModel&name=*&id=' + $routeParams.id;

	$http.get(query).success(function(data){
		l(data);
		keys = Object.keys(data);
		privateModel = data[keys[0]];
		$scope.models = privateModel;
	});

	$scope.trim = function(input) {
		var output = input.replace(/^\s+|\s+$|\r\n/g, '');
		return output;
	};

	$scope.showSimulationControlData = function() {
		if(privateModel.simulationControl !== undefined && privateModel.simulationControlParsed === undefined) {
			privateModel.simulationControlParsed = JSON.parse(privateModel.simulationControl);

		} else {
			privateModel.simulationControlParsed = undefined;
		}
	};

	$scope.searchForModelDetails = function() {
		$scope.raw.showMatrices = false;
		query = createModelDetailsUrl($scope.raw.search, privateModel.name);
		l(query);

		$http.get(query).success(function(data){
			l(data);
			var transform = transformModelDetails(data);
			l(transform);
			var name = transform[0];
			$scope.raw.header[transform[0]] = transform[1];
			$scope.raw.data[transform[0]] = transform[2];
			$scope.raw.selection = filterPropertySelectionTable(transform[0], $scope.raw.header);
			$scope.raw.factor = filterPropertyFactorTable(transform[0], $scope.raw.header);
			$scope.raw.selectionCount = Object.keys($scope.raw.selection).length;
			$scope.raw.modelName = transform[0];

			if($scope.raw.data[transform[0]].transferMatrix !== undefined) {
				$scope.raw.transferMatrix = data[name].transferMatrix;
			}
		});
	};

	// Show matrices below the details
	$scope.showMatrices = function() {

		if($scope.raw.showMatrices) {
			$scope.raw.showMatrices = false;

		} else {
			$scope.raw.showMatrices = true;
		}
	};

	// Plot data when properties are selected
	$scope.plotData = function() {
		$scope.plotPlaceholder.show = true;
		drawPlotTransposed(".placeholder", $scope.raw.selection, $scope.raw.factor, $scope.raw.data, undefined, "Position", $scope);
	};

	// Export data to csv file
	$scope.exportData = function() {
		var output = createCsvString($scope.raw.data, $scope.raw.selection, $scope.raw.factor);
		$window.open('data:application/download,' + encodeURIComponent(output));
	};

	$scope.updateModel = function(modelName) {
		l(modelName);

		var modalInstance = $modal.open({
			templateUrl: 'modal/update_model.html',
			controller: 'updateModelModalCtrl',
			resolve: {
				name: function() {
					return modelName;
				}
			}
		});
	};
});

/*
 * Show details in the right pane
 */
app.controller('showModelsDetailsCtrl', function($scope, $routeParams, $http, $q){
	// Remove image from the middle pane if there is something to show
	$scope.style.right_class = "container-scroll-last-one-no-img";
	$scope.raw = {};
	$scope.raw.search = {};
	$scope.models = {};
	$scope.compare = {};
	$scope.compare.factor = {};
	$scope.compare.show = true;
	$scope.raw.modelDetails = modelDetails;
	$scope.plotPlaceholder = {};
	$scope.plotPlaceholder.show = false;

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

		$scope.compare.nameToIdMap = nameToIdMap;

		// Return all results
		$q.all(gets).then(function(results) {

			$.each(results, function(i, result) {
				var transform = transformModelDetails(result.data);

				$scope.compare.names.push(transform[0]);
				$scope.compare.ids.push(nameToIdMap[transform[0]]);
				$scope.compare.data[transform[0]] = transform[2];

				$scope.compare.selection = createPropertySelectionTable(transform[1], transform[0], $scope.compare.selection);
				$scope.compare.modelName = transform[0];
				$scope.compare.factor = createPropertyFactorTable(transform[1], transform[0], $scope.compare.factor);

				$scope.compare.selectionCount = Object.keys($scope.compare.selection).length;
			});
		});
	};

	$scope.plotData = function() {
		$scope.plotPlaceholder.show = true;
		drawPlotTransposed(".placeholder", $scope.compare.selection, $scope.compare.factor, $scope.compare.data, nameToIdMap, "Position", $scope);
	};

	$scope.trim = function(input) {
		var output = input.replace(/^\s+|\s+$|\r\n/g, '');
		return output;
	};
});

/*
 * Upload lattice controller
 */
app.controller('uploadLatticeModalCtrl', function($scope, $modalInstance, $window) {
	$scope.upload = {};
	$scope.upload.latticeFile = "";
	$scope.upload.controlFile = "";
	$scope.upload.kickmapFile = "";

	$scope.modal = {};
	$scope.modal.error = {};
	$scope.modal.error.show = false;
	$scope.modal.error.message = "Lattice with the same parameters already exists in the database!";

	$scope.modal.success = {};
	$scope.modal.success.show = false;
	$scope.modal.success.message = "Lattice successfully uploaded!";

	$scope.modal.waiting = {};
	$scope.modal.waiting.show = false;
	$scope.modal.waiting.message = "Uploading lattice and running simulation!";

	$scope.modal.doSimulation = {};
	$scope.modal.doSimulation.show = true;
	$scope.modal.doSimulation.selected = false;

	$scope.modal.controlFile = {};
	$scope.modal.controlFile.show = false;

	$scope.modal.finishButton = "Cancel";

	$scope.modal.latticeTypes = latticeTypes;
	var uploadData = undefined;

	// Watch lattice type
	$scope.$watch('upload.latticeType', function(newValue, oldValue) {
		var value = {};

		if(newValue !== undefined) {
			value = JSON.parse(newValue);

			if(value.name === "plain") {
				$scope.modal.doSimulation.show = false;
				$scope.modal.doSimulation.selected = false;

			} else {
				$scope.modal.doSimulation.show = true;
				$scope.modal.doSimulation.selected = true;
			}

			if(value.name === "elegant") {
				$scope.modal.controlFile.show = true;

			} else {
				$scope.modal.controlFile.show = false;
			}
		}
	});

	$scope.options = {
		url: serviceurl + "lattice/upload",
		maxFileSize: 5000000,
		acceptFileTypes: /(\.|\/)(gif|jpe?g|png|txt)$/i
	};

	$scope.closeAlert = function() {
		$scope.modal.error.show = false;
		$scope.modal.success.show = false;
	};

	$scope.$on('fileuploadadd', function(e, data) {
		l(data);
		var id = data.fileInput.context.id;
		$scope.upload[id] = data.files[0].name;

		if(uploadData === undefined) {
			uploadData = data;

		} else {
			uploadData.files.push(data.files[0]);
		}
	});

	$scope.$on('fileuploaddone', function(e, data) {
		uploadData = undefined;
		$scope.modal.success.show = true;
		$scope.modal.waiting.show = false;
		$scope.modal.error.show = false;
		$scope.upload.latticeFile = "";
		$scope.upload.controlFile = "";
		$scope.upload.kickmapFile = "";

		$scope.modal.finishButton = "Finish";
	});

	$scope.$on('fileuploadfail', function(e, data) {
		$scope.modal.waiting.show = false;
		$scope.modal.success.show = false;
		$scope.modal.error.message = data.jqXHR.responseText;
		$scope.modal.error.show = true;
		$scope.modal.success.show = false;
	});

	$scope.ok = function() {
		$scope.modal.finishButton = "Cancel";

		if(
			$scope.upload.name === "" ||
			$scope.upload.branch === "" ||
			$scope.upload.version === "" ||
			$scope.upload.latticeType === undefined ||
			uploadData === undefined
		) {
			$scope.modal.error.message = "Parameters should not be empty!";
			$scope.modal.error.show = true;
			$scope.modal.success.show = false;

		} else {
			$scope.modal.error.show = false;
			$scope.modal.waiting.show = true;
			$scope.modal.success.show = false;
			l(uploadData);
			uploadData.submit();
		}
	};

	$scope.cancelButton = function() {
		$modalInstance.dismiss('cancel');
		$window.location.reload();
	};
});

/*
 * Upload model controller
 */
app.controller('uploadModelModalCtrl', function($scope, $modalInstance, modelCodeInfoService, $window, $http) {
	$scope.upload = {};
	$scope.upload.controlFile = "";
	$scope.upload.resultFile = "";
	$scope.upload.latticeid = undefined;

	$scope.$watch('upload.latticeid', function(newValue, oldValue) {
		l(newValue);
	});

	$scope.modal = {};
	$scope.modal.error = {};
	$scope.modal.error.show = false;
	$scope.modal.error.message = "Model with the same parameters already exists in the database!";

	$scope.modal.success = {};
	$scope.modal.success.show = false;
	$scope.modal.success.message = "Model successfully uploaded!";

	$scope.modal.waiting = {};
	$scope.modal.waiting.show = false;
	$scope.modal.waiting.message = "Uploading model!";

	$scope.modal.controlFile = {};
	$scope.modal.controlFile.show = false;

	$scope.modal.lattices = [];

	var query = serviceurl + 'lattice/?function=retrieveLatticeInfo&name=*&branch=*&version=*';

	// Retrieve lattices
	$http.get(query).success(function(data){

		$.each(data, function(id, lattice) {
			lattice.id = id;
			lattice.label = lattice.name + " / " + lattice.branch + " / " + lattice.version;
			lattice.value = lattice.id;
			$scope.modal.lattices.push(lattice);
		});

		l($scope.modal.lattices);
	});

	// Load Mode Code Info
	modelCodeInfoService.transform(function(serviceData){
		l("modelcodeinfo");
		l(serviceData);
		$scope.modal.modelCodeInfo = serviceData.data;
	});

	$scope.modal.finishButton = "Cancel";
	var uploadData = undefined;

	$scope.options = {
		url: serviceurl + "model/upload",
		maxFileSize: 5000000,
		acceptFileTypes: /(\.|\/)(gif|jpe?g|png|txt)$/i
	};

	$scope.closeAlert = function() {
		$scope.modal.error.show = false;
		$scope.modal.success.show = false;
	};

	$scope.$on('fileuploadadd', function(e, data) {
		l(data);
		var id = data.fileInput.context.id;
		$scope.upload[id] = data.files[0].name;

		if(uploadData === undefined) {
			uploadData = data;

		} else {
			uploadData.files.push(data.files[0]);
		}
	});

	$scope.$on('fileuploaddone', function(e, data) {
		uploadData = undefined;
		$scope.modal.success.show = true;
		$scope.modal.waiting.show = false;
		$scope.modal.error.show = false;
		$scope.upload.controlFile = "";
		$scope.upload.resultFile = "";

		$scope.modal.finishButton = "Finish";
	});

	$scope.$on('fileuploadfail', function(e, data) {
		$scope.modal.waiting.show = false;
		$scope.modal.success.show = false;
		$scope.modal.error.message = data.jqXHR.responseText;
		$scope.modal.error.show = true;
		$scope.modal.success.show = false;
	});

	$scope.ok = function() {
		$scope.modal.finishButton = "Cancel";

		if(
			$scope.upload.modelname === "" ||
			$scope.upload.simCodeAlg === undefined ||
			uploadData === undefined
		) {
			$scope.modal.error.message = "Parameters should not be empty!";
			$scope.modal.error.show = true;
			$scope.modal.success.show = false;

		} else {
			$scope.modal.error.show = false;
			$scope.modal.waiting.show = true;
			$scope.modal.success.show = false;
			l(uploadData);
			uploadData.submit();
		}
	};

	$scope.cancelButton = function() {
		$modalInstance.dismiss('cancel');
		$window.location.reload();
	};
});

/*
 * Update model controller
 */
app.controller('updateModelModalCtrl', function($scope, $modalInstance, $http, name) {
	$scope.upload = {};
	$scope.modelStatuses = modelStatuses;

	$scope.modal = {};
	$scope.modal.error = {};
	$scope.modal.error.show = false;
	$scope.modal.error.message = "Something went wrong during status saving!";

	$scope.modal.success = {};
	$scope.modal.success.show = false;
	$scope.modal.success.message = "Status successfully saved!";

	$scope.modal.waiting = {};
	$scope.modal.waiting.show = false;
	$scope.modal.waiting.message = "Saving status";

	$scope.modal.controlFile = {};
	$scope.modal.controlFile.show = false;

	$scope.modal.finishButton = "Cancel";

	$scope.closeAlert = function() {
		$scope.modal.error.show = false;
		$scope.modal.success.show = false;
	};

	$scope.ok = function() {
		$scope.modal.finishButton = "Cancel";

		if(
			$scope.upload.status === undefined ||
			$scope.upload.status === "-1"
		) {
			$scope.modal.error.message = "Parameters should not be empty!";
			$scope.modal.error.show = true;
			$scope.modal.success.show = false;

		} else {
			$scope.modal.error.show = false;
			$scope.modal.waiting.show = true;
			$scope.modal.success.show = false;
		}
		var query = serviceurl + "model/savestatus";

		$http.post(query, "status=" + $scope.upload.status + "&name=" + name).success(function(data){
			$scope.modal.success.show = true;
			$scope.modal.waiting.show = false;
			$scope.modal.error.show = false;
			$scope.modal.finishButton = "Finish";

		}).error(function(data, status, headers, config) {
			$scope.modal.waiting.show = false;
			$scope.modal.success.show = false;
			$scope.modal.error.message = data;
			$scope.modal.error.show = true;
			$scope.modal.success.show = false;
		});
	};

	$scope.cancelButton = function() {
		$modalInstance.dismiss('cancel');
	};
});

/*
 * Update lattice controller
 */
app.controller('updateLatticeModalCtrl', function($scope, $modalInstance, $http, name, version, branch) {
	$scope.upload = {};
	$scope.latticeStatuses = statuses;

	$scope.modal = {};
	$scope.modal.error = {};
	$scope.modal.error.show = false;
	$scope.modal.error.message = "Something went wrong during status saving!";

	$scope.modal.success = {};
	$scope.modal.success.show = false;
	$scope.modal.success.message = "Status successfully saved!";

	$scope.modal.waiting = {};
	$scope.modal.waiting.show = false;
	$scope.modal.waiting.message = "Saving status";

	$scope.modal.controlFile = {};
	$scope.modal.controlFile.show = false;

	$scope.modal.finishButton = "Cancel";

	$scope.closeAlert = function() {
		$scope.modal.error.show = false;
		$scope.modal.success.show = false;
	};

	$scope.ok = function() {
		$scope.modal.finishButton = "Cancel";

		if(
			$scope.upload.status === undefined ||
			$scope.upload.status === "-1"
		) {
			$scope.modal.error.message = "Parameters should not be empty!";
			$scope.modal.error.show = true;
			$scope.modal.success.show = false;

		} else {
			$scope.modal.error.show = false;
			$scope.modal.waiting.show = true;
			$scope.modal.success.show = false;
		}
		var query = serviceurl + "lattice/savestatus";

		$http.post(query, "status=" + $scope.upload.status + "&name=" + name + "&version=" + version + "&branch=" + branch).success(function(data){
			$scope.modal.success.show = true;
			$scope.modal.waiting.show = false;
			$scope.modal.error.show = false;
			$scope.modal.finishButton = "Finish";

		}).error(function(data, status, headers, config) {
			$scope.modal.waiting.show = false;
			$scope.modal.success.show = false;
			$scope.modal.error.message = data;
			$scope.modal.error.show = true;
			$scope.modal.success.show = false;
		});
	};

	$scope.cancelButton = function() {
		$modalInstance.dismiss('cancel');
	};
});