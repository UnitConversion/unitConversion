/*
 * Controllers for active interlock module
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 * @created: Mar 6, 2014
 */

app.controller('indexCtrl', function($scope){
	$scope.version = version;
});

app.controller('mainCtrl', function($scope, $routeParams, $window, $route, statusFactory, authFactory){
	$scope.urlStatus = $routeParams.status;
	$scope.path = $route.current.originalPath;
	setUpLoginForm();
	$scope.login = {};

	$scope.statuses = {};
	$scope.statuses.editable = 0;
	$scope.statuses.approved = 0;
	$scope.statuses.active = 0;
	$scope.statuses.backup = 0;
	$scope.statuses.history = 0;

	statusFactory.retrieveStatuses().then(function(result) {
		$scope.statuses.editable = result[0]['num'];
		$scope.statuses.approved = result[1]['num'];
		$scope.statuses.active = result[2]['num'];
		$scope.statuses.backup = result[3]['num'];
		$scope.statuses.history = result[4]['num'];
	});

	$scope.login = function() {
		authFactory.login($scope.login.username, $scope.login.password).then(function(data) {
			$window.location.reload();

		}, function(error) {
			$scope.login.message = error;
		});
	}

	$scope.logout = function() {
		authFactory.logout().then(function(data) {
			$window.location.reload();
		});
	}

	$scope.goTo = function(status) {

		if((status === "active" || status === "approved" || status === "backup") && $scope.statuses[status] === 0 ) {
			return;
		}

		$window.location = "#/status/" + status + "/tab/bm/bm/";
	}
});

app.controller('dataCtrl', function($scope, $routeParams, $route, $modal, $window, statusFactory){
	$scope.urlStatus = $routeParams.status;
	$scope.urlTab = $routeParams.tab;

	$scope.createDataset = function() {
		var modalInstance = $modal.open({
			templateUrl: 'modal/create_dataset.html',
			controller: 'createDatasetCtrl'
		});
	}

	$scope.approveDataset = function() {

		var modalInstance = $modal.open({
			templateUrl: 'modal/approve_dataset.html',
			controller: 'approveDatasetCtrl',
			resolve: {
				statuses: function() {
					return $scope.statuses;
				}
			}
		});
	}

	$scope.editDataset = function() {

		var modalInstance = $modal.open({
			templateUrl: 'modal/edit_dataset.html',
			controller: 'editDatasetCtrl',
			resolve: {
				statuses: function() {
					return $scope.statuses;
				}
			}
		});
	}

	$scope.activateDataset = function() {
		statusFactory.updateStatus({"status":aiStatusMap['approved'], "new_status":aiStatusMap['active'], "definition":"bm"}).then(function(data) {
			$window.location = "#/status/active/tab/bm/bm/";

		}, function(error) {
			l("error");
		});		
	}
});

/*
 * Bending magnet controller that displays anf manages everything connected to bending magnet table
 */
app.controller('bmCtrl', function($scope, $routeParams, bmFactory, logicFactory, BendingMagnet, $modal){
	$scope.error = {};
	$scope.bmArr = [];
	$scope.bmArr2 = [];
	$scope.logicArr = [];
	$scope.alert = {};
	var aiStatus = aiStatusMap[$routeParams.status];
	$scope.urlTab = $routeParams.tab;

	$scope.orderByField = 'id';
	$scope.reverseSort = false;

	// If status is not defined, skip this controller
	if ($routeParams.status === undefined) {
		return;
	}

	// Retrieve bending magnets
	bmFactory.retrieveItems({'ai_status': aiStatus}).then(function(result) {

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new BendingMagnet(item);
			$scope.bmArr.push(newItem);
		});

		bmNum = $scope.bmArr.length;
	});

	// Retrieve logic
	logicFactory.retrieveItems({'status': 3}).then(function(result) {

		$.each(result, function(i, item){

			// Build customized object
			$scope.logicArr.push(item.name);
		});
	});

	$scope.checkArrays = function() {

		if($scope.bmArr2.length === 0) {
			return;
		
		} else {

			$.each($scope.bmArr2, function(ind, obj) {
				$scope.bmArr.push(obj);
			});

			$scope.bmArr2 = [];
		}
	}

	$scope.newBm = undefined;

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	}

	$scope.addRow = function(item) {
		$scope.alert.show = false;

		if($scope.logicArr.length == 0) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = "Before adding new data, logic must be inserted and approved!";

			return;
		}

		$scope.newBm = new BendingMagnet();
		$scope.newBm.bm_type = "BPM";

		// Set properties if Copy&Create action
		if (item !== undefined) {
			$scope.newBm.set(item);
		}
		
		$('html, body').animate({ scrollTop: $(document).height() }, "fast");
	}

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
	}

	$scope.cancel = function() {
		$scope.newBm = undefined;
	}

	$scope.updateItem = function(device, typeName, propValue) {
		$scope.alert.show = false;

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

			return true;

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
			return false;
		});	
	}

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
			return true;

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
			return false;
		});	
	}

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
	}

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
	}

	$scope.saveItem = function(newItem) {
		$scope.alert.show = false;
		$scope.newBm = new BendingMagnet(newItem);
		$scope.newBm.ai_status = aiStatus;

		$scope.error = bmFactory.checkItem($scope.newBm);

		if (Object.keys($scope.error).length === 0) {
			$scope.newBm.updateProps();
			var promise = bmFactory.saveItem($scope.newBm);

			promise.then(function(data) {
				$scope.cancel();
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Data successfully saved!";

				bmFactory.retrieveItems({'ai_status': aiStatus, 'aid_id': data['id']}).then(function(result) {

					l(result);
					//$scope.bmArr = [];

					$.each(result, function(i, item){

						// Build customized object
						var newItem = new BendingMagnet(item);
						$scope.bmArr2.push(newItem);
					});

					bmNum = $scope.bmArr2.length;
				});
			
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
			$scope.alert.body = "Name and logic are mandatory!";
		}
	}
});

app.controller('idCtrl', function($scope, $routeParams, idFactory, logicFactory, InsertionDevice, $modal){
	$scope.error = {};
	$scope.idArr = [];
	$scope.idArr2 = [];
	$scope.logicArr = [];
	$scope.alert = {};
	var aiStatus = aiStatusMap[$routeParams.status];
	$scope.urlTab = $routeParams.tab;
	$scope.logicShapeDict = {};

	$scope.orderByField = 'id';
	$scope.reverseSort = false;

	// If status is not defined, skip this controller
	if ($routeParams.status === undefined) {
		return;
	}

	// Retrieve insertion devices
	idFactory.retrieveItems({'ai_status': aiStatus}).then(function(result) {

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new InsertionDevice(item);
			$scope.idArr.push(newItem);
		});

		idNum = $scope.idArr.length;
		l($scope.idArr);
	});

	// Retrieve logic
	logicFactory.retrieveItems({'status': 3}).then(function(result) {

		$.each(result, function(i, item){

			// Build customized object
			$scope.logicArr.push(item.name);
			$scope.logicShapeDict[item.name] = item.shape;
		});
	});

	$scope.checkArrays = function() {

		if($scope.idArr2.length === 0) {
			return;
		
		} else {

			$.each($scope.idArr2, function(ind, obj) {
				$scope.idArr.push(obj);
			});

			$scope.idArr2 = [];
		}
	}

	$scope.newInsD = undefined;

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	}

	$scope.addRow = function(item) {
		l("add row ");
		$scope.alert.show = false;

		if($scope.logicArr.length == 0) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = "Before adding new data, logic must be inserted and approved!";

			return;
		}

		$scope.newInsD = new InsertionDevice();

		// Set properties if Copy&Create action
		if (item !== undefined) {
			$scope.newInsD.setObj(item);
		}
		$('html, body').animate({ scrollTop: $(document).height() }, "fast");
	}

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
	}

	$scope.cancel = function() {
		$scope.newInsD = undefined;
	}

	$scope.updateItem = function(device, typeName, propValue) {
		$scope.alert.show = false;

		idFactory.updateItem({'aid_id': device.id, 'prop_type_name': typeName, 'value': propValue}).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Value successfully updated!";

			// Set status back to unapproved
			if (device.prop_statuses[typeName] === 3) {
				device.prop_statuses[typeName] = 2;
				device.prop_statuses.num_unapproved +=1;
			}

			return true;

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
			return false;
		});	
	}

	$scope.updateItemFixed = function(device, propName, propValue) {
		$scope.alert.show = false;

		var params = {};
		params['aid_id'] = device.id;
		params[propName] = propValue;

		idFactory.updateDevice(params).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Value successfully updated!";
			device.shape = $scope.logicShapeDict[device.logic];
			return true;

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
			return false;
		});	
	}

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
	}

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
	}

	$scope.saveItem = function(newItem) {
		$scope.alert.show = false;
		$scope.newInsD = new InsertionDevice(newItem);
		$scope.newInsD.ai_status = aiStatus;

		$scope.error = idFactory.checkItem($scope.newInsD);

		if (Object.keys($scope.error).length === 0) {
			$scope.newInsD.updateProps();
			var promise = idFactory.saveItem($scope.newInsD);

			promise.then(function(data) {
				$scope.cancel();
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Data successfully saved!";

				idFactory.retrieveItems({'ai_status': aiStatus, 'aid_id': data['id']}).then(function(result) {
					//$scope.idArr = [];

					$.each(result, function(i, item){

						// Build customized object
						var newItem = new InsertionDevice(item);
						$scope.idArr2.push(newItem);
					});
					l($scope.idArr2);

					idNum = $scope.idArr2.length;
				});
			
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
			$scope.alert.body = "Name and logic are mandatory!";
		}
	}
});

/*
 * Logic controller that displays logic and manages adding and updating logics
 */
app.controller('logicCtrl', function($scope, $routeParams, $modal, logicFactory, Logic){
	$scope.error = {};
	$scope.logicArr = [];
	$scope.alert = {};
	$scope.urlTab = $routeParams.tab;

	logicFactory.retrieveItems({}).then(function(result) {

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new Logic(item);
			$scope.logicArr.push(newItem);
		});
	});


	$scope.newLogic = undefined;

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	}

	$scope.addRow = function() {
		$scope.newLogic = new Logic();
	}

	$scope.deleteLogic = function(logicObj) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/delete_logic.html',
			controller: 'deleteLogicCtrl',
			resolve: {
				logic: function() {
					return logicObj;
				}
			}
		});
	}

	$scope.cancel = function() {
		$scope.newLogic = undefined;
	}

	$scope.saveItem = function(newItem) {
		$scope.alert.show = false;
		$scope.newLogic = new Logic(newItem);

		$scope.error = logicFactory.checkItem($scope.newLogic);

		if (Object.keys($scope.error).length === 0) {
			var promise = logicFactory.saveItem($scope.newLogic);

			promise.then(function(data) {
				$scope.cancel();
				$scope.alert.show = true;
				$scope.alert.success = true;
				$scope.alert.title = "Success!";
				$scope.alert.body = "Logic successfully saved!";

				logicFactory.retrieveItems({}).then(function(result) {

					$scope.logicArr = [];

					$.each(result, function(i, item){

						// Build customized object
						var newItem = new Logic(item);
						$scope.logicArr.push(newItem);
					});
				});
			
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
			$scope.alert.body = "Name is mandatory!";
		}
	}

	$scope.updateItem = function(logic, propKey, propValue) {
		$scope.alert.show = false;

		var payload = {'id': logic.id};
		payload[propKey] = propValue;

		logicFactory.updateItem(payload).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Value successfully updated!";
			logic.status = 2;
			return true;

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
			return false;
		});	
	}

	$scope.approveLogic = function(logicObj) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/approve_logic.html',
			controller: 'approveLogicCtrl',
			resolve: {
				logic: function() {
					return logicObj;
				}
			}
		});
	}

});

app.controller('historyCtrl', function($scope, headerFactory, History, $window){
	$scope.historyArr = [];

	headerFactory.retrieveHeader().then(function(result) {

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new History(item);
			$scope.historyArr.push(newItem);
		});
	});

	$scope.goTo = function(id) {
		$window.location = "#/dataset/" + id + "/tab/bm/bm/";
	}
});

/*
 * Create dataset controller
 */
app.controller('createDatasetCtrl', function($scope, $modalInstance, $window, headerFactory) {
	$scope.upload = {};
	$scope.upload.description = "";
	$scope.alert = {};
	$scope.showSaveButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		var promise = headerFactory.saveHeader($scope.upload.description);

		promise.then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Active interlock header successfully saved!";
			$scope.showSaveButton = false;
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
 * Approve cell controller
 */
app.controller('approveCellCtrl', function($scope, $modalInstance, $window, bmFactory, device, type_name) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		bmFactory.approveItem({'aid_id': device.id, 'prop_types': JSON.stringify([type_name])}).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Value successfully approved!";
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
		//$window.location.reload();

		// Set status to approved
		if (device.prop_statuses[type_name] === 2) {
			device.prop_statuses[type_name] = 3;
			device.prop_statuses.num_unapproved -=1;
		}

		$modalInstance.dismiss('cancel');
	};
});

/*
 * Approve row controller
 */
app.controller('approveRowCtrl', function($scope, $modalInstance, $window, bmFactory, device) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;
	var types = [];

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		// Gather properties than need to be approved
		$.each(device.prop_statuses, function(prop, status) {

			if (status === 2) {
				types.push(prop);
			}
		});

		bmFactory.approveItem({'aid_id': device.id, 'prop_types': JSON.stringify(types)}).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Row successfully approved!";
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
		//$window.location.reload();

		// Set status to approved
		// Gather properties than need to be approved
		$.each(device.prop_statuses, function(prop, status) {

			if (status === 2) {
				device.prop_statuses[prop] = 3;
				device.prop_statuses.num_unapproved = 0;
			}
		});

		$modalInstance.dismiss('cancel');
	};
});

/*
 * Approve dataset controller
 */
app.controller('approveDatasetCtrl', function($scope, $modalInstance, $window, statusFactory, statuses) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;
	var types = [];
	$scope.message = "The whole dataset will be approved. Do you want to continue?";

	if (statuses.approved > 0) {
		$scope.message = "There is a dataset with status approved. All data will be lost! Do you want to continue?";
	}

	if (idNum === 0 && bmNum === 0) {
		$scope.message = "Empty dataset cannot be approved!";
		$scope.showYesButton = false;
		$scope.showCancelButton = true;
		$scope.showFinishButton = false;
	}

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		statusFactory.updateStatus({"status":aiStatusMap['editable'], "new_status":aiStatusMap['approved'], "definition":"bm"}).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Dataset successfully approved!";
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
		$window.location = "#/status/approved/tab/bm/bm/";
		$modalInstance.dismiss('cancel');
	};
});

/*
 * Edit dataset controller
 */
app.controller('editDatasetCtrl', function($scope, $modalInstance, $window, statusFactory, statuses) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;
	var types = [];
	$scope.message = "The whole dataset will again be editable. Do you want to continue?";

	if (statuses.editable > 0) {
		$scope.message = "There is a dataset with status editable. All data will be lost! Do you want to continue?";
	}

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		statusFactory.updateStatus({"status":aiStatusMap['approved'], "new_status":aiStatusMap['editable'], "definition":"bm"}).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Dataset status successfully changed!";
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

/*
 * Retrieve dataset by id
 */

app.controller('historyDataCtrl', function($scope, $routeParams){
	$scope.urlTab = $routeParams.tab;
	$scope.datasetId = $routeParams.id;
});

app.controller('historyBmCtrl', function($scope, $routeParams, bmFactory, BendingMagnet){
	$scope.bmArr = [];
	$scope.urlTab = $routeParams.tab;

	$scope.orderByField = 'id';
	$scope.reverseSort = false;
	
	// Retrieve bending magnets
	bmFactory.retrieveItems({'ai_id': $scope.datasetId}).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new BendingMagnet(item);
			$scope.bmArr.push(newItem);
		});
	});
});

app.controller('historyIdCtrl', function($scope, $routeParams, idFactory, InsertionDevice){
	$scope.idArr = [];
	$scope.urlTab = $routeParams.tab;

	$scope.orderByField = 'id';
	$scope.reverseSort = false;
	
	// Retrieve insertion devices
	idFactory.retrieveItems({'ai_id': $scope.datasetId}).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new InsertionDevice(item);
			$scope.idArr.push(newItem);
		});
	});
});

app.controller('historyLogicCtrl', function($scope, $routeParams, logicFactory, Logic){
	$scope.logicArr = [];
	$scope.urlTab = $routeParams.tab;

	logicFactory.retrieveItems({}).then(function(result) {

		l(result);

		$.each(result, function(i, item){

			// Build customized object
			var newItem = new Logic(item);
			$scope.logicArr.push(newItem);
		});
	});
});

/*
 * Approve logic controller
 */
app.controller('approveLogicCtrl', function($scope, $modalInstance, $window, logicFactory, logic) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;
	var types = [];

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;


		logicFactory.updateItem({'id': logic.id, 'status': 3}).then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Logic successfully approved!";
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

		// Set status to approved
		logic.status = 3;
		$modalInstance.dismiss('cancel');
	};
});