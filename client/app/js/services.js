'use strict';


var szClient = angular.module('sz.client.services', ['ngResource']);

/* Services */
szClient.factory('placeService', function($resource){
    return $resource('../../api/places/:placeId/:ctrl', {placeId: '@data.id'}, {
        newsfeed: { method:'GET', params:{ctrl: 'newsfeed' }, isArray:false }
    });
});

szClient.factory('newsFeedService', function($resource){
    return $resource('../../api/places/:placeId/newsfeed', {}, {
        query: { method:'GET', params:{}, isArray:false }
    });
});

szClient.factory('messageService', function($resource){
    return $resource('../../api/messages/:messageId', {}, {
        query: { method:'GET', params:{}, isArray:false }
    });
});

szClient.factory('venueService', function($resource){
    return $resource('../../api/places/venues/search', {}, {
        query: { method:'GET', params:{}, isArray:false }
    });
//     return $resource('../../api/places/search', {}, {
//         query: { method:'GET', params:{}, isArray:false }
//     });
});


szClient.factory('messagePreviewService', function($http, $resource){

    var create = function(message, success, error){
        $http.post('../../api/messages/previews', message, {
            headers: { 'Content-Type': false },
            transformRequest: angular.identity,
            params: {format: 'json'}
        }).success(success).error(error);
    }
    var update = function(previewId, message, success, error){
        $http.put('../../api/messages/previews/' + previewId, message, {
            headers: { 'Content-Type': false },
            transformRequest: angular.identity,
            params: {format: 'json'}
        }).success(success).error(error);
    }

    var resource = $resource('../../api/messages/previews/:previewId', {previewId: '@data.id'}, {
        query: { method:'GET', params:{}, isArray:false }
    });

    resource.create = create;
    resource.update = update;
    return resource;
});


szClient.factory('geolocationService', function ($rootScope) {
    return {
        getCurrentPosition: function (onSuccess, onError, options) {
            navigator.geolocation.getCurrentPosition(function () {
                    var that = this,
                        args = arguments;

                    if (onSuccess) {
                        $rootScope.$apply(function () {
                            onSuccess.apply(that, args);
                        });
                    }
                }, function () {
                    var that = this,
                        args = arguments;

                    if (onError) {
                        $rootScope.$apply(function () {
                            onError.apply(that, args);
                        });
                    }
                },
                options);
        }
    };
});

szClient.factory('shmotCategoryService', function($resource){
                return $resource('../../api/categories', {}, {query: { method:'GET' }});
        });



szClient.factory('authService', function($resource){
    return $resource('../../api/auth/:action', {}, {
        login: { method:'POST', params:{action: 'login'}, isArray:false },
        logout: { method:'POST', params:{action: 'logout'}, isArray:false },
        user: { method:'GET', params:{action: 'user'}, isArray:false }
    });
});

