// 置顶工具条
$(document).ready(function () {
    if ($(window).height() > $('body').height()) {
        var content = $('#content');
        var conHeight = $(window).height() - content.prev().offset().top - content.prev().outerHeight() - content.next().outerHeight() - content.outerHeight() + content.height();
        // content.css({
            // 'min-height' : conHeight,
            // 'height' : conHeight
        // });
        if (jQuery.browser.msie && jQuery.browser.version === "6.0") {
            content.css({
                'height' : conHeight
            });
        } else {
            content.css({
                'min-height' : conHeight
            });
        }
    }
    if (jQuery.browser.msie && jQuery.browser.version === "6.0") {}
    else {
        setInterval(
            function () {
            var introLi = $(".intro li");
            introLi.eq(Math.floor(Math.random() * 10 % introLi.length)).slideToggle("slow");
        }, 2000);

        varI();

        $(window).scroll(function () {

            var scrollTop = $("#scrollTop");

            var scrollTopPrevTop = scrollTop.prev().length > 0 ? scrollTop.prev().offset().top + scrollTop.prev().outerHeight() : 0;

            if ($(window).scrollTop() >= scrollTopPrevTop) {

                var windowWidth = $(window).width();

                windowWidth < 928 && $(".intro").hide();

                var scrollTopWidth = windowWidth < 928 ? windowWidth - 20 : "928px";
                var scrollTopLeft = windowWidth - scrollTop.outerWidth() >= 0 ? (windowWidth - scrollTop.outerWidth()) / 2 : 0;

                scrollTop.css({
                    "width" : scrollTopWidth,
                    "position" : "fixed",
                    "top" : "0",
                    "left" : scrollTopLeft
                }).next("div:first").css({
                    "padding-top" : scrollTop.outerHeight()
                });

            } else {
                $(".intro").show();
                scrollTop.css({
                    "width" : "928px",
                    "position" : "relative",
                    "left" : "0px"
                }).next().css({
                    "padding-top" : "30px"
                });
            }
            GetMoreItem();
        });
    }

    $(".pinStream a").live('mouseenter',function () {
        $(this).children('.floatInfo').stop().animate({
            'bottom' : '0px'
        }, 150);
    });
    // .live('mouseleave',function () {
    //     $(this).children('.floatInfo').stop().animate({
    //         'bottom' : '-50px'
    //     }, 150);
    // });
    
    $("#lnkTopMessage, #lnkTopSetting, #lnkTopLogin").click(function () {
        $(this).toggleClass("on").next(".messagePop").toggle();
        return false;
        // event.stopPropagation();
    });
    backToTopEle();
});

// 返回顶部按钮
function backToTopEle() {
    var backToTopEle = $('<a href="javascript:void(0);" class="backToTop" title=\"返回顶部\"></a>').appendTo($("body"))
        .click(function () {
            $("html, body").animate({
                scrollTop : 0
            }, 300, "linear", function () {
                backToTopEle.hide();
            });
        });
    $(window).scroll(function () {
        var st = $(document).scrollTop();
        var winh = $(window).height();
        (st > 0) ? backToTopEle.show() : backToTopEle.hide();
        //IE6下的定位
        if (!window.XMLHttpRequest) {
            backToTopEle.css("top", st + winh - 80);
        }
    });
}

//将所有新消息数擦除
function clearMessageData() {
    $.post(URL_AJAX_GET_CLEAR_MESSAGE, function (result) {
        if (result.Success) {
            hideMessage();
        } else {
            alert(result.Message);
            return false;
        }
    });
}

// 隐藏消息层
function hideMessage() {
    $(".messageBox").removeClass("on");
    $(".messagePop").hide();
}

var w3c = (document.getElementById) ? true : false;
var agt = navigator.userAgent.toLowerCase();
var ie = ((agt.indexOf("msie") != -1) && (agt.indexOf("opera") == -1) && (agt.indexOf("omniweb") == -1));

function IeTrueBody() {
    return (document.compatMode && document.compatMode != "BackCompat") ? document.documentElement : document.body;
}

function GetScrollTop() {
    return ie ? IeTrueBody().scrollTop : window.pageYOffset;
}

function GetScrollLeft() {
    return ie ? IeTrueBody().scrollLeft : window.pageXOffset;
}

function GetMoreItem() {
    var pinStream = $(".pinStream");

    var scrollTop = GetScrollTop();
    var winHeight = $(window).height();

    var pinTop = pinStream.offset().top;
    var pinHeight = pinStream.outerHeight();

    if(count() <= 5)
    {
        if (scrollTop + winHeight + 600 >= pinTop + pinHeight) {
            $.getJSON('/ajax/more/', function(data) {
                iAdd();

                var appendHtm = '';
                $.each(data,function(a,c){
                    $.each(c,function(n,v){
                        appendHtm +=        '<div class="'+ v.class+'">';
                        appendHtm +=        '   <a href="/tag/'+v.sn+'/" target="_blank/" title="'+v.name+'">';
                        appendHtm +=        '       <img src="'+v.img+'" alt="'+v.name+'" title="'+v.name+'" />';
                        appendHtm +=        '       <span class="floatInfo">';
                        appendHtm +=        '           <span class="price">￥ '+v.amount+'</span>';
                        appendHtm +=        '           <span class="like_icon">'+v.like+'</span>';
                        appendHtm +=        '           <span class="name">'+v.name+'</span>';
                        appendHtm +=        '       </span>';
                        appendHtm +=        '   </a>';
                        appendHtm +=        '</div>';
                    });

                });

                pinStream.append(appendHtm);

            });
            pinStream.ajaxStart(function() {
                $(this).append("<div class=\"moreLoading\"><span class=\"loading_black\"></span>努力加载中...</div>");
            }).ajaxSuccess(function() {
                $(".moreLoading").remove();
            });
        }

    }
    else
    {
        // alert('done');

    }

}

function varI() {
    var i = 0;
    iAdd = function() {
        i++;
    }
    count = function(){
        return i        
    }

}