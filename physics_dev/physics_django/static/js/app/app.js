/*
 * Create module and add include dependencies
 *
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */
var app = angular.module('conversion', ['ui.bootstrap', 'ngResource', 'ngRoute', 'route-segment', 'view-segment']);

/*
 * Define routes for app module
 */
app.config(function($routeSegmentProvider, $routeProvider){

	$routeSegmentProvider.options.autoLoadTemplates = true;

	$routeSegmentProvider.
		when('/',																													's1.home').
		when('/type/:type/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/list',							's1.home.list_install').
		when('/type/:type/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/inst_id/:inst_id/step/md',		's1.home.list_install.wizard.md').
		when('/type/:type/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/inst_id/:inst_id/step/mt/m',   's1.home.list_install.wizard.mt.m').
		when('/type/:type/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/inst_id/:inst_id/step/mt/mc',  's1.home.list_install.wizard.mt.mc').
		when('/type/:type/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/id/:id/:view',					's1.home.list_install.details').
		when('/type/:type/system/:system?/name/:name?/cmpnt_type/:cmpnt_type?/serialno/:serialno?/id/:id/:view/:subview',			's1.home.list_install.details.results').
		when('/type/:type/cmpnt_type/:cmpnt_type?/serialno/:serialno?/list',														's1.home.list_inventory').
		when('/type/:type/cmpnt_type/:cmpnt_type?/serialno/:serialno?/id/:id/:view',												's1.home.list_inventory.details').
		when('/type/:type/cmpnt_type/:cmpnt_type?/serialno/:serialno?/id/:id/:view/:subview',										's1.home.list_inventory.details.results').

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
						dependencies: ['id', 'view']
					}).
					within().
						segment('results', {
							templateUrl: 'results.html',
							controller: 'showResultsCtrl',
							dependencies: ['subview']
						}).
					up().
				up().
				segment('list_install', {
					templateUrl: 'list.html',
					controller: 'listDevicesCtrl',
					dependencies: ['type', 'system', 'name', 'cmpnt_type', 'serialno']
				}).
				within().
					segment('wizard', {
						templateUrl: 'wizard.html',
						controller: 'showWizardCtrl',
						dependencies: ['inst_id']
					}).
					within().
						segment('md', {
							templateUrl: 'md.html',
							controller: 'showWizardCtrl'
						}).
						segment('mt', {
							templateUrl: 'mt.html',
							controller: 'showWizardCtrl'
						}).
						within().
							segment('m', {
								templateUrl: 'municonv.html',
								controller: 'showWizardCtrl'
							}).
							segment('mc', {
								templateUrl: 'municonv_chain.html',
								controller: 'showWizardCtrl'
							}).
						up().
					up().
					segment('details', {
						templateUrl: 'details.html',
						controller: 'showDetailsCtrl',
						dependencies: ['id', 'view']
					}).
					within().
						segment('results', {
							templateUrl: 'results.html',
							controller: 'showResultsCtrl',
							dependencies: ['subview']
						}).
					up().
				up().
			up().
		up();

		$routeProvider.otherwise({redirectTo: '/'});
});