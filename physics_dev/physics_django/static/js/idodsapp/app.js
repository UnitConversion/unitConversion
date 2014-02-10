/*
 * Create module and add include dependencies
 *
 * @created Feb 10, 2014
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */
var app = angular.module('idods', ['ui.bootstrap', 'ngResource', 'ngRoute', 'route-segment', 'view-segment', 'blueimp.fileupload']);

/*
 * Define routes for app module
 */
app.config(function($routeSegmentProvider, $routeProvider){

	$routeSegmentProvider.options.autoLoadTemplates = true;

	$routeSegmentProvider.
		when('/',																																			'index.home').
		when('/type/:type/status/:status?/name/:name?/version/:version?/branch/:branch?/desc/:desc?/creator/:creator?/latticetype/:latticetype?/list',		'index.home.lattice_list').
		when('/type/:type/status/:status?/name/:name?/version/:version?/branch/:branch?/desc/:desc?/creator/:creator?/latticetype/:latticetype?/id/:id',	'index.home.lattice_list.lattice_details').
		when('/type/:type/status/:status?/name/:name?/version/:version?/branch/:branch?/desc/:desc?/creator/:creator?/latticetype/:latticetype?/ids/:ids',	'index.home.lattice_list.lattices_details').
		when('/type/:type/status/:status?/name/:name?/list',																								'index.home.model_list').
		when('/type/:type/status/:status?/name/:name?/id/:id?',																								'index.home.model_list.model_details').
		when('/type/:type/status/:status?/name/:name?/ids/:ids?',																							'index.home.model_list.models_details').

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
					dependencies: ['type', 'status', 'name', 'version', 'branch', 'desc', 'creator', 'latticetype']
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
					dependencies: ['type', 'name', 'status']
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