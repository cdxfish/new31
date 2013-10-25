$(document).ready(function() {

    shop.getMoreItem(5).pinStream();

});

var shop = {
    plus: function() {
        var self = arguments.callee;
        if ( !! !self.i) {
            self.i = 0;
        }
        self.i++;
        return self;
    },
    speedLimit: (function(t) {

        return (function() {
            var self = arguments.callee;
            self.i = false;
            setTimeout(function() {
                self.i = true
            }, t);

            return self;
        })()

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
                if (self.plus().i < num && self.speedLimit.i) {
                    self.speedLimit()
                    self.ajaxGetItems(pinStream);
                }

            }

        });

        return this;

    },
    ajaxGetItems: function(obj) {
        var self = this;

        var load = $('<div class=\"moreLoading\"><span class=\"loading_black\"></span>努力加载中...</div>');

        $.ajax({
            type: 'GET',
            url: '/shop/itemmore/',
            dataType: 'json',
            success: function(data) {
                if (data.typ == 'error') {
                    $.dialog.msg('加载出错，请稍候再试');
                } else {
                    var appendHtm = '';

                    $.each(data.data, function(i, v) {
                        appendHtm += '<div class="styp' + v.typ + '">';
                        appendHtm += '   <a href="/tag/' + v.name + '/" target="_blank/" title="' + v.name + '">';
                        appendHtm += '       <img src="' + v.src + '" alt="' + v.name + '" title="' + v.name + '" class="b' + v.typ + '" />';
                        appendHtm += '       <span class="floatInfo">';
                        appendHtm += '           <span class="price">' + v.fee + '</span>';
                        appendHtm += '           <span class="like_icon">' + v.like + '</span>';
                        appendHtm += '           <span class="name">' + v.name + '</span>';
                        appendHtm += '       </span>';
                        appendHtm += '   </a>';
                        appendHtm += '</div>';
                    });

                    obj.append(appendHtm);

                    self.plus();
                }

            },
            beforeSend: function() {
                obj.append(load);
            },
            error: function() {
                $.dialog.msg('加载出错，请稍候再试');

            },
            complete: function() {
                load.remove();
            }
        });

        return this;

    },
    pinStream: function() {
        $('.pinStream img').each(function() {
            $(this).attr('src', $(this).attr('data-src')).attr('height', $(this).height()).attr('width', $(this).width());
        })
        $(".pinStream").on('mouseenter', 'a', function() {
            $(this).children('.floatInfo').stop().animate({
                'bottom': '0px'
            }, 150);
        })
        // .on('mouseleave', 'a', function () {
        //     $(this).children('.floatInfo').stop().animate({
        //         'bottom' : '-50px'
        //     }, 3000);
        // });
        return this;
    }

}