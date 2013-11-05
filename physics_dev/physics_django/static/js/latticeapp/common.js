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
			query += "creator=" + search.creator;
			url += "/creator/" + search.creator;

		} else {
			query += "creator=*";
			url += "/creator/";
		}
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

function createLatticeTable(header, lattice) {
	// Add header
	var table = "<tr>";

	$.each(header, function(i, column){
		table += "<th>" + column.charAt(0).toUpperCase() + column.slice(1) + "</th>";
	});

	table += "</tr>";

	// Add data
	$.each(lattice, function(j, line){
		table += "<tr class='lattice_table_row'>";

		$.each(header, function(i, column){

			if(line[column] === undefined) {
				table += "<td></td>";

			} else {

				// Ckeck for file links
				if(column.indexOf("file") !== -1) {
					table += '<td><a href="#">' + line[column] + '</a></td>';

				} else {
					table += "<td>" + line[column] + "</td>";
				}
			}
		});

		table += "</tr>";
	});

	return table;
}

/**
 * @param {type} id id od the input element
 * @param {type} name of the element that contains data
 * @param {string} table selector of the table we are filtering
 */
function filterTableItems(id, name, table){

	var filter = $(id).val();
	l(filter);

	// Slide up items that does not contain filters and are not selected
	$(table).find(name + ':not(:Contains(' + filter + ')):not(.multilist_clicked)').parent().slideUp();
	$(table).find(name + ':Contains(' + filter + ')').parent().slideDown();
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