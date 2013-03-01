﻿'use strict';function MasterPageController($scope, geolocationService, shmotCategoryService, authService) {    var userResponse = authService.user({}, function() {            $scope.user = userResponse.data;        }    )    geolocationService.getCurrentPosition(function (position) { $scope.coordinates = position.coords; })    var categories = shmotCategoryService.query(function(){$scope.categories = categories.data; });//     $scope.shmot_cat = {// 	id:99,// 	description:''//     }//     $scope.filter = {// 	category:100,// 	query:'',// 	nearby:''//     }    $scope.collapseTopMenu = false;    $scope.showContent = true;//     $scope.setFilter = function(){//         $scope.showSearchWin = !$scope.showSearchWin;//         $scope.showContent = !$scope.showContent;//         $scope.showBotMenuPanel = !$scope.showBotMenuPanel;//         $scope.showMenuPanel = !$scope.showMenuPanel;//         //     }//     $scope.setCategory = function(){//         $scope.filter.category = $scope.shmot_cat.id//     }   //     $scope.$on('ChangeCategory', function(e, catName) {//         $scope.shmot_category_active = catName;//         $scope.showShmotFilter=false;//         $scope.showContent=true;//         $scope.showBotMenuPanel = true;//         $scope.shmot_filter_btn_style={padding:'0 5px'}//     });//         $scope.showMenuPanel = true;    $scope.showBotMenuPanel = true;    $scope.scrollToTop = {top:false};    $scope.changeScrollToUp = function(){$scope.showBotMenuPanel = true;};    $scope.changeScrollToDown = function(){$scope.showBotMenuPanel = false;};    }function NewsFeedController($scope, newsFeedService) {    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            $scope.feed = newsFeedService.query({                    longitude: $scope.coordinates.longitude,                    latitude: $scope.coordinates.latitude                });    });    $scope.loadMorePlaces = function(){        if ($scope.feed.data.params.offset + $scope.feed.data.params.limit < $scope.feed.data.count)        {            $scope.feed.data.params.offset += $scope.feed.data.params.limit;            var feed = newsFeedService.query($scope.feed.data.params, function() {                        if(feed.data.results.length>0){                            $.each(feed.data.results,function(index,r){                                $scope.feed.data.results.push(r)                            });                            $scope.feed.data.params = feed.data.params;                        }                        else{$scope.$emit($scope.scrollToTop.top=true);}                    }            );        }    }    $scope.placeMessagesLimit = 1;    $scope.showAllPlaceMessages = function(len,lim){        if(lim==1){return len}        else{return 1}    }    $scope.showAllPlaceMessagesText = function(len,lim){        if(lim==1){return 'Еще '+len+' сообщений'}        else{return 'Свернуть'}    }}function PlaceController($scope, $routeParams, newsFeedService) {    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            $scope.feed = newsFeedService.query({                longitude: $scope.coordinates.longitude,                latitude: $scope.coordinates.latitude,                placeId: $routeParams.placeId            });    });    $scope.showPlaceMessages = true;    $scope.showPlacePhoto = false;        $scope.showPlaceMessagesClick = function(){        $scope.showPlaceMessages = true;        $scope.showPlacePhoto = false;    }        $scope.showPlacePhotoClick = function(){        $scope.showPlaceMessages = false;        $scope.showPlacePhoto = true;    }    }function MessageController($scope,$routeParams,MessageService){    $scope.message = MessageService.get({messageId:$routeParams.messageId})}function SearchController($scope){    $scope.filter = {        nearby:'',        query:'',        category:''    }    $scope.chCat = {};    $scope.$on('ChangeCategory', function(e,cat){        $scope.chCat = cat;        $scope.filter.category = cat.id;    })}function NewMessageController($scope){    $scope.showPlaceList = true;    $scope.showMessageText = false;    $scope.new = {        placeName: '',        placeAddress:'',        messageText:''    }    $scope.setPlace = function(name,address){        $scope.new.placeName = name;        $scope.new.placeAddress = address;        $scope.showPlaceList = false;        $scope.showMessageText = true;    }    $scope.reloadPlaceSelected = function(){        $scope.new.placeName = '';        $scope.new.placeAddress = '';        $scope.showPlaceList = true;        $scope.showMessageText = false;    }    $scope.createText = function(){        $("#btn_search").text(1)            }}function LoginController($scope, authService) {    $scope.login = function(){        var userResponse = authService.login({username: $scope.username, password: $scope.password }, function() {                $scope.user = userResponse.data;            }        )    }}