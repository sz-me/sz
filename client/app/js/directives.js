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
                        '<li  class="place_box_messages_box_mes" >'+   
                            '<div class="place_box_messages_datetime" >'+
                                '<small style="line-height:9px;font-size:80%;">'+
                                    '{{date}}'+
                                '</small >'+
                                '<small style="line-height:9px;font-size:80%;">'+
                                    ' {{time}}'+
                                '</small>'+
                            '</div>'+
//                             '<a href="#" style="margin-left:0px;margin-right:5px;float:left;margin-top:3px" id="place_box_messages_box_mes_author">'+
//                                 '<img class="media-object" src="img/user.png"  width="32" height="32" align="left">'+
//                             '</a>'+
                            '<div class="media-body place_box_messages_header" >'+
                                '<span class="badge " >8</span>'+
                                '<h6 class="place_box_messages_author" style="margin:0;display:inline;margin-left:3px;line-height:16px;">{{username}}</h6>'+
                                
                                    '<div class="place_box_messages_tags" style="line-height:14px;" >'+
//                                         '<small>'+
                                        '<a ng-repeat="category in categories" style="margin-right:3px;display:inline-block;font-size:85%;color:#999">'+
                                            '{{category}}'+
                                        '</a>'+
//                                         '</small>'+
                                    '</div>'+
                                
                            '</div>'+
                            
                            '<p class="place_box_messages_text">'+
                                '{{text}}'+
                            '</p>'+
                            
                            '<div class="place_box_messages_photo" >'+
                                '<img class="media-object" src={{photo}}>'+
                            '</div>'+
                            '<ul class="pager" >'+
                                '<li >'+
                                    '<button class="btnMy" ng-class="{btnDisable:!haveText()}" ng-click="showMessageTextFull()" style="margin-right:5px;">'+
                                       '<img class="media-object" src="img/ico/blue/glyphicons_029_notes_2.png">'+
                                    '</button>'+
                                '</li>'+
                                '<li >'+
                                    '<button class="btnMy"  ng-class="{btnDisable:!photo}" ng-click="showMessagePhoto()">'+
                                        '<img class="media-object" src="img/ico/blue/glyphicons_138_picture.png">'+
                                    '</button>'+
                                '</li>'+
                            '</ul>'+
                            
                        '</li>',
                scope: {
                    cur: '=',
                    next: '=',
                    messages:'=',
                    cat:'='
                },
                link: function (scope, element, attrs) {
                    var setPages = function () {  
                        var msg = scope.messages[scope.cur];
                        var datetime = msg.date.split('T');
                        scope.date = datetime[0];
                        var time = datetime[1].split('.')[0];
                        scope.time = time.slice(0,time.length-3)
                        scope.username = 'Генерал Плюшкин';
                        scope.text = msg.text;
                        if(msg.photo){scope.photo = msg.photo.reduced;}
//                         scope.categories = msg.categories;
                        scope.categories = []
                        $.each(msg.categories,function(index,id){
                            $.each(scope.cat,function(index,cat){
//                                 alert(cat)
                                if(cat.id==id){
                                    scope.categories.push(cat.name)
                                }
                            })
                        });
                        
                        var endMargin = -1*scope.textWidth;;
                        if (scope.fol){
                            scope.wrapper.css({height:scope.curHeiht})
                            var pHeiht = scope.pPage.height();
                            var nHeiht = scope.nPage.height();
                            scope.pPage.css({margin:'0px'})
                            scope.nPage.css({margin:'0px'})
                            scope.pPage.remove();
                            scope.nPage.remove();
                            if (scope.prev<scope.cur){
                                scope.pPage = scope.clone;
                                scope.nPage = createPage(scope.fol);
                                scope.curHeiht = nHeiht;
                                var startMargin = 0;
                            }
                            else{
                                scope.nPage = scope.clone;
                                scope.pPage = createPage(scope.fol)
                                scope.curHeiht = pHeiht;
                                var startMargin = endMargin*2;
                            }
                            scope.wrapper.prepend(scope.pPage);
                            scope.wrapper.append(scope.nPage);
                            scope.wrapper.css({marginLeft:startMargin+'px'}).animate({marginLeft:endMargin+'px',height:scope.curHeiht+'px'},700);
                        }
                        else{
                            if(scope.pPage){scope.pPage.remove();scope.nPage.remove();}
                            scope.pPage = createPage(scope.cur);
                            scope.wrapper.prepend(scope.pPage);
                            scope.nPage = createPage(scope.cur+1);
                            scope.wrapper.append(scope.nPage);
                            var datetimeH = 20;
                            var userH = 16;
                            var tagH = scope.pPage.find(".place_box_messages_tags").height();
                            var textH = scope.pPage.find(".place_box_messages_text").height();
                            var btnH = 46;
                            var m = 5+10+4;
                            var h = datetimeH+userH+tagH+textH+btnH+m;
                            scope.curHeiht = h;
                            //почему то если забирать просто как scope.pPage.height(), то фф корректно устанавливает высоту только через анимейт(через ксс или просто через height() съезжает тэги под аватар), а хром в любом случае ставит высоту пикселей на 20 меньше
                            scope.wrapper.css({marginLeft:endMargin+'px',opacity:0,height:0}).animate({opacity:1,height:scope.curHeiht+'px'},1000).height(scope.curHeiht)
                            
                        }
                        scope.bigBox.find(".place_box_messages_text").css({maxHeight:scope.textHeight+'px'});
                        scope.bigBox.find(".place_box_messages_photo").hide();
                        
                    };
                    
                    function createPage(num){
                        if(num>scope.total){var num = 0}
                        var message = scope.messages[num];
                        var $box = jQuery('<li>',{class:"place_box_messages_box_mes"});     
                        var $datetime = jQuery('<div class="place_box_messages_datetime">').appendTo($box);
                        var datetime = message.date.split('T');
                        var btnWidth = 53;
                        var btnHeight = 45;
                        var $date = jQuery('<small >',{text:datetime[0],css:{lineHeight:'9px',fontSize:'80%'}}).appendTo($datetime);
                        var $time = jQuery('<small >',{text:datetime[1].split('.')[0],css:{lineHeight:'9px',fontSize:'80%'}}).appendTo($datetime);
//                         var $user = jQuery('<a>',{href:"#",css:{marginLeft:'0px',marginRight:'5px',float:'left',marginTop:'3px'},class:"place_box_messages_box_mes_author"}).appendTo($box);
//                         var $userpic = jQuery( '<img class="media-object" src="img/user.png"  width="32" height="32" align="left">').appendTo($user);
                        var $boxHeader = jQuery('<div class="media-body place_box_messages_header" >').appendTo($box);
                        var $rait = jQuery('<span class="badge " >8</span>').appendTo($boxHeader);
                        var $username = jQuery('<h6>',{class:"place_box_messages_author",text:message.username,css:{margin:0,display:'inline',marginLeft:'3px',lineHeight:'16px'}}).appendTo($boxHeader);
                        var $thingsArea = jQuery( '<div class="place_box_messages_tags" style="line-height:14px;" >').appendTo($box);
                        $.each(message.categories,function(index,category){
                            var $category = jQuery('<a>',{class:"place_box_messages_tag",text:category,css:{marginRight:'3px',display:'inline-block',fontSize:'85%',color:'#999'}}).appendTo($thingsArea);
                        })
                        var $text = jQuery('<p>',{class:"place_box_messages_text",text:message.text}).appendTo($box);
                        var $btnUL = jQuery('<ul class="pager mybtn" >').appendTo($box);
                        var $btnTextLi = jQuery('<li >').appendTo($btnUL);
                        var $btnText = jQuery('<button class="btnMy" style="margin-right:5px;">').appendTo($btnTextLi);
                        var $btnTextIco = jQuery('<img class="media-object" src="img/ico/darkgray/glyphicons_029_notes_2.png">').appendTo($btnText);
                        var $btnPhotoLi = jQuery('<li >').appendTo($btnUL);
                        var $btnPhoto = jQuery('<button class="btnMy"> ').appendTo($btnPhotoLi);
                        var $btnPhotoIco = jQuery('<img class="media-object" src="img/ico/darkgray/glyphicons_138_picture.png">').appendTo($btnPhoto);
                   
                        $box.width(scope.textWidth);
                        return $box
                    }
                    
                    var nextPages = function(){                        
                        scope.prev = scope.cur;
                        if (scope.next>=0){
                            scope.fol = scope.next+1;
                            if(scope.next>scope.total){scope.next=0}                         
                            scope.clone = scope.messageBox.clone();
                            scope.cur=scope.next;
                        }
                        else {scope.next=0}
                    }
                    
                    scope.total = scope.messages.length-1;                    
                  
                    scope.messageBox = $(element[0]);
                    scope.wrapper = scope.messageBox.closest(".place_box_messages_wrapper");
                    scope.bigBox = scope.wrapper.closest(".place_box_messages_big_box");
                    scope.messageText =  scope.messageBox.find(".place_box_messages_text");
                    scope.textHeight = parseInt(scope.messageText.css('maxHeight'));
                    scope.textWidth = scope.bigBox.width();
                    scope.messagePhoto =  scope.messageBox.find(".place_box_messages_photo");
                    scope.datetime = scope.messageBox.find(".place_box_messages_datetime");
                    var i = scope.textWidth;
                    scope.wrapper.width(scope.textWidth*3.3);
                    scope.messageBox.width(scope.textWidth);
                    
                    scope.$watch('cur', setPages);
                    scope.$watch('next', nextPages);
                    
                    scope.showMessageTextFull = function(){  
                        scope.messagePhoto.slideUp(200)
                        textHeight();
                    }
                    scope.showMessagePhoto = function(){
                        if (scope.messagePhoto.is(":hidden"))
                        {
                            scope.messageText.animate({maxHeight:scope.textHeight+'px'},500);                            
                            scope.messagePhoto.slideDown(500);
                            var imgHeight = scope.messagePhoto.find("img").height()+20;
                            var newHeight = imgHeight+scope.curHeiht;
                            scope.wrapper.animate({height:newHeight+'px'},500);
                        }
                        else{
                            scope.messagePhoto.slideUp(500);
                            scope.wrapper.animate({height:scope.curHeiht+'px'},500);
                        }
                    }
                    
                    scope.haveText = function () {
                        return scope.messageText.height()==scope.textHeight;
                    };
                    
                    function textHeight(){
                        var messageHeight = scope.messageText.height();
                        if (messageHeight>=scope.textHeight){
                            if (messageHeight>scope.textHeight)
                                {var h=scope.textHeight;var newHeight = scope.curHeiht}
                            else{
                                var $textClone = scope.messageText.clone();
                                $textClone.css({maxHeight:'none',display:'none',width:scope.textWidth+'px',backgroundColor:'red'});
                                $("#content").prepend($textClone);
                                var h = $textClone.height();
                                $textClone.remove();
                                var newHeight = scope.curHeiht - scope.textHeight + h}
                            scope.messageText.animate({maxHeight:h+'px'},500);
                            scope.wrapper.animate({height:newHeight+'px'},500);
                        }
                    }
                }
            };
        })
        .directive('szNewMessageWriteText',function(){
            return {
                restrict:'EA',
                scope:{messageText:'='},
                link:function(scope,elm,attr){
                        var setHeight = function(){
                            var i = $("#btn_search").text();
                            $("#btn_search").text(i+';'+1);
                        }
                        scope.$watch('messageText', setHeight);
                    }
            }
        })
        .directive('szShmotCategoryInfo ', function() {            
            return {
                restrict:'EA',
                scope:{show:'=',info:'='},
                template:
                    '<div id="shmot_category_info">'+
                        '{{info}}'+
                    '</div>',
                link:function(scope,elm,attr){
                        var test = function(){
                            if(scope.showShmotCatInfo){
                                alert(1)
                            }
                            alert(scope.showShmotCatInfo)
                        }
                        scope.$watch('showShmotCatInfo', test);
                    }
            }
        })
        .directive('szDisplayFilter',function(){
            return{
                restrict:'EA',
                link:function(scope,elm,attr){
                    var test = function(){
                        if(scope.showSearchWin){
// 			    var feedWidth = $("#content").width()-16;
// 			    
// 			    if(scope.filterHeigth>feedWidth){
// 				var shmotXval = 3;
// 				var shmotX4Wid = (feedWidth-shmotXval*2-shmotXval*5)/shmotXval -shmotXval;
// 				if((shmotX4Wid*3)>scope.filterHeigth){var shmotXval = 2 }
// 			    }
// 			    else{
// 				var shmotXval = 4;
// 				var shmotX4Wid = (feedWidth-shmotXval*2-shmotXval*5)/shmotXval -shmotXval; 
// 				if((shmotX4Wid*3)>scope.filterHeigth){var shmotXval = 6 }
// 			    }
// 			    
// 			    var shmotBoxW = (feedWidth-shmotXval*2-shmotXval*5)/shmotXval -shmotXval*1.5;
// 			    $(".shmot_box").width(shmotBoxW)
                            scope.win.animate({marginTop:'10px'},500);
                            scope.showSerachWinOKBtn = true;
                            scope.showContent = false;
			    scope.showBotMenuPanel = false;
			    scope.showMenuPanel = false;
                        }
                        else{
                            scope.win.animate({marginTop:-1*scope.winMarginTop+'px'},500);
                            scope.showSerachWinOKBtn = false;
                            scope.showContent = true;
			    scope.showBotMenuPanel = true;
			    scope.showMenuPanel = true;
                        }
                        
                    }
                    scope.win = $("#searchWindow");
		    scope.winInner = $("#searchWindowInner");
		    
                    var ssHeigt = $(window).height()-20;
		    var botBtnHeight = 47;
		    var winInnerHeight = ssHeigt-botBtnHeight-10
		    var searchHeight = 47+8;
		    var shmotInfoHeight = 128;
		    scope.filterHeigth = winInnerHeight-8-searchHeight-shmotInfoHeight;
		    scope.winMarginTop = ssHeigt-80;
		    scope.win.height(ssHeigt).css({marginTop:-1*scope.winMarginTop+'px'})
		    scope.winInner.height(winInnerHeight);
		    $("#shmotFilter").height(scope.filterHeigth);

		    
                    scope.$watch('showSearchWin', test);
                }
            }
        })
        ;
        