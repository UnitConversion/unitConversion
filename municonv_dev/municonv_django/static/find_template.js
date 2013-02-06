		$(document).ready(function() {
			var urlVars = getUrlVars();
		
			if (urlVars.title) {
				document.title = urlVars.title;
				$("#title").html(urlVars.title);				
			}
			if (urlVars.close_button) {
				$("#closeButton").val(urlVars.close_button);				
			}
			
			readUrlVars(urlVars);
		
			// intercept form submit
			var form = document.form;
			if (form.attachEvent) {
			    form.attachEvent("submit", processForm);
			} else {
			    form.addEventListener("submit", processForm);
			}
			
			registerSpanToPageEnd("mainArea");
		
			refresh();
		})
		
		function readUrlVars(urlVars) {
			var form = document.form;
			if (urlVars.callback) $("#callback").val(urlVars.callback);				
			if (urlVars.query) form.query.value = urlVars.query;
			if (urlVars.limit) form.limit.value = urlVars.limit;
			if (urlVars.close_button) form.close_button.value = urlVars.close_button;
			if (urlVars.select_filter) form.select_filter.value = urlVars.select_filter;
		}
		
		function processForm(e) {
		    if (e.preventDefault) e.preventDefault();
			find();

		    // return false to prevent the default form behavior
		    return false;
		}
		
		function find() {
			var form = document.form;
			form.limit.value = form.defaultLimit.value;
			refresh();
		}
		
		function clearSearch() {
			var form = document.form;
			form.query.value = '';
			refresh();
		}
		
		function displayMore() {
			var form = document.form;
			var limit = parseInt(form.limit.value);
			var defaultLimit = parseInt(form.defaultLimit.value);
			form.limit.value = (!isNaN(limit) && !isNaN(defaultLimit)) ? limit + defaultLimit : '';
			refresh();
		}
		
		function displayAll() {
			document.form.limit.value = '';
			refresh();
		}
		
		function refresh() {
		}
		
		/* this function checks if the number of results equals the limit, and displays "More" buttons if true
		 * call this function after parsing the data in refresh()
		 *
		 * size - the number of items (rows) in retrieved result
		 */
		function setResultSize(size) {
		    var form = document.form;
		
			var size = parseInt(size);
			var limit = parseInt(form.limit.value);

			if (isNaN(limit) || (!isNaN(size) && size < limit)) {
				$("#moreButtonsPanel").removeClass("shown");
			} else {
				$("#moreButtonsPanel").addClass("shown");
			}
		}
