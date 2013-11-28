/*
 * Model filters
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/*
 * Make first letter uppercase
 */
app.filter('firstLetterUppercase', function(){

	return function(input){

		if(input.lenght <= 1) {
			return input;

		} else {
			return input.charAt(0).toUpperCase() + input.slice(1);
		}
	};
});

/*
 * Trim spaces and remove new lines
 */
app.filter('clean', function(){

	return function(input){
		return input.replace(/\r\n/g, '');
	};
});

/*
 * Round numbers to specific precision and exclude indexes
 */
app.filter('precision', function() {

	return function(input, precision, column) {

		if(column === "index" || column === "name") {
			return input;
		}

		if($.type(input) === "string") {
			return input;

		} else if($.type(input) === "number") {
			input = input.toFixed(precision);

			return input;

		} else {
			return input;
		}
	};
});