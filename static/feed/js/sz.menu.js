function topAreaWidth(){
//    var tagsTopWidth = $(window).width()-15-$("#city").width()-30-$("#place").width()-30-$("#tags").width()-30-35;
//    $("#tagsTopArea").width(tagsTopWidth);
};

function placeClick(){
    if ($("#placeArea").is(":hidden")){placeRollDown()}
    else{placeRollUp()}
};

function tagsClick(){
    if ($("#tagsArea").is(":hidden")){tagsRollDown()}
    else{tagsRollUp()}
};

function tagsCloseClick(){
    $("#tagsTopArea").empty();
    $("#tagsPlace").find(".tagBoxSelect").attr('class','tagBox');
    $("#tagsClose").text('');
};


function rollUpAllArea(){
    placeRollUp();
    tagsRollUp();

};

function placeRollUp(){
    //Сворачиваем подменю
    $("#placeArea").animate({opacity:1},300).slideUp(300).stop();
    //Удаляем из него все геотеги
    $(".geoBox").remove();
$("#category").children().animate({opacity:1},200);
 $("#feed").animate({opacity:1},200);
};


function tagsRollUp(){
    //Сворачиваем подменю
    $("#tagsArea").animate({opacity:1},300).slideUp(300).stop();
    //Удаляем из него все теги
    $("#tagsArea").find(".tagBox").remove();
    $(".moveArea").css({marginTop:'0px'});
    $("#moreTags").text('').attr('class','lessmore_noactive');
    $("#lessTags").text('').attr('class','lessmore_noactive');
$("#category").children().animate({opacity:1},200);
 $("#feed").animate({opacity:1},200);
};

function placeRollDown(){
    rollUpAllArea();
    $("#feed").animate({opacity:0.6},200);
    $.each($("#category").children(),function(index,val){if($(val).attr('id')!='place'){$(val).animate({opacity:0.6},200);}});
    //Создание геотегов
    var api = new sz.Api({uri: 'api/',request_func: $.ajax});
    function placesView(data,latitude,longitude,accuracy){
        if (data.meta.code == 200){
            $.each(data.response, function(key, value){
                var geoBox = jQuery('<div>',{class:"geoBox",id:value.venue_id,click:function(){
                                            var place_name = $(this).find(".place_name").text();
                                            $(".placeValue").text(place_name).attr('id',$(this).attr('id'));
                                            $("#placeClose").text('[X]')
                                            topAreaWidth();
                                            }}).appendTo("#placeTag");
                jQuery('<p>',{class:'place_name',text:value.name,css:{fontWeight:'bold'}}).appendTo(geoBox);
                jQuery('<p>',{class:'place_address',text:value.address}).appendTo(geoBox);}); }
        else {$(".placeValue").text(data.response.detail);}}
        
    navigator.geolocation.getCurrentPosition(function(data) {
        var latitude = data['coords']['latitude'];
        var longitude = data['coords']['longitude'];
        var accuracy = data['coords']['accuracy'];
        api.get('places',{latitude: latitude,longitude: longitude,accuracy: accuracy},
        function(r){placesView(r,latitude,longitude,accuracy); });});
    
   //Количество отображаемых за раз геотегов
   geoVal = Math.floor($(window).width()/185);
   //Количество геотегов всего
   geoLenght = $(".geoBox").length-1;
   //Отображаем только geoValShow геотегов
   $.each($(".geoBox"),function(index,val){if(index>(geoVal-1)){$(val).hide()}});
   //Если общее количество тегов больше,чем отображенное на странице - создаем меню, листающее геотеги
   if(geoLenght>(geoVal-1)){$("#morePlace").text('Следующие '+geoVal).css({cursor:'pointer'})}
   //Отображаем подменю
   $("#placeArea").animate({opacity:1},300);
   $("#placeArea").slideDown(200);
};

function tagsRollDown(){
    rollUpAllArea();
    $("#feed").animate({opacity:0.6},200);
$.each($("#category").children(),function(index,val){if($(val).attr('id')!='tags'){$(val).animate({opacity:0.6},200);}});
    $("#tags").animate({opacity:1},200);

    //Получаем тэги       
    var TagArray = {'dollyPopular':['Шапки ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски ','Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи','Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты','Носки ','Чулки ','Макасины ','Туфли ','Сандали ','Кроссовки ','Кеды ','Шапки ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски ','Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи','Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты','Носки ','Чулки ','Макасины ','Туфли ','Сандали ','Кроссовки ','Кеды ','Шапки ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски ','Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи','Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты','Носки ','Чулки ','Макасины ','Туфли ','Сандали ','Кроссовки ','Кеды ','Шапки ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски ','Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи','Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты','Носки ','Чулки ','Макасины ','Туфли ','Сандали ','Кроссовки ','Кеды ','Шапки ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски ','Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи','Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты','Носки ','Чулки ','Макасины ','Туфли ','Сандали ','Кроссовки ','Кеды ','Шапки ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски ','Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи','Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты','Носки ','Чулки ','Макасины ','Туфли ','Сандали ','Кроссовки ','Кеды ']}
//,'dollyHead':['Шапки ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски '],'dollyBody':['Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи'],'dollyLegs':['Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты'],'dollyFoot':['Носки','Чулки','Макасины','Туфли','Сандали','Кроссовки','Кеды']};
    //Строим теги для каждой из подкатегорий(популярное,голова,тело,ноги,ступни)
    $.each(TagArray['dollyPopular'],function(index,val){
        var $tagBox = jQuery('<div>',{class:"tagBox",id:'dollyPopular'+index,text:val,click:tagBoxclick}).appendTo("#dollyPopularMove");
	var $tagBoxImage = jQuery('<div>',{class:"tagBoxImage"}).appendTo($tagBox);});
    //Меняем ширину поля
    var winWidth = $("#mainmenu").width();
    tagsRow = Math.floor((winWidth-190)/85);
    var tagsPlaceWidth = tagsRow*85;

/*    if (winWidth<400){$(".lessmore_noactive,.lessmore_active").css({marginLeft:'130px'})}
    else{$(".lessmore_noactive,.lessmore_active").css({marginLeft:'50%'})}

    if (tagsPlaceWidth<85){var tagsPlaceWidth=85;$("#tagsArea").width(285);$(".lessmore_noactive,.lessmore_active").css({marginLeft:'100px'}); tagsRow=1;}
*/
    $("#tagsPlace").width(tagsPlaceWidth).css({marginLeft:'130px'})
    //Количество строк тегов
    tagsClm = 3
    //Количество тегов,которое может влезть в экран
    tagVal = tagsRow*tagsClm;
    //Если отображены не все теги(длина вссех тегов больше, чем индекс последнего видимого), отображаем кнопку далее, и указываем,что листаться будет по tagVal тэгов
    var tagLenght = $("#dollyPopularMove").children().length-1;
    if (tagLenght>(tagVal-1)){$("#moreTags").text('Следующие '+tagVal).attr('class','lessmore_active')} 
    //Отображаем подменю
    $("#tagsArea").animate({opacity:1},300);
    $("#tagsArea").slideDown(200);
$(".placeValue").text(tagsRow+';'+tagsPlaceWidth+';'+$("#mainmenu").width())

};

function morePlace(){
    var maxIndex = $(".geoBox:visible:last").index();
    var n = Math.ceil(geoLenght/geoVal)*geoVal
    if(maxIndex<(geoLenght+geoVal)){
	var newMax = maxIndex+geoVal;
        var newMin = maxIndex+1;
        $("#morePlace").animate({opacity:0.6},500).animate({opacity:1},500);
        $("#lessPlace").text('Предыдущие '+geoVal).attr('class','lessmore_active');

	$.each($(".geoBox:visible"),function(index,val){$(val).hide()})
        $.each($(".geoBox"),function(index,val){
            if(newMin<=index&&index<=newMax){$(val).slideDown(500);}});
        
        if(newMax>(n-geoVal)){$("#morePlace").text('').attr('class','lessmore_noactive')}
    }
};

function moreTags(){
    var $move_parent = $(".tagBox:visible").parent();
    var tagLenght = $($move_parent).children().length;
    var margin = $($move_parent).css('marginTop');
    var moveWidth = tagsClm*85;
    var marginNum = ((margin.slice(0,margin.length-2))*-1)+moveWidth;
    var tagsWidth = tagLenght*85/tagsRow;
    if(marginNum<tagsWidth){
        $("#moreTags").animate({opacity:0.6},500).animate({opacity:1},500);
        $("#lessTags").text('Предыдущие '+tagVal).attr('class','lessmore_active');

        var mT = '-='+moveWidth+'px';
	jQuery($move_parent).animate({marginTop:mT},500);        
	
        if((marginNum+moveWidth)>tagsWidth){$("#moreTags").text('').attr('class','lessmore_noactive')}
	
        }
};

function lessPlace(){
    var n = geoVal-1
    var minIndex = $(".geoBox:visible:first").index();
    if(minIndex>n){
        var newMin = minIndex-geoVal;
        var newMax = minIndex-1;
        $("#lessPlace").animate({opacity:0.6},500).animate({opacity:1},500);
        $("#morePlace").text('Следующие '+geoVal).attr('class','lessmore_active');

        $.each($(".geoBox:visible"),function(index,val){$(val).hide()});
        $.each($(".geoBox"),function(index,val){
            if(newMin<=index&&index<=newMax){$(val).slideDown(500);}});


        if(newMin<n){$("#lessPlace").text('').attr('class','lessmore_noactive')}
    }
        
};

function lessTags(){
    var $move_parent = $(".tagBox:visible").parent();
    var tagLenght = $($move_parent).children().length;
    var margin = $($move_parent).css('marginTop');
    var marginNum = ((margin.slice(0,margin.length-2))*-1);
    if(marginNum>0){
        $("#lessTags").animate({opacity:0.6},500).animate({opacity:1},500);
        $("#moreTags").text('Следующие '+tagVal).attr('class','lessmore_active');

        var moveWidth = tagsClm*85;
        var mT = '+='+moveWidth+'px';
	jQuery($move_parent).animate({marginTop:mT},500);        
	
        if((marginNum-moveWidth)<=0){$("#lessTags").text('').attr('class','lessmore_noactive')}
        }
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

function dollyBodyClick(){
    var catWidth = $(this).width();
    if (catWidth==100){
        $(this).animate({borderColor:'#ffa500',borderWidth:'3px',width:'110',borderRadius:'10px'},300);}
    if (catWidth==110){
        $(this).animate({borderColor:'#808080',borderWidth:'1px',width:'100',borderRadius:'2px'},300);}

};
