function RollUpMessage(){
    var $message = $(this).closest(".message");
    $($message).find(".mestagsArea").animate({height:'75px'},200)    
    $($message).find(".photo").hide();
    $($message).find(".messagebottom").animate({height:'15px'},250);
    $($message).find('.moreMessage').show();
    $(this).hide();
};
    
function RollDownMessage(){
//Развертка сообщения
    var $message = $(this).closest(".message");
    var $mestagsArea = $($message).find(".mestagsArea");
    var mestagsAreaHgh = ($($mestagsArea).find(".boxMesTag").length/messageTagWidth)*100+'px';
    $($mestagsArea).animate({height:mestagsAreaHgh},200);
    $($message).find(".messagebottom").css({height:'auto'});
    $($message).find(".photo").show();
    $($message).find('.lessMessage').show();
    $(this).hide();
};

function getMessage(){
    $(".placeValue").text('b');
    var api = new sz.Api({uri: 'api/',request_func: $.ajax});
    api.get('messages',{},
            function(r){messagesView(r);})
    $(".placeValue").text('0');
};
    
function messagesView(data){
    $(".placeValue").text('1');
    if (data.response.length == 1){
        $(".placeValue").text('2');
        $.each(data.response, function(key, value) {
            $(".placeValue").text('3');
            fulltext = value.text;
            
            })
        }
 $(".tagsValue").text(data.responses);
};

(function($){
    
    $.fn.autoResize = function(options) {
        
        // Just some abstracted details,
        // to make plugin users happy:
        var settings = $.extend({
            onResize : function(){
				 
			},
            animate : true,
            animateDuration : 150,
            animateCallback : function(){},
            extraSpace : 0,
            limit: 1000
        }, options);
        
        // Only textarea's auto-resize:
        this.filter('textarea').each(function(){
            
                // Get rid of scrollbars and disable WebKit resizing:
            var textarea = $(this).css({resize:'none','overflow-y':'hidden'}),
            
                // Cache original height, for use later:
                origHeight = textarea.height(),
				
				                
                // Need clone of textarea, hidden off screen:
                clone = (function(){

                    // Properties which may effect space taken up by chracters:
                    var props = ['height','width','lineHeight','textDecoration','letterSpacing'],
                        propOb = {};
  
                    // Create object of styles to apply:
                    $.each(props, function(i, prop){
                        propOb[prop] = textarea.css(prop);
                    });
                    
                    // Clone the actual textarea removing unique properties
                    // and insert before original textarea:
                    return textarea.clone().removeAttr('id').removeAttr('name').css({
                        position: 'absolute',
                        top: 0,
                        left: -9999
                    }).css(propOb).attr('tabIndex','-1').insertBefore(textarea);
					
                })(),
                lastScrollTop = null,
                updateSize = function() {
                    // Prepare the clone:
                    clone.height(0).val($(this).val()).scrollTop(10000);
					
                    // Find the height of text:
                    var scrollTop = Math.max(clone.scrollTop(), origHeight) + settings.extraSpace,
                        toChange = $(this).add(clone);
						
                    // Don't do anything if scrollTip hasen't changed:
                    if (lastScrollTop === scrollTop) { return; }
                    lastScrollTop = scrollTop;
					
                    // Check for limit:
                    if ( scrollTop >= settings.limit ) {
                        $(this).css('overflow-y','');
                        return;
                    }
                    // Fire off callback:
                    settings.onResize.call(this);
					
                    // Either animate or directly apply height:
                   settings.animate && textarea.css('display') === 'block' ?
                        toChange.stop().animate({height:scrollTop}, settings.animateDuration, settings.animateCallback)
                        : toChange.height(scrollTop);
						
					
                };
                                  
            // Bind namespaced handlers to appropriate events:
            textarea
                .unbind('.dynSiz')
                .bind('keyup.dynSiz', updateSize)
                .bind('keydown.dynSiz', updateSize)
                .bind('change.dynSiz', updateSize);
            
        });
        
        // Chain:
        return this;
        
    };
    
    
    
})(jQuery);
