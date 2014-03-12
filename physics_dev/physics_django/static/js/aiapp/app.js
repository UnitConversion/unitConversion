/*
 * Create module and add include dependencies
 *
 * @created Mar 6, 2014
 * @author: Dejan Dežman <dejan.dezman@cosylab.com>
 */
var app = angular.module('aiapp', ['ui.bootstrap', 'ngRoute', 'route-segment', 'view-segment', 'xeditable']);

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
		when('/status/:status/tab/:tab',		'index.status').
		when('/status/:status/tab/:tab/bm',		'index.status.bm').
		when('/status/:status/tab/:tab/id',		'index.status.id').
		when('/status/:status/tab/:tab/logic',	'index.status.logic').
		when('/history',						'index.history').
		when('/dataset/:id',					'index.dataset').

		segment('index', {
			templateUrl: 'content.html',
			controller: 'mainCtrl',
			dependencies: ['status']
		}).
		within().
			segment('status', {
				templateUrl: 'data.html',
				controller: 'dataCtrl',
				dependencies: ['status', 'tab']
			}).
			within().
				segment('bm', {
					templateUrl: 'bm.html',
					controller: 'bmCtrl',
					dependencies: ['status', 'tab']
				}).
				segment('id', {
					templateUrl: 'id.html'
				}).
				segment('logic', {
					templateUrl: 'logic.html',
					controller: 'logicCtrl',
					dependencies: ['status', 'tab']
				}).
			up().
		up().
		within().
			segment('history', {
				templateUrl: 'history.html',
				controller: 'historyCtrl'
			}).
		up();

		$routeProvider.otherwise({redirectTo: '/status/editable/tab/bm/bm'});
})