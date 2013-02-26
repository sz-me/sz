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
                    
                })
                            
            }
        })
        .directive('szScrollingToTop',function(){
            return {
                restrict:'EA',
                scope:{top:'='},
                link:function(scope,elm,attr){
                        var scrolling = function(){
                            if (scope.top){
                                $('body,html').animate({scrollTop: 0}, 800);
                                scope.top = false;
                            }
                        }
                        scope.$watch('top', scrolling);
                    }
            }
        })

        .directive('szFeedMessageBox', function () {
            return {
                restrict: 'EA',
                replace: true,
                template:
                        '<div >'+   
                            '<time style="line-height:9px;font-size:80%;text-align:center;"  >'+
                                '{{date}}'+
                                ' {{time}}'+                               
                            '</time>'+
                            '<div class="media-body place_box_messages_header" >'+
                                '<span class="badge " >8</span>'+
                                '<h6 class="place_box_messages_author" style="margin:0;display:inline;margin-left:3px;line-height:16px;">{{username}}</h6>'+
                                '<div class="place_box_messages_tags" style="line-height:14px;" >'+
                                    '<a ng-repeat="category in categories" style="margin-right:3px;display:inline-block;font-size:85%;color:#999">'+
                                        '{{category}}'+
                                    '</a>'+
                                '</div>'+
                            '</div>'+                            
                            '<p class="place_box_messages_text">'+
                                '{{text}}'+
                            '</p>'+                            
                            '<div class="place_box_messages_photo" >'+
                                '<img class="media-object" src={{photo}}>'+
                            '</div>'+
                            '<ul  style="text-align:center;margin:0" >'+
                                '<li class="btn-group" >'+
                                    '<button class="btn  btn-large" data-toggle="button"  id="btnText" ng-show="!hasText()" ng-click="showMessageTextFull()" ">'+
                                        '<img class="media-object" src="img/ico/blue/glyphicons_029_notes_2.png">'+
                                    '</button>'+
                                    '<button class="btn btn-large " data-toggle="button"  id="btnPhoto" ng-show="photo" ng-click="showMessagePhoto()">'+
                                        '<img class="media-object" src="img/ico/blue/glyphicons_138_picture.png">'+
                                    '</button>'+
                                '</li>'+
                            '</ul>'+
                        '</div>',
                scope: {
                    message:'='
                },
                link: function (scope, element, attrs) {
                    
                        var msg = scope.message;
                        var datetime = msg.date.split('T');
                        scope.date = datetime[0];
                        var time = datetime[1].split('.')[0];
                        scope.time = time.slice(0,time.length-3)
                        scope.username = 'Генерал Плюшкин';
                        scope.text = msg.text;
                        if(msg.photo){scope.photo = msg.photo.reduced;}
                        scope.categories = []
//                         $.each(msg.categories,function(index,id){
//                             $.each(scope.cat,function(index,cat){
//                                 if(cat.id==id){
//                                     scope.categories.push(cat.name)
//                                 }
//                             })
//                         });
                        scope.messageBox = $(element[0]);
                        scope.messageText =  scope.messageBox.find(".place_box_messages_text");
                        scope.textHeight = parseInt(scope.messageText.css('maxHeight'));
                        scope.textWidth = scope.messageBox.width();
                        scope.messagePhoto =  scope.messageBox.find(".place_box_messages_photo");
                        scope.btnText = scope.messageBox.find("#btnText");
                        scope.btnPhoto = scope.messageBox.find("#btnPhoto");
                        
//                         scope.textClass = function(){
//                             if(scope.textHeight>scope.messageText.height()){return 'disabled'}
//                         }
                        scope.hasText = function(){
                            return scope.textHeight>scope.messageText.height()
                        }
                        scope.showMessageTextFull = function(){
                            if(scope.textHeight==scope.messageText.height()){
                                scope.messagePhoto.slideUp(500);
//                                 scope.messageText.css({maxHeight:'none'});
                                var $textClone = scope.messageText.clone();
                                $textClone.css({maxHeight:'none',width:scope.textWidth+'px',display:'none'});
                                $("#content").prepend($textClone);
                                var h = $textClone.height();
                                $textClone.remove();
                                var newHeight = h;
                                scope.messageText.animate({maxHeight:newHeight+'px'},500);
                                scope.btnPhoto.removeClass("active");
                            }
                            else{
                                scope.messageText.animate({maxHeight:scope.textHeight+'px'},500);
//                                 scope.btnText.removeClass("active");
                            }
                        }
                        scope.showMessagePhoto = function(){
                            if (scope.messagePhoto.is(":hidden")){
                                if(scope.textHeight<scope.messageText.height()){
                                    scope.messageText.animate({maxHeight:scope.textHeight+'px'},500);
                                    scope.btnText.removeClass("active")
                                }
                                scope.messagePhoto.slideDown(500);
                            }
                            else{scope.messagePhoto.slideUp(500)}
                        }
                        
                    
                }
            };
        })
        .directive('szDetermEq',function(){
            return{
                restrict:'EA',
                link:function(scope,elm,attr){
                    var winWidth = $(window).width();
                    var winHeight = $(window).height();
                    var contentMarginL = 5;
                    var contentMargin = 10;
                    var topmenuWidth = $("#menutop>ul").width();
                                  
                    if( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
                        scope.eq = 'phone'
                    }
                    else{
                        scope.eq = 'pc'
                    }
                    
//                     if(scope.eq=='pc'){
//                         var feedWidth = winWidth*0.4;
//                         var feedMarginL = (winWidth - feedWidth)*0.5;
//                     }
//                     else{
//                         var feedWidth = winWidth-contentMargin*2.5;
//                         var feedMarginL = contentMargin;
//                     }
                    var feedWidth = winWidth-contentMargin*5;
                    var feedMarginL = contentMargin*2;
                    var contentWidth = feedWidth - contentMarginL*2;                    
                    var menutopMarginL = feedMarginL+(feedWidth-topmenuWidth)*0.5;
                    $("#menutop").width(winWidth);
                    $("#menutop>ul").css({marginLeft:menutopMarginL});
                    $("#searchWindowInner").height(winHeight-90)
                }
            }
        })
      
        ;
        