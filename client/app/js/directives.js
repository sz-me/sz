'use strict';

/* Directives */


var detectDirection = function(raw, params, delta) {
			var oldTop = params.top;
			var oldDirection = params.direction;
			var rectObject = raw.getBoundingClientRect();
			params.top = rectObject.top;
			if (oldTop < params.top) params.direction = 1;
			if (oldTop > params.top) params.direction = -1;
			var first = false;
			if (oldDirection == - params.direction){
				params.changePoint = oldTop;
				first = true;
			}
			if (params.direction * (params.top - params.changePoint) <= delta || first){
				return params.direction;
				//alert(params.direction + " " + params.direction * (params.top - params.changePoint));
				//scope.$apply(attr.szChangeScrollDirection);
			}
			else 
				if (params.direction * (params.top - params.changePoint) > delta && params.direction * (oldTop - params.changePoint) < delta)
				return params.direction;
					//scope.$apply(attr.szChangeScrollDirection);
					//alert(params.direction + " " + delta);
}



angular.module('sz.client.directives', [])
	.directive('szChangeScrollToUp', function() {
            return function(scope, elm, attr){
                var raw = elm[0];
                var params = {
                        direction: 1,
                        top: raw.getBoundingClientRect().top,
                        changePoint: raw.getBoundingClientRect().top
                };
                var delta = 1;
                angular.element(window).scroll(function(){
                    var dir = detectDirection(raw, params, delta);
                    if (dir == 1)
                            scope.$apply(attr.szChangeScrollToUp);
                    
                })
                            
            }
	})
        .directive('szChangeScrollToTop', function() {
            
            return function(scope, elm, attr){
                var raw = elm[0];
                var params = {
                        direction: 1,
                        top: raw.getBoundingClientRect().top,
                        changePoint: raw.getBoundingClientRect().top
                };
                var delta = 1;
                angular.element(window).scroll(function(){
                        var dir = detectDirection(raw, params, delta);
                        if ($(this).scrollTop() == 0)
                                scope.$apply(attr.szChangeScrollToTop);
                });
                            
            }
        })
	.directive('szChangeScrollToDown', function() {
            return function(scope, elm, attr){
		var raw = elm[0];
		var params = {
			direction: 1,
			top: raw.getBoundingClientRect().top,
			changePoint: raw.getBoundingClientRect().top
		};
		var delta = 1;
		angular.element(window).scroll(function(){
			var dir = detectDirection(raw, params, delta);
			if (dir == -1)
				scope.$apply(attr.szChangeScrollToDown);
		});
			
            }
        })  
        .directive('szFeedMessageBox', function () {
        return {
            restrict: 'EA',
            replace: true,
            template:
                    '<ul class=" place_box_messages_big_box" style="margin-left:0;list-style:none;" ">'+
//                         '<li  ng-repeat="message in messages.results.slice(showedMessageIndex) | limitTo: 1" class="place_box_messages_box_mes" style="float:left">'+
                            '<a href="#" style="margin-left:0px;margin-right:5px;float:left" id="place_box_messages_box_mes_author">'+
                                '<img class="media-object" src="img/user.png"  width="30" height="30" align="left">'+
                            '</a>'+
                            '<div class="media-body place_box_messages" >'+
                                '<span class="badge " >8</span><h6 class="place_box_messages_author" style="margin:0;display:inline;margin-left:3px;line-height:16px;">{{messages[first].username}}</h6>'+
                                '<small >'+
                                '<ul class="place_box_messages_tags" style="line-height:14px;" >'+
                                    '<em ng-repeat="thing in messages[first].things">'+
                                        '<span>{{thing}}&nbsp</span>'+
                                    '</em>'+
                                '</ul>'+
                                '</small>'+
                            '</div>'+
                            '<p class="place_box_messages_text" ng-style="place_box_messages_text">'+
                                '{{messages[first].text}}'+
                            '</p>'+
//                     '</li>'+
                    '</ul>',
            /*
                '<div class="pagination pagination-large pagination-centered">' +
                    '<ul>' +
                        '<li ng-repeat="page in pages"' +
                        '>' +
                            '<a>{{messages[page].username}}</a>' +
                        '</li>' +
                    '</ul>' +
                    '</div>',*/
            scope: {
                cur: '=',
                messages:'='
                
            },
            link: function (scope, element, attrs) {
                var calcPages = function () {
                    scope.total = scope.messages.length-1;
                    scope.start = scope.cur;
                    scope.first = scope.start;
                    if (scope.cur < 0) {scope.cur=0}
                    if (scope.cur > scope.total) {scope.cur=0}

                };
                scope.$watch('cur', calcPages);
                scope.$watch('total', calcPages);

            }
        };
    })
	;