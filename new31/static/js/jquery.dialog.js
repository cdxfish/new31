/*
 *
 * dialog 0.0 - jquery弹窗插件
 * Version 0.1.0
 * @requires jQuery v1.8.3
 *
 * Copyright (c) 2013 leiddx
 * 自用.
 *
 */

(function($) {
    $.dialog = function() {
        var obj = {
            id: 'dialog',
            css: [{
                'z-index': 999,
                'background': 'none transparent scroll repeat 0% 0%',
                'width': '100%',
                'height': '100%',
                'position': 'absolute',
                'left': '0px',
                'top': '0px'
            }, {
                'filter': 'alpha(opacity=75)',
                'width': '100%',
                'height': '100%',
                'background-color': '#000',
                'opacity': 0.45,
                'overflow': 'hidden'
            }, {
                'border-radius': '1px',
                'background': '#FFF',
                'padding': '10px 20px',
                'box-shadow': '1px 2px 5px #000',
                'position': 'fixed',
                'color': '#000'
            }, {
                'width': 'auto',
                'padding-left': '22px',
                'background': 'url(/static/images/loading_s.gif) no-repeat'
            }],
            close: function() {
                $('#' + this.id).hide(function() {
                    $(this).children(':last').html('');
                });
                return this;
            },
            ready: function() {
                var self = this;

                $(document).ready(function() {
                    $('<div>', {
                        id: self.id
                    }).css(self.css[0]).css({
                        'height': $(document).height()
                    }).hide().append($('<div>').css(self.css[1]), $('<div>').css(self.css[2])).appendTo('body').on('click', '.close', function() {
                        self.close();
                    });
                });

                return this;
            },

            show: function(htm, t) {
                var time = t ? t : 100000;
                $('#' + this.id).show(function() {
                    $(this).children(':last').html(htm);
                });

                return this.center();
            },

            center: function() {
                var divs = $('#' + this.id + ' div');

                var windowHeight = $(window).outerHeight();
                var windowouterWidth = $('body').outerWidth();
                var fOuterHeight = divs.eq(1).outerHeight() + 100;
                var fOuterWidth = divs.eq(1).outerWidth();
                var topPx = windowHeight < fOuterHeight ? 0 : (windowHeight - fOuterHeight) / 2;
                var leftPx = windowouterWidth < fOuterWidth ? 0 : (windowouterWidth - fOuterWidth) / 2;

                divs.eq(1).css({
                    top: topPx,
                    left: leftPx
                });

                return this;
            },

            loading: function(msg) {

                return this.show($('<span>').html(msg).css(this.css[3]));
            },

            msg: function(msg) {
                var self = this;

                var time = !t ? 1000 : t;


                this.show(msg).close();

                return this;
            },

            bnMsg: function(data, func, obj) {
                var cssObj = obj ? obj : {};
                if (data.typ == 'error') {
                    this.msg(data.msg);

                } else {
                    var h = '';
                    h += '   <div class="topBox" style="width:100%;height:22px;line-height:22px;padding-bottom: 5px;float:right;"><a class="close" href="javascript:void(0);" style="background:url(/static/images/btn_close.gif) no-repeat; display:block;height: 22px; width:22px;text-indent:-9999em;float:right;">关闭</a></div>';
                    h += '   <div class="box" style="overflow:hidden; _zoom:1; background:#f0f0f0; border:2px dashed #d6d6d6; padding:15px;margin-bottom: 10px; clear:both;">  \r\n';
                    h += func(data);
                    h += '      </div>  \r\n';
                    h += '   </div>  \r\n';

                    this.show(h, cssObj);
                }
            },

            ajaxGET: function(url, func, obj) {
                var self = this;

                self.loading('努力加载中，请稍候');
                $.ajax({
                    type: "GET",
                    url: url,
                    dataType: 'json',
                    success: function(data) {
                        self.bnMsg(data, func, obj ? obj : {
                            width: 460
                        });
                    },
                    error: function() {
                        $.dialog.msg('加载出错，请稍候再试');
                    }
                });
            }

        }

        obj = obj.ready();

        return obj;

    }()


    // $.extend({});
})(jQuery);