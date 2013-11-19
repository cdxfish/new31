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
                    'background-position': '1px -83px'
                },
                off: {
                    'background-position': '-19px -83px'
                }
            }
            return {
                ul: $this.clone().css({
                    'height': '100%',
                    'overflow': 'hidden',
                    'list-style': 'none'
                }),
                //切换间隔时间
                interv: 5000,
                //切换速速
                speed: 500,
                // 滚动锚点
                site: [],
                // 滚动按钮
                btns: [],
                //焦点轮换图片容器
                warper: $('<div>').css({
                    'height': '100%',
                    'width': '100%',
                    'overflow': 'hidden'
                }),
                //控制焦点按钮容器
                num: $('<center>', {
                    'class': 'num'
                }).css({
                    'position': 'relative',
                    'bottom': '20px'
                }),
                //控制焦点按钮
                button: function() {
                    var self = this;
                    return $('<span>').css({
                        'display': 'inline-block',
                        'background': 'url(/static/shop/images/imgPlayer.png) no-repeat -19px -83px',
                        'margin': '0px 2px',
                        'overflow': 'hidden',
                        'width': '14px',
                        'cursor': 'pointer',
                        'height': '13px'
                    }).hover(function() {
                        $(this).css(css.on);
                    }, function() {
                        if (!$(this).hasClass('on')) {
                            $(this).css(css.off);
                        }
                    }).click(function() {
                        $(this).addClass('on').css(css.on).siblings().removeClass('on').css(css.off);

                        self.ul.animate({
                            "marginLeft": self.site[$(this).index()].width() * $(this).index() * -1
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
                    var i = this.num.find('.on').index() + 1;

                    this.btns[(i == this.site.length) ? 0 : i].click();

                    return this;
                },
                ready: function() {
                    var self = this;
                    self.ul.find('*').css({
                        'float': 'left'
                    });

                    self.ul.css({
                        'width': 3544
                    }).find('li').each(function(i) {
                        self.site.push($(this));
                        self.btns.push(self.button());
                    });

                    self.btns[0].addClass('on').css(css.on);

                    $this.after(self.warper.append(self.ul, self.num.append(self.btns))).hide();

                    return this.start();
                }
            }.ready();
        }
    });


})(jQuery);