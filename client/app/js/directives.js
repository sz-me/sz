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
                .directive('szNewsFeedMessageBox', function () {
            return {
                restrict: 'EA',
                replace: true,
                template:
                        '<div >'+   
                            '<time >'+
                                '{{date}}'+
                                ' {{time}}'+                               
                            '</time>'+
                            '<span class="badge margin-top-big" >8</span>'+
                            '<strong class="margin-left">{{username}}</strong>'+
                            '<div >'+                                
                                '<div ng-show="photo" id="photo" style="text-align:center;overflow:hidden;margin-bottom:-60px;margin-top:5px;min-height:60px;">'+
                                    '<a href="#/places/{{place.id}}/messages/{{messageid}}" class="inline-block" id="photoA">'+
                                        '<img class="media-object" src={{photo}} id="photoFile" ng-style={marginTop:"-33%"}>'+
                                    '</a>'+
                                '</div>'+
                                '<div class="circle-parent"  >'+
//                                     '<a ng-repeat="categoryname in categoriesname" style="margin-right:3px;display:inline-block;font-size:85%;color:#999">'+
//                                         '{{categoryname}}'+
//                                     '</a>'+
                                        '<div style="background:green" class="catDiv">'+
                                            '<img class="media-object" style="margin-left:6px;margin-top:5px;" src="img/ico/white/glyphicons_283_t-shirt.png" >'+
                                        '</div>'+                                        
                                        '<div style="background:#7a43b6" class="catDiv">'+
                                            '<img class="media-object" style="margin-left:6px;margin-top:5px;" src="img/ico/white/glyphicons_284_pants.png">'+
                                        '</div>'+    
                                        '<div style="background:#ffc40d" class="catDiv">'+
                                            '<img class="media-object" style="margin-left:6px;margin-top:5px;" src="img/ico/white/glyphicons_285_sweater.png">'+
                                        '</div>'+    
                                        '<div style="background:#045fdb" class="catDiv">'+
                                            '<img class="media-object" style="margin-left:6px;margin-top:5px;" src="img/ico/white/glyphicons_283_t-shirt.png">'+
                                        '</div>'+    
                                '</div>'+
                                
                               
                            '</div>'+       
                            '<p class="max-h  margin-top-big" id="text">'+
                                '{{text}}'+
                            '</p>'+                            

                           '<div  style="text-align:center;margin:5px 0;" >'+
                                '<span>'+
                                    '<button class="btn" data-toggle="button"  id="btnText" ng-show="!hasText()" ng-click="showMessageTextFull()" >'+
                                        '<i class="icon-2x" ng-class="btnTextClass"></i>'+
                                    '</button>'+
//                                     '<button class="btn" data-toggle="button"  id="btnPhoto" ng-show="photo" ng-click="showMessagePhoto()" >'+
//                                         '<i class="icon-picture icon-2x" ></i>'+
//                                     '</button>'+
                                '</span>'+
                            '</div>'+
                        '</div>',
                scope: {
                    message:'=',
                    categories:'=',
                    place:'='
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
                        if(msg.photo){
                            scope.photo = msg.photo.full;
                            scope.messageid=msg.id
                        
                        }
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
                        scope.photoMaxH = 150;
                        var photoH = scope.messagePhoto.height();
                        scope.messagePhoto.css({maxHeight:scope.photoMaxH})
//                         scope.photoMarginTop = -1*(photoH-scope.photoMaxH)*0.5+'px';
                        scope.photoMarginTop = function(){
//                             return '-200px'
                               return 0
                        }
                        scope.btnText = scope.messageBox.find("#btnText");
                        scope.btnPhoto = scope.messageBox.find("#btnPhoto");
//                         scope.btnTextClass='icon-caret-down';
                        scope.btnTextClass='icon-reorder';
                        scope.hasText = function(){
                            return scope.textHeight>scope.messageText.height()
                        }
                        scope.showMessageTextFull = function(){
                            if(scope.textHeight==scope.messageText.height()){
//                                 scope.messagePhoto.slideUp(500);
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
//                         scope.showMessagePhoto = function(){
//                             if (scope.messagePhoto.is(":hidden")){
//                                 if(scope.textHeight<scope.messageText.height()){
//                                     scope.messageText.animate({maxHeight:scope.textHeight+'px'},500);
//                                     scope.btnText.removeClass("active")
// //                                     scope.btnTextClass='icon-caret-down';
//                                 }
//                                 scope.messagePhoto.slideDown(500);
//                             }
//                             else{scope.messagePhoto.slideUp(500)}
//                         }
                        
                    
                }
            };
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
                                        '<div style="background:green" class="catDiv">'+
                                            '<img class="media-object" style="margin-left:6px;margin-top:5px;" src="img/ico/white/glyphicons_283_t-shirt.png" >'+
                                        '</div>'+                                        
                                        '<div style="background:#7a43b6" class="catDiv">'+
                                            '<img class="media-object" style="margin-left:6px;margin-top:5px;" src="img/ico/white/glyphicons_284_pants.png">'+
                                        '</div>'+    
                                        '<div style="background:#ffc40d" class="catDiv">'+
                                            '<img class="media-object" style="margin-left:6px;margin-top:5px;" src="img/ico/white/glyphicons_285_sweater.png">'+
                                        '</div>'+    
                                        '<div style="background:#045fdb" class="catDiv">'+
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
                                '<a href="#/places/{{place.id}}/messages/{{messageid}}" class="inline-block">'+
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
                    categories:'=',
                    place:'='
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
        .directive('szCollapseTopMenu',function(){
            return{
                restrict:'EA',
                link:function(scope,elm,attr){
                    var collapse = function(){
                        if(scope.collapseTopMenu){$("#collapseMenu").animate({maxHeight:scope.h+'px'},200)}
                        else{$("#collapseMenu").animate({maxHeight:0},200)}
                    }
                    scope.h = 110;
                    scope.$watch('collapseTopMenu', collapse);
                    
                }
            }
        })
        
//         .directive('szNewMessageCategories',function(){
//             return{
//                 restrict:'EA',
//                 template:
//                     '<ul class="class="media-list"">'+
//                         '<li >'+
//                             'Добавить категорию'
//                         '</li>'+
//                     '</ul>',
//                 link:function(scope,elm,attr){
//                     var collapse = function(){
//                         if(scope.collapseTopMenu){$("#collapseMenu").animate({maxHeight:scope.h+'px'},200)}
//                         else{$("#collapseMenu").animate({maxHeight:0},200)}
//                     }
//                     scope.h = 110;
//                     scope.$watch('collapseTopMenu', collapse);
//                     
//                 }
//             }
//         })
        
//         .directive('szPrevPhoto',function(){
//             return{
//                 restrict:'EA',
//                 link:function(scope,elm,attr){
// //                     var placeID = scope.placeID
//                     
//                     function stateChange(event) {
//                         if (event.target.readyState == 4) {
//                             if (event.target.status == 200) {
//                                 $("#res").text('Загрузка успешно завершена!');
//                             } else {
//                                 $("#res").text('Произошла ошибка!');
//                             }
//                         }
//                     }
//                     
//                     function handleFileSelect(evt) {
//                         var files = evt.target.files;
//                         var photo = evt.target.files[0]
//                         var photoName = photo.name;
//                         if (photo.type.match('image.*')) {
//                             var reader = new FileReader();
//                             reader.onload = (function(theFile) {
//                                 return function(e) {
//                                     var span = document.getElementById('photoPrev');
//                                     span.innerHTML = ['<img class="thumb" src="', e.target.result,
//                                                         '" title="', escape(photoName), '"/>'].join('');
//                                     $("#message-photo-remove-ico").show();
//                                     var xhr = new XMLHttpRequest();
// //                                      xhr.upload.addEventListener('progress', uploadProgress, false);
//                                     xhr.onreadystatechange = stateChange;
//                                     xhr.open('POST', '../../api/places/'+scope.place.id+'/messages?format=json');
//                                     xhr.setRequestHeader('X-FILE-NAME', photoName);
//                                     xhr.send(photo);
//                                 };
//                                 
//                             })(photo);      
//                             reader.readAsDataURL(photo);
//                         }
//                     }
//                     document.getElementById('files').addEventListener('change', handleFileSelect, false);
//                 }
//             }
//         })
//         .directive('szRemovePhoto',function(){
//             return{
//                 restrict:'EA',
//                 link:function(scope,elm,attr){
//                        var remove = function(){
//                             if(scope.removePhoto){
//                                 var span = document.getElementById('photoPrev');
//                                 span.innerHTML = [''].join('');
//                                 $("#message-photo-remove-ico").hide();
//                                 scope.removePhoto = false;
//                             }
//                     }
//                     scope.$watch('removePhoto', remove);
//                     
//                 }
//             }
//         })


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
    .directive('szFileModel', function() {
        return function(scope, element, attrs) {
            scope.$watch(attrs.szFileModel, function() {
                angular.element(element[0]).bind('change', function(){
                    if (angular.isUndefined(element[0].files))
                        throw new Error("This browser does not support HTML5 File API.");
                    if (element[0].files.length == 1)
                        scope[attrs.szFileModel] = element[0].files[0]
                });

            });
        }
    });
        