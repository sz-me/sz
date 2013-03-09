'use strict';


var szClient = angular.module('sz.client.services', ['ngResource']);

/* Services */
szClient.factory('placeService', function($resource){
    return $resource('../../api/places/:placeId', {}, {
        query: { method:'GET', params:{}, isArray:false }
    });
});

szClient.factory('newsFeedService', function($resource){
    return $resource('../../api/places/:placeId/newsfeed', {}, {
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

szClient.factory('messagePreviewService', function($http){
    var create = function(params, success, error){
        $http.post('../../api/places/'+ params.placeId +'/messages', params.message, {
            headers: { 'Content-Type': false },
            transformRequest: angular.identity,
            params: {format: 'json'}
        }).success(success).error(error);
    }

    return { create: create }
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

