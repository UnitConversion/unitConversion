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
		when('/vendor',																										'index.vendor').
		when('/vendor/search/:search/name/:name?/description/:description?/list',											'index.vendor.list').
		when('/vendor/search/:search/name/:name?/description/:description?/id/:id/action/:action',							'index.vendor.list.details').
		
		when('/cmpnt_type',																									'index.cmpnt_type').
		when('/cmpnt_type/search/:search/name/:name?/description/:description?/list',										'index.cmpnt_type.list').
		when('/cmpnt_type/search/:search/name/:name?/description/:description?/id/:id/action/:action',						'index.cmpnt_type.list.details').
		
		when('/cmpnt_type_type',																							'index.cmpnt_type_type').
		when('/cmpnt_type_type/search/:search/name/:name?/description/:description?/list',									'index.cmpnt_type_type.list').
		when('/cmpnt_type_type/search/:search/name/:name?/description/:description?/id/:id/action/:action',					'index.cmpnt_type_type.list.details').

		when('/inventory',																									'index.inventory').
		when('/inventory/search/:search/name/:name?/list',																	'index.inventory.list').
		when('/inventory/search/:search/name/:name?/id/:id/action/:action',													'index.inventory.list.details').

		when('/inventory_type',																								'index.inventory_type').
		when('/inventory_type/search/:search/name/:name?/list',																'index.inventory_type.list').
		when('/inventory_type/search/:search/name/:name?/id/:id/action/:action',											'index.inventory_type.list.details').
		
		when('/install',																																			'index.install').
		when('/install/search/:search/name/:name?/cmpnt_type/:cmpnt_type?/description/:description?/coordinatecenter/:coordinatecenter?/list',						'index.install.list').
		when('/install/search/:search/name/:name?/cmpnt_type/:cmpnt_type?/description/:description?/coordinatecenter/:coordinatecenter?/id/:id/action/:action',		'index.install.list.details').

		when('/install_rel',																								'index.install_rel').
		when('/install_rel/search/:search/description/:description?/parent_install/:parent_install?/list',					'index.install_rel.list').
		when('/install_rel/search/:search/description/:description?/parent_install/:parent_install?/id/:id/action/:action',	'index.install_rel.list.details').

		when('/install_rel_type',																							'index.install_rel_type').
		when('/install_rel_type/search/:search/name/:name?/list',															'index.install_rel_type.list').
		when('/install_rel_type/search/:search/name/:name?/id/:id/action/:action',											'index.install_rel_type.list.details').

		when('/data_method',																								'index.data_method').
		when('/data_method/search/:search/name/:name?/description/:description?/list',										'index.data_method.list').
		when('/data_method/search/:search/name/:name?/description/:description?/id/:id/action/:action',						'index.data_method.list.details').
		
		when('/offline_data',																								'index.offline_data').
		when('/offline_data/search/:search/inventory_name/:inventory_name?/description/:description?/list',					'index.offline_data.list').
		when('/offline_data/search/:search/inventory_name/:inventory_name?/description/:description?/id/:id/action/:action','index.offline_data.list.details').
		
		when('/online_data',																								'index.online_data').
		when('/online_data/search/:search/install_name/:install_name?/description/:description?/list',						'index.online_data.list').
		when('/online_data/search/:search/install_name/:install_name?/description/:description?/id/:id/action/:action',		'index.online_data.list.details').

		segment('index', {
			templateUrl: 'content.html',
			controller: 'mainCtrl'
		}).
		
		within().
			segment('vendor', {
				templateUrl: 'search/vendor.html',
				controller: 'searchVendorCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list/vendor.html',
					controller: 'listVendorCtrl',
					dependencies: ['search']
				}).
				within().
					segment('details', {
						templateUrl: 'details/vendor.html',
						controller: 'showVendorCtrl',
						dependencies: ['id', 'action']
					}).
				up().
			up().
		up().

		within().
			segment('cmpnt_type', {
				templateUrl: 'search/cmpnt_type.html',
				controller: 'searchCmpntTypeCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list/cmpnt_type.html',
					controller: 'listCmpntTypeCtrl',
					dependencies: ['search']
				}).
				within().
					segment('details', {
						templateUrl: 'details/cmpnt_type.html',
						controller: 'showCmpntTypeCtrl',
						dependencies: ['id', 'action']
					}).
				up().
			up().
		up().

		within().
			segment('cmpnt_type_type', {
				templateUrl: 'search/cmpnt_type_type.html',
				controller: 'searchCmpntTypeTypeCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list/cmpnt_type_type.html',
					controller: 'listCmpntTypeTypeCtrl',
					dependencies: ['search']
				}).
				within().
					segment('details', {
						templateUrl: 'details/cmpnt_type_type.html',
						controller: 'showCmpntTypeTypeCtrl',
						dependencies: ['id', 'action']
					}).
				up().
			up().
		up().

		within().
			segment('inventory', {
				templateUrl: 'search/inventory.html',
				controller: 'searchInventoryCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list/inventory.html',
					controller: 'listInventoryCtrl',
					dependencies: ['search']
				}).
				within().
					segment('details', {
						templateUrl: 'details/inventory.html',
						controller: 'showInventoryCtrl',
						dependencies: ['id', 'action']
					}).
				up().
			up().
		up().

		within().
			segment('inventory_type', {
				templateUrl: 'search/inventory_type.html',
				controller: 'searchInventoryTypeCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list/inventory_type.html',
					controller: 'listInventoryTypeCtrl',
					dependencies: ['search']
				}).
				within().
					segment('details', {
						templateUrl: 'details/inventory_type.html',
						controller: 'showInventoryTypeCtrl',
						dependencies: ['id', 'action']
					}).
				up().
			up().
		up().

		within().
			segment('install', {
				templateUrl: 'search/install.html',
				controller: 'searchInstallCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list/install.html',
					controller: 'listInstallCtrl',
					dependencies: ['search']
				}).
				within().
					segment('details', {
						templateUrl: 'details/install.html',
						controller: 'showInstallCtrl',
						dependencies: ['id', 'action']
					}).
				up().
			up().
		up().

		within().
			segment('install_rel', {
				templateUrl: 'search/install_rel.html',
				controller: 'searchInstallRelCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list/install_rel.html',
					controller: 'listInstallRelCtrl',
					dependencies: ['search']
				}).
				within().
					segment('details', {
						templateUrl: 'details/install_rel.html',
						controller: 'showInstallRelCtrl',
						dependencies: ['id', 'action', 'parent_install']
					}).
				up().
			up().
		up().

		within().
			segment('install_rel_type', {
				templateUrl: 'search/install_rel_type.html',
				controller: 'searchInstallRelTypeCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list/install_rel_type.html',
					controller: 'listInstallRelTypeCtrl',
					dependencies: ['search']
				}).
				within().
					segment('details', {
						templateUrl: 'details/install_rel_type.html',
						controller: 'showInstallRelTypeCtrl',
						dependencies: ['id', 'action']
					}).
				up().
			up().
		up().

		within().
			segment('data_method', {
				templateUrl: 'search/data_method.html',
				controller: 'searchDataMethodCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list/data_method.html',
					controller: 'listDataMethodCtrl',
					dependencies: ['search']
				}).
				within().
					segment('details', {
						templateUrl: 'details/data_method.html',
						controller: 'showDataMethodCtrl',
						dependencies: ['id', 'action']
					}).
				up().
			up().
		up().

		within().
			segment('offline_data', {
				templateUrl: 'search/offline_data.html',
				controller: 'searchOfflineDataCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list/offline_data.html',
					controller: 'listOfflineDataCtrl',
					dependencies: ['search']
				}).
				within().
					segment('details', {
						templateUrl: 'details/offline_data.html',
						controller: 'showOfflineDataCtrl',
						dependencies: ['id', 'action']
					}).
				up().
			up().
		up().

		within().
			segment('online_data', {
				templateUrl: 'search/online_data.html',
				controller: 'searchOnlineDataCtrl'
			}).
			within().
				segment('list', {
					templateUrl: 'list/online_data.html',
					controller: 'listOnlineDataCtrl',
					dependencies: ['search']
				}).
				within().
					segment('details', {
						templateUrl: 'details/online_data.html',
						controller: 'showOnlineDataCtrl',
						dependencies: ['id', 'action']
					}).
				up().
			up().
		up();
	
		//$routeProvider.otherwise({redirectTo: '/vendor'});
});