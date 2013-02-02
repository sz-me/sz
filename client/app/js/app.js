'use strict';
angular.module('sz.client', ['sz.client.directives', 'sz.client.services','ui'])
	.config(['$routeProvider', function($routeProvider) {$routeProvider
		.when('/q/:query/:location', {templateUrl: 'partials/feed.html', controller: FeedController})
		.when('/q/:query', {templateUrl: 'partials/feed.html', controller: FeedController})
                .when('/place_list:query', {templateUrl: 'partials/place_list.html', controller: PlaceListController})
		.when('/v/:placeId', {templateUrl: 'partials/place.html', controller: PlaceController})
		.otherwise({redirectTo: '/q//city'});
        
}])
.constant('ENDPOINT','LOCAL');