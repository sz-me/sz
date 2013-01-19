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
	;