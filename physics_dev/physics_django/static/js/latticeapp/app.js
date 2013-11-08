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
		when('/',																								'index.home').
		when('/type/:type/name/:name?/version/:version?/branch/:branch?/desc/:desc?/creator/:creator?/list',	'index.home.lattice_list').
		when('/type/:type/name/:name?/version/:version?/branch/:branch?/desc/:desc?/creator/:creator?/id/:id',	'index.home.lattice_list.lattice_details').
		when('/type/:type/name/:name?/version/:version?/branch/:branch?/desc/:desc?/creator/:creator?/ids/:ids','index.home.lattice_list.lattices_details').
		when('/type/:type/name/:name?/list',																	'index.home.model_list').
		when('/type/:type/name/:name?/id/:id?',																	'index.home.model_list.model_details').
		when('/type/:type/name/:name?/ids/:ids?',																'index.home.model_list.models_details').

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
					dependencies: ['type', 'name', 'version', 'branch', 'desc', 'creator']
				}).
				within().
					segment('lattice_details', {
						templateUrl: 'details.html',
						controller: 'showLatticeDetailsCtrl',
						dependencies: ['id']
					}).
					segment('lattices_details', {
						templateUrl: 'details.html',
						controller: 'showLatticesDetailsCtrl',
						dependencies: ['ids']
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
						controller: 'showModelDetailsCtrl',
						dependencies: ['id']
					}).
					segment('models_details', {
						templateUrl: 'model_details.html',
						controller: 'showModelsDetailsCtrl',
						dependencies: ['ids']
					}).
				up().
			up().
		up();

		//$routeProvider.otherwise({redirectTo: '/'});
});