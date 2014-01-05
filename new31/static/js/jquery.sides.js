/*
 *
 * sides 0.0 - jquery幻灯片插件
 * Version 0.0.1
 * @requires jQuery v1.8.3
 *
 * Copyright (c) 2013 leiddx
 * 自用.
 *
 */
(function($) {
    $.fn.extend({
        sides: function() {
            var $this = $(this);
            var css = {
                on: {
                    'background-color': '#ca3c5b'
                    // 'background-position': '1px -83px'
                },
                off: {
                    'background-color': '#8d8d8d'
                    // 'background-position': '-19px -83px'
                }
            }
            return {
                ul: $this.clone().css({
                    'height': '100%',
                    'overflow': 'hidden',
                    'list-style': 'none'
                }).show(),
                // 切换间隔时间
                interv: 5000,
                // 切换速速
                speed: 500,
                // 切换计时ID
                t: 0,
                // 滚动锚点
                site: [],
                // 滚动按钮
                btns: [],
                // 焦点轮换图片容器
                warper: $('<div>').css({
                    'height': '100%',
                    'width': '100%',
                    'overflow': 'hidden'
                }),
                // 控制焦点按钮容器
                num: $('<center>', {
                    'class': 'num'
                }).css({
                    'position': 'relative',
                    'bottom': '20px'
                }),
                // 控制焦点按钮
                button: function() {
                    var self = this;
                    return $('<span>').css({
                        'display': 'inline-block',
                        // 'background': 'url(/static/shop/images/imgPlayer.png) no-repeat -19px -83px',
                        'background-color': '#8d8d8d',
                        'margin': '0px 2px',
                        'overflow': 'hidden',
                        'width': '12px',
                        'height': '12px',
                        'cursor': 'pointer',
                        'border-radius': '20px'
                    }).hover(function() {
                        $(this).css(css.on);
                        self.stop();
                    }, function() {
                        if (!$(this).hasClass('on')) {
                            $(this).css(css.off);
                        }
                        self.start();
                    }).click(function() {
                        $(this).addClass('on').css(css.on).siblings().removeClass('on').css(css.off);
                        // 不要问我为什么不用index, 都是傻逼ie6
                        var index = $(this).prevAll('span').length;
                        var width = 0;

                        for (var i = 0; i < index; i++) {
                            width += self.site[i].width();
                        };

                        self.ul.animate({
                            "marginLeft": -width
                        }, self.speed);
                    });
                },
                start: function() {
                    var self = this;
                    this.t = setInterval(function() {
                        self.roll()
                    }, this.interv)
                },
                stop: function() {
                    if (this.t) {
                        clearInterval(this.t);
                    }
                },
                roll: function() {
                    // 不要问我为什么不用index, 都是傻逼ie6
                    var i = this.num.find('.on').prevAll('span').length + 1;

                    this.btns[(i == this.site.length) ? 0 : i].click();

                    return this;
                },
                ready: function() {
                    var self = this;
                    self.ul.find('*').css({
                        'float': 'left'
                    });

                    self.ul.find('li').each(function(i) {
                        self.site.push($(this));
                        self.btns.push(self.button());
                    });

                    self.btns[0].addClass('on').css(css.on);

                    $this.after(self.warper.append(self.ul, self.num.append(self.btns))).hide();

                    self.ul.css({
                        'width': self.ul.width() * self.site.length
                    })

                    return this.start();
                }
            }.ready();
        }
    });


})(jQuery);