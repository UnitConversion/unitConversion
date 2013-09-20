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
function showDetails(data){

	l(data);

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

	var series = [prepareSeries(data)];

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
function prepareSeries(data) {

	var currents = data.current;
	var fields = data.field;

	var series = [];

	if(currents !== undefined && fields !== undefined) {

		for(var i=0; i<currents.length; i++){
			series.push([currents[i], fields[i]]);
		}
	}

	return series;
}