/*
 * This file contains angular.js directives
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

			scope.$watch('tableData', function(newData, oldData) {

				for(var key in newData) {
					scope.data[key] = returnFirstXCharacters(JSON.stringify(newData[key]), 100);
				}
			});
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
					<th>Algorithm</th>\n\
					<th>Initial value</th>\n\
					<th>Initial unit</th>\n\
					<th>Converted value</th>\n\
					<th>Converted unit</th>\n\
					<th>Show</th>\n\
				</tr>\n\
				<tr ng-repeat="(index, result) in results">\n\
					<td>{{result.from}}2{{result.to}}</td>\n\
					<td>{{result.init_value}}</td>\n\
					<td>{{result.init_unit}}</td>\n\
					<td>{{result.conv_value}}</td>\n\
					<td>{{result.conv_unit}}</td>\n\
					<td><input ng-model="result.show_result" name="show_result" type="checkbox" ng-change="show(result)" /></td>\n\
				</tr>\n\
			</table>\n\
		',
		scope: {
			results: '=',
			visible: '=',
			onShowClick: '&'
		},
		link: function(scope, elem, attrs) {
			scope.data = {};

			scope.show = function(result) {
				result.show = result.show_result;
				scope.onShowClick({result: scope.results});
			};
		}
	};
});

/*
 * Enter keypress event. It is primarily made for pressing enter on input tags
 */
app.directive('ngEnter', function() {
	return function(scope, element, attrs) {
		element.bind("keydown keypress", function(event) {

			if(event.which === 13) {
				scope.$apply(function(){
					scope.$eval(attrs.ngEnter);
				});

				event.preventDefault();
			}
		});
	};
});