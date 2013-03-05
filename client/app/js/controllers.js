﻿function MasterPageController($scope, $cookies, $http, $location, geolocationService, shmotCategoryService, authService) {    $scope.$watch('user', function(newValue, oldValue) {        if (angular.isDefined($scope.user))            $scope.showBtnNewMessage = $scope.user.is_authenticated;        else            $scope.showBtnNewMessage = false;        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;    });    var userResponse = authService.user({}, function() {        $scope.user = userResponse.data;    })    $scope.logout = function(){        var userResponse = authService.logout({}, function(){            $scope.user = userResponse.data;        })    }    $scope.login = function(username, password){        var userResponse = authService.login({username: username, password: password }, function() {                $scope.user = userResponse.data;            }        )    }    geolocationService.getCurrentPosition(        function (position) { $scope.coordinates = position.coords; },        function (error) { $location.path('/errors/geolocation'); }    )    var categories = shmotCategoryService.query(function(){$scope.categories = categories.data; });    $scope.collapseTopMenu = false;    $scope.showContent = true;    $scope.showMenuPanel = true;    $scope.showBotMenuPanel = true;    $scope.scrollToTop = {top:false};    $scope.changeScrollToUp = function(){$scope.showBotMenuPanel = true;};    $scope.changeScrollToDown = function(){$scope.showBotMenuPanel = false;};}function LoginController($scope) {}function RegistrationController($scope){    $scope.registration = function(){}}function NewsFeedController($scope, newsFeedService) {    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            $scope.feed = newsFeedService.query({                    longitude: $scope.coordinates.longitude,                    latitude: $scope.coordinates.latitude                });    });    $scope.loadMorePlaces = function(){        if ($scope.feed.data.params.offset + $scope.feed.data.params.limit < $scope.feed.data.count)        {            $scope.feed.data.params.offset += $scope.feed.data.params.limit;            var feed = newsFeedService.query($scope.feed.data.params, function() {                        if(feed.data.results.length>0){                            $.each(feed.data.results,function(index,r){                                $scope.feed.data.results.push(r)                            });                            $scope.feed.data.params = feed.data.params;                        }                        else{$scope.$emit($scope.scrollToTop.top=true);}                    }            );        }    }    $scope.placeMessagesLimit = 1;    $scope.showAllPlaceMessages = function(len,lim){        if(lim==1){return len}        else{return 1}    }    $scope.showAllPlaceMessagesText = function(len,lim){        if(lim==1){return 'Еще '+len+' сообщений'}        else{return 'Свернуть'}    }}function PlaceController($scope, $routeParams, newsFeedService) {    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            $scope.feed = newsFeedService.query({                longitude: $scope.coordinates.longitude,                latitude: $scope.coordinates.latitude,                placeId: $routeParams.placeId            });    });    $scope.showPlaceMessages = true;    $scope.showPlacePhoto = false;        $scope.showPlaceMessagesClick = function(){        $scope.showPlaceMessages = true;        $scope.showPlacePhoto = false;    }        $scope.showPlacePhotoClick = function(){        $scope.showPlaceMessages = false;        $scope.showPlacePhoto = true;    }}function MessageController($scope,$routeParams,messageService){    $scope.message = messageService.get({messageId:$routeParams.messageId})}function SearchController($scope){    $scope.showCollapseCat = false;    $scope.filter = {        radius:'',        query:'',        category:''    }    $scope.setCategory = function(){        if($scope.shmot_cat){$scope.filter.category = $scope.shmot_cat.id}        else{$scope.filter.category = ''}    }}function MessageAdditionController($location, $scope, $routeParams, placeService, messageService) {    var place = placeService.get({placeId: $routeParams.placeId}, function(){ $scope.place = place.data })//     var marks = messageService.marks({}, function(){ $scope.marks = marks.data })    $scope.results = function(response) {        var responseObj = angular.fromJson(response);        if (responseObj.meta.code = 201){            var return_url = '/v/' + $scope.place.id;            $location.path(return_url);        }        else            alert(response);    }}function PlaceListController($scope,venueService){    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            var placeListResponse = venueService.query(                {                longitude: $scope.coordinates.longitude,                latitude: $scope.coordinates.latitude,                },                function(){                    $scope.placeList=placeListResponse.data;                }            );    });}