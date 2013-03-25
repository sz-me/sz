'use strict';
var szApp = angular.module('sz.client', ['sz.client.directives', 'sz.client.services', 'ngResource', 'ngCookies'])

szApp.config(['$routeProvider', function($routeProvider) {
    $routeProvider
        .when('/newsfeed', {templateUrl: 'partials/newsfeed.html', controller: NewsFeedController})
        .when('/places/select', {templateUrl: 'partials/place-select.html', controller: PlaceSelectionController})
        .when('/places/:placeId', {templateUrl: 'partials/place.html', controller: PlaceController})
        .when('/places/:placeId/messages/add', {templateUrl: 'partials/message-edit.html', controller: MessageEditorController})
        .when('/messages/previews/:previewId/edit', {templateUrl: 'partials/message-edit.html', controller: MessageEditorController})
        .when('/messages/previews/:previewId/publish', {templateUrl: 'partials/message-pub.html', controller: MessagePublisherController})
        .when('/places/:placeId/gallery', {templateUrl: 'partials/gallery.html', controller: GalleryController})
        .when('/messages/:messageId', {templateUrl: 'partials/message.html', controller: MessageController})
        .when('/login', {templateUrl: 'partials/login.html', controller: LoginController})
        .when('/registration', {templateUrl: 'partials/registration.html', controller: RegistrationController})
        .when('/search', {templateUrl: 'partials/search.html', controller: SearchController,reloadOnSearch:false})
//         .when('/search:query', {templateUrl: 'partials/search.html', controller: SearchController})
        .when('/errors/geolocation', {templateUrl: 'partials/geolocation-error.html'})
        .otherwise({redirectTo: '/newsfeed'});
}]);

szApp.config(['$httpProvider', function($httpProvider){
    $httpProvider.responseInterceptors.push(function($q) {
        return function(promise){
            return promise.then(function(response) {
                if (angular.isDefined(response.data.data))
                    response.data = response.data.data;
                return response;
            }, function(response) {
                console.error(angular.toJson(response.data));
                return $q.reject(response);
            });
        }
    });
}]);

szApp.constant('ENDPOINT','LOCAL');
