/*
 * Helper functions for IDODS client
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
 * Create routing url
 * @param search search or $routeParams object
 * @param type name of the item we are dealing with e.g. vendor, cmpnt_type
 * @param paramList array of parameter names that should be concatenated
 */
function createRouteUrl(search, type, paramList) {
	var url = "#";

	// Add type
	url += "/" + type;

	// Redirect to new entity
	if(search === undefined) {
		return url;
	}
	
	// Add search time part
	if(search.search !== undefined) {
		url += "/search/" + search.search;
	}

	$.each(paramList, function(i, param) {

		// Add param
		if(search[param] !== undefined) {
			url += "/" + param + "/" + search[param];

		} else {
			url += "/" + param + "/";
		}
	});

	// Return URL
	return url;
}

/**
 * Prepare url post parameter. This function us used to avoid problems when using $http.post function.
 * @param dictOfValues dictionary of key and value of parameters
 */
function prepareUrlParameters(listOfKeys, dictOfValues, listOfMandatoryKeys) {
	var params = [];

	$.each(listOfKeys, function(i, key) {

		if(key in dictOfValues) {

			if (dictOfValues[key] !== undefined) {
				params.push(key + "=" + dictOfValues[key]);
			}
		
		} else if(listOfMandatoryKeys && listOfMandatoryKeys.indexOf(key) >= 0) {
			params.push(key + "=*");
		}
	});
	
	return params.join("&");
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

		// Add status part
		if(search.status !== undefined) {
			query += "status=" + search.status + "&";
			url += "/status/" + search.status;

		} else {
			query += "";
			url += "/status/";
		}

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

/*
 * Check if all selected lattices have the same lattice format
 * @param {type} lattices array of lattices
 * @returns {Boolean} are lattices equal or not
 */
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

/*
 * Check whether two lattices are the same or not and return css rule.
 * @param {type} keys
 * @returns {String}
 */
function checkDiff(keys) {

	if(JSON.stringify(keys[0]) === JSON.stringify(keys[1])) {
		return "diff_green";

	} else {
		return "diff_red";
	}
}

/*
 * Download text as a file
 * @param filename name of the file that will be downloaded
 * @param text text that will be present in the downloaded file
 */
function download(filename, text) {
    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:application/octet-stream,' + encodeURIComponent(text));
    pom.setAttribute('download', filename);
    pom.click();
}

function saveOfflineData($scope, offlineDataFactory) {

	$scope.alert.show = false;
	var result;
	l(result);

	if($scope.action === "update") {
		result = offlineDataFactory.checkItem($scope.element);

	} else if($scope.action == "save") {
		result = offlineDataFactory.checkItem($scope.new);
	}

	if(result !== true) {
		$scope.error = result.errorDict;
	
	} else {
		var propsObject = {};

		delete $scope.error;
		var promise;
		
		if($scope.action === "update") {
			promise = offlineDataFactory.updateItem($scope.element);

		} else if($scope.action == "save") {
			promise = offlineDataFactory.saveItem($scope.new);
		}
		
		promise.then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Offline data successfully saved!";
		
		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
		});
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

/*
 * Create lattice comparison row. It consists of two lattices.
 * @param {type} latticesData object with lattice data
 * @param {type} key lattice name
 * @returns {String} prepared html to be put into the dom
 */
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

/*
 * Create REST URL to access model details
 * @param {type} search scope object
 * @param {type} modelName name of the selected model
 * @returns {String} model details URL
 */
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

/*
 * Change the model details object so they all have index in the first column
 * and that name and position follow it
 * @param {type} data details object
 * @returns {Array}
 */
function transformModelDetails(data) {
	l(data);
	var modelNames = Object.keys(data);
	var header = [];

	// All detail types should have index column. If not, copy them from order to index
	if(data[modelNames[0]].index === undefined) {
		data[modelNames[0]].index = data[modelNames[0]].order;
	}

	// In the property list, index, name and position should be on the start
	header.push("index");
	header.push("name");
	header.push("position");

	var columns = Object.keys(data[modelNames[0]]);

	// Add other properties to the property list
	$.each(columns, function(i, column) {

		if(
			column === "transferMatrix" ||
			column === "order" ||
			column === "index" ||
			column === "name" ||
			column === "position"
		) {
			return;
		}

		header.push(column);
	});

	var outputData = data[modelNames[0]];
	return [modelNames[0], header, outputData];
}

/*
 * Create table row with checkboxes for every property of each
 * selected model
 * @param {type} headerRows array of header rows
 * @param {type} modelName name of the selected model
 * @param {type} selection dictionary of checkbox selection values
 * @returns {unresolved}
 */
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
 * Create object with factors for multiplying data
 * selected model
 * @param {type} headerRows array of header rows
 * @param {type} modelName name of the selected model
 * @param {type} selection dictionary of checkbox selection values
 * @returns {unresolved}
 */
function createPropertyFactorTable(headerRows, modelName, selection) {

	$.each(headerRows, function(i, head) {

		if(head === "index" || head === "position" || head === "name") {
			return;
		}

		if(modelName in selection) {
			selection[modelName][head] = 1;

		} else {
			selection[modelName] = {};
			selection[modelName][head] = 1;
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

/*
 * Clean headers array of index, position and name headers and create object
 * of factor values data arrays should be multiplied by
 * @param {type} headers array of headers that needs to be cleaned
 * @returns {filterPropertySelectionTable.properties|Array} filtered properties
 */
function filterPropertyFactorTable(modelName, headers) {
	var properties = {};
	var modelHeaders = headers[modelName];
	properties[modelName] = {};

	$.each(modelHeaders, function(i, header) {

		if(header === "index" || header === "position" || header === "name") {
			return;
		}

		properties[modelName][header] = 1;
	});

	return properties;
}

/**
 * Filter lattice comparison table based on device name
 * @param {type} filters Object with filter data
 * @param {type} name of the element that contains data
 * @param {string} table selector of the table we are filtering
 */
function filterTableItems(filters, name, table){
	var filter = filters.deviceName.toLowerCase();
	var cells = $(table).find(name);

	$.each(cells, function(i, cell) {
		var parentElement = $(cell).parent();
		var diffElement = parentElement.find('.diff_details');
		var value = $(cell).text().toLowerCase();
		var visible = true;

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
}

/*
 * Function will prepare configuration and draw plot
 * @param {type} placeholder div selector where plot will be put
 * @param {type} selection which checkboxes are selected in a property/model table
 * @param {type} factor multiply data array for a factor
 * @param {type} data data to be plotted
 * @param {type} nameToIdMap object that maps model name to model id
 * @param {type} x_axis fixed label on x axis
 * @param {type} scope current controller scope
 */
function drawPlotTransposed(placeholder, selection, factor, data, nameToIdMap, x_axis, scope){
	//container.addClass("placeholder_hidden");

	var series = [];
	var yaxisLabel = [];
	var yaxis2Label = [];

	$.each(selection, function(moduleName, select) {

		$.each(select, function(prop, checked) {

			// Property selected for specific module name
			if(checked === true) {
				l(factor);

				var seriesData = [];

				if(factor !== undefined) {
					seriesData = createSeriesAndMultiply(data[moduleName]['position'], data[moduleName][prop], factor[moduleName][prop]);

				} else {
					seriesData = createSeries(data[moduleName]['position'], data[moduleName][prop]);
				}

				l(seriesData);

				// Add series of conversion points
				var seriesLabel = "";

				if(nameToIdMap !== undefined){
					seriesLabel = nameToIdMap[moduleName] + " - " + prop;

				} else {
					seriesLabel = prop;
				}

				// If factor is defined write for how much did we multiply
				if(factor !== undefined) {
					seriesLabel += " " + factor[moduleName][prop] + "x";
				}

				if(prop === "betax" || prop === "betay") {
					series.push({label: seriesLabel, lines: { show: true }, points: { show: true }, data: seriesData, yaxis: 1});
					yaxisLabel.push(seriesLabel);

				} else {
					series.push({label: seriesLabel, lines: { show: true }, points: { show: true }, data: seriesData, yaxis: 2});
					yaxis2Label.push(seriesLabel);
				}
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
		yaxes: [{
			tickDecimals: 4
		},
		{
			alignTicksWithAxis: null,
			position: "right"
		}],
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

	var container = $(placeholder);
	var resizeContainer = $(".resize_container");

	// We have at least one series
	if(series.length > 0) {
		//container.removeClass("placeholder_hidden");

		// Initialize plot
		var flotPlot = $.plot(container, series, optionsFlot);

		resizeContainer.resizable({
			maxWidth: 2000,
			maxHeight: 700,
			minWidth: 900,
			minHeight: 400
		});

		// If there are too many element, just write all the rest
		if(yaxis2Label.length > 2) {
			yaxis2Label = ["All the rest"];
		}

		// Create y axis labe
		var yaxisLabel = $(".y_label").text(yaxisLabel.join(",."));

		// Create second y axis labe
		var yaxis2Label = $(".y2_label").text(yaxis2Label.join(", "));

		// Create x axis label
		var xaxisLabel = $(".x_label").text(x_axis);

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

/*
 * Create 2D array of points from two 1D data arrays and multiply data for a
 * factor of factor
 * @param {type} xData data on x axis
 * @param {type} yData data on y axis
 * @returns {createSeries.data|Array} 2D array of points to be plotted
 */
function createSeries(xData, yData) {
	var data = [];

	$.each(xData, function(i, x) {
		data.push([x, yData[i]]);
	});

	return data;
}

/*
 * Create 2D array of points from two 1D data arrays
 * @param {type} xData data on x axis
 * @param {type} yData data on y axis
 * @param {type} factor multiply data for a factor
 * @returns {createSeries.data|Array} 2D array of points to be plotted
 */
function createSeriesAndMultiply(xData, yData, factor) {
	var data = [];

	$.each(xData, function(i, x) {
		data.push([x, yData[i] * factor]);
	});

	return data;
}

/*
 * Add pan arrow to the plot
 * @param {type} classNamePart part of the name that represents the direction on an arrow
 * @param {type} offset where should plot be panned ond for how much
 * @param {type} placeholder position on a parent element
 * @param {type} plot element
 */
function addArrow(classNamePart, offset, placeholder, plot) {
	$("<div class='pan pan_" + classNamePart + "'></div>")
		.appendTo(placeholder)
		.click(function (e) {
			e.preventDefault();
			plot.pan(offset);
		});
}

/*
 * Show tooltip next to the mouse cursor when mouse cursor is hovering over
 * the point on a plot
 * @param {type} x x position of tooltip
 * @param {type} y y position of tooltip
 * @param {type} contents contents on a tooltip
 */
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
function drawDataTree(html, data, level){

	if(data === undefined) {
		return "";

	} else {
		html += "<ul>";

		for(var prop in data) {
			l(prop);
			l(data);
			html += "<li>";
			html += "<b><a href ng-click='showTreeNodeDetails(\"" + data[prop]['id'] + "\")'>" + prop + "</a></b>";

			if (level > 0 && level <= 3) {
				html += " <a ng-click='addItem(\"" + prop + "\")' href>Add child</a>";
			}

			// Find object
			if($.type(data[prop]) === 'object') {
				html = drawDataTree(html, data[prop]['children'], level+1);

			} else {
				html += ': ' + data[prop];
			}
			html += "</li>";
		}
		html += "</ul>";
	}

	return html;
}

function toggleChildren(el) {
	var elObj = $(el).find(':first-child');

	if (elObj.hasClass('icon-chevron-down')) {
		elObj.removeClass('icon-chevron-down');
		elObj.addClass('icon-chevron-right');
	
	} else {
		elObj.removeClass('icon-chevron-right');
		elObj.addClass('icon-chevron-down');
	}

	var block = $(el).next().next();
	block.toggle();
}

/**
 * Represent jason data as a tree with <ul> and <li> elements.
 * @param {type} html html code to start with
 * @param {type} data json data object
 * @returns {String} html with tree content
 */
function drawDataTree2(html, data, level){

	if(data === undefined) {
		return "";

	} else {
		html += "<ul class='none-style'>";

		for(var prop in data) {
			html += "<li>";

			if (level >= 3) {
				html += "<b><a href ng-click='listData(\"" + prop + "\")'>" + prop + "</a></b>";

			} else {
				html += "<span onclick='toggleChildren(this);'><i class='icon-chevron-down'></i></span>";
				html += "<b>" + prop + "</b>";
			}

			// Find object
			if($.type(data[prop]) === 'object') {
				html = drawDataTree2(html, data[prop]['children'], level+1);

			} else {
				html += ': ' + data[prop];
			}
			html += "</li>";
		}
		html += "</ul>";
	}

	return html;
}

/*
 * Prepare form for login. Form is a part on a dropdown so some mesures should
 * be taken to change the dropdown functionality.
 */
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

/**
 * Create CSV string that can be then downloaded as a CSV file
 * @param {type} data model data
 * @param {type} selection selection object (which checkboxes are checked)
 * @param {type} factor factor object (what is the value of factor in an input)
 * @returns {String} CSV string
 */
function createCsvString(data, selection, factor) {
	var outputArr = [];
	var mandatoryCols = ["index", "name", "position"];
	var models = Object.keys(data);

	// Add header row
	var headerRowArr = [];

	$.each(mandatoryCols, function(i, col) {
		headerRowArr.push(col);
	});

	$.each(selection[models[0]], function(propName, propValue) {

		if(propValue) {
			headerRowArr.push(propName);
		}
	});

	outputArr.push(headerRowArr.join("\t"));

	// Add other rows
	$.each(data[models[0]]['index'], function(indexKey, indexValue) {
		var bodyRowArr = [];

		$.each(mandatoryCols, function(i, propName) {
			bodyRowArr.push(data[models[0]][propName][indexKey]);
		});

		$.each(selection[models[0]], function(propName, propValue) {

			if(propValue) {
				var value = data[models[0]][propName][indexKey];
				var factorValue = factor[models[0]][propName];
				bodyRowArr.push(value * factorValue);
			}
		});

		outputArr.push(bodyRowArr.join("\t"));
	});

	return outputArr.join("\n");
}