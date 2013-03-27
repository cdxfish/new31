$(document).ready(function() {

    (function() {
        var i = 0;
        addi = function() {
            i++;
        }
        vi = function() {
            return i;
        }

    })()


    getMoreItem();
    pinStream();

});


pinStream = function() {
    $(".pinStream a").live('mouseenter', function() {
        $(this).children('.floatInfo').stop().animate({
            'bottom': '0px'
        }, 150);
    });
    // .live('mouseleave',function () {
    //     $(this).children('.floatInfo').stop().animate({
    //         'bottom' : '-50px'
    //     }, 150);
    // });

}



getMoreItem = function() {
    $(window).scroll(function() {
        var pinStream = $(".pinStream");

        var scrollTop = getScrollTop();
        var winHeight = $(window).height();

        var pinTop = pinStream.offset().top;
        var pinHeight = pinStream.outerHeight();

        if (vi() <= 5) {
            if (scrollTop + winHeight + 600 >= pinTop + pinHeight) {
                $.getJSON('/ajax/moreitem/', function(data) {
                    addi();

                    var appendHtm = '';
                    $.each(data, function(a, c) {
                        $.each(c, function(n, v) {
                            appendHtm += '<div class="' + v.cssClass + '">';
                            appendHtm += '   <a href="/tag/' + v.itemName + '/" target="_blank/" title="' + v.itemName + '">';
                            appendHtm += '       <img src="' + v.img + '" alt="' + v.itemName + '" title="' + v.itemName + '" />';
                            appendHtm += '       <span class="floatInfo">';
                            appendHtm += '           <span class="price">￥ ' + v.amount + '</span>';
                            appendHtm += '           <span class="like_icon">' + v.like + '</span>';
                            appendHtm += '           <span class="name">' + v.itemName + '</span>';
                            appendHtm += '       </span>';
                            appendHtm += '   </a>';
                            appendHtm += '</div>';
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

        } else {
            // alert('done');

        }

    });

}