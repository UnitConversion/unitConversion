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
	$scope.alert = {};
	$scope.view = $routeParams.view;
	$scope.inventory_id = $routeParams.inventory_id;
	$scope.inv = new Inventory();

	$scope.rcdColumns = {};
	$scope.rawRcdColumns = [];
	$scope.rcdHeaderColumns = ['alias', 'meas_coil_id', 'ref_radius', 'magnet_notes', 'login_name', 'cond_curr'];
	$scope.hpdColumns = {};
	$scope.rawHpdColumns = [];
	$scope.hpdHeaderColumns = ['alias', 'measured_at_location', 'run_identifier', 'login_name', 'conditioning_current'];

	$scope.firstRotCoilDataId = -1;
	$scope.rotCoilData = {};
	$scope.rotCoilData2 = {};

	$scope.firstHallProbeDataId = -1;
	$scope.hallProbeData = {};
	$scope.hallProbeData2 = {};

	$scope.measurementData = {
		'rot_coil_data': new RotCoilData(),
		'hall_probe_data': new HallProbeData()
	};

	// Return if there is no inventory name in the URL
	if(!$scope.inventory_id) {
		return;
	}

	$scope.newRCDs = {};
	$scope.numRCDs = 0;

	$scope.newHPDs = {};
	$scope.numHPDs = 0;

	// Retrieve all Inventory items
	inventoryFactory.retrieveItemById({'inventory_id': $scope.inventory_id}).then(function(result) {
		var ids = Object.keys(result);
		$scope.inv = new Inventory();
		$scope.inv.set(result);
		l($scope.inv);

		// Load rotation coil data columns
		if($scope.inv.__measurement_data_settings__ && $scope.inv.__measurement_data_settings__.rot_coil_data) {

			$.each($scope.inv.__measurement_data_settings__.rot_coil_data, function(column, columnObj) {

				// Map columns names to column display names
				if(columnObj.display_name && columnObj.display_name !== "") {
					$scope.rcdColumns[column] = columnObj.display_name;

				} else {
					$scope.rcdColumns[column] = column;
				}

				// Skip some columns
				if((column === 'id' || column === 'inventory_id' || $.inArray(column, $scope.rcdHeaderColumns) != -1) && $routeParams.view === 'readwrite') {
					return;
				}

				if(columnObj.displayed) {
					$scope.rawRcdColumns.push(column);
				}
			});
		}

		// Load hall probe data columns
		if($scope.inv.__measurement_data_settings__ && $scope.inv.__measurement_data_settings__.hall_probe_data) {

			$.each($scope.inv.__measurement_data_settings__.hall_probe_data, function(column, columnObj) {

				// Map columns names to column display names
				if(columnObj.display_name && columnObj.display_name !== "") {
					$scope.hpdColumns[column] = columnObj.display_name;

				} else {
					$scope.hpdColumns[column] = column;
				}

				// Skip some columns
				if((column === 'id' || column === 'inventory_id' || $.inArray(column, $scope.hpdHeaderColumns) != -1) && $routeParams.view === 'readwrite') {
					return;
				}

				if(columnObj.displayed) {
					$scope.rawHpdColumns.push(column);
				}
			});
		}

		rotCoilDataFactory.retrieveItems({'inventory_id': $scope.inv.id}).then(function(result) {
			// Delete everything in a table if a refresh happened during table creation.
			if(!isArrayEmpty(result) && !$scope.inv.__measurement_data_settings__.source['rot_coil_data']) {
				var promise = rotCoilDataFactory.deleteItem({'inventory_id': $scope.inv.id, 'rot_coil_data_id': undefined});

				promise.then(function(data) {
					l("Deleting RotCoilData table data after refresh successful.");

				}, function(error) {
					l("ERROR: " + error);
				});
			}
			// Normally load data.
			else {
				$scope.rotCoilData = result;
				l(result);

				if($scope.numElements(result) > 0) {
					$scope.firstRotCoilDataId = Object.keys(result)[0];
				}
			}
		});

		hallProbeDataFactory.retrieveItems({'inventory_id': $scope.inv.id}).then(function(result) {
			// Delete everything in a table if a refresh happened during table creation.
			if(!isArrayEmpty(result) && !$scope.inv.__measurement_data_settings__.source['hall_probe_data']) {
				var promise = hallProbeDataFactory.deleteItem({'inventory_id': $scope.inv.id, 'hall_probe_data_id': undefined});

				promise.then(function(data) {
					l("Deleting HallProbeData table data after refresh successful.");

				}, function(error) {
					l("ERROR: " + error);
				});
			}
			// Normally load data.
			else {
				$scope.hallProbeData = result;
				l(result);

				if($scope.numElements(result) > 0) {
					$scope.firstHallProbeDataId = Object.keys(result)[0];
				}
			}

		});	
	});

	$scope.numElements = function(obj) {
		return parseInt(Object.keys(obj).length);
	};

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.paste = function(mdIndex, prop, index, event, sourceTable) {
		var pastedData = event.originalEvent.clipboardData.getData('text/plain').split('\n');
		event.preventDefault();

		var rowKeys;

		if(sourceTable === 'rot_coil_data') {
			rowKeys = Object.keys($scope.newRCDs);

		} else {
			rowKeys = Object.keys($scope.newHPDs);
		}

		var rowIndex = $.inArray(mdIndex, rowKeys);

		if(pastedData.length > 0) {

			for(var j=0; j<pastedData.length; j++) {
				row = pastedData[j].split('\t');
				var columnIndex = 0;

				// Skip empty pasted rows
				if(row.length <= 1 && row[0] !== undefined && row[0] === "") {
					continue;
				}

				// Create new row if it does not exist
				if(!rowKeys[rowIndex]) {
					$scope.addRow(undefined, sourceTable);

					if(sourceTable === 'rot_coil_data') {
						rowKeys = Object.keys($scope.newRCDs);

					} else {
						rowKeys = Object.keys($scope.newHPDs);
					}
				}

				var cellValue;

				if(sourceTable === 'rot_coil_data') {

					for(var i=index; i<$scope.rawRcdColumns.length; i++) {

						if(row[columnIndex] !== undefined) {

							cellValue = row[columnIndex];

							// Check if value is numberic and parse it as float
							if($.isNumeric(cellValue)) {
								cellValue = parseFloat(cellValue);
							}

							$scope.newRCDs[rowKeys[rowIndex]][$scope.rawRcdColumns[i]] = cellValue;
						}
						columnIndex ++;
					}

				} else {

					for(var i2=index; i2<$scope.rawHpdColumns.length; i2++) {

						if(row[columnIndex] !== undefined) {

							cellValue = row[columnIndex];

							// Check if value is numberic and parse it as float
							if($.isNumeric(cellValue)) {
								cellValue = parseFloat(cellValue);
							}

							$scope.newHPDs[rowKeys[rowIndex]][$scope.rawHpdColumns[i2]] = cellValue;
						}
						columnIndex ++;
					}
				}

				rowIndex ++;
			}
		}
	};

	$scope.addRow = function(item, sourceTable) {
		$scope.alert.show = false;
		var md;

		if(sourceTable === 'rot_coil_data') {
			md = new RotCoilData();

		} else {
			md = new HallProbeData();
		}

		// Set properties if Copy&Create action
		if (item !== undefined) {
			md.set(item);
		}

		// Set inventory name
		md.inventory_id = $scope.inventory_id;

		var key = $.now();

		if(sourceTable === 'rot_coil_data') {
			// Make key unique
			while($scope.newRCDs[key] !== undefined) {
				key++;
			}

			$scope.newRCDs[key] = md;
			$scope.numRCDs ++;

		} else {
			// Make key unique
			while($scope.newHPDs[key] !== undefined) {
				key++;
			}

			$scope.newHPDs[key] = md;
			$scope.numHPDs ++;
		}

		//$('html, body').animate({ scrollTop: $(document).height() }, "fast");
	};

	$scope.closeTable = function(sourceTable) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/close_table.html',
			controller: 'closeDataCtrl',
			resolve: {
				device: function() {
					return undefined;
				},
				source: function() {
					return sourceTable;
				},
				inventory_obj: function() {
					return $scope.inv;
				}
			}
		});
	};

	$scope.deleteTable = function(sourceTable) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/delete_data.html',
			controller: 'deleteDataCtrl',
			resolve: {
				device: function() {
					return undefined;
				},
				source: function() {
					return sourceTable;
				},
				inventory_obj: function() {
					return $scope.inv;
				},
				data_scope: function() {
					return $scope;
				}
			}
		});
	};

	$scope.deleteRow = function(deviceObj, sourceTable) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/delete_data.html',
			controller: 'deleteDataCtrl',
			resolve: {
				device: function() {
					return deviceObj.id;
				},
				source: function() {
					return sourceTable;
				},
				inventory_obj: function() {
					return $scope.inv;
				},
				data_scope: function() {
					return $scope;
				}
			}
		});
	};

	$scope.manageColumns = function(sourceTable, button) {

		var modalInstance = $modal.open({
			templateUrl: 'modal/update_measurement_data_columns.html',
			controller: 'manageMeasurementDataColumnsCtrl',
			resolve: {
				source: function() {
					return sourceTable;
				},
				inventory_obj: function() {
					return $scope.inv;
				},
				button: function() {
					return button;
				}
			}
		});
	};

	$scope.generateColumns = function(sourceTable) {

		// If settings does not exist, create them
		if(!$scope.inv.__measurement_data_settings__) {
			$scope.inv.__measurement_data_settings__ = {};
		}

		$scope.inv.__measurement_data_settings__[sourceTable] = {};

		var columnList = $scope.measurementData[sourceTable].retrieve;

		$.each(columnList, function(i, column) {

			if(column === 'inventory_id' || column === 'sub_device') {
				$scope.inv.__measurement_data_settings__[sourceTable][column] = {'display_name': '', 'displayed': true};

			} else {
				$scope.inv.__measurement_data_settings__[sourceTable][column] = {'display_name': '', 'displayed': false};
			}
		});

		// Set table to visible
		if(!$scope.inv.__measurement_data_settings__.source) {
			$scope.inv.__measurement_data_settings__.source = {};
		}

		$scope.inv.__measurement_data_settings__.source[sourceTable] = true;

		l($scope.inv.__measurement_data_settings__);

		// Open new window with column manager
		$scope.manageColumns(sourceTable, true);

		// Create header item
		var headerItem;

		if(sourceTable === 'rot_coil_data') {
			headerItem = new RotCoilData();

		} else {
			headerItem = new HallProbeData();
		}
		headerItem.sub_device = $scope.inv.id;
		headerItem.inventory_id = $scope.inv.id;

		$scope.addRow(headerItem, sourceTable);
		$scope.saveItem(0, headerItem, sourceTable);
	};

	$scope.cancel = function(sourceTable) {

		if(sourceTable === 'rot_coil_data') {
			$scope.newRCDs = {};
			$scope.numRCDs = 0;

		} else {
			$scope.newHPDs = {};
			$scope.numHPDs = 0;
		}
	};

	$scope.updateItem = function(device, typeName, propValue, sourceTable) {
		$scope.alert.show = false;
		var promise;
		var params;

		if(sourceTable === 'rot_coil_data') {
			params = {};
			params.rot_coil_data_id = device.id;
			params[typeName] = propValue;
			promise = rotCoilDataFactory.updateItem(params);

		} else {
			params = {};
			params.hall_probe_id = device.id;
			params[typeName] = propValue;
			promise = hallProbeDataFactory.updateItem(params);
		}

		promise.then(function(data) {
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
			device[typeName] = undefined;
			return false;
		});
	};

	$scope.saveItems = function(sourceTable) {

		if(sourceTable === 'rot_coil_data') {

			$.each($scope.newRCDs, function(i, newItem) {
				$scope.saveItem(i, newItem, sourceTable);
			});

		} else {
			$.each($scope.newHPDs, function(i, newItem) {
				$scope.saveItem(i, newItem, sourceTable);
			});
		}
	};

	$scope.saveItem = function(newItemIndex, newItem, sourceTable) {
		$scope.alert.show = false;
		$scope.error = {};

		if(sourceTable === 'rot_coil_data') {
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

			if(sourceTable === 'rot_coil_data') {
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

				if(sourceTable === 'rot_coil_data') {
					promise = rotCoilDataFactory.retrieveItems({'inventory_id': $scope.inv.id});

				} else {
					promise = hallProbeDataFactory.retrieveItems({'inventory_id': $scope.inv.id});
				}

				promise.then(function(result) {

					$.each(result, function(index, obj) {

						if(sourceTable === 'rot_coil_data') {

							if(!(index in $scope.rotCoilData)) {
								$scope.rotCoilData2[index] = obj;
							}

						} else {

							if(!(index in $scope.hallProbeData)) {
								$scope.hallProbeData2[index] = obj;
							}
						}
					});
				});

				$timeout(function() {$scope.closeAlert();}, alertTimeout);

			}, function(error) {
				$scope.alert.show = true;
				$scope.alert.success = false;
				$scope.alert.title = "Error!";
				$scope.alert.body = error;
			});

			if(sourceTable === 'rot_coil_data') {
				delete $scope.newRCDs[newItemIndex];
				$scope.numRCDs --;

			} else {
				delete $scope.newHPDs[newItemIndex];
				$scope.numHPDs --;
			}


		} else {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = $scope.error;
		}
	};
});

/*
 * Delete data controller
 */
app.controller('deleteDataCtrl', function($scope, $modalInstance, $window, RotCoilData, HallProbeData, inventoryFactory, rotCoilDataFactory, hallProbeDataFactory, device, source, inventory_obj, data_scope) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		var promise;

		if(source === 'rot_coil_data') {
			promise = rotCoilDataFactory.deleteItem({'inventory_id': inventory_obj.id, 'rot_coil_data_id': device});

		} else {
			promise = hallProbeDataFactory.deleteItem({'inventory_id': inventory_obj.id, 'hall_probe_id': device});
		}

		promise.then(function(data) {

			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Data successfully deleted!";
			$scope.showYesButton = false;
			$scope.showCancelButton = false;
			$scope.showFinishButton = true;

			// Create header item
			if(!device) {

				// Create header item
				var headerItem;

				if(source === 'rot_coil_data') {
					headerItem = new RotCoilData();

				} else {
					headerItem = new HallProbeData();
				}
				headerItem.sub_device = inventory_obj.id;
				headerItem.inventory_id = inventory_obj.id;

				data_scope.addRow(headerItem, source);
				data_scope.saveItem(0, headerItem, source);
			}

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
 * Close table controller
 */
app.controller('closeDataCtrl', function($scope, $modalInstance, $window, inventoryFactory, rotCoilDataFactory, hallProbeDataFactory, device, source, inventory_obj) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		$scope.alert.show = false;

		var promise;

		if(source === 'rot_coil_data') {
			promise = rotCoilDataFactory.deleteItem({'inventory_id': inventory_obj.id, 'rot_coil_data_id': device});

		} else {
			promise = hallProbeDataFactory.deleteItem({'inventory_id': inventory_obj.id, 'hall_probe_id': device});
		}

		promise.then(function(data) {

			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Table closed and data successfully deleted!";
			$scope.showYesButton = false;
			$scope.showCancelButton = false;
			$scope.showFinishButton = true;

			// Set table view to false
			if(!device) {

				var propsObject = {};
				$scope.element = inventory_obj;
				$scope.element.__measurement_data_settings__.source[source] = false;

				$scope.element.prop_keys.push({'name': '__measurement_data_settings__', 'value': $scope.element.__measurement_data_settings__});

				$.each($scope.element.prop_keys, function(i, prop) {
					propsObject[prop.name] = prop.value;
				});

				$scope.element.props = JSON.stringify(propsObject);

				// Set old name so we can update
				$scope.element.inventory_id = $scope.element.id;

				l($scope.element);
				l(source);
				inventoryFactory.updateItem($scope.element);
			}

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
 * Manage measurement data columns controller
 */
app.controller('manageMeasurementDataColumnsCtrl', function($scope, $modalInstance, $window, RotCoilData, HallProbeData, inventoryFactory, source, inventory_obj, button, rotCoilDataFactory, hallProbeDataFactory) {
	$scope.alert = {};
	$scope.showYesButton = true;
	$scope.showCancelButton = true;
	$scope.showFinishButton = false;
	$scope.element = inventory_obj;
	$scope.sourceTable = source;

	$scope.measurementData = {
		'rot_coil_data': new RotCoilData(),
		'hall_probe_data': new HallProbeData()
	};

	$scope.closeAlert = function() {
		$scope.alert.show = false;
	};

	$scope.ok = function() {
		var propsObject = {};
		$scope.alert.show = false;

		$scope.element.prop_keys.push({'name': '__measurement_data_settings__', 'value': $scope.element.__measurement_data_settings__});

		$.each($scope.element.prop_keys, function(i, prop) {
			propsObject[prop.name] = prop.value;
		});

		$scope.element.props = JSON.stringify(propsObject);

		// Set old name so we can update
		$scope.element.inventory_id = $scope.element.id;

		var promise = inventoryFactory.updateItem($scope.element);

		promise.then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Data successfully saved!";
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
		l("Preform delete function on X button: " + button);
		if(button) {
			$scope.cancelDestroy();
		}
		else {
			$modalInstance.dismiss('cancel');
		}
	};

	$scope.cancelDestroy = function() {
		var promise;

		if(source === 'rot_coil_data') {
			promise = rotCoilDataFactory.deleteItem({'inventory_id': inventory_obj.id, 'rot_coil_data_id': undefined});

		} else {
			promise = hallProbeDataFactory.deleteItem({'inventory_id': inventory_obj.id, 'hall_probe_id': undefined});
		}

		promise.then(function(data) {
			l("Deleting table data successful.");

		}, function(error) {
			l("ERROR: " + error);
		});
		$window.location.reload();
	};

	$scope.finish = function() {
		$window.location.reload();
		$modalInstance.dismiss('cancel');
	};
});