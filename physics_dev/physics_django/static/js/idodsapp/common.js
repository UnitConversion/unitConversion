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
var plot;

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
 * Start parsing search input value from left to right and return type and search
 * value.
 * @param {type} value unparsed string part
 * @returns {Array} array that consists of search type, search value and remainder
 */
function parseSearchLanguageRec(value){

	var searchString = "";
	var filterType = "";
	var remainder = "";

	var re = new RegExp("(name:|description:|^)(.*?)(name:.*|description:.*|$)", "i");
	var searchParts = re.exec(value);

	if(searchParts === null) {
		searchString = value;

	} else {
		filterType = searchParts[1];
		searchString = searchParts[2];
		remainder = searchParts[3];
	}

	return [filterType, searchString, remainder];
}

/**
 * Build search query from search input
 * @returns {String} prepared search query
 */
function parseSearchLanguage(searchQuery){

	var value = searchQuery;
	var query = "";
	var langDict = {};

	var parsedStringParts = parseSearchLanguageRec(value);

	// Get custom part of search value
	if(parsedStringParts[0] === "") {

		// Prepend and append a star
		if(trim(parsedStringParts[1]) !== "") {
			query += trim(parsedStringParts[1]) + " ";
			langDict.display = trim(parsedStringParts[1]);
		}

	} else {

		if(parsedStringParts[0] !== undefined) {
			query += parsedStringParts[0] + trim(parsedStringParts[1]) + " ";
			langDict[parsedStringParts[0]] = trim(parsedStringParts[1]);
		}
	}

	// Get fields that are present in search input
	while (parsedStringParts[2] !== "") {
		parsedStringParts = parseSearchLanguageRec(parsedStringParts[2]);

		if(parsedStringParts[0] !== undefined) {
			query += parsedStringParts[0] + trim(parsedStringParts[1]) + " ";
			langDict[parsedStringParts[0]] = trim(parsedStringParts[1]);
		}
	}
	return [query, langDict];
}

function generateSearchQuery(search, type, paramList) {
	var newDisplayString = parseSearchLanguage(search.display);
	return newDisplayString;
}

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
		if(search[param] !== undefined && search[param] !== null) {
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

/*
 * Download data as a file
 * @param filename name of the file that will be downloaded
 * @param data data that will be present in the downloaded file
 */
function download(filename, data, is_ascii) {

	var mime = 'application/octet-stream';

	if (is_ascii) {
		data = decode64(data);

	} else {
		mime = 'application/octet-stream;base64';
	}

    var pom = document.createElement('a');
    pom.setAttribute('href', 'data:' + mime + ',' + encodeURIComponent(data));
    pom.setAttribute('download', filename);
    pom.click();
}

function saveData($scope, dataFactory) {
	l($scope);
	l(dataFactory);

	$scope.alert.show = false;
	var result;

	if($scope.action === "update") {
		result = dataFactory.checkItem($scope.element);

	} else if($scope.action == "save") {
		result = dataFactory.checkItem($scope.new);
	}
	l(result);

	if(result !== true) {
		$scope.error = result.errorDict;

	} else {
		var propsObject = {};

		delete $scope.error;
		var promise;

		if($scope.action === "update") {
			promise = dataFactory.updateItem($scope.element);

		} else if($scope.action == "save") {
			promise = dataFactory.saveItem($scope.new);
		}

		promise.then(function(data) {
			$scope.alert.show = true;
			$scope.alert.success = true;
			$scope.alert.title = "Success!";
			$scope.alert.body = "Data successfully saved!";

		}, function(error) {
			$scope.alert.show = true;
			$scope.alert.success = false;
			$scope.alert.title = "Error!";
			$scope.alert.body = error;
		});
	}
}

/**
 * Function converts base64 encoded string to ASCII format
 * @param {type} input base64 input string
 * @returns {decode64.output}
 */
function decode64(input) {
	var base64_keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
	var output = "";
	var chr1, chr2, chr3;
	var enc1, enc2, enc3, enc4;
	var i = 0;

	// remove all characters that are not A-Z, a-z, 0-9, +, /, or =
	input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");

	while (i < input.length) {
		enc1 = base64_keyStr.indexOf(input.charAt(i++));
		enc2 = base64_keyStr.indexOf(input.charAt(i++));
		enc3 = base64_keyStr.indexOf(input.charAt(i++));
		enc4 = base64_keyStr.indexOf(input.charAt(i++));

		chr1 = (enc1 << 2) | (enc2 >> 4);
		chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
		chr3 = ((enc3 & 3) << 6) | enc4;

		output = output + String.fromCharCode(chr1);

		if (enc3 !== 64) {
			output = output + String.fromCharCode(chr2);
		}
		if (enc4 !== 64) {
			output = output + String.fromCharCode(chr3);
		}
	}
	return output;
}

/**
 * Represent jason data as a tree with <ul> and <li> elements.
 * @param {type} html html code to start with
 * @param {type} data json data object
 * @returns {String} html with tree content
 */
function drawDataTree(html, data, currentNode, level){

	// Hide all but the top level
	var display = "  style='display:none;'  ";

	if(level === 0) {
		display = " style='display:block;' ";
	}

	html += "<ul " + display + " class='none-style'>";

	for(var childName in currentNode.children) {
		var child = data[currentNode.children[childName]];
		l(child);

		html += "<li>";

		// Show expand/collapse icons only if element is not a leaf element
		if (child.data && child.data.__node_type__ && child.data.__node_type__ !== "real") {
			html += "<span onclick='toggleChildren(this)'><i class='icon-chevron-right'></i></span> ";
		}

		//html += "<b><a href ng-click='showTreeNodeDetails(\"" + data[prop].id + "\")'>" + prop + "</a></b>";
		html += "<b><a href ng-click='walkThroughTree(\"" + child.name + "\")'>" + child.name + "</a></b>";

		// Show rel button
		html += " <a title='view relation' ng-click='showDetailsRaw(\"" + child.name + "\")' href><i class='icon-pencil'></i></a>";

		// Show add child only if element is not a leaf element
		if (child.data && child.data.__node_type__ && child.data.__node_type__ !== "real") {
			html += " <a title='add child' ng-click='addItem(\"" + child.name + "\")' href><i class='icon-plus'></i></a>";
		}

		// Find object
		if(child.children.length > 0) {
			html = drawDataTree(html, data, child, level+1);
		}

		html += "</li>";
	}
	html += "</ul>";

	return html;
}

/**
 * Toggle icon next to the element. Icon means children are collapsed or extended
 * @param  {[type]} el DOM element that has icon in it
 * @return {[type]}    [description]
 */
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

	// Maybe UL is the next element
	while(!block.is("ul")) {
		block = block.next();
	}

	block.toggle();
}

/**
 * Toggle icon next to the element. Icon means children are collapsed or extended
 * @param  {[type]} el DOM element that has icon in it
 * @param  {[type]} type should we toggle online data tables or offline data tables
 * @return {[type]}    [description]
 */
function toggleOnlineOfflineData(el, type) {
	var elObj = $(el).find(':first-child');

	if (elObj.hasClass('icon-chevron-down')) {
		elObj.removeClass('icon-chevron-down');
		elObj.addClass('icon-chevron-right');

	} else {
		elObj.removeClass('icon-chevron-right');
		elObj.addClass('icon-chevron-down');
	}

	var block = $(el).parent().find('.' + type);
	block.toggle();
}

/**
 * Toggle table rows and Show/Hide button
 * @param  {[type]} el DOM element that has icon in it
 * @param  {[type]} type should we toggle online data tables or offline data tables
 * @return {[type]}    [description]
 */
function toggleTableRows(el, type) {
	var elObj = $(el);
	l(type);

	if (elObj.html() == 'Show') {
		elObj.html('Hide');
		elObj.addClass('active');

	} else {
		elObj.html('Show');
		elObj.removeClass('active');
	}

	var block = $(el).parents('table').find('.' + type);
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
				html = drawDataTree2(html, data[prop].children, level+1);

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
	// $('.dropdown-toggle').dropdown();

	// // Fix input element click problem
	// $('.dropdown-menu').click(function(e) {
	// 	e.stopPropagation();
	// });

	// $('#user_login_dropdown').click(function(){
	// 	$('.user_dropdown_menu').ready(function(){
	// 		$('#user_username').focus();
	// 	});
	// });

	$('#user_login_dropdown').click(function(e) {
		$('.user_dropdown_menu').toggle();
	});
}

/*
 * Prepare form for search. Form is a part on a dropdown so some messures should
 * be taken to change the dropdown functionality.
 */
function setUpSearchForm() {
	// Setup drop down menu

	$('.search_dropdown_menu_button').click(function(e) {
		$('.search_dropdown_menu').toggle();
	});

	$('.close_dropdown').click(function(e) {
		$('.search_dropdown_menu').hide();
	});

	$('.search_dropdown_menu').bind("keydown keypress", function(event) {

		if(event.which === 13) {
			$('.search_dropdown_menu').toggle();
		}
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
	$.each(data[models[0]].index, function(indexKey, indexValue) {
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