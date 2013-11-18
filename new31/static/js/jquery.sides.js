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
            return {
                id: $(this),
                num: $('<center>', {
                    'class': 'num'
                }).css({
                    'position': 'relative',
                    'bottom': '20px'
                }),
                ready: function() {
                    var self = this;
                    self.id.css({
                        'height': '100%',
                        'overflow': 'hidden',
                        'list-style': 'none'
                    }).show().find('li').each(function() {
                        var li = $(this);
                        self.num.append(
                        $('<span>').css({
                            'display': 'inline-block',
                            'background': 'url(/static/shop/images/imgPlayer.png) no-repeat -19px -83px',
                            'margin': '0px 2px',
                            'overflow': 'hidden',
                            'width': '14px',
                            'cursor': 'pointer',
                            'height': '13px'
                        }).hover(function() {
                            li.css({
                                'background-position': '1px -83px'
                            });

                        }, function() {
                            li.css({
                                'background-position': '-19px -83px'
                            });
                        }));

                        li.css({
                            'float': 'left'
                        }).find('a').css({
                            'float': 'left'
                        });
                    });
                    return this;
                }
            }.ready();
        }
    });


})(jQuery);