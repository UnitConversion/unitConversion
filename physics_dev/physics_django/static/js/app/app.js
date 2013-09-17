/*
 * Create module and add include dependencies
 */
var app = angular.module('conversion', ['ui.bootstrap', 'ngResource', 'ngRoute', 'route-segment', 'view-segment']);

/*
 * Define routes for our module
 */
app.config(function($routeSegmentProvider, $routeProvider){

	$routeSegmentProvider.options.autoLoadTemplates = true;

	$routeSegmentProvider.
		when('/',																						's1.home').
		when('/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/list',			's1.home.list').
		when('/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/id/:id',			's1.home.list.details').
		when('/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/id/:id/:view',	's1.home.list.details.results').

		segment('s1', {
			templateUrl: 'content.html',
			controller: 'mainCtrl'
		}).
		within().
			segment('home', {
				templateUrl: 'search.html',
				controller: 'searchFormCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list.html',
					controller: 'listDevicesCtrl',
					dependencies: ['system', 'name', 'cmpnt_type', 'serialno']
				}).
				within().
					segment('details', {
						templateUrl: 'details.html',
						controller: 'showDetailsCtrl',
						dependencies: ['id']
					}).
					within().
						segment('results', {
							templateUrl: 'results.html',
							controller: 'showResultsCtrl',
							dependencies: ['view']
						}).
					up().
				up().
			up().
		up();

		$routeProvider.otherwise({redirectTo: '/'});
});