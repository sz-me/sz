
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
	inputWidth = feedWidth-asideWidth-smallPadding*2;
    $("body").width(bodyWidth).css({marginLeft:bodyMargin});
    $("#feed").width(feedWidth).css({marginLeft:marginLeft});
    $("#searchString").height(asideWidth);
    $("#searchStrin>input").height(asideWidth-smallPadding).width(inputWidth).css({paddingLeft:smallPadding});
//     $("aside").css({marginTop:$("header").height()});
    $("textarea").width(feedWidth-0.4*em);
    
    var placeTopHeight = $("header").height() + $("#placeTop").height()+$("#distance").height()+$("#mesPowerString").height()+em*3;
    var mapHeight = $(window).height() - Math.ceil(placeTopHeight);
    $("#map").height(mapHeight);
}