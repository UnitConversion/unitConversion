/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
var app = angular.module('conversion', ['ui.bootstrap', 'ngResource']);

app.config(['$routeProvider', function($routeProvider){
	$routeProvider.
		when('/system=:systemName', {
			templateUrl: 'content.html',
			controller: 'devicesListCtrl'
		}).
		when('/', {
			templateUrl: 'content.html',
			controller: 'systemsListCtrl'
		}).
		otherwise({redirectTo: '/'});
}]);