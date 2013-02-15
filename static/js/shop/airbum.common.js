// 置顶工具条
$(document).ready(function () {
    // if(jQuery.browser.msie && jQuery.browser.version === "6.0") { }
    // else {
        setInterval(
            function () {
            $(".intro li").eq(Math.floor(Math.random() * 10 / 3)).slideToggle("slow");
        }, 2000);
        $(window).scroll(function () {
                var scrollTop = $("#scrollTop");

                var scrollTopPrevTop = scrollTop.prev().length > 0 ? scrollTop.prev().offset().top  + scrollTop.prev().outerHeight() : 0;

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
                        "padding-top" : "0px"
                    });
                }
        });
    // }

    $(".pinStream a").mouseenter( function () {
        $(this).children('.floatInfo').stop().animate({
            'bottom' : '0px'
        }, 150);
    }).mouseleave( function () {
        $(this).children('.floatInfo').stop().animate({
            'bottom' : '-50px'
        }, 150);
    });
    $(".messageBox").click(function () {
        $(this).toggleClass("on").find(".messagePop").toggle();
        event.stopPropagation();
    });
    backToTopEle();
});


// 返回顶部按钮
function backToTopEle(){
    backToTopEle = $('<a href="javascript:void(0);" class="backToTop" title=\"返回顶部\"></a>').appendTo($("body"))
        .click(function () {
            $("html, body").animate({
                scrollTop : 0
            }, 300, "linear", function () {
                backToTopEle.hide()
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
    })
}


// 隐藏消息层
function hideMessage() {
    $(".messageBox").removeClass("on");
    $(".messagePop").hide();
}