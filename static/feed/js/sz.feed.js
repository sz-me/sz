function lessmoreMessageClick(){
var $lessmore = $(this);
if($(this).text()=='Больше'){RollDownMessage($lessmore)}
else{RollUpMessage($lessmore)}
};


function RollUpMessage($lessmore){
    var $message = $($lessmore).closest(".message");
    $($message).animate({borderColor:'#999',borderWidth:'1px'},200);
    $($message).find(".mestagsArea").animate({height:'92px'},200)    
    $($message).find(".photo").hide();
    $($message).find(".messagebottom").animate({height:'15px'},250);
    $($message).find('.moreMessage').show();
    $($lessmore).text('Больше');
};
    
function RollDownMessage($lessmore){
//Развертка сообщения
    var $message = $($lessmore).closest(".message");
    var $mestagsArea = $($message).find(".mestagsArea");
    var mestagsAreaHgh = ($($mestagsArea).find(".boxMesTag").length/messageTagWidth)*120+'px';
    $($mestagsArea).animate({height:mestagsAreaHgh},200);
    $($message).animate({borderColor:'#FF9933',borderWidth:'2px'},200);
    $($message).find(".messagebottom").css({height:'auto'});
    $($message).find(".photo").show();
    $($message).find('.lessMessage').show();
    $($lessmore).text('Меньше');
};

function getMessage(){
    var api = new sz.Api({uri: 'api/',request_func: $.ajax});
    api.get('messages',{},
            function(r){messagesView(r);})
};
    
function messagesView(data){
    if ($.isArray(data.response)){
        $.each(data.response, function(key, value) {
            var username = 'Vasya';
            var userpic = '';
            var place_name = value.place_id;
            var place_address = ' , ул Амурская 17';
            var city = value.city_id;
            var tagsKey = ['Трусы','Бондаж','Корсет','Плетка','Носки','Чулки','Шарфик','Шапочка','Пипетка','Макосины','Валенки','Джинсы','Шорты','Одеяло','Подушка','Сандали','Кроссовки','Свитер','Борода','Майка','Колготы','Кеды','Бандана','Комбинизон','Сорочка','Лыжи','Боди','Платье','Каска','Респиратор','Очки','Бюстье']
            var fulltext = value.text;
            var photoSource = "../img/photo.jpg"
            //Создаем див самого сообщения
            var $message = jQuery('<div class="message">').appendTo("#feed");
            var $loc = jQuery('<div>',{class:"location"}).appendTo($message);
            //В нем создаем див для отображаемой части сообщения
            var $messagetop = jQuery('<div>',{class:"messagetop"}).appendTo($message);
            //В нем создаем место для юзерпика
            var $user = jQuery('<div>',{class:"user"}).appendTo($messagetop);
            jQuery('<div>',{class:"userpic"}).appendTo($user);
            jQuery('<div>',{class:"username",text:username}).appendTo($user);
            //В нем же создаем место для геотэгов

            //В месте для геотэгов создаем место под магазин
            var $place = jQuery('<div>',{class:"place"}).appendTo($loc);
            //В место под магазин добавляем название магазина
            jQuery('<span>',{class:"place_name",text:place_name}).appendTo($place);
            //и его адрес
            jQuery('<span>',{class:"place_address",text:place_address}).appendTo($place);
            //В месте под геотэги создаем див с названием города
       //     jQuery('<div>',{class:"city",text:city}).appendTo($loc);
            //Создаем место под тэги
            var $mestagsArea = jQuery('<div>',{class:"mestagsArea"}).appendTo($messagetop);
            //Для каждого из элемента полученного массива тэгов, создаем иконку тэга
            $.each(tagsKey,function(index,val){
                var $tagBox = jQuery('<div>',{class:"tagTopBox",text:val}).appendTo($mestagsArea);
                //В ней размещаем название тэга
//                jQuery('<p>',{marginTop:'1px',text:val}).appendTo($tagBox);
                //Изображение
//                jQuery('<div>',{class:"boxMesTagImg"}).appendTo($tagBox);
                //И его рейтинг в контексте данного сообщения
//                jQuery('<div>',{class:"boxMesTagrRat",text:'+15-'}).appendTo($tagBox);
            });
            //Создаем иконку развертки сообщения
//            jQuery('<div>',{class:"moreMessage",text:'>>',click:RollDownMessage}).appendTo($messagetop); 
            //Создаем див для скрытых элементов сообщения
            var $messagebottom = jQuery('<div>',{class:"messagebottom"}).appendTo($message);
            //В него помещаем фотографию
            jQuery('<img>',{class:"photo",src:photoSource,align:'left',width:'150',alt:'PHOTO',css:{border:'1px solid #444',borderRadius:'5px',marginRight:'15px',marginBottom:'5px'},click:(function(){
                                    jQuery(($(this).clone())).animate({width:'+=400px',height:'+=400px'},200).dialog({modal:'true',width:'auto',show:'slideDown',click:(function(event,ui){$(this).remove()})})})}).appendTo($messagebottom).hide();
            //Text
            jQuery('<div>',{text:fulltext}).appendTo($messagebottom);
            //Иконка свертки сообщения
            jQuery('<div>',{class:"lessmoreMessage",text:'Больше',click:lessmoreMessageClick}).appendTo($message);
            //Количество тэгов в одном ряду - уменьшенная на 100(ширина юзерпика) ширина самого сообщения,деленная на 80(ширина одно тэга), и все это окгругляем вниз

            messageTagWidth = ($mestagsArea.width())/80
            })
        }
 
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
