'use strict';

var szClient = angular.module('sz.client.services', ['ngResource']);
/* Services */

'use strict';

var szClient = angular.module('sz.client.services', ['ngResource']);
/* Services */

szClient.factory('feedService', function($resource){
    return $resource('../../api/places/feed', {}, {
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
                var id = '4f5c11d0e4b0a4baa31f481b'
                return $resource('../../api/places/'+id,{}, {
                        query: { method:'GET' } 
                });
        });

