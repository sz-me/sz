'use strict';
angular.module('sz.client', ['sz.client.directives', 'sz.client.services'])
	.config(['$routeProvider', function($routeProvider) {$routeProvider
        .when('/newsfeed', {templateUrl: 'partials/feed.html', controller: FeedController})
        .when('/new_message:query', {templateUrl: 'partials/new_message.html', controller: NewMessageController})
		.when('/v/:placeId', {templateUrl: 'partials/place.html', controller: PlaceController})
		.otherwise({redirectTo: '/newsfeed'});
        
}])
.constant('ENDPOINT','LOCAL');
