﻿'use strict';function MasterPageController($scope) {    $scope.scrollToTop = {top:false};    $scope.showSearchPanel = true;    $scope.showMenuPanel = true;    $scope.changeScrollToUp = function(){        $scope.showSearchPanel = true;        $scope.showMenuPanel = false;    };    $scope.changeScrollToDown = function(){ 	$scope.scrollToTop.top = false;        $scope.showSearchPanel = false;        $scope.showMenuPanel = true;            };    $scope.changeScrollToTop = function(){        $scope.showMenuPanel = true;    };}function FeedController($scope, $routeParams, Places) {//     $scope.places = Places.query();}function PlaceListController($scope, $routeParams){    }function PlaceController($scope, $routeParams) {    $scope.id = $routeParams.placeId}function FilterCtrl() {    var scope = this;    scope.doFilter = function(elem) { 	i = $("#logo").text();	$("#logo").text(i+1);        if(!scope.searchText) return true;        return elem.name.toLowerCase().indexOf( scope.searchText.toLowerCase()) == 0;     };}function FeedPlaceBox($scope) {    $scope.PlaceBoxMessage = {        prev:0,        cur: 0,        next:0,        fol:0,        messages:[]    }}