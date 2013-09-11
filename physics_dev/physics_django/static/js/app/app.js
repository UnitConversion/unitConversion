/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
var app = angular.module('conversion', ['ui.bootstrap', 'ngResource', 'ngRoute', 'route-segment', 'view-segment']);

app.config(function($routeSegmentProvider, $routeProvider){

	$routeSegmentProvider.options.autoLoadTemplates = true;

	$routeSegmentProvider.
		when('/',									's1.home').
		when('/system=:systemName&name=:name',		's1.home.list').
		when('/:query/id=:id',						's1.home.list.details').

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
					controller: 'listDevicesCtrl'
				}).
				within().
					segment('details', {
						templateUrl: 'details.html',
						controller: 'showDetailsCtrl'
					}).
				up().
			up().
		up();

		$routeProvider.otherwise({redirectTo: '/'});
});