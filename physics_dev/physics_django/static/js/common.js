/*
 * Functions common to complete application
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

$(document).ready(function(){

	// Write data from cookie back to object and remove cookie
	if($.cookie(filtersCookieName) !== undefined) {
		selectedElements = $.parseJSON($.cookie(filtersCookieName));
	}

	// Read data from settings cookie and set it to converterSettings object
	if($.cookie(settingsCookieName) !== undefined) {
		converterSettings = $.parseJSON($.cookie(settingsCookieName));
	}

	// Set version number
	$('.version').html("v" + version);

	// Create new comparator
	jQuery.expr[':'].Contains = function(a, i, m) {
		return (a.textContent || a.innerText || "").toUpperCase().indexOf(m[3].toUpperCase()) >= 0;
	};
});

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
 * Save filter data into a cookie
 * @param {type} dataToBeSaved object to be saved into a cookie
 */
function saveFilterData(dataToBeSaved) {
	l("save filters data");
	l(dataToBeSaved);
	$.cookie(filtersCookieName, JSON.stringify(dataToBeSaved));
}

/**
 * Save settings data to a cookie
 * @param {type} dataToBeSaved data to be saved into a cookie
 */
function saveOlogSettingsData(dataToBeSaved) {
	$.cookie(settingsCookieName, JSON.stringify(dataToBeSaved));
}