/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

$(document).ready(function(){
});

/**
 * Input search query and request data from the server
 * @param {type} searchQuery prebuilt search query
 * @param {type} resetPageCouner on some occasions we want page counter to be reset
 */
function searchForLogs(searchQuery, resetPageCouner) {

	// Reset page counter if new filters are selected
	if(resetPageCouner === true) {
		page = 1;
	}

	searchQuery = serviceurl + 'magnets/devices/?system=' + searchQuery;
	l(searchQuery);

	// Load logs
	$.getJSON(searchQuery, function(logs) {
		$(".device").remove();
		repeatLogs(logs, false);
		startListeningForLogClicks();
	});
}

/**
 * Show logs in the middle section. Some of the data must be formated to be shown properly
 * @param {type} data data in JSON format
 * @param {type} prepend prepend or append new log entry
 * @returns replaces template with data and puts it in the right place
 */
function repeatLogs(data, prepend){
	var template = getTemplate("#template_device");
	var html = "";
	var htmlBlock = "";

	// Go through all the logs
	$.each(data, function(i, item) {
		//savedLogs[item.id] = item;

		// Build customized Log object
		var newItem = {
			name: item.name,
			serialNumber: item.serialNumber,
			typeDescription: item.typeDescription
		};

		// Alternate background colors
		if(i%2 === 0) {
			newItem.color = "bg_dark";

		} else {
			newItem.color = "bg_light";
		}

		// Check if we have an URL and select selected Log
		if(selectedLog !== -1 && parseInt(item.id) === selectedLog) {
			newItem.click = "device_click";

		} else {
			newItem.click = "";
		}

		html = Mustache.to_html(template, newItem);

		if(prepend === false) {
			$("#load_devices").append(html);

		} else {
			htmlBlock += html;
		}

	});

	// Prepend the whole block of Logs in the beginning of list
	if(prepend === true) {
		$("#load_devices #form-search").after(htmlBlock);
	}
}

/**
 * When logs are loaded onto the page, start listening for mouse clicks on them
 * @returns {undefined}
 */
function startListeningForLogClicks(){
	var actionElement = null;

	$('.device').unbind('click');
	$(".device").click(function(e){
		$('.device').removeClass("device_click");

		if($(e.target).is("div")){
			actionElement = $(e.target);

		}else if($(e.target).parent().is("div")){
			actionElement = $(e.target).parent();
		}

		var id = actionElement.find('[name=id]').val();

		$('html, body').animate({
			scrollTop: $('.container-right').offset().top
		}, 100);

		actionElement.toggleClass("device_click");

		var details = getDeviceDetails(actionElement.find("input[name=id]").val());
		showDetails(details[0], details[1])
	});
}