/*
 * This file contains directives - repetitive chunks of code with its own templates
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */

/*
 * Directive for dispaying a table of key-value pairs
 */
app.directive('keyValueTable', function() {
	return {
		restrict: 'A',
		template : '\
			<table class="table table-bordered" ng-show="visible">\n\
				<tr>\n\
					<th>Key</th>\n\
					<th>Value</th>\n\
				</tr>\n\
				<tr ng-repeat="(key, value) in data">\n\
					<td>{{key}}</td>\n\
					<td>{{value}}</td>\n\
				</tr>\n\
			</table>\n\
		',
		scope: {
			tableData: '=',
			visible: '='
		},
		link: function(scope, elem, attrs) {
			scope.data = {};

			for(var key in scope.tableData) {
				scope.data[key] = returnFirstXCharacters(JSON.stringify(scope.tableData[key]), 100);
			}
		}
	};
});

/*
 * Directive for displaying a table of algorithms
 */
app.directive('algorithm', function() {
	return {
		restrict: 'C',
		template : '\
					<td>{{name}}</td>\n\
					<td>{{data.function}}</td>\n\
					<td>{{data.initialUnit}}</td>\n\
					<td>{{data.algorithmId}}</td>\n\
					<td>{{data.resultUnit}}</td>\n\
					<td>{{data.auxInfo}}</td>\n\
		',
		scope: {
			name: '=',
			tableData: '='
		},
		link: function(scope, elem, attrs) {
			scope.data = scope.tableData;
		}
	};
});

/*
 * Directive for displaying a table with results
 */
app.directive('resultsTable', function() {
	return {
		restrict: 'A',
		template : '\
			<table class="table table-bordered" ng-show="visible">\n\
				<tr>\n\
					<th>Initial value</th>\n\
					<th>Initial unit</th>\n\
					<th>Converted value</th>\n\
					<th>Converted unit</th>\n\
				</tr>\n\
				<tr ng-repeat="result in results">\n\
					<td>{{result.init_value}}</td>\n\
					<td>{{result.init_unit}}</td>\n\
					<td>{{result.conv_value}}</td>\n\
					<td>{{result.conv_unit}}</td>\n\
				</tr>\n\
			</table>\n\
		',
		scope: {
			results: '=',
			visible: '='
		},
		link: function(scope, elem, attrs) {
		}
	};
});