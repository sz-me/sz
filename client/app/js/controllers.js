﻿function MasterPageController($scope, $cookies, $http, $location, geolocationService, shmotCategoryService, authService) {    $scope.isGeolocationInProgress = false;    $scope.$watch('user', function(newValue, oldValue) {        if (angular.isDefined($scope.user))            $scope.showBtnNewMessage = $scope.user.is_authenticated;        else            $scope.showBtnNewMessage = false;        $http.defaults.headers.post['X-CSRFToken'] = $cookies.csrftoken;        $http.defaults.headers.put['X-CSRFToken'] = $cookies.csrftoken;        $scope.csrftoken = $cookies.csrftoken    });    var userResponse = authService.user({}, function() {        $scope.user = userResponse.data;    })    $scope.logout = function(){        var userResponse = authService.logout({}, function(){            $scope.user = userResponse.data;        })    }    $scope.login = function(username, password){        var userResponse = authService.login({username: username, password: password }, function() {                $scope.user = userResponse.data;            }        )    }    geolocationService.getCurrentPosition(        function (position) { $scope.coordinates = position.coords; },        function (error) { $location.path('/errors/geolocation'); }    )    var categories = shmotCategoryService.query(function(){$scope.categories = categories.data; });    $scope.collapseTopMenu = false;    $scope.showContent = true;    $scope.showMenuPanel = true;    $scope.showBotMenuPanel = true;    $scope.scrollToTop = {top:false};    $scope.changeScrollToUp = function(){$scope.showBotMenuPanel = true;};    $scope.changeScrollToDown = function(){$scope.showBotMenuPanel = false;};    $scope.test = function(){alert(1)}}function LoginController($scope) {}function RegistrationController($scope){    $scope.registration = function(){}}function NewsFeedController($scope, newsFeedService) {    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            $scope.feed = newsFeedService.query({                longitude: $scope.coordinates.longitude,                latitude: $scope.coordinates.latitude            });    });    $scope.loadMorePlaces = function(){        if ($scope.feed.data.params.offset + $scope.feed.data.params.limit < $scope.feed.data.count)        {            $scope.feed.data.params.offset += $scope.feed.data.params.limit;            var feed = newsFeedService.query($scope.feed.data.params, function() {                    if(feed.data.results.length>0){                        $.each(feed.data.results,function(index,r){                            $scope.feed.data.results.push(r)                        });                        $scope.feed.data.params = feed.data.params;                    }                    else{$scope.$emit($scope.scrollToTop.top=true);}                }            );        }    }    $scope.placeMessagesLimit = 1;    $scope.showAllPlaceMessages = function(len,lim){        if(lim==1){return len}        else{return 1}    }    $scope.showAllPlaceMessagesText = function(len,lim){        if(lim==1){return 'Еще '+len+' сообщений'}        else{return 'Свернуть'}    }}function PlaceController($scope, $routeParams, placeService) {    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            var feed = placeService.newsfeed({                    longitude: $scope.coordinates.longitude,                    latitude: $scope.coordinates.latitude,                    placeId: $routeParams.placeId                },                function(){                    $scope.feed=feed.data.messages;                    $scope.place=feed.data.place;                    $scope.feedPhoto=feed.data.photos;                });    });    $scope.loadMore = function(){        var oldFeed = $scope.feed;        if (oldFeed.params.offset + oldFeed.params.limit < oldFeed.count)        {            oldFeed.params.offset += oldFeed.params.limit;            oldFeed.params['placeId'] = $routeParams.placeId;            oldFeed.params['longitude'] = $scope.coordinates.longitude;            oldFeed.params['latitude'] = $scope.coordinates.latitude;            var feed = newsFeedService.query(oldFeed.params,                function() {                    if(feed.data.messages.results.length>0){                        $.each(feed.data.messages.results,function(index,r){                            $scope.feed.results.push(r)                        });                        $scope.feed.params = feed.data.messages.params;                    }                    else{$scope.$emit($scope.scrollToTop.top=true);}                }            );        }    }}function GalleryController($scope,$routeParams,newsFeedService){    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            var feed = newsFeedService.query({                    longitude: $scope.coordinates.longitude,                    latitude: $scope.coordinates.latitude,                    placeId: $routeParams.placeId                },                function(){                    $scope.place=feed.data.place;                    $scope.feedPhoto=feed.data.photos;                });    });    $scope.loadMore = function(){        var oldFeed = $scope.feedPhoto;        if (oldFeed.params.offset + oldFeed.params.limit < oldFeed.count)        {            oldFeed.params.offset += oldFeed.params.limit;            oldFeed.params['placeId'] = $routeParams.placeId;            oldFeed.params['longitude'] = $scope.coordinates.longitude;            oldFeed.params['latitude'] = $scope.coordinates.latitude;            var feed = newsFeedService.query(oldFeed.params,                function() {                    if(feed.data.photos.results.length>0){                        $.each(feed.data.photos.results,function(index,r){                            $scope.feedPhoto.results.push(r)                        })                        $scope.feedPhoto.params = feed.data.photos.params;                    }                    else{$scope.$emit($scope.scrollToTop.top=true);}                }            );        }    }}function MessageController($scope,$routeParams,messageService){    var message = messageService.get({messageId:$routeParams.messageId},        function(){$scope.message = message.data})}function SearchController($scope){    $scope.showCollapseCat = false;    $scope.filter = {        radius:'',        query:'',        category:''    }    $scope.setCategory = function(){        if($scope.shmot_cat){$scope.filter.category = $scope.shmot_cat.id}        else{$scope.filter.category = ''}    }}function MessageEditorController($location, $scope, $routeParams, placeService, messagePreviewService) {    var place = placeService.get({placeId: $routeParams.placeId}, function(){ $scope.place = place.data; })    if (angular.isDefined($routeParams.previewId))        var preview = messagePreviewService.get({previewId: $routeParams.previewId}, function(){            $scope.text = preview.data.text;            $scope.photoUrl = preview.data.photo.thumbnail        });    $scope.inProgress = false;    $scope.send = function() {        $scope.inProgress = true;        var message = new FormData();        message.append( 'place', $routeParams.placeId);        message.append( 'text', $scope.text);        message.append( 'photo', $scope.photo);        message.append( 'smile', 1);        var redirectToPublish = function(previewId){            var pub_page_url = '/places/' + $routeParams.placeId                + '/messages/add/' + previewId + '/pub';            $location.path(pub_page_url);        }        if (angular.isUndefined($routeParams.previewId))            messagePreviewService.create(message,                function(response){                    $scope.inProgress = false;                    $scope.response = response.data;                    var edit_page_url = '/places/' + $routeParams.placeId                        + '/messages/add/' + $scope.response.id + '/edit';                    //$location.replace()                    history.replaceState(null, "SZ - Edit message", '#' + edit_page_url);                    redirectToPublish(response.data.id);                },                function(error){alert(angular.toJson(error, true));});        else            messagePreviewService.update($routeParams.previewId, message,                function(response){                    $scope.inProgress = false;                    $scope.response = response.data;                    redirectToPublish(response.data.id);                },                function(error){alert(angular.toJson(error, true));});    }}function MessagePublisherController($location, $scope, $routeParams, placeService, messagePreviewService) {    if (angular.isDefined($routeParams.previewId))        var preview = messagePreviewService.get({previewId: $routeParams.previewId}, function(){            $scope.text = preview.data.text;            $scope.photoUrl = preview.data.photo.reduced        });    $scope.removeCat = function(messageCat){        $.each($scope.new_message_categories,function(index,cat){            if(cat.name==messageCat.name){                $scope.new_message_categories.splice(index, 1)            }        })    }    $scope.ok = function(){        var path = '/places/' + $scope.place.id;        $location.path(path);    }}function PlaceListController($scope,venueService){    $scope.filter={        radius:0    }    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            var placeListResponse = venueService.query(                {                    longitude: $scope.coordinates.longitude,                    latitude: $scope.coordinates.latitude,                    radius:$scope.filter.radius                },                function(){                    $scope.placeList=placeListResponse.data;                }            );    });    $scope.newList = function(){        if (angular.isDefined($scope.coordinates))            var placeListResponse = venueService.query(                {                    longitude: $scope.coordinates.longitude,                    latitude: $scope.coordinates.latitude,                    radius:$scope.filter.radius                },                function(){                    $scope.placeList=placeListResponse.data;                }            );    }}