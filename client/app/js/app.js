'use strict';
angular.module('sz.client', ['sz.client.directives', 'sz.client.services', 'ngResource', 'ngCookies'])
	.config(['$routeProvider', function($routeProvider) {$routeProvider
        .when('/newsfeed', {templateUrl: 'partials/newsfeed.html', controller: NewsFeedController})
        .when('/place_list', {templateUrl: 'partials/place_list.html', controller: PlaceListController})
        .when('/places/:placeId', {templateUrl: 'partials/place.html', controller: PlaceController})
        .when('/places/:placeId/messages/add', {templateUrl: 'partials/message-edit.html', controller: MessageEditorController})
        .when('/places/:placeId/messages/add/:previewId/edit', {templateUrl: 'partials/message-edit.html', controller: MessageEditorController})
        .when('/places/:placeId/messages/add/:previewId/pub', {templateUrl: 'partials/message-pub.html', controller: MessagePublisherController})
        .when('/places/:placeId/gallery', {templateUrl: 'partials/gallery.html', controller: GalleryController})
        .when('/places/:placeId/messages/:messageId', {templateUrl: 'partials/message.html', controller: MessageController})
        .when('/login', {templateUrl: 'partials/login.html', controller: LoginController})
        .when('/registration', {templateUrl: 'partials/registration.html', controller: RegistrationController})
        .when('/search', {templateUrl: 'partials/search.html', controller: SearchController})
        .when('/errors/geolocation', {templateUrl: 'partials/geolocation-error.html'})
        
        .otherwise({redirectTo: '/newsfeed'});
        
}])
.constant('ENDPOINT','LOCAL');
