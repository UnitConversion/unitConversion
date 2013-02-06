/* Includes functions related to opening subviews in iframe elements and resizing those views.
 * Also includes other common functions such as for parsing URL parameters.
 */




//--- format parsing functions ---///

// Returns the URL parameters as a dictionary.
function getUrlVars() {

	var href = window.location.href;
	
	var hashStart = href.indexOf('?');
	if (hashStart != -1) {
		href = href.slice(hashStart + 1);
	} else {
		return {};
	}
	
	var hashEnd = href.indexOf('#');
	if (hashEnd != -1) {
		href = href.slice(0, hashEnd);
	}
	
	var hashes = href.split('&');
	var vars = {};
	
	for(var i = 0; i < hashes.length; i++) {
		var hash = hashes[i].split('=');
		
		key = hash[0]
		value = hash[1]
		
		// unescape parameters
		if (value) value = unescape(value);
		
		// Replace "+" back to spaces. Space to '+' happens when using jQuery.param function.
		if (value) value = value.replace(/\+/g, " ");
		
		// If an array, store it as array.
		if (endsWith(key, "[]")) {
			if (!vars[key]) vars[key] = [];
			vars[key].push(value);
		} else {
			vars[key] = value;
		}
	}
	return vars;
}

// encodes the string in html, substituting special characters
function htmlEncode(s) {
    var el = document.createElement("div");
    el.innerText = el.textContent = s;
    s = el.innerHTML;
    return s;
}

// Returns true if str ends with suffix, else false. 
function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

// Replaces empty string with null and returns it.
function emptyToNull(value) {
	// do not compare using value == '' as this does not preserve value 0
	return value != null && value.length == 0 ? null : value; 
}

// replaces '\n' line breaks in the given string text with '<br/>'
function htmlEncodeLineBreaks(text) {
	return text.replace(/\n/g, '<br />');
}

// returns the first row of the given text, or the first row_character_limit characters if the row is longer than this
var row_character_limit = 100;
function toSingleRow(text) {
    var endOfLine = text.indexOf("\n"); 
    if (endOfLine >= 0) {
    	text = text.substring(0, endOfLine);
    }
    text = text.substring(0, row_character_limit);
    return text;
}

/* checks the server callback and displays a message in case of an error
 * returns: true if no error, false if error
 */
function checkServerCallback(res, status) {
	if (status != "success") {
		alert("There was an error contacting the server");
		return false;
	}

	var data = eval('(' + res.responseText + ')');
		
	if (data.error_msg) {
	    alert(data.error_msg);
	    return false;
	}
	return true;
}


//--- layout helper functions ---///

// Returns the y position on the page.
function pageY(elem) {
	return elem.offsetParent ? (elem.offsetTop + pageY(elem.offsetParent)) : elem.offsetTop;
}

var spanToPageEndIds;
var spanToPageEndMargins;
// Registers handlers to update the height of the element with the given id to end of page. 
function registerSpanToPageEnd(ids, margins) {

	// convert to array
	ids = [].concat(ids);
	margins = [].concat(margins);

	// restore the height of the previous registered element
	if (spanToPageEndIds) {
		for (var i = 0; i < spanToPageEndIds.length; i++) {
			// ignore elements that are going to be reregistered
			if (ids.indexOf(spanToPageEndIds[i]) >= 0) continue;
			
			var element = document.getElementById(spanToPageEndIds[i]);
			if (element) element.style.height = '';
		}
	}
	
	spanToPageEndIds = ids;
	spanToPageEndMargins = margins;
	for (var i = 0; i < spanToPageEndIds.length; i++) {
		var element = document.getElementById(spanToPageEndIds[i]);
		if (element) element.onload = resizeSpanToPageEnd;
	}
	window.onresize = resizeSpanToPageEnd;
	
	resizeSpanToPageEnd();
}

// Make element with id from spanToPageEndIds span the remaining height of the screen.
function resizeSpanToPageEnd() {

	for (var i = 0; i < spanToPageEndIds.length; i++) {
		var element = document.getElementById(spanToPageEndIds[i]);
		if (element) {
			var height = document.documentElement.clientHeight;
			
			var margin = 20; // by default, use scroll bar buffer
			if (spanToPageEndMargins && spanToPageEndMargins[i]) {
				margin = spanToPageEndMargins[i];
			}
			
			height -= pageY(element) + margin;
			height = (height < 0) ? 0 : height;
			element.style.height = height + 'px';
		}
	}
}




//--- view handling functions ---///

// sets the style of the element given by id to block
var showElement = function(id) {
	$("#" + id).get(0).style.display = "block";
}

// sets the style of the element given by id to none
var hideElement = function(id) {
	$("#" + id).get(0).style.display = "none";
}

/* Opens a subview in an iframe or a new window.
 * 
 * url       - the url to open
 * target    - the id of iframe to use, or 'window' to open in a new window
 * features  - window features to pass to new window 
 * noHistory - if true, the call does not store the new iframe address in browser history 
 */
function openView(url, target, features, noHistory) {
	if (target == 'window') {
		window.open(url, "", features);
		void(0);
	} else {
		_setIframeUrl(url, target, noHistory);
	}
}

function _setIframeUrl(url, target, noHistory) {
	if (noHistory) {
		/* the only way to not save browser history is to replace the iframe with a copy with new url
		 * http://stackoverflow.com/questions/821359/reload-an-iframe-without-adding-to-the-history
		 */
	    var frameElement = $("#" + target).get(0);
	    var newFrameElement = document.createElement("iframe");
	    newFrameElement.className = frameElement.className;
	    newFrameElement.id = frameElement.id;
	    newFrameElement.src = url;

	    frameElement.parentNode.replaceChild(newFrameElement, frameElement);
	    // refresh the layout
	    resizeSpanToPageEnd();
    } else {
		$("#" + target).attr('src', url);
    }
}

/* Closes (clears) an opened subview.
 *
 * target - the id of iframe containing the view
 * noHistory - if true, the call does not store the new iframe address in browser history 
 */
function closeView(target, noHistory) {
	_setIframeUrl('', target, noHistory);
}

/* Passes the data to parent view and closes this one.
 * This function assumes callback function is stored in a value of an element with id "callback".
 */
function closeThisView(data) {

	try {
		callback = $("#callback").val();
		
		// test if opened from another window
		if (window.opener) {
			window.opener[callback](data);
			window.close();
		} else {
			parent[callback](data);
		}

	} catch (objError) {
		alert("There was an error passing the data back to the parent view");
	}
}

/* Refreshes an iframe subview.
 * 
 * target - the id of iframe to use.
 */
function refreshView(target) {
	var contentWindow = document.getElementById(target).contentWindow;
	
	if (!contentWindow || !contentWindow.refresh) return;
	
	contentWindow.refresh();
}

// Refreshes the parent view of this view.
function refreshParentView() {

	// test if opened from another window
	if (window.opener) {
		window.opener["refresh"](data);
	} else {
		parent["refresh"](data);
	}
}

// Cancel button function. 
function cancel() {
	closeThisView(null);
}

/* Closes this window and returns data to parent window. This function assumes callback function
 * is stored in a form element with id "callback".
 */
function returnAndClose(data) {
	try {
		parent = $("#callback").val();
		window.opener[parent](data);
		window.close();

	} catch (objError) {
		alert("There was an error passing the data back to the parent window");
	}
}

/* Sets the URL parameter in all links in a container.
 * The existing parameters are deleted.
 *
 * container - DOM element that contains links
 * parameters - the string to attach to the URL
 */
function setLinkParameters(container, parameters) {
	// loop through all links
	$(container).find("a").each(function(index) {

        var href = $(this).attr("href");
    	// strip the current parameters
    	href = href.split("?")[0];
    	
    	if (parameters) {
    		href += parameters;
    	}
    	
    	$(this).attr("href", href);
	});
}

/* Displays the given help message.
 * The message is displayed in a popup.
 */
function displayHelp(text) {
	alert(text);
}