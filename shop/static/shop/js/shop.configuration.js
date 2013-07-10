$(document).ready(function() {

    shop.getMoreItem().pinStream();

});

var shop = {
    vi: (function() {
        var i = 0;
        this.addi = function() {
            i++;
        }

        return function() {
            return i;
        }
    })(),
    getMoreItem: function() {
        var self = this;

        $(window).scroll(function() {
            var pinStream = $(".pinStream");

            var scrollTop = getScrollTop();
            var winHeight = $(window).height();

            var pinTop = pinStream.offset().top;
            var pinHeight = pinStream.outerHeight();


            if (self.vi() <= 5) {
                if (scrollTop + winHeight + 600 >= pinTop + pinHeight) {
                    $.getJSON('/ajax/itemmore/', function(data) {
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

            }

        });

        return this;
    },


    pinStream: function() {
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

        return this;
    }

}