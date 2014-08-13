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

/*
 * Order by object key. Usage example:
 * ng-repeat="item in items | orderObjectBy:'position'"
 */
app.filter('orderObjectBy', function(){
 return function(input, attribute) {
    if (!angular.isObject(input)) return input;

    var array = [];
    for(var objectKey in input) {
        array.push(input[objectKey]);
    }

    array.sort(function(a, b){
        a = parseInt(a[attribute]);
        b = parseInt(b[attribute]);
        return a - b;
    });
    return array;
 };
});

/*
 * Inline if. Example of usage: {{foo == "bar" | iif : "it's true" : "no, it's not"}}
 * found at: http://stackoverflow.com/questions/14164371/inline-conditionals-in-angular-js
 */
app.filter('iff', function () {
   return function(input, trueValue, falseValue) {
        return input ? trueValue : falseValue;
   };
});