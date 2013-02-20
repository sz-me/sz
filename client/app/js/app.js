'use strict';
angular.module('sz.client', ['sz.client.directives', 'sz.client.services'])
	.config(['$routeProvider', function($routeProvider) {$routeProvider
		.when('/q/:query/:location', {templateUrl: 'partials/feed.html', controller: FeedController})
		.when('/q/:query', {templateUrl: 'partials/feed.html', controller: FeedController})
                .when('/new_message:query', {templateUrl: 'partials/new_message.html', controller: NewMessageController})
		.when('/place/feed', {templateUrl: 'partials/feed.html', controller: FeedController})
		.when('/v/:placeId', {templateUrl: 'partials/place.html', controller: PlaceController})
		.otherwise({redirectTo: '/place/feed'});
        
}])
.constant('ENDPOINT','LOCAL');
