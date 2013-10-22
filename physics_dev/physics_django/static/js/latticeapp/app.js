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
		when('/',																									'index.home').
		when('/type/:type/name/:name?/version/:version?/branch/:branch?/desc/:desc?/creator/:creator?/list',		'index.home.list_lattice').
		when('/type/:type/name/:name?/version/:version?/branch/:branch?/desc/:desc?/creator/:creator?/details',		'index.home.list_lattice.details').
		when('/type/:type/cmpnt_type/:cmpnt_type?/serialno/:serialno?/list',										'index.home.list_model').
		when('/type/:type/cmpnt_type/:cmpnt_type?/serialno/:serialno?/id/:id/:view',								'index.home.list_model.details').

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
				segment('list_lattice', {
					templateUrl: 'list.html',
					controller: 'listLatticeCtrl',
					dependencies: ['type', 'name', 'version', 'branch', 'desc', 'creator']
				}).
				within().
					segment('details', {
						templateUrl: 'details.html',
						controller: 'showDetailsCtrl'
					}).
				up().
				segment('list_model', {
					templateUrl: 'list.html',
					controller: 'listDevicesCtrl',
					dependencies: ['type', 'system', 'name', 'cmpnt_type', 'serialno']
				}).
				within().
					segment('details', {
						templateUrl: 'details.html',
						controller: 'showDetailsCtrl',
						dependencies: ['id', 'view']
					}).
				up().
			up().
		up();

		//$routeProvider.otherwise({redirectTo: '/'});
});