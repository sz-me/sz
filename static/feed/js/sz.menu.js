function topAreaWidth(){
    var tagsTopWidth = $(window).width()-120-$("#city").width()-30-$("#place").width()-30-$("#tags").width()-30-35;
    $("#tagsTopArea").width(tagsTopWidth);
};

function placeClick(){
    if ($("#placeArea").is(":hidden")){placeRollDown()}
    else{placeRollUp()}
};

function tagsClick(){
    if ($("#tagsArea").is(":hidden")){tagsRollDown()}
    else{tagsRollUp()}
};

function messageClick(){
    if ($("#messageArea").is(":hidden")){
        rollUpAllArea();
        var j = $("#category").height();
        $("#feed").stop().animate({marginTop:'300px'},100);
        $("#message").animate({backgroundColor:'#ffa500'},500);
        $("#messageArea").slideDown(200);
    }
    else{messageRollUp()}
};

function tagsCloseClick(){
    $("#tagMessage").attr('class','NoaddMessage')
    $("#tagsTopArea").empty();
    $("#tagsClose").text('');
};


function rollUpAllArea(){
    placeRollUp();
    tagsRollUp();
    messageRollUp()
};

function placeRollUp(){
    //Сворачиваем подменю
    $("#placeArea").animate({opacity:0},300).slideUp(300).stop();
    //Удаляем из него все геотеги
    $(".geoBox").remove();
    //Поднимаем фид и меняем цвета меню
//    $("#feed").animate({marginTop:130},500);
    $("#place").animate({backgroundColor:'#808080'},300);
    $("#placeClose").css({color:'#ffa500'});
};

function messageRollUp(){
    $("#messageArea").animate({opacity:0},300).slideUp(300).stop();
//    $("#feed").animate({marginTop:110},500);
    $("#message").animate({backgroundColor:'#808080'},300)
}

function tagsRollUp(){
    //Сворачиваем подменю
    $("#tagsArea").animate({opacity:0},300).slideUp(300).stop();
    //Удаляем из него все теги
    $("#tagsArea").find(".tagBox").remove();
    //Поднимаем фид и меняем цвета меню
//    $("#feed").animate({marginTop:130},500);
    $("#tags").animate({backgroundColor:'#808080'},300);
    $("#tagsClose").css({color:'#ffa500'});
};

function placeRollDown(){
    rollUpAllArea();
//Иконку самого плэсе меняем на оранжевый
    $("#place").animate({backgroundColor:'#ffa500'},500);
//Иконку закрыть меняем на зеленую
    $("#placeClose").css({color:'#008000'});
    //Создание геотегов
    var api = new sz.Api({uri: 'api/',request_func: $.ajax});
    function placesView(data,latitude,longitude,accuracy){
        if (data.meta.code == 200){
            $.each(data.response.places, function(key, value) {
                var geoBox = jQuery('<div>',{class:"geoBox",click:function(){
                                            var place_name = $(this).find(".place_name").text();
                                            $(".placeValue").text(place_name).attr('id',$(this).attr('id'));
                                            $("#placeClose").text('[X]')
                                            topAreaWidth();
                                            }
                            }).appendTo("#placeTag");
                jQuery('<p>',{class:'place_name',text:value.name,css:{fontWeight:'bold'}}).appendTo(geoBox);
                jQuery('<p>',{class:'place_address',text:value.address}).appendTo(geoBox);}); }
        else {$(".placeValue").text(data.response.detail);}}
        
    navigator.geolocation.getCurrentPosition(function(data) {
        var latitude = data['coords']['latitude'];
        var longitude = data['coords']['longitude'];
        var accuracy = data['coords']['accuracy'];
        api.get('places',{latitude: latitude,longitude: longitude,accuracy: accuracy},
        function(r){placesView(r,latitude,longitude,accuracy); });});
    
    $.each($(".geoBox"),function(index,val){$(val).find(".place_name").text(index)});
   //Количество отображаемых за раз геотегов
   geoVal = Math.floor($(window).width()/185);
   //Количество геотегов всего
   geoLenght = $(".geoBox").length-1;
   //Отображаем только geoValShow геотегов
   $(".cityValue").text(geoVal+';'+geoLenght);
   $.each($(".geoBox"),function(index,val){if(index>(geoVal-1)){$(val).hide()}});
   //Если общее количество тегов больше,чем отображенное на странице - создаем меню, листающее геотеги
   if(geoLenght>(geoVal-1)){$("#morePlace").text('>>'+geoVal).css({cursor:'pointer'})}
   //Отображаем подменю
   var j = $("#category").height()+$("#placeArea").height()+55;
  //$("#feed").stop().animate({marginTop:'300px'},100);
   $("#placeArea").animate({opacity:1},300);
   $("#placeArea").slideDown(200);
   //Сдвигаем фид вниз

};

function tagsRollDown(){
    rollUpAllArea();
    //Меняем цвета меню
    $("#tags").animate({backgroundColor:'#ffa500'},500);
    $("#tagsClose").css({color:'#008000'});
    //Получаем тэги       
    var TagArray = {'dollyPopular':['Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель','Штаны','Носки','Трусы','Галоши','Кепка','Валенки','Шинель'],'dollyHead':['Шапки ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски '],'dollyBody':['Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи'],'dollyLegs':['Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты'],'dollyFoot':['Носки','Чулки','Макасины','Туфли','Сандали','Кроссовки','Кеды']};
    //Строим теги для каждой из подкатегорий(популярное,голова,тело,ноги,ступни)
    $.each(TagArray['dollyPopular'],function(index,val){
        var tagBox = jQuery('<div>',{class:"tagBox",text:val,click:cloneTags}).appendTo("#dollyPopularPlace");
        $(tagBox).hide();});
      
    $.each(TagArray['dollyHead'],function(index,val){
        var tagBox = jQuery('<div>',{class:"tagBox",text:val,css:{backgroundColor:'green'},click:cloneTags}).appendTo("#dollyHeadPlace");
        $(tagBox).hide();});
        
    $.each(TagArray['dollyBody'],function(index,val){
        var tagBox = jQuery('<div>',{class:"tagBox",text:val,css:{backgroundColor:'red'},click:cloneTags}).appendTo("#dollyBodyPlace");
        $(tagBox).hide();});
        
    $.each(TagArray['dollyLegs'],function(index,val){
        var tagBox = jQuery('<div>',{class:"tagBox",text:val,css:{backgroundColor:'blue'},click:cloneTags}).appendTo("#dollyLegsPlace");
        $(tagBox).hide();});
        
    $.each(TagArray['dollyFoot'],function(index,val){
        var tagBox = jQuery('<div>',{class:"tagBox",text:val,css:{backgroundColor:'orange'},click:cloneTags}).appendTo("#dollyFootPlace");
        $(tagBox).hide();});
    //Количество тегов в одной строке
    var tagWidth = Math.ceil($(window).width()*0.86/80);
    //Количество строк тегов(минус 1 про запас)
    var tagHgh = Math.ceil($("#tagsPlace").height()/85);
    //Количество тегов,которое может влезть в экран
    tagVal = tagWidth*tagHgh;
    //Оставляем отображенными только то количество тегов,которое влазит в экран
    $.each($("#dollyPopularPlace").children(),function(index,val){if(index<tagVal){$(val).show()}});
    //Если отображены не все теги(длина вссех тегов больше, чем индекс последнего видимого), отображаем кнопку далее, и указываем,что листаться будет по tagVal тэгов
    tagLenght = $("#dollyPopularPlace").children().length-1;
    if (tagLenght>(tagVal-1)){$("#moreTags").text('>>'+tagVal).css({cursor:'pointer'})} 
    //Сдвигаем фид вниз
    var j = $("#category").height()+$("#tagsArea").height()+55;
//    $("#feed").stop().animate({marginTop:j},500);
    //Отображаем подменю
    $("#tagsArea").animate({opacity:1},300);
    $("#tagsArea").slideDown(200);

};

function morePlace(){
    var maxIndex = $(".geoBox:visible:last").index();
    var n = Math.ceil(geoLenght/geoVal)*geoVal
    if(maxIndex<(geoLenght+geoVal)){
	var newMax = maxIndex+geoVal;
        var newMin = maxIndex+1;
        $("#morePlace").animate({backgroundColor:'#ffa500'},300);
        $("#lessPlace").text('<<'+geoVal).css({cursor:'pointer'});

	$.each($(".geoBox:visible"),function(index,val){$(val).hide()})
        $.each($(".geoBox"),function(index,val){
            if(newMin<=index&&index<=newMax){$(val).slideDown(500);}});
        
        $("#morePlace").animate({backgroundColor:'#808080'},100);
        if(newMax>(n-geoVal)){$("#morePlace").text('').css({cursor:'default'})}
    }
};

function moreTags(){
    var $parent = $(".tagBox:visible").parent();
    var maxIndex = $($parent).find(".tagBox:visible:last").index();
    var n = Math.ceil(tagLenght/tagVal)*tagVal
    if(maxIndex<(tagLenght+tagVal)){
        var newMin = maxIndex+1;
        var newMax = maxIndex+tagVal;

        $("#moreTags").animate({backgroundColor:'#ffa500'},300);
        $("#lessTags").text('<<'+tagVal).css({cursor:'pointer'});

        $.each($($parent).children(":visible"),function(index,val){$(val).hide()})
        $.each($($parent).children(),function(index,val){
                if(newMin<=index&&index<=newMax){
                    $(val).slideDown(500);
                }});
        
        $("#moreTags").animate({backgroundColor:'#808080'},100);
        if(newMax>(n-tagVal)){$("#moreTags").text('').css({cursor:'default'})}
        }
};

function lessPlace(){
    var n = geoVal-1
    var minIndex = $(".geoBox:visible:first").index();
    if(minIndex>n){
        var newMin = minIndex-geoVal;
        var newMax = minIndex-1;
        $("#lessPlace").animate({backgroundColor:'#ffa500'},300);
        $("#morePlace").text('>>'+geoVal).css({cursor:'pointer'});

        $.each($(".geoBox:visible"),function(index,val){$(val).hide()})
        $.each($(".geoBox"),function(index,val){
            if(newMin<=index&&index<=newMax){$(val).slideDown(500);}});
        $("#lessPlace").animate({backgroundColor:'#808080'},100);

        if(newMin<n){$("#lessPlace").text('').css({cursor:'default'})}
    }
        
};

function lessTags(){
    var n = tagVal-1
    var $parent = $(".tagBox:visible").parent();
    var minIndex = $($parent).find(".tagBox:visible:first").index();
    if(minIndex>n){
        var newMin = minIndex-tagVal;
        var newMax = minIndex-1;
        $("#lessTags").animate({backgroundColor:'#ffa500'},300);
        $("#moreTags").text('>>'+tagVal).css({cursor:'pointer'});

        $.each($($parent).children(":visible"),function(index,val){$(val).hide()})
        $.each($($parent).children(),function(index,val){
            if(newMin<=index&&index<=newMax){
                $(val).slideDown(500);
            }});

        $("#lessTags").animate({backgroundColor:'#808080'},100);

        if(newMin<n){$("#lessTags").text('').css({cursor:'default'})}
    }
};


function cloneTags(){
    $("#tagsClose").text('[X]');
    if($("#placeClose").text()=='[X]'){$("#tagMessage").attr('class','addMessage');}
    var $topBox = jQuery('<div>',{class:"tagTopBox"}).appendTo("#tagsTopArea");
    jQuery('<div>',{class:"topClose",text:'[X]',click:(function(){
								$topBox = $(this).parent(); $($topBox).remove();var topBoxLenght = $("#tagsTopArea").children().length; if(topBoxLenght==0){tagsCloseClick()}
})}).appendTo($topBox);
    jQuery('<div>',{class:"tagTop_name",text:$(this).text()}).appendTo($topBox);
    var marginTopVal = '-'+($("#tagsTopArea").height()+5)+'px'
    $("#tagsTopArea").css({marginTop:marginTopVal})
    if($("#tagsTopArea").height()>70){$("#top").animate({height:($("#tagsTopArea").height()-70)},100);}
    $topBox.clone().appendTo("#newmessage_tagsValue")
};

function dollyBodyClick(){
    var catWidth = $(this).width();
    if (catWidth==100){
        $(this).animate({borderColor:'#ffa500',borderWidth:'3px',width:'110',borderRadius:'10px'},300);}
    if (catWidth==110){
        $(this).animate({borderColor:'#808080',borderWidth:'1px',width:'100',borderRadius:'2px'},300);}

};
