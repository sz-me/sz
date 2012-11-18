function geoClick(place,place_name,place_id,latitude,longitude,accuracy,city_id){
    var i = ($(window).width()-330)/2;
    
    $("#root").text("Пару слов,пожалуйста");
    $("#area").empty();
    
    jQuery('<div>',{id:'textArea'}).appendTo("#area");
    jQuery('<textarea>',{rows:"10",cols:"45",id:'text'}).appendTo("#textArea");
    jQuery('<div>',{id:'tagString',text:'Добавить тэги',click:tagSelect}).appendTo("#textArea");
    jQuery('<div>',{id:'geoString',text:place_name,click:geoSelect}).appendTo("#textArea");
    jQuery('<input>',{id:'send',value:'Отправить',type:'button',click:sendForm(place,place_id,latitude,longitude,accuracy,city_id,$("#tagString").text(),'hjhj')}).appendTo("#textArea");
    
    $("#textArea").children().css({marginLeft:i});
};

function tagSelect(){
    $("#area").children().hide()
    var n = $("#area").find("#tag").length
    if (n==0){
    jQuery('<div>',{id:'tag'}).appendTo("#area")
    var tagSearch = jQuery('<input>',{css:{width:'270px'},type:'text',value:'Начните вводить название',focus:(function(){$(this).val('');})}).appendTo(jQuery('<li>',{css:{width:'100%'}}).appendTo("#tag"));
        jQuery('<div>',{id:'gender'}).appendTo("#tag");
        jQuery('<div>',{id:'genderArea'}).appendTo("#tag");
        jQuery('<a>',{id:'female',text:'0',click:function(){var tagMassiv = femaleTag; thisArea = $("#femaleArea");genderArea(tagMassiv,thisArea)}}).appendTo("#gender");
        jQuery('<a>',{id:'male',text:'0',click:function(){var tagMassiv = femaleTag; thisArea = $("#maleArea");genderArea(tagMassiv,thisArea)}}).appendTo("#gender");
        jQuery('<a>',{id:'kind',text:'0'}).appendTo("#gender");
        jQuery('<a>',{id:'unisex',text:'0'}).appendTo("#gender");
        
        jQuery('<input>',{type:'button', value:'Добавить',id:'tagAddBut',css:{width:'100px',marginTop:'5px'},click:tagAdd}).appendTo("#genderArea")
        
        jQuery('<div>',{id:'femaleArea'}).appendTo("#genderArea");
        jQuery('<div>',{id:'maleArea'}).appendTo("#genderArea");
        jQuery('<div>',{id:'kindArea'}).appendTo("#genderArea");
        jQuery('<div>',{id:'unisexArea'}).appendTo("#genderArea");
        
        var tagMassiv = femaleTag; thisArea = $("#femaleArea");
        
        genderArea(tagMassiv,thisArea)}
    else{$("#tag").show()}
};   

function genderArea(tagMassiv,thisArea){
    var n = $(thisArea).children().length;
    i = ($(window).width()-100)/2;
    
    $(thisArea).siblings().hide();
    $("#tagAddBut").show()
    $(thisArea).show();
    
    if (n==0){
        var catDiv = jQuery('<div>',{class:'catArea'}).appendTo(thisArea);
        jQuery('<div>',{class:'headCat',click:function (){var clickThis = $(this); massiv = tagMassiv['head'];tagArea = $(tagDiv).find(".headTag"); catClick(clickThis,massiv,tagArea)}, style:'background-image:url({{ STATIC_URL }}img/headLtl.png);'}).appendTo(catDiv);
        jQuery('<div>',{class:'bodyCat',click:function (){var clickThis = $(this); massiv = tagMassiv['body'];tagArea = $(tagDiv).find(".bodyTag"); catClick(clickThis,massiv,tagArea)}, style:'background-image:url({{ STATIC_URL }}img/bodyLtl.png);'}).appendTo(catDiv);
        jQuery('<div>',{class:'legsCat',click:function (){var clickThis = $(this); massiv = tagMassiv['legs'];tagArea = $(tagDiv).find(".legsTag"); catClick(clickThis,massiv,tagArea)}, style:'background-image:url({{ STATIC_URL }}img/legLtl.png);'}).appendTo(catDiv);
        jQuery('<div>',{class:'footCat',click:function (){var clickThis = $(this); massiv = tagMassiv['foot'];tagArea = $(tagDiv).find(".footTag"); catClick(clickThis,massiv,tagArea)}, style:'background-image:url({{ STATIC_URL }}img/footLtl.png);'}).appendTo(catDiv);   
        
        $.each($(catDiv).children(),function(index,val){$(val).css({'margin-left':i});});
        $("#tagAddBut").css({'margin-left':i});
        
        var tagDiv = jQuery('<div>',{class:'tagArea', style:'float:left;margin-top:-150px;margin-left:88px;'}).appendTo(thisArea);
        jQuery('<div>', {class:'headTag'}).appendTo(tagDiv);
        jQuery('<div>', {class:'bodyTag'}).appendTo(tagDiv);
        jQuery('<div>', {class:'legsTag'}).appendTo(tagDiv);
        jQuery('<div>', {class:'footTag'}).appendTo(tagDiv);}
    else{
        $(thisArea).find('.tagArea').find('div').hide()
        $.each($(thisArea).find('.catArea').find('div'),function(index,val){
           j = $(val).width()
           if (j==50){var h=$(val).height()*2;$(val).css({marginLeft:i,width:'100px',height:h,borderColor:'black',borderWidth:'1px'})}
           if (j==80){var h=$(val).height()*1.25;$(val).css({marginLeft:i,width:'100px',height:h,borderColor:'black',borderWidth:'1px'})}
       })
        
    }
};

function checkArea(tagArea,massiv){
    $(tagArea).find('div').show()
    var n = $(tagArea).children().length;
    if (n==0){
        var selectTagArea = jQuery('<div>',{css:{width:'100%',textAlign:'center',marginBottom:'5px'}}).appendTo(tagArea)
        selectTagALL = jQuery('<a>',{click:function(){$(tagArea).find(".boxMulty").attr('class','boxSelect')},text:'Выбрать всю категорию',css:{marginLeft:'5px',fontWeight:'bold',borderColor:'black',borderWidth:'1px',borderStyle:'solid',width:'230px'}}).appendTo(selectTagArea)
        selectTagNoth = jQuery('<a>',{click:function(){$(tagArea).find(".boxSelect").attr('class','boxMulty')},text:'Сбросить всю категорию',css:{marginLeft:'5px',fontWeight:'bold',borderColor:'black',borderWidth:'1px',borderStyle:'solid',width:'230px'}}).appendTo(selectTagArea)
        $.each(massiv,function(index,val){
            var tagDiv=jQuery('<div>',{text:' '+val+' ',class:'boxMulty',
                              click:(function(){$(this).attr('class',function(index,oldval){
                                if (oldval=='boxMulty') {return 'boxSelect'}
                                if (oldval=='boxSelect') {return 'boxMulty'}});})}).appendTo(tagArea)});}
};

function catClick(clickThis,massiv,tagArea){
    var i = ($(window).width()-100)/2;w=$(clickThis).width();catDiv=$(clickThis).parent();
    if (w==80){var hthis = $(clickThis).height()*1.25
        $(tagArea).hide();
        $.each($(catDiv).find('div'),function(index,val){
            if ($(val).width()!=80){var h=$(val).height()*2;
            $(val).stop().animate({marginLeft:i,width:'100px',height:h,borderColor:'black',borderWidth:'1px'},1500)}});
        $(clickThis).animate({marginLeft:i,width:'100px',height:hthis,borderColor:'black',borderWidth:'1px'},1500)}
    if(w==50){var hthis = $(clickThis).height()*1.6
        $(tagArea).siblings().hide();
        $(tagArea).show()
        $.each($(catDiv).find('div'),function(index,val){if ($(val).width()==80){var h=$(val).height()*0.625;  
            $(val).stop().animate({marginLeft:'15px',width:'50px',height:h,borderColor:'black',borderWidth:'1px'},1500)}}) 
        $(clickThis).stop().animate({marginLeft:'0px',width:'80px',height:hthis,borderColor:'green',borderWidth:'2px'},1500,checkArea(tagArea,massiv));}
    if(w==100){var hthis = $(clickThis).height()*0.8
        $(tagArea).show()
        $.each($(catDiv).find('div'),function(index,val){var h = $(val).height()/2
            $(val).stop().animate({marginLeft:'15px',width:'50px',height:h,borderColor:'black',borderWidth:'1px'},1500);});
        $(clickThis).stop().animate({marginLeft:'0px',width:'80px',height:hthis,borderColor:'green',borderWidth:'2px'},1500,checkArea(tagArea,massiv)); }
};


function tagAdd(){
    var tagValue = []
    $.each($("#genderArea").find(".boxSelect"),function(key,val){tagValue.push($(val).text())});
    $("#textArea").show();
    $("#tag").hide();
    $("#tagString").text(tagValue);
    $("#textArea").show();
    
};

function geoSelect(){}

function showPlaces(city_id){
    var api = new sz.Api({uri: 'api/',request_func: $.ajax});
    function placesView(data,latitude,longitude,accuracy){
        if (data.meta.code == 200){
            $("#root").text('Место');
            $("#area").append($('<div><input type="input" id="searchGeo"/></div>'));
            $("#area").append($('<input type="checkbox" id="closerCheck"/> <label for="closerCheck">Ближайшие</label>'));
            jQuery('<div>',{id:"places"}).appendTo("#area");
            $.each(data.response.places, function(key, value) {
                var geoBox = jQuery('<div>',{class:'geoBox',id:value.venue_id,click:(function(){
            var place_id = $(this).attr('id');
                place_name = $(this).find(".place_name").text();
                latitude = latitude;
                longitude = longitude;
                accuracy = accuracy;
            geoClick(place_id,place_name,latitude,longitude,accuracy)
        })}).appendTo("#places");
                jQuery('<p>',{text:value.name,css:{fontWeight:'bold'}}).appendTo(geoBox);
                jQuery('<p>',{text:value.address}).appendTo(geoBox);
            });}
        else { $("#root").text(data.response.detail);}}
        
    navigator.geolocation.getCurrentPosition(function(data) {
        var latitude = data['coords']['latitude'];
        var longitude = data['coords']['longitude'];
        var accuracy = data['coords']['accuracy'];
        api.get('places',{latitude: latitude,longitude: longitude,accuracy: accuracy},
        function(r){placesView(r,latitude,longitude,accuracy); });});
}

function sendForm(place,place_id,latitude,longitude,accuracy,city_id,things,text){
//     var api = new sz.Api({uri: 'api/',request_func: $.ajax});
//     
//     api.post('messages',{
//         "text":text,
//         "latitude": latitude,
//         "longitude": longitude,
//         "accuracy": accuracy,
//         "city_id": city_id,
//         "place_id": place_id,
//         "bargain_date": null,
//         "date": "2012-11-12T14:16:51.944Z",
//         "user": 1,
//         "things": []
//     })
}

function Add(city_id){
    $("#content").empty();
    femaleTag = {'head':['Шапки ','Шляпы ','Ушанки ','Банданы ','Косынки ','Шлемы ','Кепки ','Бейсболки ','Тэниски '],
                     'body':['Платье','Сарафан','Футболка','Топ','Толстовка','Кардиган','Пуловер','Блузка','Туника','Костюм','Водолазка','Комбинизон','Свитер','Свитшот','Логнслив','Худи'],
                    'legs':['Штаны','Трусы','Джинсы','Леггинсы','Треники','Панталоны','Шорты'],
                    'foot':['Носки','Чулки','Макасины','Туфли','Сандали','Кроссовки','Кеды']};
    jQuery('<div>',{id:"root"}).appendTo("#content");
    jQuery('<div>' ,{id:"area"}).appendTo("#content");
    
//     $("#root").text('Место');
//     $("#area").append($('<div><input type="input" id="searchGeo"/></div>'));
//     $("#area").append($('<input type="checkbox" id="closerCheck"/> <label for="closerCheck">Ближайшие</label>'));
//     jQuery('<div>',{id:"places"}).appendTo("#area");
//     $.each([0,1,2,3,4], function(key, value) {
//         var geoBox = jQuery('<div>',{class:'geoBox',id:'4db189220f2c0353f5cb6141',click:(function(){
//             var place_id = $(this).attr('id');
//                 place_name = $(this).find(".place_name").text();
//                 latitude = 50.263495219396574;
//                 longitude = 127.53357833117961;
//                 accuracy = 10.0;
//             geoClick(place_id,place_name,latitude,longitude,accuracy,city_id)
//         })}).appendTo("#places");
//         jQuery('<p>',{class:'place_name',text:'Салон-магазин МТС',css:{fontWeight:'bold'}}).appendTo(geoBox);
//         jQuery('<p>',{text:'Автовокзал Горького 129,4 этаж каб.62 зеленая дверь'}).appendTo(geoBox);});  
     showPlaces(city_id)
}
    
