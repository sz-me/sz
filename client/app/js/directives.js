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
                            '<time>'+
                                '{{date}}'+
                                ' {{time}}'+                               
                            '</time>'+
                             
                            '<div >'+                                
                                '<div class="circle-parent">'+
//                                     '<a ng-repeat="categoryname in categoriesname" style="margin-right:3px;display:inline-block;font-size:85%;color:#999">'+
//                                         '{{categoryname}}'+
//                                     '</a>'+
                                        '<div style="background:green">'+
                                            '<img class="media-object" style="margin-left:6px;margin-top:5px;" src="img/ico/white/glyphicons_283_t-shirt.png" >'+
                                        '</div>'+                                        
                                        '<div style="background:#7a43b6">'+
                                            '<img class="media-object" style="margin-left:6px;margin-top:5px;" src="img/ico/white/glyphicons_284_pants.png">'+
                                        '</div>'+    
                                        '<div style="background:#ffc40d">'+
                                            '<img class="media-object" style="margin-left:6px;margin-top:5px;" src="img/ico/white/glyphicons_285_sweater.png">'+
                                        '</div>'+    
                                        '<div style="background:#045fdb">'+
                                            '<img class="media-object" style="margin-left:6px;margin-top:5px;" src="img/ico/white/glyphicons_283_t-shirt.png">'+
                                        '</div>'+    
                                '</div>'+
                                '<span class="badge " >8</span>'+
                                '<strong class="margin-left">{{username}}</strong>'+
                            '</div>'+       
                            '<p class="max-h" id="text">'+
                                '{{text}}'+
                            '</p>'+                            
                            '<div class="box-hide" id="photo">'+
                                '<a href="#/message/{{messageid}}" class="inline-block">'+
                                    '<img class="media-object" src={{photo}}>'+
                                '</a>'+
                            '</div>'+
                           '<div  style="text-align:center;margin:5px 0;" >'+
                                '<span>'+
                                    '<button class="btn" data-toggle="button"  id="btnText" ng-show="!hasText()" ng-click="showMessageTextFull()" >'+
                                        '<i class="icon-2x" ng-class="btnTextClass"></i>'+
                                    '</button>'+
                                    '<button class="btn" data-toggle="button"  id="btnPhoto" ng-show="photo" ng-click="showMessagePhoto()" >'+
                                        '<i class="icon-picture icon-2x" ></i>'+
                                    '</button>'+
                                '</span>'+
                            '</div>'+
                        '</div>',
                scope: {
                    message:'=',
                    categories:'='
                },
                link: function (scope, element, attrs) {
//                     alert(scope.categories)
                        var msg = scope.message;
                        var datetime = msg.date.split('T');
                        scope.date = datetime[0];
                        var time = datetime[1].split('.')[0];
                        scope.time = time.slice(0,time.length-3)
                        scope.username = 'Генерал Плюшкин';
                        scope.text = msg.text;
                        if(msg.photo){scope.photo = msg.photo.reduced;scope.messageid=msg.id}
                        scope.categoriesname = []
                        $.each(msg.categories,function(index,id){
                            $.each(scope.categories,function(index,cat){
                                if(cat.id==id){
                                    scope.categoriesname.push(cat.name)
                                }
                            })
                        });
                        scope.messageBox = $(element[0]);
                        scope.messageText =  scope.messageBox.find("#text");
                        scope.textHeight = parseInt(scope.messageText.css('maxHeight'));
                        scope.textWidth = scope.messageBox.width();
                        scope.messagePhoto =  scope.messageBox.find("#photo");
                        scope.btnText = scope.messageBox.find("#btnText");
                        scope.btnPhoto = scope.messageBox.find("#btnPhoto");
//                         scope.btnTextClass='icon-caret-down';
                        scope.btnTextClass='icon-reorder';
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
//                                 scope.btnTextClass='icon-caret-up';
                            }
                            else{
                                scope.messageText.animate({maxHeight:scope.textHeight+'px'},500);
//                                 scope.btnTextClass='icon-caret-down';
                            }
                        }
                        scope.showMessagePhoto = function(){
                            if (scope.messagePhoto.is(":hidden")){
                                if(scope.textHeight<scope.messageText.height()){
                                    scope.messageText.animate({maxHeight:scope.textHeight+'px'},500);
                                    scope.btnText.removeClass("active")
//                                     scope.btnTextClass='icon-caret-down';
                                }
                                scope.messagePhoto.slideDown(500);
                            }
                            else{scope.messagePhoto.slideUp(500)}
                        }
                        
                    
                }
            };
        })

//         .directive('szDetermEq',function(){
//             return{
//                 restrict:'EA',
//                 link:function(scope,elm,attr){
//                     var winWidth = $(window).width();
//                     var winHeight = $(window).height();
//                     var contentMarginL = 5;
//                     var contentMargin = 10;
//                                   
//                     if( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
//                         scope.eq = 'phone'
//                     }
//                     else{
//                         scope.eq = 'pc'
//                     }
//                     
// //                     if(scope.eq=='pc'){
// //                         var feedWidth = winWidth*0.4;
// //                         var feedMarginL = (winWidth - feedWidth)*0.5;
// //                     }
// //                     else{
// //                         var feedWidth = winWidth-contentMargin*2.5;
// //                         var feedMarginL = contentMargin;
// //                     }
//                     var menuWidth = 385;
//                     var menuMargin = (winWidth-menuWidth)*0.5;
// //                     $("#dropdownMenu").css({marginLeft:menuMargin});
//                     
// //                     $("#searchWindowInner").height(winHeight-90)
//                 }
//             }
//         })
      
        ;
        