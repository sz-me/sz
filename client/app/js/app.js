'use strict';
angular.module('sz.client', ['sz.client.directives', 'sz.client.services'])
	.config(['$routeProvider', function($routeProvider) {$routeProvider
		.when('/place/feed', {templateUrl: 'partials/feed.html', controller: FeedController})
                .when('/place/search', {templateUrl: 'partials/place_list.html', controller: PlaceListController})
		.when('/v/:placeId', {templateUrl: 'partials/place.html', controller: PlaceController})
		.otherwise({redirectTo: '/place/feed'});
        
}])
.constant('ENDPOINT','LOCAL');