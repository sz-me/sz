function tagsClick(){
    if ($("#tagsArea").is(":hidden")){tagsRollDown()}
    else{tagsRollUp()}
};

function tagsRollUp(){
    //Сворачиваем подменю
    $("#tagsArea").hide();
    //Удаляем из него все теги
    $("#tagsArea").find(".tagBox").remove();
 $("#menu").show();
  $("#sepStringTop").show();
    $("#sepStringBot").show();
    $("#newmessageBox").show();
};

function tagsRollDown(){
    $("#menu").hide();
    $("#sepStringTop").hide();
    $("#sepStringBot").hide();
    $("#newmessageBox").hide();
    $("#feed").animate({opacity:0.6},200);

    var elHeight = $("#screen").height()-103;
    var winWidth = $("#screen").width();
    //Настраиваем размер куколки
    var dollyWidth = (elHeight+34)/2.7;
    
    if (dollyWidth<110){
//         $("#dollyPlace").height(elHeight+34);
//         $("#gender").css({marginTop:'-32px'});
//         $(".dollyBody,.dollyLegs,.dollyFoot").css({marginTop:elHeight*0.03+'px'});
//         $("#tagsPlace").height(elHeight);
    }
    else{
        var dollyHeight = 296;
        var tagsHight=304;
        $("#dollyPlace").height(dollyHeight);
//         $("#gender").css({marginTop:'30px'});
        var dollyWidth=110;
        $("#tagsLeft").height(dollyHeight+39).width(dollyWidth*1.3);
        $(".dollyFoot").css({marginTop:'9px'});
        $(".dollyLegs,.dollyBody").css({marginTop:'7px'});
        $("#tagsPlace").height(tagsHight);
        
    }
    $(".ok").css({marginLeft:(winWidth/2-$(".ok").width()/2)+'px'});
    tagsRow = Math.floor((winWidth-dollyWidth*1.5-15)/76);
    var tagsPlaceWidth = tagsRow*76;
    $("#tagsRight").width(tagsPlaceWidth+dollyWidth*0.2)
    var margin = (winWidth-$("#tagsLeft").width()-$("#tagsRight").width()-5)/3;
    var tagsMarginLeft = $("#tagsLeft").width()+margin*2+5;
    $("#tagsLeft").css({marginLeft:margin+'px'});
    $("#tagsRight").css({marginLeft:tagsMarginLeft+'px'}).height(dollyHeight+39);
    $("#dollyPlace").width(dollyWidth);    
    $("#lessTags").css({marginLeft:dollyWidth*0.1});
    $("#moreTags").css({marginRight:dollyWidth*0.1});
    
//     $(".searchString").css({marginRight:(margin+tagsPlaceWidth/2-$(".searchString").width()/2)+'px'});
    $("#tagsPlace").width(tagsPlaceWidth);
    
    
    $("#dollyPlace,#tagsPlace").css({marginLeft:(dollyWidth*0.1)+'px'});
    $(".changeGender").css({marginLeft:(dollyWidth/2-$(".changeGender").width()/2+dollyWidth*0.1)+'px'});
    $("#tagsSearchString").css({marginLeft:(tagsPlaceWidth/2-$("#tagsSearchString").width()/2+dollyWidth*0.1)+'px'});
/*    var i = margin+dollyWidth/2-$("#changeGender").width()/2;
    $("#changeGender").css({marginLeft:i+'px'});
    $("#lessTags").css({marginLeft:i+2+'px'});
    $("#moreTags").css({marginLeft:(tagsPlaceWidth-2*$(".lessmore_active").width()-9)+'px'});*/
//     $("#moreTags,#lessTags").css({marginLeft:tagsMarginLeft+tagsPlaceWidth/2-43+'px'});
    //Получаем тэги       
    var TagArray = {'dollyPopular':['Шапки ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски ','Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи','Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты','Носки ','Чулки ','Макасины ','Туфли ','Сандали ','Кроссовки ','Кеды ']}
    //Строим теги для каждой из подкатегорий(популярное,голова,тело,ноги,ступни)
    $.each(TagArray['dollyPopular'],function(index,val){
        var $tagBox = jQuery('<div>',{class:"tagBox",id:'dollyPopular'+index,text:val,click:tagBoxclick}).appendTo("#dollyPopularMove");
        var $tagBoxImage = jQuery('<div>',{class:"tagBoxImage"}).appendTo($tagBox);});
        
    //Количество строк тегов
    tagsClm = 3
    //Количество тегов,которое может влезть в экран
    tagVal = tagsRow*tagsClm;
    
    //Отображаем подменю
//     $("#tagsArea").animate({opacity:1},300);
    $("#tagsArea").show();

};

function tagBoxclick(){
    var $tagBox = $(this);
    if($(this).attr('class')=='tagBox'){cloneTags($tagBox)}
    else{removeTags($tagBox)}
};

function removeTags($tagBox){
    $($tagBox).attr('class','tagBox');
    tagBoxID = '#'+$($tagBox).attr('id')+'top'
    $("#tagsTopArea").find(tagBoxID).remove();
    if($("#tagsTopArea").children().length==0){$("#tagsClose").text('');}
    $("#newmessage_tagsValue").find(tagBoxID).remove();
};

function cloneTags($tagBox){
    $($tagBox).attr('class','tagBoxSelect');
    $("#tagsClose").text('[X]');
    var $topBox = jQuery('<div>',{class:"tagTopBox",id:$($tagBox).attr('id')+'top'}).appendTo("#tagsTopArea");
    jQuery('<span>',{class:"topClose",text:'[X]',click:(function(){
        var $topBox = $(this).parent();var tagBoxID = $topBox.attr('id');$($topBox).remove();$("#tagsPlace").find('#'+tagBoxID.slice(0,tagBoxID.length-3)).attr('class','tagBox');
        var topBoxLenght = $("#tagsTopArea").children().length; if(topBoxLenght==0){tagsCloseClick()}
    })}).appendTo($topBox);
    jQuery('<span>',{class:"tagTop_name",text:$($tagBox).text()}).appendTo($topBox);
    var marginTopVal = '-'+($("#tagsTopArea").height()+5)+'px'
    
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
