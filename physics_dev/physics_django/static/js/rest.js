/*
 * All REST calls and other helper functions can be found in this file
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

var plot = undefined;

/**
 * Get Logbooks from REST service
 * @param targetId id of the element Logbooks will be placed in
 * @param {type} showByDefault should logbooks be shown by default or not
 * @param {type} saveSelectedItemsIntoACookie only save current selected data into a cookie if this flag is set to true
 * @param {type} showSelectedItemsFromACookie should selected items from a cookie be displayed or not
 */
function loadSystems(showByDefault){
	var targetId = "#load_systems";

	// Remove all systems before loading new ones
	$(targetId).find("li:gt(1)").remove();

	// Load Systems
	$.getJSON(serviceurl + 'magnets/system/', function(systems) {
		var template = getTemplate("#template_system");
		var html = "";

		$.each(systems, function(i, item) {
			var customItem = {};
			customItem.name = item;
			customItem.clicked = "";

			// Should Tags be shown by default or not
			if(showByDefault !== undefined && showByDefault === true) {
				customItem.show = "";

			} else {
				customItem.show = "display_none";
			}

			// Alternate background colors
			if(i%2 === 0) {
				customItem.color = "bg_dark";

			} else {
				customItem.color = "bg_light";
			}

			html = Mustache.to_html(template, customItem);

			$(targetId).append(html);
		});

		// Open or close filter group
		if(converterSettings.filtersOpened !== undefined && converterSettings.filtersOpened['load_systems'] === true) {
			openFilterGroup($(targetId));

		} else {
			closeFilterGroup($(targetId));
		}

		// Load system filters
		singleselect("list");

		// Filter systems
		filterListItems("systems_filter_search", "list");

		// Listen for filters toggle
		startListeningForToggleFilterClicks();

	}).fail(function(){
		$('#modal_container').load(modalWindows + ' #serverErrorModal', function(response, status, xhr){
			$('#serverErrorModal').modal('toggle');
		});
	});
}

/**
 * Return raw template
 * @param {type} id div id selector that holds the template
 * @returns template as a string
 */
function getTemplate(id){
	$.ajaxSetup({async:false});
	var template = "";

	$('#template_container').load(templates + ' ' + id, function(response, status, xhr){
		template = $(id).html();
	});

	return template;
}

/**
 * Get log from json object or from REST if it does not exist.
 * @param {type} id log id
 * @return Array with log data and logId
 */
function getDeviceDetails(id){
	var deviceData = null;
	var serialNumber = id;

	// Load log
	if(id in savedDevices){
		deviceData = savedDevices[id];

	} else {
		$.ajaxSetup({async:false});
		var searchQuery = serviceurl + 'magnets/conversion/?id=' + id;
		l(searchQuery);
		$.getJSON(searchQuery, function(device) {
			savedDevices[id] = device;
			deviceData = device;
		});
	}

	return [deviceData, serialNumber];
}

/**
 * Show log that was read from json object or from REST
 * @param {type} details details object
 * @param id id of the log in saved logs array
 */
function showDetails(details, id){

	$('#load_details').show("fast");
	l(details);

	//var data = JSON.stringify(details);

//	var data = drawDataTree("", details[id]);
//	$('#raw').html(data);

	var options = {
		title: 'Plot',
		series: [{}, {showLine:false}],
		axesDefaults: {
			labelRenderer: $.jqplot.CanvasAxisLabelRenderer
		},
		axes: {
			xaxis: {
				label: "Current",
				pad: 0
			},
			yaxis: {
				label: "Magnetic Field"
			}
		}
	};

	var series = [prepareSeries(details[id])];

	// Destroy previous plot
	if(plot !== undefined) {
		plot.destroy();
		$('#plot').html("");
	}

	// Only draw plot if something is in series
	if(series[0] !== undefined) {
		plot = $.jqplot ('plot', series, options);
	}

//	series.push([[1,4], [2,5]]);
//	plot.replot({data: series});
//	l(plot.data);
}

function drawDataTree(html, data){
	//l(data);

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

function prepareSeries(data) {

	if(data.municonv.standard === undefined) {
		return;
	}

	var currents = data.municonv.standard.measurementData.current;
	var fields = data.municonv.standard.measurementData.field;

	var series = [];

	if(currents !== undefined && fields !== undefined) {

		for(var i=0; i<currents.length; i++){
			series.push([currents[i], fields[i]]);
		}
	}

	return series;
}