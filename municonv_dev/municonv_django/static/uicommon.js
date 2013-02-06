/* Includes common functions for dynamic user interface interaction.
 */

/* Checks if the value of the given element was changed and/or is valid and updates its css.
 * Call this for instance on input onchanged event to show changed/invalid state.
 *
 * element         - the dom element to check
 * isValidCallback - function to test the validity in the form of function(element); if not
 *                   specified validation is not checked
 */
function checkInputValue(element, isValidCallback) {

	// if element does not support default value, always mark it as modified
	if (element.defaultValue == undefined || element.defaultValue != element.value) {
		$(element).addClass('modified');
	} else {
		$(element).removeClass('modified');
	}
	
	if (isValidCallback && !isValidCallback(element)) {
		$(element).addClass('invalid');
	} else {
		$(element).removeClass('invalid');
	}
}

// Resets the modified state for the given dom element.
function resetInputValue(element) {
	element.defaultValue = element.value;
	checkInputValue(element);
}

/* Registers the click on the table row to the given callback, and adds the on mouse over
 * highlight to the table rows.
 *
 * tableId       - the id of the element that is the table; if it does not exist, nothing is done
 * clickCallback - a on row clicked callback function in the form function(event); if not
 *                 specified, the callback is not registered
 */
function addTableEvents(tableId, clickCallback) {

	// ignore the first row as it is the header
	var rows = $("#" + tableId + " tbody tr:not(:first)");
	
	if (rows) {
		if (clickCallback) {
			rows.on("click", clickCallback);
		}
	
		rows.on("mouseover", function(event) {
			$(this).find("td").addClass('highlight');
		});
	
		rows.on("mouseout", function(event) {
			$(this).find("td").removeClass('highlight');
		});
	}
}
