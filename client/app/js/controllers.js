﻿function MasterPageController($scope, $cookies, $http, $location, geolocationService, shmotCategoryService, authService) {    $scope.$watch('user', function(newValue, oldValue) {        if (angular.isDefined($scope.user))            $scope.showBtnNewMessage = $scope.user.is_authenticated;        else            $scope.showBtnNewMessage = false;        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;        $scope.csrftoken = $cookies.csrftoken    });    var userResponse = authService.user({}, function() {        $scope.user = userResponse.data;    })    $scope.logout = function(){        var userResponse = authService.logout({}, function(){            $scope.user = userResponse.data;        })    }    $scope.login = function(username, password){        var userResponse = authService.login({username: username, password: password }, function() {                $scope.user = userResponse.data;            }        )    }    geolocationService.getCurrentPosition(        function (position) { $scope.coordinates = position.coords; },        function (error) { $location.path('/errors/geolocation'); }    )    var categories = shmotCategoryService.query(function(){$scope.categories = categories.data; });    $scope.collapseTopMenu = false;    $scope.showContent = true;    $scope.showMenuPanel = true;    $scope.showBotMenuPanel = true;    $scope.scrollToTop = {top:false};    $scope.changeScrollToUp = function(){$scope.showBotMenuPanel = true;};    $scope.changeScrollToDown = function(){$scope.showBotMenuPanel = false;};}function LoginController($scope) {}function RegistrationController($scope){    $scope.registration = function(){}}function NewsFeedController($scope, newsFeedService) {    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            $scope.feed = newsFeedService.query({                    longitude: $scope.coordinates.longitude,                    latitude: $scope.coordinates.latitude                });    });    $scope.loadMorePlaces = function(){        if ($scope.feed.data.params.offset + $scope.feed.data.params.limit < $scope.feed.data.count)        {            $scope.feed.data.params.offset += $scope.feed.data.params.limit;            var feed = newsFeedService.query($scope.feed.data.params, function() {                        if(feed.data.results.length>0){                            $.each(feed.data.results,function(index,r){                                $scope.feed.data.results.push(r)                            });                            $scope.feed.data.params = feed.data.params;                        }                        else{$scope.$emit($scope.scrollToTop.top=true);}                    }            );        }    }    $scope.placeMessagesLimit = 1;    $scope.showAllPlaceMessages = function(len,lim){        if(lim==1){return len}        else{return 1}    }    $scope.showAllPlaceMessagesText = function(len,lim){        if(lim==1){return 'Еще '+len+' сообщений'}        else{return 'Свернуть'}    }}function PlaceController($scope, $routeParams, newsFeedService) {    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            var feed = newsFeedService.query({                longitude: $scope.coordinates.longitude,                latitude: $scope.coordinates.latitude,                placeId: $routeParams.placeId                },                function(){                    $scope.feed=feed.data.messages;                    $scope.place=feed.data.place;                    $scope.feedPhoto=feed.data.photos;                });    });    $scope.showPlaceMessages = true;    $scope.showPlacePhoto = false;        $scope.showPlaceMessagesClick = function(){        $scope.showPlaceMessages = true;        $scope.showPlacePhoto = false;    }        $scope.showPlacePhotoClick = function(){        $scope.showPlaceMessages = false;        $scope.showPlacePhoto = true;    }        $scope.loadMore = function(){        if($scope.showPlacePhoto){var oldFeed = $scope.feedPhoto}        if($scope.showPlaceMessages){var oldFeed = $scope.feed}                if (oldFeed.params.offset + oldFeed.params.limit < oldFeed.count)        {            oldFeed.params.offset += oldFeed.params.limit;            oldFeed.params['placeId'] = $routeParams.placeId;            oldFeed.params['longitude'] = $scope.coordinates.longitude;            oldFeed.params['latitude'] = $scope.coordinates.latitude;            var feed = newsFeedService.query(oldFeed.params,                    function() {                        if($scope.showPlacePhoto){var newFeed = feed.data.photos}                        if($scope.showPlaceMessages){var newFeed = feed.data.messages}                        if(newFeed.results.length>0){                            $.each(newFeed.results,function(index,r){                                if($scope.showPlacePhoto){$scope.feedPhoto.results.push(r)}                                if($scope.showPlaceMessages){$scope.feed.results.push(r)}                            });                            if($scope.showPlacePhoto){$scope.feedPhoto.params = newFeed.params;}                            if($scope.showPlaceMessages){$scope.feed.params = newFeed.params;}                                                    }                        else{$scope.$emit($scope.scrollToTop.top=true);}                    }            );        }    }}function MessageController($scope,$routeParams,messageService){    $scope.message = messageService.get({messageId:$routeParams.messageId})}function SearchController($scope){    $scope.showCollapseCat = false;    $scope.filter = {        radius:'',        query:'',        category:''    }    $scope.setCategory = function(){        if($scope.shmot_cat){$scope.filter.category = $scope.shmot_cat.id}        else{$scope.filter.category = ''}    }}function MessageAdditionController($location, $scope, $routeParams, placeService, messagePreviewService) {    var place = placeService.get({placeId: $routeParams.placeId}, function(){ $scope.place = place.data; })    $scope.inProgress = false;    $scope.messagePhotoIco = 'icon-picture';    $scope.removePhoto = false;    $scope.send = function() {        var message = new FormData();        message.append( 'text', $scope.text);        message.append( 'photo', $scope.photo);        $scope.inProgress = true;        messagePreviewService.create({placeId: $routeParams.placeId, message: message},            function(){                $location.path('/v/' + $scope.place.id);            },            function(response){                alert(response.meta.code);                $scope.inProgress = false;            });    }}function PlaceListController($scope,venueService){    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            var placeListResponse = venueService.query(                {                longitude: $scope.coordinates.longitude,                latitude: $scope.coordinates.latitude                },                function(){                    $scope.placeList=placeListResponse.data;                }            );    });}