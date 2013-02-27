'use strict';


var szClient = angular.module('sz.client.services', ['ngResource']);
/* Services */

szClient.factory('feedService', function($resource){
    return $resource('../../api/places/newsfeed', {}, {
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

/*
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
                            d.resolve(position)
                            //$rootScope.$apply(function () {
                            //    changeLocation(position.coords);
                            //});
                        },
                        function (error) {
                            d.reject(error);
                        }
                    );
                }
                else {
                    d.reject('Geolocation service is not available!');
                }
            }
            catch (err) {
                d.reject(err);
            }
        }, 1000);
        return d.promise;

        var deferred = $q.defer();

        setTimeout(function() {
            // since this fn executes async in a future turn of the event loop, we need to wrap
            // our code into an $apply call so that the model changes are properly observed.
            $rootScope.$apply(function() {
                if (navigator.geolocation) {

                    navigator.geolocation.getCurrentPosition(

                        function (position) { deferred.resolve(position); },
                        function (error){ deferred.reject(error); },
                        {
                            enableHighAccuracy: false,
                            timeout: 30000,
                            maximumAge: 0
                        }
                    );

                } else {
                    deferred.reject({message:'Geolocation service is not available!'});
                }
            });
        }, 1000);

        return deferred.promise;
    };}]);
*/
szClient.factory('shmotCategoryService', function($resource){
                return $resource('../../api/categories', {}, {
                        query: { method:'GET' }
                });
        });

szClient.factory('placeService', function($resource){
                var id = '4f5c11d0e4b0a4baa31f481b'
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

