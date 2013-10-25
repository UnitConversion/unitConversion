/*
 * Create module and add include dependencies
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */
var app = angular.module('lattice', ['ui.bootstrap', 'ngResource', 'ngRoute', 'route-segment', 'view-segment']);

/*
 * Define routes for app module
 */
app.config(function($routeSegmentProvider, $routeProvider){

	$routeSegmentProvider.options.autoLoadTemplates = true;

	$routeSegmentProvider.
		when('/',																												'index.home').
		when('/search/:search/type/:type/name/:name?/version/:version?/branch/:branch?/desc/:desc?/creator/:creator?/list',		'index.home.lattice_list').
		when('/search/:search/type/:type/name/:name?/version/:version?/branch/:branch?/desc/:desc?/creator/:creator?/details',	'index.home.lattice_list.lattice_details').
		when('/search/:search/type/:type/name/:name?/list',																		'index.home.model_list').
		when('/search/:search/type/:type/name/:name?/details',																	'index.home.model_list.model_details').

		segment('index', {
			templateUrl: 'content.html',
			controller: 'mainCtrl'
		}).
		within().
			segment('home', {
				templateUrl: 'search.html',
				controller: 'searchFormCtrl'
			}).
			within().
				segment('lattice_list', {
					templateUrl: 'list.html',
					controller: 'listLatticeCtrl',
					dependencies: ['search']
				}).
				within().
					segment('lattice_details', {
						templateUrl: 'details.html',
						controller: 'showDetailsCtrl',
						dependencies: ['type', 'name', 'version', 'branch', 'desc', 'creator']
					}).
				up().
				segment('model_list', {
					templateUrl: 'model_list.html',
					controller: 'listModelCtrl',
					dependencies: ['type', 'name']
				}).
				within().
					segment('model_details', {
						templateUrl: 'model_details.html',
						controller: 'showModelDetailsCtrl'
					}).
				up().
			up().
		up();

		//$routeProvider.otherwise({redirectTo: '/'});
});