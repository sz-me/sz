'use strict';
angular.module('sz.client', ['sz.client.directives', 'sz.client.services'])
	.config(['$routeProvider', function($routeProvider) {$routeProvider
		.when('/q/:query/:location', {templateUrl: 'partials/feed.html', controller: FeedController})
		.when('/q/:query', {templateUrl: 'partials/feed.html', controller: FeedController})
		.when('/v/:placeId', {templateUrl: 'partials/place.html', controller: PlaceController})
		.otherwise({redirectTo: '/q//city'});
}])
.constant('ENDPOINT','LOCAL');