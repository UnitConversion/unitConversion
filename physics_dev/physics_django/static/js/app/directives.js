/**
 * This file contains directives - repetitive chunks of code with its own templates
 */

/*
 * Directive for dispaying a table of key-value pairs
 */
app.directive('keyValueTable', function() {
	return {
		restrict: 'A',
		template : '\
			<table class="table table-bordered">\n\
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
			tableData: '='
		},
		link: function(scope, elem, attrs) {
			scope.data = scope.tableData;
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
			<table class="table table-bordered">\n\
				<tr>\n\
					<th>Algorithm</th>\n\
					<th>Function</th>\n\
					<th>Initial unit</th>\n\
					<th>Algorithm id</th>\n\
					<th>Result unit</th>\n\
					<th>Aux info</th>\n\
				</tr>\n\
				<tr>\n\
					<td>{{name}}</td>\n\
					<td>{{data.function}}</td>\n\
					<td>{{data.initialUnit}}</td>\n\
					<td>{{data.algorithmId}}</td>\n\
					<td>{{data.resultUnit}}</td>\n\
					<td>{{data.auxInfo}}</td>\n\
				</tr>\n\
			</table>\n\
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