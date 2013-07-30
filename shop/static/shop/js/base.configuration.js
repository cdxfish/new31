$(document).ready(function() {
    b.autoHight().intro().topToolsMessage().backToTopEle();

    if (jQuery.browser.msie && jQuery.browser.version === "6.0") {} else {
        b.scrollTop();
    }

    $('.date').Zebra_DatePicker({
        direction: true
    }); //日期选择控件

    $('select').jgdDropdown({
        clsLIExpand: false
        // selected: 'RS'
    });

});

var b = {

    scrollTop: function() {
        $(window).scroll(function() {

            var scrollTop = $("#scrollTop");
            var bar = $('#scrollTop .bar');

            var scrollTopPrevTop = scrollTop.prev().length > 0 ? scrollTop.prev().offset().top + scrollTop.prev().outerHeight() : 0;

            if ($(window).scrollTop() >= scrollTopPrevTop) {

                var windowWidth = $(window).width();

                windowWidth < 928 && $(".intro").hide();

                var barWidth = windowWidth < 928 ? windowWidth - 20 : "928px";
                var barLeft = windowWidth - bar.outerWidth() >= 0 ? (windowWidth - bar.outerWidth()) / 2 : 0;

                bar.css({
                    "width": barWidth,
                    "position": "fixed",
                    "top": "0",
                    "left": barLeft
                })

            } else {

                bar.css({
                    "width": "928px",
                    "position": "relative",
                    "left": "0px"
                })
            }
        });

        return this

    },


    intro: function() {
        $(".intro").show();
        setInterval(

        function() {
            var introLi = $(".intro li");
            introLi.eq(Math.floor(Math.random() * 10 % introLi.length)).slideToggle("slow");
        }, 2000);
        return this
    },


    autoHight: function() {
        if ($(window).height() > $('body').height()) {
            var content = $('#content');
            var conHeight = $(window).height() - content.prev().offset().top - content.prev().outerHeight() - content.next().outerHeight() - content.outerHeight() + content.height();
            if (jQuery.browser.msie && jQuery.browser.version === "6.0") {
                content.css({
                    'height': conHeight
                });
            } else {
                content.css({
                    'min-height': conHeight
                });
            }
        }

        return this
    },

    topToolsMessage: function() {
        $("#lnkTopMessage, #lnkTopSetting, #lnkTopLogin").click(function() {
            $(this).toggleClass("on").next(".messagePop").toggle();
            return false;
            // event.stopPropagation();
        });

        return this
    },

    // 返回顶部按钮
    backToTopEle: function() {
        var backToTopEle = $('<a href="javascript:void(0);" class="backToTop" title=\"返回顶部\"></a>').appendTo($("body")).click(function() {
            $("html, body").animate({
                scrollTop: 0
            }, 300, "linear", function() {
                backToTopEle.hide();
            });
        });
        $(window).scroll(function() {
            var st = $(document).scrollTop();
            var winh = $(window).height();
            (st > 0) ? backToTopEle.show() : backToTopEle.hide();
            //IE6下的定位
            if (!window.XMLHttpRequest) {
                backToTopEle.css("top", st + winh - 80);
            }
        });

        return this
    },

    //将所有新消息数擦除
    clearMessageData: function() {
        $.post(URL_AJAX_GET_CLEAR_MESSAGE, function(result) {
            if (result.Success) {
                hideMessage();
            } else {
                alert(result.Message);
                return false;
            }
        });
    },

    // 隐藏消息层
    hideMessage: function() {
        $(".messageBox").removeClass("on");
        $(".messagePop").hide();

        return this
    },
    chng: function(obj, url) {
        obj.change(

        function() {
            var self = $(this);
            self.ajaxGET(url + '?' + $(this).attr('name') + '=' + $(this).val());


        });
        return this;
    }

}


var w3c = (document.getElementById) ? true : false;
var agt = navigator.userAgent.toLowerCase();
var ie = ((agt.indexOf("msie") != -1) && (agt.indexOf("opera") == -1) && (agt.indexOf("omniweb") == -1));

ieTrueBody = function() {
    return (document.compatMode && document.compatMode != "BackCompat") ? document.documentElement : document.body;
}

getScrollTop = function() {
    return ie ? ieTrueBody().scrollTop : window.pageYOffset;
}

getScrollLeft = function() {
    return ie ? ieTrueBody().scrollLeft : window.pageXOffset;
}