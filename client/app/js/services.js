'use strict';


var szClient = angular.module('sz.client.services', ['ngResource']);

/* Services */
szClient.factory('newsFeedService', function($resource){
    return $resource('../../api/places/:placeId/newsfeed', {}, {
        query: { method:'GET', params:{}, isArray:false }
    });
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
                return $resource('../../api/categories', {}, {
                        query: { method:'GET' }
                });
        });

szClient.factory('placeService', function($resource){
                var id = '5003c692e4b0946792cb335e'
                return $resource('../../api/places/'+id,{}, {
                        query: { method:'GET' } 
                });
        });

szClient.factory('authService', function($resource){
    return $resource('../../api/auth/:action', {}, {
        login: { method:'POST', params:{action: 'login'}, isArray:false },
        logout: { method:'POST', params:{action: 'logout'}, isArray:false },
        user: { method:'GET', params:{action: 'user'}, isArray:false }
    });
});

