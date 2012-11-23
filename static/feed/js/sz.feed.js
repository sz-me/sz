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
    var username = 'Vasya';
    var    place_name = 'Кожа-Да-Кости,Секс-Шоп ';
    var    place_address = 'ул Амурская 17';
    var    city = 'Blagoveschensk, RU';
    var    tagsKey = ['Трусы','Бондаж','Корсет','Плетка','Носки','Чулки','Шарфик','Шапочка','Пипетка','Макосины','Валенки','Джинсы','Шорты','Одеяло','Подушка','Сандали','Кроссовки','Свитер','Борода','Майка','Колготы','Кеды','Бандана','Комбинизон','Сорочка','Лыжи','Боди','Платье','Каска','Респиратор','Очки','Бюстье']
    var    fulltext = 'Распродажа кожи и латекса в магазине Кожа-Да-Кости! В продаже имеются трусы,бондажи,корсеты, костюмы медсестры,учительницы, спанчбоба, патрика, котопса, рэйнбоу-даш, всех остальных поняш, слоупка, лилы, пикачу, рекурсивной функции, объекта и многое другое. Пятидесяти процентная скидка на хит продаж - костюм матрицы! Спешите! Акция продлится до 21 декабря 2012 года! Жи Ши пиши через и. Будь внимательней с тся и ться! Граммар негодуэ! Пыщпыщ трололо, кипяточек поспяшо!Все жанры искусства хороши, кроме Секс шоп, но Секс шоп – не жанр. Секс шоп – тут дело не в мощности, а в функциональности. Модным трендом последних лет стали тонкие телефоны, тонкие телевизоры и тонкие тела. В целом, модная индустрия до сих пор выбирает идеал по принципу «чем тоньше Секс шоп, тем лучше». Если все вышесказанное относится к вам, то милости просим к нам, мы вам будем рады, да и вы нам, надеемся, тоже. История знает много примеров, когда в занятой или бесперспективной, на первый взгляд, нише внезапно возникали новые лидеры, например, Секс шоп. Обливаться из таза холодной водой уже не модно. Злобные люди придумали новый способ прервать ваш утренний сон. Нравится вам, например, Секс шоп, который при попытке прикоснуться к нему бьет током? Не нравится? Мне тоже, а что делать, если надо проснуться, а сон никак не уходит? Вот свежая новость: как сообщает заместитель начальника управления таксопарком города Ма Яньцзе, водители такси, замеченные в общении с Секс шоп, будут оштрафованы на сумму 100–200 юаней, а их имена будут опубликованы в СМИ. Секс шоп – испытание идеи на прочность. У вас есть достаточный опыт работы с Секс шоп, или вы просто словами бросаетесь? Я в дискуссии о Секс шоп не вступаю. Правда, мой опыт с Секс шоп небольшой: было лет 7-8 назад. На днях кто-то сказал: «А еще я слышал, вы тут к Секс шоп плохо относитесь. Это что? Дискриминация что ли?» Могут быть несколько причин. Первая: голоса в голове. Вторая: кто-то тебе действительно сказал, что тут к Секс шоп плохо относятся. Тогда спроси у него. Третее: ты неправильно понял услышанное, например, кто-то тебе что-то сказал, а тебе послышалось: «Там к Секс шоп плохо относятся.» На самом деле это не так. А вот «Пош скес» – это Секс шоп наоборот.';
    var photoSource = "/home/kunla/project/static/feed/img/photo.jpg"

    //Создаем див самого сообщения
    var $message = jQuery('<div class="message">').appendTo("#feed");
    //В нем создаем див для отображаемой части сообщения
    var $messagetop = jQuery('<div>',{class:"messagetop"}).appendTo($message);
    //В нем создаем место для юзерпика
    jQuery('<div>',{class:"user",text:username}).appendTo($messagetop);
    //В нем же создаем место для геотэгов
    var $loc = jQuery('<div>',{class:"location"}).appendTo($messagetop);
    //В месте для геотэгов создаем место под магазин
    var $place = jQuery('<div>',{class:"place"}).appendTo($loc);
    //В место под магазин добавляем название магазина
    jQuery('<span>',{class:"place_name",text:place_name}).appendTo($place);
    //и его адрес
    jQuery('<span>',{class:"place_address",text:place_address}).appendTo($place);
    //В месте под геотэги создаем див с названием города
    jQuery('<div>',{class:"city",text:city}).appendTo($loc);
    //Создаем место под тэги
    var $messageTags = jQuery('<div>',{class:"mestagsArea"}).appendTo($messagetop);
    //Для каждого из элемента полученного массива тэгов, создаем иконку тэга
    $.each(tagsKey,function(index,val){
        var $tagBox = jQuery('<div>',{class:"boxMesTag"}).appendTo($messageTags);
        //В ней размещаем название тэга
        jQuery('<p>',{marginTop:'1px',text:val}).appendTo($tagBox);
        //И его рейтинг в контексте данного сообщения
        jQuery('<p>',{fontWeight:'bold',marginTop:'32px',text:'+15-'}).appendTo($tagBox);
    });
    //Создаем иконку развертки сообщения
    jQuery('<div>',{class:"moreMessage",text:'>>',click:RollDownMessage}).appendTo($messagetop); 
    //Создаем див для скрытых элементов сообщения
    var $messagebottom = jQuery('<div>',{class:"messagebottom"}).appendTo($message);
    //В него помещаем фотографию
    jQuery('<img>',{class:"photo",src:photoSource,align:'left',width:'150',css:{border:'1px solid #444',borderRadius:'5px',marginRight:'5px',marginBottom:'5px'},click:(function(){
                               jQuery(($(this).clone())).animate({width:'+=400px',height:'+=400px'},200).dialog({modal:'true',width:'auto',show:'slideDown',click:(function(event,ui){$(this).remove()})})})}).appendTo($messagebottom).hide();
    //Text
    jQuery('<div>',{text:fulltext}).appendTo($messagebottom);
    //Иконка свертки сообщения
    jQuery('<div>',{class:"lessMessage",text:'<<',click:RollUpMessage}).appendTo($message);
    //Количество тэгов в одном ряду - уменьшенная на 100(ширина юзерпика) ширина самого сообщения,деленная на 80(ширина одно тэга), и все это окгругляем вниз

    messageTagWidth = ($messageTags.width())/80;

  
}
