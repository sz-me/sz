﻿'use strict';function MasterPageController($scope) {    $scope.showSearchPanel = true;    $scope.showMenuPanel = true;    $scope.changeScrollToUp = function(){        $scope.showSearchPanel = true;        $scope.showMenuPanel = false;    };    $scope.changeScrollToDown = function(){         $scope.showSearchPanel = false;        $scope.showMenuPanel = true;            };    $scope.changeScrollToTop = function(){        $scope.showMenuPanel = true;    };}function FeedController($scope, $routeParams, Places) {//     $scope.places = Places.query(); $scope.myTest = function(){     $(".place_box").css({backgroundColor:'red'})}}function PlaceController($scope, $routeParams) {    $scope.id = $routeParams.placeId}function FilterCtrl() {    var scope = this;    scope.doFilter = function(elem) { 	i = $("#logo").text();	$("#logo").text(i+1);        if(!scope.searchText) return true;        return elem.name.toLowerCase().indexOf( scope.searchText.toLowerCase()) == 0;     };}function FeedPlaceBox($scope) {    $scope.PlaceBoxMessage = {        cur: 0,        messages:[]    }}