/*
 * Create module and add include dependencies
 *
 * @created Avg 1, 2014
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */
var app = angular.module('measurementdataapp', ['ui.bootstrap', 'ngRoute', 'route-segment', 'view-segment', 'xeditable']);

/*
 * Start xeditable
 */
app.run(function(editableOptions, editableThemes) {
	editableOptions.theme = 'bs3'; // bootstrap3 theme. Can be also 'bs2', 'default'
	editableThemes.bs3.inputClass = 'input-sm';
	editableThemes.bs3.buttonsClass = 'btn-sm';
});

/*
 * Define routes for app module
 */
app.config(function($routeSegmentProvider, $routeProvider) {

	$routeSegmentProvider.options.autoLoadTemplates = true;

	$routeSegmentProvider.
		when('/inventory_id/:inventory_id?/view/:view', 'data').
		when('/cmpnt_type_name/:cmpnt_type_name?/view/:view', 'ctdata').

		segment('data', {
			templateUrl: 'content.html',
			controller: 'dataCtrl',
			dependencies: ['view', 'inventory_id']
		}).
		segment('ctdata', {
			templateUrl: 'content.html',
			controller: 'ctDataCtrl',
			dependencies: ['view', 'cmpnt_type_name']
		});

		$routeProvider.otherwise({redirectTo: '/inventory_id//view/readwrite'});
});