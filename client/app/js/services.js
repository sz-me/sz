'use strict';


var szServices = angular.module('sz.client.services', ['ngResource']);

/* Services */
szServices.factory('placeService', function($resource){
    return $resource('../../api/places/:listCtrl:placeId/:docCtrl', {placeId: '@id'}, {
        $newsfeed: { method:'GET', params:{docCtrl: 'newsfeed' }, isArray:false },
        newsfeed: { method:'GET', params:{listCtrl: 'newsfeed', placeId: '' }, isArray:false },
        search: { method:'GET', params:{listCtrl: 'search' }, isArray:true },
        searchInVenues: { method:'GET', params:{listCtrl: 'search-in-venues' }, isArray:true }
    });
});

szServices.factory('messageService', function($resource){
    return $resource('../../api/messages/:messageId', {messageId: '@id'}, {
        query: { method:'GET', params:{}, isArray:false },
        search: { method:'GET', params:{messageId:'search'}, isArray:false }
    });
});


szServices.factory('messagePreviewService', function($http, $resource){

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

    var resource = $resource('../../api/messages/previews/:previewId/:docCtrl', {previewId: '@id'}, {
        query: { method:'GET', params:{}, isArray:false },
        publish: { method:'POST', params:{docCtrl: 'publish'}, isArray:false }
    });

    resource.create = create;
    resource.update = update;
    return resource;
});


szServices.factory('geolocationService', function ($rootScope) {
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


szServices.factory('categoryService', function($resource){
                return $resource('../../api/categories', {}, {});
        });


szServices.factory('sessionService', function($resource){
    return $resource('../../api/auth/:action', {}, {
        login: { method:'POST', params:{action: 'login'}, isArray:false },
        logout: { method:'POST', params:{action: 'logout'}, isArray:false },
        current: { method:'GET', params:{action: 'user'}, isArray:false }
    });
});

