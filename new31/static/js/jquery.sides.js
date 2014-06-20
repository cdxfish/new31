/*
 *
 * sides 0.1 - jquery幻灯片插件
 * Version 0.1.4
 * @requires jQuery v1.8.3
 *
 * Copyright (c) 2013 leiddx
 * 自用.
 *
 * v0.1.2 修正无图片情况下roll方法失效bug
 * v0.1.4 兼容IE6+
 *        改进滚动视觉效果
 *
 */
(function($) {
    $.fn.extend({
        sides: function() {
            var $this = $(this);
            var css = {
                on: {
                    'background-color': '#ca3c5b'
                },
                off: {
                    'background-color': '#8d8d8d'
                }
            }
            return {
                ul: $('ul', $this).css({
                    'height': '100%',
                    'list-style': 'none',
                    'margin': 0,
                    'padding': 0,
                    'position': 'relative'
                }).show(),
                // 切换间隔时间
                interv: 5000,
                // 切换速速
                speed: 500,
                // 切换计时ID
                t: 0,
                // 滚动锚点
                seg: 0,
                // 滚动表
                site: [],
                // 滚动按钮
                btns: [],
                // 滚动按钮高亮锚点
                odd: 0,
                // 焦点轮换图片容器
                warper: $('<div>').css({
                    'height': '100%',
                    'width': '100%',
                    'overflow': 'hidden'
                    // 'float': 'left'
                }),
                // 控制焦点按钮容器
                num: $('<div>', {
                    'class': 'num'
                }).css({
                    'position': 'relative',
                    'text-align': 'center',
                    'bottom': '1.5em',
                    'z-index': 999
                }),
                // 控制焦点按钮
                button: function() {
                    var self = this;
                    return $('<span>').css({
                        'display': 'inline-block',
                        'background-color': '#8d8d8d',
                        'margin': '0px 0.2em',
                        'overflow': 'hidden',
                        'width': '0.875em',
                        'height': '0.875em',
                        'cursor': 'pointer',
                        'border-radius': '1.5em'
                    }).hover(function() {
                        $(this).css(css.on);
                        self.stop();
                    }, function() {
                        var $_this = $(this);
                        if (!$_this.hasClass('on')) {
                            $_this.css(css.off);
                        }
                        self.start();
                    }).click(function() {
                        var $_this = $(this);
                        $_this.addClass('on').css(css.on).siblings().removeClass('on').css(css.off);
                        // 不要问我为什么不用index, 都是傻逼ie6
                        var index = $_this.prevAll('span').length;

                        var seg = self.site[index].seg;

                        if (!index && self.odd + 2 == self.site.length) {
                            seg = self.site[self.odd + 1].seg;

                        }
                        var w = (self.site[index].width() - $this.width()) / 2;

                        seg += w > 0 ? w : 0;

                        self.ul.animate({
                            'left': -seg
                        }, self.speed, function() {
                            $(this).css({
                                'left': -self.site[index].seg - w
                            });
                        });

                        self.odd = index;
                    });
                },
                start: function() {
                    var self = this;

                    this.t = setInterval(function() {
                        self.roll()
                    }, this.interv);
                },
                stop: function() {
                    if (this.t) {
                        clearInterval(this.t);
                    }
                },
                roll: function() {

                    this.btns.length && this.btns[(this.odd == this.btns.length - 1) ? 0 : this.odd + 1].click();

                    return this;
                },
                ready: function() {
                    var self = this;
                    self.ul.append(self.ul.find('li:first').clone()).wrap(self.warper);

                    var width = 0;
                    self.ul.find('li').css({
                        'float': 'left',
                        'height': '100%'
                    }).hover(function() {
                        self.stop();
                    }, function() {
                        self.start();
                    }).each(function(i) {
                        var $_this = $(this);
                        $_this.seg = width;

                        width += $(this).width();

                        self.site.push($_this);
                        self.btns.push(self.button());
                    });

                    self.ul.css({
                        'width': width
                    }).find('img').css({
                        'border': 0
                    });

                    // 弹出最后按钮
                    self.btns.pop();

                    $this.append(self.num.append(self.btns));

                    self.btns[0].click();

                    return this.start();
                }
            }.ready();
        }
    });
})(jQuery);
