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
                        '<li  class="place_box_messages_box_mes" >'+
                            '<div class="place_box_messages_datetime">'+
                                '<strong >'+
                                    '{{date}}'+
                                '</strong>'+'<br>'+
                                '<small >'+
                                    '{{time}}'+
                                '</small>'+
                            '</div>'+
                            '<a href="#" style="margin-left:0px;margin-right:5px;float:left;margin-top:6px" id="place_box_messages_box_mes_author">'+
                                '<img class="media-object" src="img/user.png"  width="32" height="32" align="left">'+
                            '</a>'+
                            '<div class="media-body place_box_messages_header" >'+
                                '<span class="badge " >8</span><h6 class="place_box_messages_author" style="margin:0;display:inline;margin-left:3px;line-height:16px;">{{username}}</h6>'+
                                
//                                     '<div class="place_box_messages_tags" style="line-height:14px;" >'+
//                                         '<small>'+
//                                         '<em ng-repeat="thing in things">'+
//                                             '<div class="place_box_messages_tag">{{thing}}</div>'+
//                                         '</em>'+
//                                         '</small>'+
//                                     '</div>'+
                                
                            '</div>'+
                            
                            '<p class="place_box_messages_text">'+
                                '{{text}}'+
                            '</p>'+
                            
//                             '<div class="place_box_messages_photo" >'+
//                                 '<img class="media-object" src="img/photo.jpg" width="220">'+
//                             '</div>'+
// 
//                             '<ul class="pager mybtn" >'+
// 
//                                 '<li >'+
//                                     '<a href=""  ng-click="showMessageTextFull()" style="margin-right:5px;">'+
//                                        '<img class="media-object" src="img/ico/white/glyphicons_029_notes_2.png">'+
//                                     '</a>'+
//                                 '</li>'+
//                                 '<li >'+
//                                     '<a href="" ng-click="showMessagePhoto()"> '+
//                                         '<img class="media-object" src="img/ico/white/glyphicons_138_picture.png">'+
//                                     '</a>'+
//                                 '</li>'+
//                             '</ul>'+
                        '</li>',
                scope: {
                    cur: '=',
                    next: '=',
                    messages:'='
                },
                link: function (scope, element, attrs) {
                    var setPages = function () {
                        scope.messageText.css({maxHeight:scope.textHeight+'px'});
                        scope.messagePhoto.hide();
                        
                        var msg = scope.messages[scope.cur];
                        var datetime = msg.date.split('T');
                        scope.date = datetime[0];
                        scope.time = datetime[1].split('.')[0];
                        scope.username = msg.username;
                        scope.things = msg.things;
                        scope.text = msg.text;
                        
                        var w = scope.textWidth;
//                         $("#btn_page_scroll_Up").text(scope.prev+';'+scope.cur+';'+scope.fol)
                        if (scope.fol){
                            var pHeiht = scope.pPage.height();
                            var nHeiht = scope.nPage.height();
                            
                            scope.pPage.remove();
                            scope.nPage.remove();
                            if (scope.prev<scope.cur){
                                scope.pPage = scope.clone;
                                scope.wrapper.prepend(scope.pPage);
//                                 scope.pPage.css({backgroundColor:'red'});
                                scope.nPage = createPage(scope.fol);
//                                 scope.nPage.css({backgroundColor:'blue'});
                                scope.wrapper.append(scope.nPage);
                                var curHeiht = nHeiht;
                                scope.wrapper.css({marginLeft:0}).animate({marginLeft:-1*w+'px',height:curHeiht+'px'},700);
                                
                            }
                            else{
                                scope.nPage = scope.clone;
//                                 scope.nPage.css({backgroundColor:'silver'});
                                scope.wrapper.append(scope.nPage);
                                scope.pPage = createPage(scope.fol)
//                                 scope.pPage.css({backgroundColor:'green'});
                                scope.wrapper.prepend(scope.pPage);
                                var curHeiht = pHeiht;
                                if(scope.fol<scope.total+1){
                                    scope.wrapper.css({marginLeft:-2*w+'px'}).animate({marginLeft:-1*w+'px',height:curHeiht+'px'},700);
                                }
                                else{
                                    scope.wrapper.css({marginLeft:-1*w+'px',height:curHeiht+'px'})
                                }
                            }
//                             $("#btn_search").text('pPage:'+scope.pPage.height()+';nPage:'+scope.nPage.height())
                        }
                        else{
                            if(scope.pPage){scope.pPage.remove();scope.nPage.remove();}
                            scope.pPage = createPage(scope.cur);
                            scope.wrapper.prepend(scope.pPage);
//                             scope.pPage.css({backgroundColor:'yellow'});
                            scope.nPage = createPage(scope.cur+1);
//                             scope.nPage.css({backgroundColor:'olive'});
                            scope.wrapper.append(scope.nPage);
//                             $("#btn_page_scroll_Up").text('pPage:'+scope.pPage.height()+';nPage:'+scope.nPage.height())
                            var curHeiht = scope.pPage.height();
                            scope.wrapper.css({height:curHeiht+'px'});
                        }
                        
                        
//                         scope.wrapper.animate({height:curHeiht+'px'},500);
                        
                        
                    };
                    
                    function createPage(num){
                        if(num>scope.total){var num = 0}
                        var message = scope.messages[num];
                        var $box = jQuery('<li>',{class:"place_box_messages_box_mes"});
                        var $datetime = jQuery('<div class="place_box_messages_datetime">').appendTo($box);
                        var datetime = message.date.split('T');
                        var btnWidth = 53;
                        var btnHeight = 45;
                        var $date = jQuery('<strong >',{text:datetime[0]}).appendTo($datetime);
                        jQuery('<br>').appendTo($datetime);
                        var $time = jQuery('<small >',{text:datetime[1].split('.')[0]}).appendTo($datetime);
                        $datetime.width(scope.textWidth-btnWidth*2).css({marginLeft:btnWidth+'px',marginTop:-1*btnHeight+'px'});
                        var $user = jQuery('<a>',{href:"#",css:{marginLeft:'0px',marginRight:'5px',float:'left',marginTop:'6px'},class:"place_box_messages_box_mes_author"}).appendTo($box);
                        var $userpic = jQuery( '<img class="media-object" src="img/user.png"  width="32" height="32" align="left">').appendTo($user);
                        var $boxHeader = jQuery('<div class="media-body place_box_messages_header" >').appendTo($box);
                        var $rait = jQuery('<span class="badge " >8</span>').appendTo($boxHeader);
                        var $username = jQuery('<h6>',{class:"place_box_messages_author",text:message.username}).appendTo($boxHeader);
                        var $text = jQuery('<p>',{class:"place_box_messages_text",text:message.text}).appendTo($box);
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
                    $("#btn_page_scroll_Up").text(scope.textWidth+';'+i)
                    var btnWidth = 53;
                    var btnHeight = 45;
                    scope.datetime.width(scope.textWidth-btnWidth*2).css({marginLeft:btnWidth+'px',marginTop:-1*btnHeight+'px'});
                    scope.$watch('cur', setPages);
                    scope.$watch('next', nextPages);
                    
                    scope.showMessageTextFull = function(){  
                        scope.messagePhoto.slideUp(200)
                        textHeight();
                    }
                    scope.showMessagePhoto = function(){
                        if (scope.messagePhoto.is(":hidden"))
                        {
                            scope.messageText.animate({maxHeight:scope.textHeight+'px'},500)
                            scope.messagePhoto.slideDown(500);
                        }
                        else{scope.messagePhoto.slideUp(500);}
                    }
                    
                    
                    
                    function textHeight(){
//                         scope.wrapper.css({height:'auto'});
                        var messageHeight = scope.messageText.height();
                        if (messageHeight>scope.textHeight){var h=scope.textHeight; }
                        else{
                            var $textClone = scope.messageText.clone();
                            $textClone.css({maxHeight:'none',display:'none',width:scope.textWidth+'px',backgroundColor:'red'});
                            $("#content").prepend($textClone);
                            var h = $textClone.height();
                            $textClone.remove();                            
                        }                        
                        scope.messageText.animate({maxHeight:h+'px'},500)
                    }
                }
            };
    })
	;
        