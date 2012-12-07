
function createTags($parentArea){
    $parentArea = $("#search_send_area").find(".area");
    
    var winWidth = $("#screen").width();
    var elHeight = $("#screen").height()*0.45;
    $("#mainmenu").hide();
 //Получаем тэги       
    var TagArray = {'dollyPopular':['Шапки ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски ','Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи','Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты','Носки ','Чулки ','Макасины ','Туфли ','Сандали ','Кроссовки ','Кеды ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски ','Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи','Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты','Носки ','Чулки ','Макасины ','Туфли ','Сандали ','Кроссовки ','Кеды ']}
    //Строим теги для каждой из подкатегорий(популярное,голова,тело,ноги,ступни)
    $.each(TagArray['dollyPopular'],function(index,val){
        var $tagBox = jQuery('<div>',{class:"tagBox",id:'dollyPopular'+index,text:val,click:tagBoxclick}).appendTo($parentArea.find("#dollyPopularMove"));
        var $tagBoxImage = jQuery('<div>',{class:"tagBoxImage"}).appendTo($tagBox);});
    
    var $dollyPlace = $parentArea.find("#dollyPlace");
    var $tagsLeft = $parentArea.find("#tagsLeft");
    var $tagsPlace = $parentArea.find("#tagsPlace");
    var $tagsRight = $parentArea.find("#tagsRight");
    var $moreTags = $parentArea.find("#moreTags");
    var $lessTags = $parentArea.find("#lessTags");
    var $searchString = $parentArea.find("#searchString");
    var $prevGender = $parentArea.find("#prevGender");
    var $nextGender = $parentArea.find("#nextGender");
    
    var dollyWidth = winWidth*0.074;
   
    var dollyHeight = dollyWidth*2.7;
    //Корректировка высоты и ширины элементов
    if (dollyHeight>elHeight){var dollyHeight = elHeight; var dollyWidth = dollyHeight/2.7}
//     if (dollyWidth<(winWidth-60)){var dollyWidth=40; var dollyHeight=dollyWidth*2.7;}
    var i = dollyWidth/6
    var topelMargintop = -1*dollyWidth/9;
    var elPaddinttop = dollyWidth/18;
    var tagBoxWidth = dollyHeight/4.4;
    
    var fontSize = tagBoxWidth*10/66;
    var tagBoxMargin = tagBoxWidth*0.1;
    var lessmoreTagsWidth = tagBoxWidth/2;
    var tagsHight = dollyHeight+tagBoxWidth*0.1;
    var changegenderWidth = 2*i;
    var marginEl = dollyHeight*0.1;
    $dollyPlace.children(".dollyLegs,.dollyBody,.dollyFoot").css({marginTop:(dollyHeight*0.12-11)/3});
    $dollyPlace.height(dollyHeight);
    var dollyHeight = dollyHeight-11;
    var tagsLeftHight = dollyHeight*1.04+dollyWidth/3+dollyWidth/9;
    var tagsLeftWidth = dollyWidth*1.3;
    $tagsLeft.height(tagsLeftHight).width(tagsLeftWidth);
    $dollyPlace.width(dollyWidth).css({marginLeft:dollyWidth*0.1});    
    
    $parentArea.css({marginTop:marginEl});
    
    
    var placeWidth = winWidth-dollyWidth*0.05-tagsLeftWidth-dollyWidth*0.1-dollyWidth*0.05;
    var tagsRow = Math.floor(placeWidth/(tagBoxWidth*1.1));
    
    var tagsPlaceWidth = tagsRow*tagBoxWidth*1.1+tagsRow*2;
    var tagsRightWidth = tagsPlaceWidth+dollyWidth*0.2;
    $tagsRight.width(tagsRightWidth);
    var margin = (winWidth-tagsRightWidth-$tagsLeft.width()-dollyWidth*0.25)/3;
    var tagsMarginLeft = $tagsLeft.width()+margin*2+dollyWidth*0.15+dollyWidth*0.05;
    $tagsLeft.css({marginLeft:margin+dollyWidth*0.05});
    $tagsRight.css({marginLeft:tagsMarginLeft}).height(tagsLeftHight);
    $tagsPlace.height(tagsHight).width(tagsPlaceWidth).css({marginLeft:dollyWidth*0.1});
    $parentArea.find(".tagBox").width(tagBoxWidth).height(tagBoxWidth).css({fontSize:fontSize+'px',marginTop:tagBoxMargin,marginRight:tagBoxMargin});   
    $.each($parentArea.find(".tagBox"),function(index,val){if((index+1)%tagsRow==0){$(val).css({marginRight:0});}});
    $parentArea.find(".tagBoxImage").width(tagBoxWidth-fontSize*1.3).height(tagBoxWidth-fontSize*1.3).css({marginLeft:(tagBoxWidth-(tagBoxWidth-fontSize*1.3))/2}); 
    
    
    
    $prevGender.height(i).width(changegenderWidth).css({marginLeft:(3*i-changegenderWidth/2+dollyWidth*0.1),marginBottom:dollyHeight*0.04,marginTop:topelMargintop,paddingTop:elPaddinttop});
    $nextGender.height(i).width(changegenderWidth).css({marginLeft:(margin+dollyWidth*0.6-changegenderWidth/2),marginTop:topelMargintop,paddingTop:elPaddinttop});
    $searchString.width(tagBoxWidth*2.5).height(i+elPaddinttop).css({marginLeft:(tagsPlaceWidth/2-$searchString.width()/2+dollyWidth*0.1),marginBottom:dollyHeight*0.04-tagBoxMargin,marginTop:(i+elPaddinttop)/-2});
    $searchString.find("#searcStringIcn").width(dollyWidth/9).height(dollyWidth/9).css({marginLeft:i*0.15,marginTop:-1*dollyWidth/20});
    $searchString.find("#tagsSearchString").width($searchString.width()-i*0.7-dollyWidth/9).css({fontSize:dollyWidth/10,marginTop:-1*dollyWidth/20});
    
    $parentArea.find(".lessmore_active").width(lessmoreTagsWidth).height(i).css({paddingTop:elPaddinttop,fontSize:dollyWidth/12});
    $lessTags.css({marginRight:tagsRightWidth-dollyWidth*0.05+margin-lessmoreTagsWidth,marginTop:-1*(dollyWidth*2/9+3)});
    $moreTags.css({marginRight:dollyWidth*0.15+margin,marginTop:-1*(dollyWidth*2/9+3)});
    
    var $placeArea = $parentArea.find("#placeArea");
    var staticPlaceHeight = tagBoxWidth+dollyHeight*0.06;
    var placeAreaHeight = topelMargintop*-1+staticPlaceHeight+dollyHeight*0.04;
    var placeAreaWidth = winWidth-margin*2-dollyWidth*0.1;
    $placeArea.height(placeAreaHeight).width(placeAreaWidth).css({marginLeft:margin+dollyWidth*0.05,marginBottom:marginEl});    
    $placeArea.find("#lessPlace").css({marginLeft:dollyWidth*0.1,marginTop:topelMargintop});
    $placeArea.find("#morePlace").css({marginLeft:placeAreaWidth-dollyWidth*0.1-lessmoreTagsWidth,marginTop:topelMargintop*2});
    var staticPlaceMargin = dollyWidth*0.1;
    var staticPlaceWidth = placeAreaWidth-staticPlaceMargin*2;
    $placeArea.find("#staticPlace").width(staticPlaceWidth).height(staticPlaceHeight).css({marginLeft:staticPlaceMargin,marginTop:(topelMargintop*-1)});
    
    var $newMessage = $parentArea.find(".newMessage");
    var $myuserpic = $newMessage.find(".myuserpic");
    var $messageText = $newMessage.find(".messageText");
    var $myusername = $newMessage.find(".myusername");
    var $sendmessage = $newMessage.find(".sendmessage");
   
    $newMessage.width(winWidth-tagsMarginLeft-margin-dollyWidth*0.05).css({marginTop:marginEl/2,marginLeft:tagsMarginLeft});
    $myusername.css({fontSize:fontSize*0.9});
    var userWidth = fontSize*5;
    $myuserpic.height(userWidth).width(userWidth);
    $messageText.width($newMessage.width()-userWidth*1.5)
//         .text(function(){if($parentArea.attr('id')=='searchArea'){return 'Спроси о ништяках'} else{return 'Расскажи о ништяках'}})
        .css({fontSize:fontSize,color:'#999',marginBottom:fontSize*1.5})
        .data('originalText', $messageText.text())
        .focus(function() {
            var $el = $(this);
            if (this.value == $el.data('originalText')) {
                this.value = '';
                $(this).attr('rows','2').animate({color:'#444'},200);
                jQuery($(this)).autoResize();
                $myusername.show();
                $sendmessage.show();
                $myuserpic.show();
            }
        })
        .blur(function() {
            if (this.value == '') {
                this.value = $(this).data('originalText');
                $(this).attr('rows','1').animate({color: '#999'},200);
                $myusername.hide();
                $sendmessage.hide();
                $myuserpic.hide();
            }
        });
    $sendmessage.css({marginLeft:($newMessage.width()-$sendmessage.width())/2,padding:fontSize/2,fontSize:fontSize}).height(fontSize);
    
    
    //Создание геотегов
    function placesView(data,latitude,longitude,accuracy){
        if (data.meta.code == 200){
            $.each(data.data, function(key, value){
                var geoBox = jQuery('<div>',{class:"geoBox",id:value.venue_id,click:geoBoxClick}).appendTo($placeArea.find("#movePlace"));
                jQuery('<p>',{class:"place_name",text:value.name,css:{fontSize:fontSize}}).appendTo(geoBox);
                jQuery('<p>',{class:"place_address",text:value.address,css:{fontSize:fontSize*0.8}}).appendTo(geoBox);}); 
                jQuery('<div>',{class:"place_search",text:'Искать',css:{display:'none'}})
            var geoBoxValue = Math.floor(staticPlaceWidth/(tagBoxWidth*2));
            var geoBoxW = ((staticPlaceWidth-geoBoxValue*2)/geoBoxValue);
            var geoBoxWidth = geoBoxW*0.9+geoBoxW*0.1/geoBoxValue;
            $placeArea.find(".geoBox").height(tagBoxWidth).width(geoBoxWidth).css({marginTop:dollyHeight*0.04});  
        //     $placeArea.find(".geoBox:eq(8)").css({marginRight:0})
            $.each($placeArea.find(".geoBox"),function(index,val){if(index!=(geoBoxValue-1)){$(val).css({marginRight:geoBoxW*0.1})}});
             //Отображаем подменю
            $placeArea.find("#movePlace").width(staticPlaceWidth*$placeArea.find(".geoBox"));
           
        }
                
        else {$placeArea.find("#movePlace").text(data.data.detail);}
         
    };
        
    navigator.geolocation.getCurrentPosition(function(data) {
        var latitude = data['coords']['latitude'];
        var longitude = data['coords']['longitude'];
        var accuracy = data['coords']['accuracy'];
        api.get('places',{latitude: latitude,longitude: longitude,accuracy: accuracy},
        function(r){placesView(r,latitude,longitude,accuracy); });});
   $parentArea.show();
};

function searchMenuClick(){
    $("#search_send_area").find(".area").attr('id','searchArea');
    createTags();
};

function sendMenuClick(){
    $("#search_send_area").find(".area").attr('id','sendArea');
    createTags();
};

function tagBoxclick(){
    var $tagBox = $(this);
    var $parentArea = $tagBox.closest(".area");
    if($parentArea.attr('id')=='sendArea'){
        if($tagBox.attr('class')=='tagBox'){cloneTags($tagBox)}
        else{removeTags($tagBox)}
    }
    else{return 0}
};

function removeTags($tagBox){
    var tagBoxWidth = $tagBox.width()
    $tagBox.attr('class','tagBox');
    var tagBoxID = '#'+$($tagBox).attr('id')+'top'
    $("#tagsMessage").find(tagBoxID).remove();
};

function cloneTags($tagBox){
    var tagBoxWidth = $tagBox.width()
    var fontSize = (tagBoxWidth*10/66)*0.8;
    $tagBox.attr('class','tagBoxSelect');
    var $topBox = jQuery('<div>',{class:"tagMessageBox",id:$($tagBox).attr('id')+'top',css:{fontSize:fontSize}}).appendTo("#tagsMessage");
    jQuery('<span>',{class:"topClose",text:'[X]',click:(function(){
        var $topBox = $(this).parent();var tagBoxID = $topBox.attr('id');$($topBox).remove();$("#tagsPlace").find('#'+tagBoxID.slice(0,tagBoxID.length-3)).attr('class','tagBox');
    })}).appendTo($topBox);
    jQuery('<span>',{class:"tagTop_name",text:$($tagBox).text(),css:{marginLeft:3}}).appendTo($topBox);
    
};

function geoBoxClick(){
    var $geoBox = $(this);
    var $parentArea = $geoBox.closest(".area");
    if($parentArea.attr('id')=='sendArea'){
        if($geoBox.attr('class')=='geoBox'){cloneGeo($geoBox)}
        else{removeGeo($geoBox)}
    }
    else{return 0}
};

function removeGeo($geoBox){
    var geoBoxWidth = $geoBox.width()
    $geoBox.attr('class','geoBox');
    var geoBoxID = '#'+$($geoBox).attr('id');
    $("#geoMessage").find(geoBoxID).remove();
};

function cloneGeo($geoBox){
    var geoBoxWidth = $geoBox.width()
    var fontSize = (geoBoxWidth*10/66)*0.8;
    $geoBox.attr('class','geoBoxSelect');
    var $topBox = jQuery('<div>',{class:"geoMessageBox",id:$($geoBox).attr('id'),css:{fontSize:fontSize}}).appendTo("#geoMessage");
//     jQuery('<span>',{class:"topClose",text:'[X]',click:(function(){
//         var $topBox = $(this).parent();var geoBoxID = $topBox.attr('id');$($topBox).remove();$("#movePlace").find('#'+geoBoxID).attr('class','geoBox');
//     })}).appendTo($topBox);
    jQuery('<span>',{class:"geoTop_name",text:$($geoBox).text(),css:{marginLeft:3}}).appendTo($topBox);
};

function feedMenuClick(){
    $("#mainmenu").hide();
    var elHeight = $("#screen").height()*0.45;
    var winWidth = $("#screen").width();
    var $parentArea = $("#feedArea");
    var fontSize = $("#city").css('fontSize');
    //Создание сообщений
//     $.each([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],function(index,val){
        var shopName = 'Офигенский магазин';
        var shopAddr = 'Да тут прям рядом, пару кварталов пройти только';
        var text = 'Купил труселя. Красивые и дешево. Такие труселя -всем труселям труселя. Ах посмотрите, какой на них кармашик, какой изящный паттерн украшает их. Это просто произведение исскуства, а не труселя. Такие труселя должны храниться в Лувре, а я купил их всего лишь за 100 рублей';
        var photo = '';
        var username = 'Повелитель мопсов';
        var userpic = '';
        var messageTag = [['Труселя','15'],['Трусишки','15'],['Труселябры','15'],['Трусы','15'],['Трусищи','15'],['Трусинчики','15'],['Трусбусбусы','15'],['Пантсы','15'],['Слипове','15'],['Слипы','15'],['Андрербаксер','15'],['Кальсоны','15'],['Панталоны','15'],['Нейку','15'],['Бреф','15'],['Трампикесы','15'],['Майтки','15'],['Куэкасики','15'],['Кангенг най','15'],['Кюлот']];
        var simValue = '12';
        
        var messageWidth = winWidth*0.85;
        var messageMarginLeft = winWidth*0.1;
        var messageMarginTop = elHeight*0.2;
        var elMargin = messageWidth*0.005;
        var $message = jQuery('<div>',{class:"message",width:messageWidth,css:{marginTop:messageMarginTop,marginLeft:messageMarginLeft,fontSize:fontSize}}).appendTo($parentArea);
        
        var messageLeftHeight = elHeight*0.4;
        var messageLeftMarginLeft = winWidth*-0.05;
        var messageLeftMarginTop = messageLeftHeight*-0.125;
        var messageLeftWidth = messageLeftHeight*0.75+messageLeftMarginLeft*-1+elMargin;
        var $messageLeft = jQuery('<div>',{class:"messageLeft",width:messageLeftWidth,height:messageLeftHeight,css:{marginLeft:messageLeftMarginLeft,marginTop:messageLeftMarginTop,marginBottom:elMargin}}).appendTo($message);
        
        var shopHeight = messageLeftHeight*0.25;
        var $shop = jQuery('<div>',{class:"shop",text:shopName,height:shopHeight,css:{}}).appendTo($messageLeft);
//         jQuery('<p>',{class:"shopName",text:shopName,css:{}}).appendTo($shop);
        
        var userHeight = messageLeftHeight*0.75-elMargin;
        var $user = jQuery('<div>',{class:"user",width:userHeight,height:userHeight,css:{marginTop:elMargin}}).appendTo($messageLeft);
        
        var messageTagWidth = messageWidth-messageLeftWidth+messageLeftMarginLeft*-1-elMargin*2;
        var messageTagHeight = messageLeftHeight-messageLeftMarginTop*-1;
        var $messageTag = jQuery('<div>',{class:"messageTag",width:messageTagWidth,height:messageTagHeight,css:{marginBottom:elMargin,marginLeft:elMargin}}).appendTo($message);
        
        var textWidth = messageWidth-elMargin*2;
        var $text = jQuery('<div>',{class:"messageText",height:fontSize*2,text:text,css:{margin:elMargin}}).appendTo($message);
        
//     });
    
    $parentArea.show();
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