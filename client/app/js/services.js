'use strict';


var szClient = angular.module('sz.client.services', ['ngResource']);
/* Services */

szClient.factory('feedService', function($resource){
    return $resource('../../api/places/newsfeed', {}, {
        query: { method:'GET', params:{}, isArray:false }
    });
});

szClient.factory('geolocationService', ['$q', '$rootScope', function($q, $rootScope) {
    return function() {
        var changeLocation= function (coords) {
            $rootScope.$broadcast("locationChanged", {
                coordinates: coords
            });
        };
        var d = $q.defer();
        setTimeout(function () {
            try {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function (position) {
                            $rootScope.$apply(function () {
                                changeLocation(position.coords);
                            });
                        },
                        function (error) {
                            d.reject(error);
                        }
                    );
                }
                else {
                    d.reject('location services not allowed');
                }
            }
            catch (err) {
                d.reject(err);
            }
        }, 1000);
        return d.promise;
    };}]);

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

