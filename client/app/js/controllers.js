﻿'use strict';function MasterPageController($scope,geolocationService,shmotCategoryService) {    geolocationService();    $scope.$on("locationChanged", function (event, parameters) {        $scope.coordinates = parameters.coordinates;    });    $scope.shmot_category = shmotCategoryService.query();    $scope.shmot_cat = {	id:'',	description:''    }    $scope.filter = {	category:$scope.shmot_cat.id,	query:'',	nearby:''    }    $scope.showSearchWin = false;    $scope.showSerachWinOKBtn = false;//     $scope.showShmotInner = false;    $scope.showContent = true;    $scope.showShmotFilter = false;    $scope.showShmotFilterOver = false;    $scope.showShmotCatInfo = false;            $scope.setFilter = function(){        if($scope.shmot_category_active){            $scope.shmot_category_active = '';            $scope.shmot_filter_btn_style={padding:'0'}        }        else{            $scope.showShmotFilter=true;            $scope.showContent=false;            $scope.showBotMenuPanel = false;        }    }        $scope.$on('ChangeCategory', function(e, catName) {        $scope.shmot_category_active = catName;        $scope.showShmotFilter=false;        $scope.showContent=true;        $scope.showBotMenuPanel = true;        $scope.shmot_filter_btn_style={padding:'0 5px'}    });        $scope.scrollToTop = {top:false};    $scope.showBotMenuPanel = true;    $scope.showMenuPanel = true;    $scope.changeScrollToUp = function(){        $scope.showBotMenuPanel = true;    };    $scope.changeScrollToDown = function(){        $scope.showBotMenuPanel = false;    };    $scope.distanceList = ['250m','1km','3km','city'];    $scope.indexD = 3;    $scope.nextD = function(){        if($scope.indexD>($scope.distanceList.length-2)){$scope.indexD=-1;}        $scope.indexD = $scope.indexD + 1;    }    $scope.prevD = function(){        if($scope.indexD==0){$scope.indexD=$scope.distanceList.length}        $scope.indexD=$scope.indexD - 1;    }    }function FeedController($scope, feedService) {    $scope.$watch('coordinates', function(newValue, oldValue) {        if (angular.isDefined($scope.coordinates))            $scope.feed = feedService.query({                    longitude: $scope.coordinates.longitude,                    latitude: $scope.coordinates.latitude                });    });    $scope.loadMorePlaces = function(){        if ($scope.feed.data.params.offset + $scope.feed.data.params.limit < $scope.feed.data.count)        {            $scope.feed.data.params.offset += $scope.feed.data.params.limit;            var feed = feedService.query($scope.feed.data.params, function() {                        if(feed.data.results.length>0){                            $.each(feed.data.results,function(index,r){                                $scope.feed.data.results.push(r)                            });                            $scope.feed.data.params = feed.data.params;                        }                        else{$scope.$emit($scope.scrollToTop.top=true);}                    }            );        }    }    $scope.PlaceBoxMessage = {        cat:$scope.shmot_category.data,        prev:0,        cur: 0,        next:0,        fol:0,        messages:[]    }}function PlaceController($scope, $routeParams,placeService) {    $scope.id = $routeParams.placeId;    $scope.place = placeService.query();    }function NewMessageController($scope){    $scope.showPlaceList = true;    $scope.showMessageText = false;    $scope.new = {        placeName: '',        placeAddress:'',        messageText:''    }    $scope.setPlace = function(name,address){        $scope.new.placeName = name;        $scope.new.placeAddress = address;        $scope.showPlaceList = false;        $scope.showMessageText = true;    }    $scope.reloadPlaceSelected = function(){        $scope.new.placeName = '';        $scope.new.placeAddress = '';        $scope.showPlaceList = true;        $scope.showMessageText = false;    }    $scope.createText = function(){        $("#btn_search").text(1)            }}