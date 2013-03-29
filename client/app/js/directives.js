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
                            '<a href="#/messages/{{messageid}}" class="graydark">'+
                                '<time >'+
                                    '{{date}}'+
                                    ' {{time}}'+                               
                                '</time>'+
                            '</a>'+
                            '<span class="badge margin-top-big" >8</span>'+
                            '<strong class="margin-left">{{username}}</strong>'+
                            '<div >'+                               
                                '<div ng-show="photo" id="photo" ng-style="{marginBottom:photoStyle}">'+
                                    '<a href="#/messages/{{messageid}}" class="inline-block" id="photoA">'+
                                        '<img class="media-object" ng-src={{photo}} id="photoFile" ng-style={marginTop:"-33%"}>'+
                                    '</a>'+
                                '</div>'+
                                '{{category}}'+
                                '<div class="circle-parent" ng-show="message_categories" >'+
                                    '<div class="catDiv" ng-repeat="cat in message_categories" ng-class="cat.alias">'+
                                        '<i class="catDivI"></i>'+
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
                        scope.message_categories = []
                        $.each(msg.categories,function(index,id){
                            $.each(scope.categories,function(index,cat){
                                if(cat.id==id){
                                    scope.message_categories.push(cat)
                                }
                            })
                        });
                        scope.photoStyle = function(){
                            if(scope.message_categories[0]){return "-55px";}
                            else{return 0}
                        }
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
                }
            };
        })
        .directive('szFeedMessageBox', function () {
            return {
                restrict: 'EA',
                replace: true,
                template:
                        '<div >'+   
                            '<a href="#/messages/{{messageid}}" class="graydark">'+
                                '<time>'+
                                    '{{date}}'+
                                    ' {{time}}'+                               
                                '</time>'+
                            '</a>'+
                            '<div >'+                                
                                '<div class="circle-parent" ng-show="message_categories">'+
                                    '<div class="catDiv" ng-repeat="cat in message_categories" ng-class="cat.alias">'+
                                        '<i class="catDivI"></i>'+
                                    '</div>'+
                                '</div>'+
                                '<span class="badge " >8</span>'+
                                '<strong class="margin-left">{{username}}</strong>'+
                            '</div>'+       
                            '<p class="max-h" id="text">'+
                                '{{text}}'+
                            '</p>'+                            
                            '<div class="box-hide" id="photo">'+
                                '<a href="#/messages/{{messageid}}" class="inline-block">'+
                                    '<img class="media-object" ng-src={{photo}}>'+
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
                        scope.message_categories = []
                        $.each(msg.categories,function(index,id){
                            $.each(scope.categories,function(index,cat){
                                if(cat.id==id){
                                    scope.message_categories.push(cat)
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

        .directive('szCollapsibleMenu', function() {
            return function(scope, element, attrs) {
                var maxH = 255
                scope.$watch(attrs.szCollapsibleMenu, function(value) {
                    if (value)
                        $(element[0]).animate({maxHeight:0}, 200);
                    else
                        $(element[0]).animate({maxHeight:maxH+'px'}, 200);
                });
            };
        })
        .directive('szAutoResizeTextArea', function() {
            return function(scope, element, attrs) {
                $(element[0]).autoResize()
            };
        })
//         .directive('szLiveSearch',function(){
//             return{
//                 restrict:'EA',
//                 template:
//                         '<ul class="noList">'+
//                             '<li id="mySearch" class="liveSearchLi">'+
//                                 '<i class="icon-remove-sign icon-3x pull-right"  style="vertical-align:-50%" ng-click="removeQuery()"></i>'+
//                                 '<div ng-click="newQuery(filter.query)">'+
//                                     '<i class="icon-search icon-2x"  style="vertical-align:-50%"></i>'+
//                                     '<span class="margin-left" style="vertical-align:-60%">'+
//                                         '{{filter.query}}'+
//                                     '</span>'+
//                                 '</div>'+
//                             '</li>'+
//                             '<li class="liveSearchLi" ng-repeat="(hint,cat) in autoCompleteList | filter:{hint:filter.query}" ng-class="liveSearchLiClass($last)" ng-click="newQuery(hint)">'+
//                                 '<div style="height:45px;">'+
//                                     '<div class="catDiv pull-right" ng-class="cat" >'+
//                                         '<i class="catDivI"></i>'+
//                                     '</div> '+
//                                     '<i class="icon-search icon-2x" class="graydark" style="vertical-align:-50%"></i>'+
//                                     '<span class="margin-left" style="vertical-align:-60%">'+
//                                         '{{hint}}'+
//                                     '</span>'+
//                                 '</div>'+
//                             '</li>'+
//                         '</ul>',
//                 link:function(scope,elm,attr){
//                     var liveSearch = function(){
//                         if(scope.filter.query){
//                             if(scope.query.is( ":focus" )){
//                                 scope.showSearchResults = false;
//                             }
//                         }
//                         else{
//                             scope.showSearchResults = true;
//                         }
//                     }
//                     scope.query = $("#searchFiletrQuery");
//                     scope.removeQuery = function(){
//                         scope.filter.query = ''
//                     }
//                     scope.newQuery = function(hint){
//                         scope.filter.query = hint;
//                         scope.showSearchResults = true;
//                     }
//                     
//                     scope.liveSearchLiClass = function(last){
//                         if(!last){
//                             return 'messageBox'
//                         }
//                     }
//                     scope.$watch('filter.query', liveSearch);
//                     
//                 }
//             }
//         })
//         .directive('szAutoCompleteSearch',function(){
//             return{
//                 restrict:'EA',
//                 template:
// //                         '<div style="display:inline-block;background:red;">'+
//                             '<div id="autoCompleteParent">'+
//                                 '<div id="autoComplete">'+
//                                     '<div ng-repeat="hint in autoCompleteList | filter:filter.query | limitTo:6" ng-click="filter.query = hint">{{hint}}</div>'+
//                                 '</div>'+
// //                             '</div>'+
//                         '<div>',
//                 link:function(scope,elm,attr){
//                     var searchAutoComplete = function(){
//                         if(scope.filter.query){
//                             if(scope.query.is( ":focus" )){
//                                 $("#autoCompleteParent").show()
//                                 var children = $("#autoComplete").children()
//                                 if(children.length<2){
//                                     if(children.text()==scope.filter.query){
//                                         $("#autoCompleteParent").hide()
//                                     }
//                                 }
//                             }
//                         }
//                         else{$("#autoCompleteParent").hide()}
//                     }
//                     
//                     scope.query = $("#searchFiletrQuery");
//                     scope.query
//                         .blur(function(){
//                             setTimeout(function() { $("#autoCompleteParent").hide() }, 100)
//                         })
//                         .keydown(function(e){
//                             if(e.keyCode==27){scope.query.blur()}
//                             if(e.keyCode==13){
//                                 $("#autoCompleteParent").hide()
//                                 scope.newList()
//                             }
//                         })
//                     scope.newQuery = function(hint){
//                         scope.filter.query = hint;
//                         $("#autoCompleteParent").hide()
//                     }
//                     scope.$watch('filter.query', searchAutoComplete);
//                 }
//             }
//         })
        

        
//         .directive('szPrevPhoto',function(){
//             return{
//                 restrict:'EA',
//                 link:function(scope,elm,attr){
//                     function handleFileSelect(evt) {
//                         var files = evt.target.files;
//                         var photo = evt.target.files[0]
//                         var photoName = photo.name;
//                         var photoNameCont = document.getElementById('photoPrevName');
//                         if (photo.type.match('image.*')) {
//                             var reader = new FileReader();
//                             reader.onload = (function(theFile) {
//                                 return function(e) {
//                                     var photoCont = document.getElementById('photoPrev');
//                                     photoCont.innerHTML = ['<img  src="', e.target.result,
//                                                         '" title="', escape(photoName), '"/>'].join('');
//                                     photoNameCont.innerHTML = [photoName].join('');
//                                 };
//                                 
//                             })(photo);      
//                             reader.readAsDataURL(photo);
//                         }
//                         else{
//                             photoNameCont.innerHTML = ['Недопустимый формат'].join('');
//                         }
//                     }
//                     document.getElementById('message-edit-photo').addEventListener('change', handleFileSelect, false);
//                 }
//             }
//         })
    .directive('szFileModel', function() {
        return function(scope, element, attrs) {
            scope.$watch(attrs.szFileModel, function() {
                angular.element(element[0]).bind('change', function(){
                    if (angular.isUndefined(element[0].files))
                    {throw new Error("This browser does not support HTML5 File API.");}
                    if (element[0].files.length == 1){
                        scope[attrs.szFileModel] = element[0].files[0]
                        var photo = element[0].files[0];
                        var $photoNameCont = $("#photoPrevName");
                        var photoName = photo.name;
                        $photoNameCont.text(photoName)
                        if (photo.type.match('image.*')) {
                            var reader = new FileReader();
                            reader.onload = (function(theFile) {
                                return function(e) {
                                    var photoCont = document.getElementById('photoPrev');
                                    photoCont.innerHTML = ['<img  src="', e.target.result,
                                                        '" title="', escape(photoName), '"/>'].join('');
                                };                                
                            })(photo);      
                            reader.readAsDataURL(photo);
                        }
                        else{
                            photoNameCont.innerHTML = ['Недопустимый формат'].join('');
                        }
                    }
                });

            });
        }
    });
        