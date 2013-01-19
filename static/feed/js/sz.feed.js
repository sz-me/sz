
function cityView(data){
    if (data.data.length == 1)
        {
        var $value = data.data[0],city=$value.name,cityID = $value.geoname_id;
        $.cookie("shmotCity", city);
        $.cookie("shmotCityID", cityID);
        }
    if (data.meta.code == 403)
        {document.location = '/api-auth/login/?next={% url feed-index %}'}
}


function getPosition(params){
    $("#messageArea").empty();
    $("#messageArea").text('Loading...');
    var latitude = $.cookie("shmotLatitude")*1;
    var nearby = $('#nearby').attr('class')
    if(latitude&&$.isEmptyObject(nearby)){
        var longitude = $.cookie("shmotLongitude")*1;
        params.latitude = latitude;
        params.longitude = longitude;
        getFeed(params,nearby);
        }
    else{
        navigator.geolocation.getCurrentPosition(function(data) {
            var latitude = data.coords.latitude;
            var longitude = data.coords.longitude;
            $.cookie("shmotLatitude",latitude);
            $.cookie("shmotLongitude",longitude);
            params.latitude = latitude;
            params.longitude = longitude;
            getFeed(params,nearby);
            });
        }
}

function getFeed(params,nearby){
    $("#messageArea").text('Loading...');
    
    if(nearby){params.nearby=''}
    szApi.get('places/',
            params,
            function(response){ 
                if(response.meta.code==200){placesView(response);}
                else{
                    if(response.meta.code!=403){$("#messageArea").text(response.data.detail)
            }
                }
            });
    var city = $.cookie("shmotCity");
    var cityID = $.cookie("shmotCityID");
    if(city){$("#city").text(city)}
    else{
        szApi.get('cities/',
            {latitude: params.latitude,longitude: params.longitude},
            function(response){ cityView(response);});
        }
};




function pageUp(){

var $pageUp = $("#pageUp");
	    var	speed = 500;
	    $pageUp.click(function(){
		    $("html:not(:animated)" +( !$.browser.opera ? ",body:not(:animated)" : "")).animate({ scrollTop: 0}, 500 );
		    return false;
	    });
	    function show_scrollTop(){
		    ( $(window).scrollTop()>50 ) ? $pageUp.fadeIn(600) : $pageUp.hide();
	    }
	    $(window).scroll( function(){show_scrollTop()} ); show_scrollTop();	    
}

function pageSize(){
    var winWidth = $(window).width();
    $("body").css({fontSize:'1em'});
    var f = $("body").css('fontSize'),
	em = f.slice(0,f.length-2)*1,
	smallPadding = 0.2*em,
	normalPadding = 0.4*em,
	asideWidth = $("aside>a").width();
    //desktop
    if (winWidth>800){
	var feedMarginR = 0;
	if(winWidth>1200){
	    var bodyWidth = winWidth*0.4;
	}
	if(1000<winWidth&&winWidth<1199){
	    var bodyWidth = winWidth*0.5;
	}
	if(winWidth&&winWidth<999){
	    var bodyWidth = winWidth*0.6;
	}
    }
    else{
	var feedMarginR = em*2,
	    bodyWidth = winWidth-feedMarginR;
// 	//phone horizontal
// 	if(570<winWidth&&winWidth<799){}
// 	//phone vertical
// 	if(410<winWidth&&winWidth<569){}
// 	//small screen
// 	if(winWidth<409){}
    }
    var bodyMargin = (winWidth-bodyWidth)*0.5,
	marginLeft = asideWidth+em,
	feedWidth = bodyWidth-marginLeft-feedMarginR,
	inputWidth = feedWidth-asideWidth-smallPadding*2,
        menuWidth = em*15,
        menuMargin = (bodyWidth-menuWidth)*0.5;
    if (menuWidth>feedWidth){var menuWidth=bodyWidth,menuMargin=0;}
    var menuPaddding = (menuWidth-2*em-3*1.05*em)*0.5
    $("body").width(bodyWidth).css({marginLeft:bodyMargin});
    $("#feed").width(feedWidth).css({marginLeft:marginLeft});
    $("#menu").width(menuWidth).css({marginLeft:menuMargin,borderRadius:menuWidth,paddingTop:menuPaddding,paddingBottom:menuPaddding-em});;
    $("#searchString").height(asideWidth);
    $("#searchStrin>input").height(asideWidth-smallPadding).width(inputWidth).css({paddingLeft:smallPadding});
//     $("aside").css({marginTop:$("header").height()});
    $("textarea").width(feedWidth-0.4*em);
    
    var placeTopHeight = $("header").height() + $("#placeTop").height()+$("#distance").height()+$("#mesPowerString").height()+em*3;
    var mapHeight = $(window).height() - Math.ceil(placeTopHeight);
    $("#map").height(mapHeight);
}