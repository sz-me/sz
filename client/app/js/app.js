'use strict';
angular.module('sz.client', ['sz.client.directives', 'sz.client.services'])
	.config(['$routeProvider', function($routeProvider) {$routeProvider
        .when('/newsfeed', {templateUrl: 'partials/newsfeed.html', controller: NewsFeedController})
        .when('/new_message:query', {templateUrl: 'partials/new_message.html', controller: NewMessageController})
        .when('/v/:placeId', {templateUrl: 'partials/place.html', controller: PlaceController})
        .when('/message/:messageId', {templateUrl: 'partials/message.html', controller: MessageController})
        .when('/login', {templateUrl: 'partials/login.html', controller: LoginController})
        .when('/search', {templateUrl: 'partials/search.html', controller: SearchController})
        .otherwise({redirectTo: '/newsfeed'});
        
}])
.constant('ENDPOINT','LOCAL');
