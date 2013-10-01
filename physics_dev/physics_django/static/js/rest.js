/*
 * All REST calls and other helper functions can be found in this file
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

var plot = undefined;

/**
 * Show log that was read from json object or from REST
 * @param {type} details details object
 * @param id id of the log in saved logs array
 */
function showDetails(data, x_axis, y_axis, newSeries){

	l(data);

	//var data = JSON.stringify(details);

//	var data = drawDataTree("", details[id]);
//	$('#raw').html(data);

	var options = {
		series: [{}, {showLine:false}],
		seriesColors: ["#c5b47f", "#953579"],
		axesDefaults: {
			labelRenderer: $.jqplot.CanvasAxisLabelRenderer
		},
		axes: {
			xaxis: {
				label: x_axis,
				pad: 0
			},
			yaxis: {
				label: y_axis
			}
		},
		highlighter: {
			show: true,
			sizeAdjust: 7.5
		},
		cursor: {
			show: false
		}
	};

	var preparedSeries = prepareSeries(data, x_axis, y_axis);
	var series = [];

	// Add prepared series
	if(preparedSeries.length !== 0) {
		series.push(preparedSeries);
	}

	// Destroy previous plot
	if(plot !== undefined) {
		plot.destroy();
		$('#plot').html("");
	}

	// Only draw plot if something is in series
	if(series.length !== 0) {
		plot = $.jqplot ('plot', series, options);
	}

	// Redraw conversion points
	if(newSeries.length !== 0) {

		if(series.length === 0) {
			series.push([[0,0]]);
			series.push(newSeries);
			plot = $.jqplot ('plot', series, options);

		} else {
			series.push(newSeries);
			plot.replot({data: series});
		}
	}
//	l(plot.data);
}

/**
 * Represent jason data as a tree with <ul> and <li> elements.
 * @param {type} html html code to start with
 * @param {type} data json data object
 * @returns {String} html with tree content
 */
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

/**
 * Prepare series for plotting
 * @param {type} data object that contains data for the series
 * @returns {Array} array of points in series
 */
function prepareSeries(data, x_axis, y_axis) {
	var series = [];

	// Check if data is udefined
	if(data === undefined) {
		return series;
	}

	var currents = data.current;
	var fields = data.field;

	// Set the new vector on x axis
	if(x_axis !== undefined) {
		currents = data[x_axis];
	}

	// Set the new vector on y axis
	if(y_axis !== undefined) {
		fields = data[y_axis];
	}

	if(currents !== undefined && fields !== undefined) {

		for(var i=0; i<currents.length; i++){
			series.push([currents[i], fields[i]]);
		}
	}

	return series;
}