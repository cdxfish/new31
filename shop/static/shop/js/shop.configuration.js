$(document).ready(function() {

    shop.getMoreItem(5).pinStream();

});

var shop = {
    count: (function() {
        var i = 0;
        this.plusi = function() {
            i++;
        }

        return function() {
            return i;
        }
    })(),
    speedLimit: (function(t) {
        var i = true;
        this.timeSwitch = function() {
            return i
        }
        return function() {
            i = false;
            setTimeout(function() {
                i = true
            }, t);
        }

    })(2000),
    getMoreItem: function(num) {
        var self = this;

        $(window).scroll(function() {
            var pinStream = $(".pinStream");

            var scrollTop = getScrollTop();
            var winHeight = $(window).height();

            var pinTop = pinStream.offset().top;
            var pinHeight = pinStream.outerHeight();

            if (scrollTop + winHeight + 600 >= pinTop + pinHeight) {
                if (self.count() < num && timeSwitch()) {
                    self.speedLimit()
                    self.ajaxGetItems(pinStream);
                }

            }

        });

        return this;

    },
    ajaxGetItems: function(obj) {
        if (!$(".moreLoading").length) {
            obj.append("<div class=\"moreLoading\" style=\"display:none;\"><span class=\"loading_black\"></span>努力加载中...</div>");
        }

        var load = $(".moreLoading");
        obj.ajaxStart(function() {
            load.show()
        }).ajaxSuccess(function() {
            load.remove();
        });

        $.getJSON('/ajax/itemmore/', function(data) {

            if (data.err) {
                alert(data.msg);
            } else {
                var appendHtm = '';

                $.each(data.data, function(i, v) {
                    appendHtm += '<div class="s' + v.width + '">';
                    appendHtm += '   <a href="/tag/' + v.name + '/" target="_blank/" title="' + v.name + '">';
                    appendHtm += '       <img src="' + v.src + '" alt="' + v.name + '" title="' + v.name + '" />';
                    appendHtm += '       <span class="floatInfo">';
                    appendHtm += '           <span class="price">' + v.fee + '</span>';
                    appendHtm += '           <span class="like_icon">' + v.like + '</span>';
                    appendHtm += '           <span class="name">' + v.name + '</span>';
                    appendHtm += '       </span>';
                    appendHtm += '   </a>';
                    appendHtm += '</div>';
                });

                obj.append(appendHtm);

                plusi();
            }

        });

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