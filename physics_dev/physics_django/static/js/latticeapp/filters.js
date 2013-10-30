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