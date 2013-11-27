/*
 * Helper functions for Unit Conversion client
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

$(document).ready(function(){
	// Create new comparator
	jQuery.expr[':'].Contains = function(a, i, m) {
		return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
	};
});

// Global plot variable
var plot = undefined;

/**
 * Write logs to Chrome or Firefox console
 * @param input input string
 */
function l(input) {

	if(writeLogs === true) {
		console.log(input);
	}
}

/**
 * Trim spaces from the start and the end of the string
 * @param {type} str input string
 * @returns {unresolved} string without spaces in the start and at the end of string
 */
function trim(str) {
	str = str.replace(/^\s+/, '');
	for (var i = str.length - 1; i >= 0; i--) {
		if (/\S/.test(str.charAt(i))) {
			str = str.substring(0, i + 1);
			break;
		}
	}
	return str;
}

/**
 * Check if elements is present in the current DOM or not
 * @returns {Boolean}
 */
jQuery.fn.doesExist = function(){
	return jQuery(this).length > 0;
};

/**
 * Create query for listing lattice
 * @param {type} search search or $routeParams object
 * @param {boolean} returnUrl return url or query
 * @returns {String} return url or query string
 */
function createLatticeListQuery(search, returnUrl) {
	var query = "";
	var url = "#";

	// Add type
	url += "/type/" + search.type;

	if(search.type === "lattice") {

		// Add name part
		if(search.name !== undefined) {
			query += "name=" + search.name + '&';
			url += "/name/" + search.name;

		} else {
			query += "name=*&";
			url += "/name/";
		}

		// Add version part
		if(search.version !== undefined) {
			query += "version=" + search.version + '&';
			url += "/version/" + search.version;

		} else {
			query += "version=*&";
			url += "/version/";
		}

		// Add branch part
		if(search.branch !== undefined) {
			query += "branch=" + search.branch + '&';
			url += "/branch/" + search.branch;

		} else {
			query += "branch=*&";
			url += "/branch/";
		}

		// Add description part
		if(search.desc !== undefined) {
			query += "description=" + search.desc + '&';
			url += "/desc/" + search.desc;

		} else {
			query += "description=*&";
			url += "/desc/";
		}

		// Add creator part
		if(search.creator !== undefined) {
			query += "creator=" + search.creator + '&';
			url += "/creator/" + search.creator;

		} else {
			query += "creator=*&";
			url += "/creator/";
		}

		// Add lattice type part
		if(search.latticetype !== undefined) {
			query += 'latticetype={"name":"' + search.latticetype + '"}';
			url += "/latticetype/" + search.latticetype;

		} else {
			query += "";
			url += "/latticetype/";
		}

		// Add status part
//		if(search.status !== undefined) {
//			query += "status=" + search.status;
//			url += "/status/" + search.status;
//
//		} else {
//			query += "status=*";
//			url += "/status/";
//		}
	}

	// Return URL or query
	if(returnUrl) {
		return url;

	} else {
		return query;
	}
}

/**
 * Create query for listing models
 * @param {type} search search or $routeParams object
 * @param {boolean} returnUrl return url or query
 * @returns {String} return url or query string
 */
function createModelListQuery(search, returnUrl) {
	var query = "";
	var url = "#";

	// Add type
	url += "/type/" + search.type;

	if(search.type === "model") {

		// Add name part
		if(search.name !== undefined) {
			query += "name=" + search.name;
			url += "/name/" + search.name;

		} else {
			query += "name=*";
			url += "/name/";
		}
	}

	// Return URL or query
	if(returnUrl) {
		return url;

	} else {
		return query;
	}
}

/*
 * Create modal window on top of the web app
 * Example of use: createModal($modal, $scope);
 */
function createModal(modal, scope) {
	var modalInstance = modal.open({
		template: '\n\
		<div class="modal-header">\n\
			<h3>Im a modal!</h3>\n\
		</div>\n\
		<div class="modal-body">\n\
		body\n\
		</div>\n\
		<div class="modal-footer">\n\
			<button class="btn btn-primary" ng-click="ok()">OK</button>\n\
			<button class="btn btn-warning" ng-click="cancel()">Cancel</button>\n\
		</div>\n\
		',
		controller: "modalCtrl"
	});

	modalInstance.result.then(function(selectedItem) {
		scope.selected = selectedItem;
	}, function() {
		l("modal dismissed");
	});
}

/*
 * Retun first X characters from the string.
 * @param {type} string input string
 * @param {type} count how many characters do we want to return
 * @returns {String} First X words
 */
function returnFirstXCharacters(string, count){

	if(string.length > count) {
		return string.substring(0, count) + " ...";

	} else {
		return string;
	}
}

function checkLatticeFormat(lattices) {
	var keys = Object.keys(lattices[0].data);
	var format = lattices[0].data[keys[0]].latticeFormat;
	var equalFormat = true;

	$.each(lattices, function(i, lattice){
		keys = Object.keys(lattice.data);

		if(lattice.data[keys[0]].latticeFormat !== format) {
			equalFormat = false;
		}
	});

	return equalFormat;
}

function checkDiff(keys) {

	//l(keys);

	if(JSON.stringify(keys[0]) === JSON.stringify(keys[1])) {
		return "diff_green";

	} else {
		return "diff_red";
	}
}

/*
 * Create lattice data table
 * @param {type} header array of header columns
 * @param {type} lattice lattice object data
 * @param {type} url lattice raw file url
 * @returns {String} html string
 */
function createLatticeTable(header, lattice, url) {
	// Add header
	var table = "<tr>";

	$.each(header, function(i, column){
		table += "<th>" + column.charAt(0).toUpperCase() + column.slice(1) + "</th>";
	});

	table += "</tr>";

	// Add data
	$.each(lattice, function(j, line){

		// Skip rows that are not lattice
		if(j === "columns" || j === "typeunit") {
			return;
		}

		table += "<tr class='lattice_table_row'>";

		$.each(header, function(i, column){

			if(line[column] === undefined) {
				table += "<td></td>";

			} else {

				// Ckeck for file links
				if(column.indexOf("file") !== -1 || column.indexOf("FILE") !== -1) {
					var fileName = line[column][0].replace(/"/gi, "");
					var urlParts = url.split("/");
					var mapUrl = urlParts.slice(0, urlParts.length-1).join("/") + '_map/';
					table += '<td><a target="_blank" href="' + mapUrl + fileName + '">' + fileName + '</a></td>';

				} else {
					table += "<td>" + line[column] + "</td>";
				}
			}
		});

		table += "</tr>";
	});

	return table;
}

function createLatticeComparinsonRows(latticesData, key) {
	var html = "";

	$.each(latticesData[key].data, function(i, latticeLine) {
		var deviceKeys = [];
		var deviceName = latticeLine.name;
		var keysRaw = {};

		if(deviceName === undefined) {
			return;
		}

		// Skip if this line heas already been compared
		if(latticeLine['compared'] === true) {
			return;
		}

		html += "<tr><td class='lattice_table2_row'>" + i + "</td>";

		$.each(latticesData, function(k, lattice) {
			var keys = [];

			$.each(lattice.keys, function(j, header) {

				if(header === "name" || header === "id") {
					return;
				}

				// Add property to object
				if(!(header in keysRaw)) {
					keysRaw[header] = {};
					keysRaw[header]['valid'] = Object.keys(latticesData).length;
				}

				if(lattice.data[deviceName] !== undefined) {
					lattice.data[deviceName]['compared'] = true;

					if(lattice.data[deviceName][header] === undefined) {
						keys.push(header + "=");
						// Add lattice value
						keysRaw[header][k] = "";

					} else {
						keys.push(header + "=" + lattice.data[deviceName][header]);
						// Add lattice value
						keysRaw[header][k] = lattice.data[deviceName][header];

						// Every ok entry should substract 1 from valid. If we get 0 at the end, we got values from all lattices we compare
						keysRaw[header]['valid'] = keysRaw[header]['valid'] - 1;
					}
				}
			});

			deviceKeys.push(keys);

			html += "<td>" + keys.join(", ") + "</td>";
		});

		var cssClass = checkDiff(deviceKeys);

		html += "<td ng-click='diffDetails(\"" + deviceName + "\")' class='diff_details " + cssClass + "'><i class='parent_" + deviceName + " icon-chevron-up'></i></td>";

		html += "</tr>";


		l(keysRaw);

		$.each(keysRaw, function(j, latticeData) {

			if(j === "name" || j === "id") {
				return;
			}

			if(latticeData['valid'] > 1) {
				return;
			}

			var tds = "";
			var tmpValue = "";
			var diff = 0;

			$.each(latticeData, function(latticeName, latticeValue) {

				if(latticeName === "valid" || latticeName === "diff") {
					return;
				}

				if(latticeValue !== tmpValue) {
					diff ++;
				}

				tmpValue = latticeValue;

				tds += "<td>" + latticeValue + "</td>";

			});

			var rowBackground = "compare_children";

			if(diff > 1) {
				rowBackground = "diff_orange";
			}

			html += "<tr class='" + rowBackground + " children_" + deviceName + "' style='display:none;'>";

			html += "<td>" + j + "</td>";

			html += tds;

			html += "<td></td>";

			html += "</tr>";
		});


	});

	return html;
}

/**
 * Compare particular device in both lattices and create array that will serve as basis for the table
 * @param {type} latticesData
 * @param {type} latticesKeys
 * @param {type} key
 * @param {type} device
 * @returns {createLatticeComparisonDetails.detailsData|Array}
 */
function createLatticeComparisonDetails(latticesData, latticesKeys, key, device) {
	var firstLatticeProperties = latticesData[key].keys;
	var firstLatticeDeviceData = latticesData[key].data[device];
	var detailsData = [];

	// Go through properties from the first lattice
	if(firstLatticeDeviceData !== undefined) {

		$.each(firstLatticeProperties, function(i, property) {

			// Continue if property was already displayed
			if(
				latticesData[key].data[device].displayed !== undefined &&
				latticesData[key].data[device].displayed[property] !== undefined &&
				latticesData[key].data[device].displayed[property] === true
			) {
				return;
			}

			// Continue if we are at id property
			if(property === "id") {
				return;
			}

			var detailsDataEntry = {};
			detailsDataEntry["property"] = property;
			detailsDataEntry["color"] = "";

			var value = latticesData[key].data[device][property];
			var valuesEqual = true;
			var valueEmpty = 0;

			// Go through all the lattices
			$.each(latticesKeys, function(i, key) {

				if(latticesData[key].data[device] !== undefined && latticesData[key].data[device].displayed === undefined) {
					latticesData[key].data[device].displayed = {};
				}

				if(latticesData[key].data[device] !== undefined && latticesData[key].data[device][property] !== undefined) {
					detailsDataEntry[key] = latticesData[key].data[device][property];
					latticesData[key].data[device].displayed[property] = true;

					if(detailsDataEntry[key] !== value) {
						valuesEqual = false;
					}

				} else {
					detailsDataEntry[key] = "";

					if(latticesData[key].data[device] !== undefined) {
						latticesData[key].data[device].displayed[property] = true;
					}
				}

				// Check if value is ampty or null or undefined
				if(detailsDataEntry[key] === "" || detailsDataEntry[key] === undefined || detailsDataEntry[key] === null) {
					valueEmpty += 1;
				}
			});

			// Change color for row with equal values
			if(!valuesEqual) {
				detailsDataEntry["color"] = "diff";
			}

			l(valueEmpty);
			l(detailsDataEntry[key]);

			// Push not empty rows to array
			//if(valueEmpty <= 1) {
				detailsData.push(detailsDataEntry);
			//}

			// Reset empty counter
			valueEmpty = 0;
		});
	}

	return detailsData;
}

function createModelDetailsUrl(search, modelName) {
	var detail = search.detail;

	if(detail === undefined) {
		detail = "*";
	}

	var from = search.from;

	if(from === undefined) {
		from = "0";
	}

	var to = search.to;

	if(to === undefined) {
		to = "1";
	}

	return serviceurl + 'lattice/?function=' + detail + '&modelname=' + modelName + '&from=' + from + '&to=' + to;
}

function transformModelDetails(data) {
	var modelNames = Object.keys(data);
	l(data[modelNames[0]]);
	var header = [];

	if(data[modelNames[0]].index === undefined) {
		data[modelNames[0]].index = data[modelNames[0]].order;
	}

	header.push("index");

	var columns = Object.keys(data[modelNames[0]]);


	$.each(columns, function(i, column) {

		if(column === "transferMatrix" || column === "order" || column === "index") {
			return;
		}

		header.push(column);
	});

	var outputData = data[modelNames[0]];

	return [modelNames[0], header, outputData];
}

function createPropertySelectionTable(headerRows, modelName, selection) {

	$.each(headerRows, function(i, head) {

		if(head === "index" || head === "position" || head === "name") {
			return;
		}

		if(modelName in selection) {
			selection[modelName][head] = false;

		} else {
			selection[modelName] = {};
			selection[modelName][head] = false;
		}
	});

	return selection;
}

/*
 * Clean headers array of index, position and name headers and create selection object
 * @param {type} headers array of headers that needs to be cleaned
 * @returns {filterPropertySelectionTable.properties|Array} filtered properties
 */
function filterPropertySelectionTable(modelName, headers) {
	var properties = {};
	var modelHeaders = headers[modelName];
	properties[modelName] = {};

	$.each(modelHeaders, function(i, header) {

		if(header === "index" || header === "position" || header === "name") {
			return;
		}

		properties[modelName][header] = false;
	});

	return properties;
}

/**
 * @param {type} filters Object with filter data
 * @param {type} name of the element that contains data
 * @param {string} table selector of the table we are filtering
 */
function filterTableItems(filters, name, table){

	var filter = filters.deviceName.toLowerCase();
	l(filter);

	var cells = $(table).find(name);

	$.each(cells, function(i, cell) {
		var parentElement = $(cell).parent();
		var diffElement = parentElement.find('.diff_details');
		var value = $(cell).text().toLowerCase();
		var visible = true;

		//l(parentElement);
		//l(diffElement);
		//l(value);

		if(filters.showOnlyDifferent === true && diffElement[0].className.indexOf('diff_red') === -1) {
			visible = false;
		}

		if(visible && value.indexOf(filter) === -1) {
			visible = false;
		}

		if(visible) {
			parentElement.slideDown();

		} else {
			parentElement.slideUp();
		}
	});

	// Slide up items that does not contain filters and are not selected
	//$(table).find(name + ':not(:Contains(' + filter + ')):not(.multilist_clicked)').parent().slideUp();
	//$(table).find(name + ':Contains(' + filter + ')').parent().slideDown();
}

/**
 * Create plot from the two vectors from measurement data table
 * @param {type} data measurement data object
 * @param {type} x_axis measurement data object property that should be put on the x axis
 * @param {type} y_axis measurement data object property that should be put on the y axis
 * @param {type} newSeries array of conversion result points that should be put on the plot together with measurement data
 * @param {type} scope $scope object
 */
function drawPlot(placeholder, selection, data, nameToIdMap, x_axis, y_axis){
	l(data);

	var container = $(placeholder);
	container.addClass("placeholder_hidden");

	var series = [];

	$.each(selection, function(prop, select) {
		l(prop);
		l(select);

		$.each(select, function(moduleName, checked) {

			// Property selected for specific module name
			if(checked === true) {
				var seriesData = createSeries(data[moduleName]['position'], data[moduleName][prop]);
				// Add series of conversion points

				var seriesLabel = "";

				if(nameToIdMap !== undefined){
					seriesLabel = nameToIdMap[moduleName] + ", " + prop;

				} else {
					seriesLabel = prop;
				}
				series.push({label: seriesLabel, lines: { show: true }, points: { show: true }, data: seriesData});
			}
		});
	});

	l(series);

	// Plot options
	var optionsFlot = {
		legend: {
			show: true,
			position: "nw"
		},
		xaxis: {
			tickDecimals: 4
		},
		yaxis: {
			tickDecimals: 4
		},
		zoom: {
			interactive: true
		},
		pan: {
			interactive: true
		},
		grid: {
			hoverable: true
		}
	};

	// We have at least one series
	if(series.length > 0) {
		container.removeClass("placeholder_hidden");

		// Initialize plot
		var flotPlot = $.plot(container, series, optionsFlot);

		// Create y axis labe
		var yaxisLabel = $("<div class='axisLabel yaxisLabel'></div>")
			.text(y_axis)
			.appendTo(container);
		yaxisLabel.css("margin-top", yaxisLabel.width() / 2 - 20);

		// Create x axis label
		var xaxisLabel = $("<div class='axisLabel xaxisLabel'></div>")
			.text(x_axis)
			.appendTo(container);
		xaxisLabel.css("margin-left", xaxisLabel.width() / 2 - 30);

		// Create zoom out button
		$("<div class='zoom zoom_out'></div>")
			.appendTo(container)
			.click(function (event) {
				event.preventDefault();
				flotPlot.zoomOut();
			}
		);

		// Create zoom in button
		$("<div class='zoom zoom_in'></div>")
			.appendTo(container)
			.click(function (event) {
				event.preventDefault();
				flotPlot.zoom();
			}
		);

		// Create pan arrows
		addArrow("up", {top: -100}, container, flotPlot);
		addArrow("left", {left: -100}, container, flotPlot);
		addArrow("down", {top: 100}, container, flotPlot);
		addArrow("right", {left: 100}, container, flotPlot);

		// Create tooltips when hovering over points
		container.bind("plothover", function (event, pos, item) {

			if (item) {
				$("#tooltip").remove();
				var x = item.datapoint[0].toFixed(4);
				var y = item.datapoint[1].toFixed(4);
				showTooltip(item.pageX, item.pageY, x + ", " + y);

			} else {
				$("#tooltip").remove();
			}
		});

	}
}

function drawPlotTransposed(placeholder, selection, data, nameToIdMap, x_axis, y_axis){
	l(data);

	var container = $(placeholder);
	container.addClass("placeholder_hidden");

	var series = [];

	$.each(selection, function(moduleName, select) {
		l(select);

		$.each(select, function(prop, checked) {

			// Property selected for specific module name
			if(checked === true) {
				var seriesData = createSeries(data[moduleName]['position'], data[moduleName][prop]);
				// Add series of conversion points

				var seriesLabel = "";

				if(nameToIdMap !== undefined){
					seriesLabel = nameToIdMap[moduleName] + ", " + prop;

				} else {
					seriesLabel = prop;
				}
				series.push({label: seriesLabel, lines: { show: true }, points: { show: true }, data: seriesData});
			}
		});
	});

	l(series);

	// Plot options
	var optionsFlot = {
		legend: {
			show: true,
			position: "nw"
		},
		xaxis: {
			tickDecimals: 4
		},
		yaxis: {
			tickDecimals: 4
		},
		zoom: {
			interactive: true
		},
		pan: {
			interactive: true
		},
		grid: {
			hoverable: true
		}
	};

	// We have at least one series
	if(series.length > 0) {
		container.removeClass("placeholder_hidden");

		// Initialize plot
		var flotPlot = $.plot(container, series, optionsFlot);

		// Create y axis labe
		var yaxisLabel = $("<div class='axisLabel yaxisLabel'></div>")
			.text(y_axis)
			.appendTo(container);
		yaxisLabel.css("margin-top", yaxisLabel.width() / 2 - 20);

		// Create x axis label
		var xaxisLabel = $("<div class='axisLabel xaxisLabel'></div>")
			.text(x_axis)
			.appendTo(container);
		xaxisLabel.css("margin-left", xaxisLabel.width() / 2 - 30);

		// Create zoom out button
		$("<div class='zoom zoom_out'></div>")
			.appendTo(container)
			.click(function (event) {
				event.preventDefault();
				flotPlot.zoomOut();
			}
		);

		// Create zoom in button
		$("<div class='zoom zoom_in'></div>")
			.appendTo(container)
			.click(function (event) {
				event.preventDefault();
				flotPlot.zoom();
			}
		);

		// Create pan arrows
		addArrow("up", {top: -100}, container, flotPlot);
		addArrow("left", {left: -100}, container, flotPlot);
		addArrow("down", {top: 100}, container, flotPlot);
		addArrow("right", {left: 100}, container, flotPlot);

		// Create tooltips when hovering over points
		container.bind("plothover", function (event, pos, item) {

			if (item) {
				$("#tooltip").remove();
				var x = item.datapoint[0].toFixed(4);
				var y = item.datapoint[1].toFixed(4);
				showTooltip(item.pageX, item.pageY, x + ", " + y);

			} else {
				$("#tooltip").remove();
			}
		});

	}
}

function createSeries(xData, yData) {
	l(xData);
	l(yData);

	var data = [];

	$.each(xData, function(i, x) {
		data.push([x, yData[i]]);
	});

	return data;
}

function addArrow(classNamePart, offset, placeholder, plot) {
	$("<div class='pan pan_" + classNamePart + "'></div>")
		.appendTo(placeholder)
		.click(function (e) {
			e.preventDefault();
			plot.pan(offset);
		});
}

function showTooltip(x, y, contents) {
	$("<div id='tooltip'>" + contents + "</div>").css({
		position: "absolute",
		display: "none",
		top: y + 5,
		left: x + 5,
		border: "1px solid #fdd",
		padding: "2px",
		"background-color": "#fee",
		opacity: 0.80
	}).appendTo("body").fadeIn(100);
}

/**
 * Represent jason data as a tree with <ul> and <li> elements.
 * @param {type} html html code to start with
 * @param {type} data json data object
 * @returns {String} html with tree content
 */
function drawDataTree(html, data){

	if(data === undefined) {
		return "";

	} else {
		html += "<ul>";

		for(var prop in data) {
			html += "<li>";
			html += "<b>" + prop + "</b>";

			// Find object
			if($.type(data[prop]) === 'object') {
				html = drawDataTree(html, data[prop]);

			} else {
				html += ': ' + data[prop];
			}
			html += "</li>";
		}
		html += "</ul>";
	}

	return html;
}

function setUpLoginForm() {
	// Setup drop down menu
	$('.dropdown-toggle').dropdown();

	// Fix input element click problem
	$('.dropdown-menu').click(function(e) {
		e.stopPropagation();
	});

	$('#user_login_dropdown').click(function(){
		$('.user_dropdown_menu').ready(function(){
			$('#user_username').focus();
		});
	});
}