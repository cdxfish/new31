/*
 *
 * debug 0.0 - jquery消息提示
 * Version 0.0.1
 * @requires jQuery v1.8.3
 *
 * Copyright (c) 2013 leiddx
 * 自用.
 *
 */
(function($) {

    $.debug = function() {

        var debug = {
            id: '#debug',
            css: {
                wrapper: {
                    'position': 'fixed',
                    'display': 'none',
                    'left': 0,
                    'bottom': '24px',
                    'width': 'auto',
                    'text-align': 'left',
                    'z-index': 10,
                    'margin': 0,
                    'padding': 0
                },
                item: {
                    'width': 'auto',
                    'height': 'auto',
                    'line-height': '24px',
                    'display': 'table',
                    'position': 'relative',
                    'color': '#FFF',
                    'background-color': '#34495E',
                    'padding': '0 8px 0 0px',
                    'margin': '0 0 8px 0',
                    'border-left': '5px solid #2C3E50',
                    'border-radius': '1px',
                    'z-index': 11,
                    'font-size': '12px',
                    'font-weight': 'bold',
                    'font-family': '"Microsoft YaHei", "微软雅黑", tahoma, arial, simsun, "宋体"',
                    'white-space': 'pre-wrap',
                    'word-break': 'break-all',
                    'box-shadow': '0 1px 3px rgba(0, 0, 0, 0.3)',
                    'left': '0px',
                    'opacity': 1
                },
                warning: {
                    'background-color': '#E67E22',
                    'border-color': '#D35400'
                },
                error: {
                    'background-color': '#E74C3C',
                    'border-color': '#C0392B'
                },
                success: {
                    'background-color': '#2ECC71',
                    'border-color': '#27AE60'
                },
                info: {
                    'background-color': '#3498db',
                    'border-color': '#2980B9'
                },
                debug: {
                    'background-color': '#9B59B6',
                    'border-color': '#8E44AD'
                },
                ico: {
                    'display': 'inline-block',
                    '*zoom': 1,
                    'position': 'relative',
                    'width': '14px',
                    '_width': 'auto',
                    'height': '14px',
                    'line-height': 1,
                    '_height': '16px',
                    '_line-height': '16px',
                    'vertical-align': 'text-top',
                    'background-image': 'url(/static/images/icon.png)',
                    '_background-image': 'none',
                    'background-position': '14px 14px',
                    'background-repeat': 'no-repeat',
                    'margin-right': '4px',
                    '*margin-right': '.3em',
                    '_margin-right': 0,
                    'overflow': 'hidden',
                    'color': '#999',
                    'font-style': 'normal',
                    'font-size': 0,
                    '_font-size': '10px'
                }

            },
            warning: function(text, func) {
                return this.show(this.css.warning, text, func);
            },
            error: function(text, func) {
                return this.show(this.css.error, text, func);
            },
            success: function(text, func) {
                return this.show(this.css.success, text, func);
            },
            info: function(text, func) {
                return this.show(this.css.info, text, func);
            },
            debug: function(text, func) {
                return this.show(this.css.debug, text, func);
            },
            show: function(css, text, func) {
                var item = $('<p>').text(text).css($.extend(this.css.item, css));
                var wrapper = $(this.id).append(item).show();
                var w = item.width();

                item.one('mouseover', function() {
                    $(this).remove();

                    window.clearTimeout(wrapper.data().timer);

                    wrapper.data().timer = window.setTimeout(function() {
                        if (!wrapper.find('p').length) {
                            wrapper.hide();
                        }
                    }, 200);

                }).animate({
                    left: 0,
                    opacity: 1
                }, 200).delay(600000).animate({
                    left: -w,
                    opacity: 0
                }, 200, function() {
                    $(this).mouseover()
                });

                if ( !! func) {
                    func();
                }

                return this;
            },
            ready: function() {
                var self = this;
                $(document).ready(function() {

                    $('body').append($('<div>').attr('id', self.id.slice(1)).css(self.css.wrapper).hide());
                    setInterval(function() {
                        $.getJSON('/message/get/', function(data) {
                            if (data.err) {
                                self.error(data.msg);
                            } else {
                                var read = [];
                                $.each(data.data, function(i, v) {
                                    self[v.typ](v.time + '： ' + v.data)
                                    read.push(v.id);
                                })

                                if (read.length) {

                                    $.getJSON('/message/read/', {
                                        id: read
                                    }, function(data) {
                                        if (data.err) {
                                            self.error(data.msg);
                                        }
                                    })
                                }
                            }
                        });

                    }, 6000);

                });
                return self;
            }
        }
        var debug = debug.ready();
        debug.w = debug.warning;
        debug.e = debug.error;
        debug.s = debug.success;
        debug.i = debug.info;
        debug.d = debug.debug;

        return debug;

    }();

    $.d = $.debug;

})(jQuery);