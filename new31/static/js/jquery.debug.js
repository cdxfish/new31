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
    $('body').append('<div id="area-info" style="display: block;"></div><div id="area-window" style="display: block;"></div>');

    $.fn.hoverInfo = function(param, callback) {
        var func = {
            name: '$.fn.hoverInfo()'
        };
        return this.each(function() {
            $(this).off('.hoverInfo').on('mouseenter.hoverInfo', function() {
                $(this).info(param, callback)
            }).on('mouseleave.hoverInfo', function() {
                $('#win-hint').click()
            })
        })
    };
    $.info = function(para, callback) {
        var func = {
            name: '$.info()',
            token: 'mimiko',
            text: '',
            type: 'default',
            display: 'default',
            ul: 10,
            callback: callback,
            debug: true,
            timer: {
                hintFadeOut: 1000
            }
        };
        if ( !! para) {
            if ($.type(para) == 'string') {
                if (para.search(/\:\:/) == -1) {
                    func.text = $.trim(para)
                } else {
                    var a = para.split('::');
                    func.text = a[1];
                    func.type = $.trim(a[0])
                }
            } else if ($.type(para) == 'object') {
                if ( !! para.token) {
                    $.extend(func, para)
                } else {
                    func.text = $.parseString(para)
                }
            } else if ($.type(para) == 'array') {
                func.text = para.join(', ')
            } else if ($.type(para) == 'number') {
                func.text = para.toString()
            } else if ($.type(para) == 'boolean') {
                func.text = 'true'
            } else {
                $.info('debug::[' + func.name + ']非法的信息格式。')
            }
        } else {
            if ($.type(para) == 'boolean') {
                func.text = 'false'
            } else if ($.type(para) == 'number') {
                func.text = '0'
            } else if ($.type(para) == 'undefined') {
                func.text = 'undefined'
            } else {
                func.text = 'null'
            }
        };
        if ( !! func.text) {
            if (func.type != 'debug' || (func.type == 'debug' && func.debug == 1)) {
                var area = $('#area-info');
                var type = func.type == 'default' ? '' : func.type.slice(0, 1).toUpperCase() + func.type.slice(1) + ': ';
                var icon = '';
                switch (func.type) {
                case 'debug':
                    icon = '<i class="icon white icon-comment"></i>';
                    break;
                case 'error':
                    icon = '<i class="icon white icon-exclamation-sign"></i>';
                    break;
                case 'info':
                    icon = '<i class="icon white icon-info-sign"></i>';
                    break;
                case 'success':
                    icon = '<i class="icon white icon-ok-circle"></i>';
                    break;
                case 'warning':
                    icon = '<i class="icon white icon-warning-sign"></i>';
                    break;
                default:
                    icon = '<i class="icon white icon-chevron-right"></i>';
                    break
                };
                area.css({
                    display: 'block'
                }).append('<p class="item ' + func.type + '">' + icon + (func.debug ? type : '') + func.text + '</p>');
                var objs = area.children('p');
                var info = objs.last();
                if (objs.length > func.ul) {
                    objs.first().mouseover()
                };
                var w = info.width();

                info.css({
                    left: -w,
                    opacity: 0
                }).animate({
                    left: 0,
                    opacity: 1
                }, 200, function() {
                    info.delay(10000).animate({
                        left: -w,
                        opacity: 0
                    }, 200, function() {
                        info.mouseover()
                    });
                    if ($.isFunction(func.callback)) {
                        func.callback()
                    }
                });
                if (func.display == 'default') {
                    info.one('mouseover', function() {
                        info.remove();
                        window.clearTimeout(area.data().timer);
                        area.data().timer = window.setTimeout(function() {
                            if (!area.find('p').length) {
                                area.css({
                                    display: 'none'
                                })
                            }
                        }, 200)
                    })
                }
            }
        } else {
            $.info('debug::[' + func.name + ']为空的非法信息。')
        }
    };
    $.i = function(param, callback) {
        $.info(param, callback)
    };
    $.fn.info = function(param, callback) {
        var func = {
            name: '$.fn.info()',
            id: 'win-hint',
            type: 'default',
            direction: 'auto',
            text: null,
            cooldown: 5000,
            fadeout: 5000,
            callback: callback
        };
        if (param) {
            if ($.type(param) == 'string') {
                if (param.search('::') == -1) {
                    func.text = param
                } else {
                    func.type = param.replace(/\:\:.+/, '');
                    func.text = param.replace(/.+?\:\:/, '')
                }
            } else if ($.type(param) == 'object') {
                $.extend(func, param);
                func.name = '$.fn.info()';
                if (func.text && func.text.search('::') != -1) {
                    func.type = func.text.replace(/\:\:.+/, '');
                    func.text = func.text.replace(/.+?\:\:/, '')
                }
            } else if ($.isFunction(param)) {
                func.text = null;
                func.callback = param
            } else {
                $.info('debug::' + func.name + '错误类型的非法参数。')
            }
        } else {
            func.text = null
        };
        return this.each(function() {
            var obj = $(this);
            if (!func.text) {
                if (obj.attr('title')) {
                    obj.data({
                        title: obj.attr('title')
                    }).removeAttr('title')
                };
                func.text = obj.data().title || null
            };
            if (func.text) {
                if (func.text.substr(func.text.length - 1) == '。') {
                    func.text = func.text.substr(0, func.text.length - 1)
                };
                if (func.id == 'win-hint') {
                    // window.clearTimeout(func.timer.hintFadeOut);
                    window.clearTimeout(1000);
                    var win = $('#win-hint');
                    if (!win.hasClass('win-hint')) {
                        win.addClass('win-hint')
                    };
                    var cs = 'error success info debug warning';
                    win.removeClass(cs)
                } else {
                    var win = $('#' + func.id);
                    if (!win.length) {
                        $('#area-window').append('<div id="' + func.id + '" class="win win-hint"><div class="mainer"></div><div class="tail"></div></div>');
                        var win = $('#' + func.id)
                    }
                };
                var mainer = win.find('div.mainer');
                var tail = win.find('div.tail');
                win.addClass(func.type);
                mainer.html($.trim(func.text));
                var s = {
                    w: win.width(),
                    h: win.height()
                };
                var o = {
                    l: obj.offset().left,
                    t: obj.offset().top,
                    w: obj.width(),
                    h: obj.height()
                };
                var w = {
                    w: $(window).innerWidth(),
                    h: $(window).innerHeight(),
                    t: $(window).scrollTop()
                };
                var getY = function() {
                        if (o.t - s.h - 32 > w.t) {
                            var r = [o.t - s.h - 8, 'top', -4]
                        } else {
                            var r = [o.t + o.h + 8, 'bottom', 4]
                        };
                        return r
                    };
                var getX = function() {
                        if (o.l + s.w < w.w - 16) {
                            var r = [o.l + o.w + 16, 'right', 4]
                        } else {
                            var r = [o.l - s.w - 16, 'left', -4]
                        };
                        return r
                    };
                var cs = 'left right top bottom';
                switch (func.direction) {
                case 'x':
                    var r = getX();
                    var left = r[0],
                        top = o.t,
                        fix = [r[2], 0];
                    tail.removeClass(cs).addClass(r[1]);
                    break;
                case 'y':
                    var r = getY();
                    var left = o.l,
                        top = r[0],
                        fix = [0, r[2]];
                    tail.removeClass(cs).addClass(r[1]);
                    break;
                case 'left':
                    var left = o.l - s.w - 16,
                        top = o.t,
                        fix = [-4, 0];
                    tail.removeClass(cs).addClass('left');
                    break;
                case 'right':
                    var left = o.l + o.w + 16,
                        top = o.t,
                        fix = [4, 0];
                    tail.removeClass(cs).addClass('right');
                    break;
                case 'top':
                    var left = o.l,
                        top = o.t - s.h - 8,
                        fix = [0, -4];
                    tail.removeClass(cs).addClass('top');
                    break;
                case 'bottom':
                    var left = o.l,
                        top = o.t + o.h + 8,
                        fix = [0, 4];
                    tail.removeClass(cs).addClass('bottom');
                    break;
                default:
                    var r = getY();
                    var left = o.l,
                        top = r[0],
                        fix = [0, r[2]];
                    tail.removeClass(cs).addClass(r[1]);
                    break
                };
                win.stop(false, true).css({
                    left: left,
                    top: top,
                    opacity: 0,
                    display: 'block'
                }).animate({
                    left: left + fix[0],
                    top: top + fix[1],
                    opacity: 1
                }, 200, function() {
                    if ($.isFunction(func.callback)) {
                        func.callback()
                    };
                    if (func.id == 'win-hint') {
                        if (func.fadeout && func.fadeout > 0) {
                            func.timer.hintFadeOut = window.setTimeout(function() {
                                win.click()
                            }, func.fadeout)
                        }
                    } else {
                        if (func.fadeout && func.fadeout > 0) {
                            window.setTimeout(function() {
                                win.click()
                            }, func.fadeout)
                        }
                    }
                })
            } else {
                $.info('debug::' + func.name + '为空的非法信息。')
            }
        })
    };
    $.fn.riseInfo = function(param, callback) {
        var func = {
            name: '$.fn.riseInfo()',
            text: '+1',
            callback: callback
        };
        if (param) {
            if ($.type(param) == 'string') {
                func.text = param
            } else if ($.type(param) == 'object') {
                $.extend(param, func);
                func.name = '$.fn.riseInfo()'
            } else {
                $.info('debug::[' + func.name + ']错误类型的非法参数。')
            }
        };
        return this.each(function() {
            var singer = $(this);
            var mid = $.mid();
            $('#area-window').append('<span id="info-' + mid + '-rise" class="info-rise">' + func.text + '</span>');
            var obj = $('#info-' + mid + '-rise');
            var top = singer.offset().top - obj.height();
            obj.css({
                opacity: 0,
                left: singer.offset().left,
                top: top
            }).animate({
                opacity: 1,
                top: top - 16
            }, 250).animate({
                top: top - 20
            }, 500).animate({
                opacity: 0,
                top: top - 32
            }, 250, function() {
                obj.remove()
            })
        })
    }
})(jQuery);