/*
 * Controllers for measurement data manager
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created: Avg 1, 2014
 */

app.controller('indexCtrl', function($scope){
});

/*
 * Bending magnet controller that displays anf manages everything connected to bending magnet table
 */
app.controller('dataCtrl', function($scope, $routeParams, $http, $modal, $timeout, Inventory, inventoryFactory, EntityError, RotCoilData, HallProbeData, hallProbeDataFactory, rotCoilDataFactory){
	$scope.error = {};
	$scope.bmArr = [];
	$scope.bmArr2 = [];
	$scope.logicArr = [];
	$scope.alert = {};
	$scope.view = $routeParams.view;
	$scope.inv = new Inventory();
	$scope.columns = [];
	$scope.rawColumns = [];
	$scope.measurementData = {};
	$scope.measurementData2 = {};

	$scope.newMD = undefined;

	// Retrieve all Inventory items
	inventoryFactory.retrieveItems({'name': 'inv2'}).then(function(result) {
		var ids = Object.keys(result);
		$scope.inv = new Inventory(result[ids[0]]);
		l($scope.inv);

		$.each($scope.inv.__measurement_data_settings__.columns, function(column, columnObj) {

			if(columnObj.displayed) {
				$scope.rawColumns.push(column);

				if(columnObj.display_name && columnObj.display_name !== "") {
					$scope.columns.push(columnObj.display_name);

				} else {
					$scope.columns.push(column);
				}
			}
		});

		var promise;

		if($scope.inv.__measurement_data_settings__.source === 'rot_coil_data') {
			promise = rotCoilDataFactory.retrieveItems({'inventory_name': $scope.inv.name});

		} else {
			promise = hallProbeDataFactory.retrieveItems({'inventory_name': $scope.inv.name});
		}

		promise.then(function(result) {
			$scope.measurementData = result;
			l(result);
		});

	});

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.addRow = function(item) {
		$scope.alert.show = false;


		if($scope.inv.__measurement_data_settings__.source === 'rot_coil_data') {
			$scope.newMD = new RotCoilData();

		} else {
			$scope.newMD = new HallProbeData();
		}

		// Set properties if Copy&Create action
		if (item !== undefined) {
			$scope.newMD.set(item);
		}

		$('html, body').animate({ scrollTop: $(document).height() }, "fast");
	};

	$scope.deleteRow = function(deviceObj, typeName) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/delete_data.html',
			controller: 'deleteDataCtrl',
			resolve: {
				device: function() {
					return deviceObj;
				},
				type_name: function() {
					return typeName;
				}
			}
		});
	};

	$scope.cancel = function() {
		$scope.newMD = undefined;
	};

	$scope.updateItem = function(device, typeName, propValue) {
		$scope.alert.show = false;

		// Convert to float
		if(typeName === 'bm_s') {
			device[typeName] = parseFloat(propValue);
		}

		bmFactory.updateItem({'aid_id': device.id, 'prop_type_name': typeName, 'value': propValue}).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Value successfully updated!";

			// Set status back to unapproved
			if (device.prop_statuses[typeName] === 3) {
				device.prop_statuses[typeName] = 2;
				device.prop_statuses.num_unapproved +=1;
			}

			$scope.orderByField = "";
			$timeout(function() {$scope.closeAlert();}, alertTimeout);
			return true;

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
			return false;
		});
	};

	$scope.updateItemFixed = function(device, propName, propValue) {
		$scope.alert.show = false;

		var params = {};
		params['aid_id'] = device.id;
		params[propName] = propValue;

		bmFactory.updateDevice(params).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Value successfully updated!";
			$timeout(function() {$scope.closeAlert();}, alertTimeout);
			return true;

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
			return false;
		});
	};

	$scope.approveCell = function(deviceObj, typeName) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/approve_cell.html',
			controller: 'approveCellCtrl',
			resolve: {
				device: function() {
					return deviceObj;
				},
				type_name: function() {
					return typeName;
				}
			}
		});
	};

	$scope.approveRow = function(deviceObj) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/approve_row.html',
			controller: 'approveRowCtrl',
			resolve: {
				device: function() {
					return deviceObj;
				}
			}
		});
	};

	$scope.saveItem = function(newItem) {
		$scope.alert.show = false;
		$scope.error = {};

		if($scope.inv.__measurement_data_settings__.source === 'rot_coil_data') {
			$scope.newMD = new RotCoilData(newItem);
			$scope.error = rotCoilDataFactory.checkItem($scope.newMD);

		} else {
			$scope.newMD = new HallProbeData(newItem);
			$scope.error = hallProbeDataFactory.checkItem($scope.newMD);
		}

		l($scope.error);

		if ($scope.error === true || Object.keys($scope.error).length === 0) {
			//$scope.newMD.updateProps();
			var promise;

			if($scope.inv.__measurement_data_settings__.source === 'rot_coil_data') {
				promise = rotCoilDataFactory.saveItem($scope.newMD);

			} else {
				promise = hallProbeDataFactory.saveItem($scope.newMD);
			}

			promise.then(function(data) {
				$scope.cancel();
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Data successfully saved!";

				var promise;

				if($scope.inv.__measurement_data_settings__.source === 'rot_coil_data') {
					promise = rotCoilDataFactory.retrieveItems({'inventory_name': $scope.inv.name});

				} else {
					promise = hallProbeDataFactory.retrieveItems({'inventory_name': $scope.inv.name});
				}

				promise.then(function(result) {

					$.each(result, function(index, obj) {

						if(!(index in $scope.measurementData)) {
							$scope.measurementData2[index] = obj;
						}
					});

					l($scope.measurementData2);
				});

				$timeout(function() {$scope.closeAlert();}, alertTimeout);

			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});

		} else {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = $scope.error;
		}
	};
});

/*
 * Delete device controller
 */
app.controller('deleteDataCtrl', function($scope, $modalInstance, $window, bmFactory, device, type_name) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		bmFactory.deleteItem(device.id).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Data successfully deleted!";
			$scope.showYesButton = false;
			$scope.showCancelButton = false;
			$scope.showFinishButton = true;

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
		});
	};

	$scope.cancel = function() {
		$modalInstance.dismiss('cancel');
	};

	$scope.finish = function() {
		$window.location.reload();

		$modalInstance.dismiss('cancel');
	};
});

/*
 * Delete device controller
 */
app.controller('deleteLogicCtrl', function($scope, $modalInstance, $window, logicFactory, logic) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		logicFactory.deleteItem(logic.id).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Logic successfully deleted!";
			$scope.showYesButton = false;
			$scope.showCancelButton = false;
			$scope.showFinishButton = true;

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
		});
	};

	$scope.cancel = function() {
		$modalInstance.dismiss('cancel');
	};

	$scope.finish = function() {
		$window.location.reload();

		$modalInstance.dismiss('cancel');
	};
});

/*
 * Copy dataset controller
 */
app.controller('copyDatasetCtrl', function($scope, $modalInstance, $window, statusFactory, headerFactory, statuses, status, map) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;
	var types = [];
	$scope.ai = undefined;
	$scope.description = "";

	headerFactory.retrieveHeader(status).then(function (data) {

		if (data !== undefined) {
			var keys = Object.keys(data);
			$scope.ai = data[keys[0]];
			$scope.description = "Copy from dataset id: " + $scope.ai.id + ", " + $scope.ai.description;
		}
	});

	$scope.message = "The whole dataset will be copied. Do you want to continue?";

	if (statuses.editable > 0) {
		$scope.message = "There is a dataset with status editable. All data will be lost! Do you want to continue?";
	}

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		statusFactory.copyStatus({"status":status, "description": $scope.description}).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Dataset status successfully copied!";
			$scope.showYesButton = false;
			$scope.showCancelButton = false;
			$scope.showFinishButton = true;

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
		});
	};

	$scope.cancel = function() {
		$modalInstance.dismiss('cancel');
	};

	$scope.finish = function() {
		$window.location = "#/status/editable/tab/bm/bm/";
		$modalInstance.dismiss('cancel');
	};
});