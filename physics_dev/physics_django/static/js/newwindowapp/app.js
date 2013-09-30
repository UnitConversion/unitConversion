/*
 * Create new window module and add include dependencies
 */
var measurementDataApp = angular.module('measurementData', ['ngResource', 'ngRoute', 'route-segment', 'view-segment']);

/*
 * Define routes for our module
 */
//measurementDataApp.config(function($routeSegmentProvider, $routeProvider){
//
//	$routeSegmentProvider.options.autoLoadTemplates = true;
//
//	$routeSegmentProvider.
//		when('/type/:type/id/:id', 's1').
//
//		segment('s1', {
//			templateUrl: "measurement_data.html",
//			controller: 'measurementDataCtrl'
//		});
//
//		//$routeProvider.otherwise({redirectTo: '/'});
//});