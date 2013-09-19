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
		when('/',																								's1.home').
		when('/type/:type/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/list',		's1.home.list_install').
		when('/type/:type/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/id/:id',		's1.home.list_install.details').
		when('/type/:type/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/id/:id/:view','s1.home.list_install.details.results').
		when('/type/:type/cmpnt_type/:cmpnt_type?/serialno/:serialno?/list',									's1.home.list_inventory').
		when('/type/:type/cmpnt_type/:cmpnt_type?/serialno/:serialno?/id/:id',									's1.home.list_inventory.details').
		when('/type/:type/cmpnt_type/:cmpnt_type?/serialno/:serialno?/id/:id/:view',							's1.home.list_inventory.details.results').

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
				segment('list_inventory', {
					templateUrl: 'list.html',
					controller: 'listDevicesCtrl',
					dependencies: ['type', 'cmpnt_type', 'serialno']
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
				segment('list_install', {
					templateUrl: 'list.html',
					controller: 'listDevicesCtrl',
					dependencies: ['type', 'system', 'name', 'cmpnt_type', 'serialno']
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