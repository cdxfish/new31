/*
 *
 * dialog 0.0 - jquery弹窗插件
 * Version 1.0.1
 * @requires jQuery v1.8.3
 *
 * Copyright (c) 2013 leiddx
 * 自用.
 *
 */

(function($) {
    $.dialog = function() {
        return {
            body: $('<div>', {
                id: 'dialog'
            }).css({
                'z-index': 999,
                // 'background': 'none transparent scroll repeat 0% 0%',
                'width': '100%',
                'height': '100%',
                'position': 'absolute',
                'left': '0px',
                'top': '0px'
            }),

            maskLayer: $('<div>').css({
                'filter': 'alpha(opacity=75)',
                'width': '100%',
                'height': '100%',
                'background': '#000',
                'opacity': 0.45,
                'overflow': 'hidden'
            }),

            msgBox: $('<div>').css({
                'border-radius': '1px',
                'background': '#FFF',
                'padding': 5,
                'box-shadow': '1px 2px 5px #000',
                'position': 'fixed'
            }),

            interval: [],

            clear: function() {
                for (i in this.interval) {
                    clearTimeout(this.interval[i])
                }

                this.interval = [];

                return this;
            },

            close: function(t) {
                var self = this.clear();

                self.body.hide(function() {
                    self.msgBox.html('');
                });

                return this;
            },

            ready: function() {
                var self = this;

                $(document).ready(function() {
                    self.body.css({
                        'height': $(document).height()
                    }).hide().append(self.maskLayer, self.msgBox).appendTo('body').on('click', '.close', function() {
                        self.close();
                    });
                });

                return this;
            },

            show: function(element) {
                var self = this;

                self.body.show(function() {
                    self.msgBox.empty().append(element);

                    return self.center();
                });

                return this;
            },

            center: function() {
                var self = this;

                var windowHeight = $(window).outerHeight();
                var windowouterWidth = $('body').outerWidth();
                var mOuterHeight = this.msgBox.outerHeight() + 100;
                var mOuterWidth = this.msgBox.outerWidth();
                var topPx = windowHeight < mOuterHeight ? 0 : (windowHeight - mOuterHeight) / 2;
                var leftPx = windowouterWidth < mOuterWidth ? 0 : (windowouterWidth - mOuterWidth) / 2;

                this.msgBox.css({
                    top: topPx,
                    left: leftPx
                });

                return this;
            },

            loading: function(element) {
                var element = element ? element : 'loading....';
                return this.show($('<span>').css({
                    // 'width': 'auto',
                    'padding-left': '22px',
                    'background': 'url(/static/images/loading_s.gif) no-repeat'
                }).append(element));
            },

            msg: function(element) {
                var self = this.show(element).clear();
                self.interval.push(setTimeout(function() {
                    self.close()
                }, 3000));

                return this;
            },

            popup: function(data, func) {
                var a = $('<a>', {
                    href: 'javascript:void(0);'
                }).text('关闭').addClass('close').css({
                    'float': 'right'
                });
                var box = $('<div>').css({
                    'overflow': 'hidden',
                    '_zoom': 1,
                    'background': '#f0f0f0',
                    'border': '2px dashed #d6d6d6',
                    'padding': 5,
                    'clear': 'both'
                }).append(func(data));

                var h = $('<div>').css({
                    'width': '100%',
                    'height': 20,
                    'color': '#000',
                    'float': 'left'
                }).append(a).after(box);

                return this.show(h);
            },

            ajax: function(url, func, type) {
                var self = this;

                $.ajax({
                    type: type ? type : "GET",
                    url: url,
                    dataType: 'json',
                    success: function(data) {
                        if (data.typ == 'error') {
                            self.msg(data.msg);

                        } else {
                            self.popup(data, func);
                        }
                    },
                    error: function() {
                        self.msg('加载出错，请稍候再试');
                    },
                    beforeSend: function() {
                        self.loading('努力加载中，请稍候');
                    }
                });

                return this;
            }

        }.ready();

    }()


    // $.extend({});
})(jQuery);