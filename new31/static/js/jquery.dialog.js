/*
 *
 * dialog 0.0 - jquery弹窗插件
 * Version 0.0.1
 * @requires jQuery v1.8.3
 *
 * Copyright (c) 2013 leiddx
 * 自用.
 *
 */

(function($) {
    $.extend({
        dialog: {
            id: '#dialog',
            css: {
                dialog: {
                    'display': 'none',
                    'z-index': 997,
                    'background': 'none transparent scroll repeat 0% 0%',
                    'width': '100%',
                    'height': '100%',
                    'position': 'absolute',
                    'left': '0px',
                    'top': '0px'
                },
                maskLayer: {
                    'z-index': -1,
                    'filter': 'alpha(opacity=75)',
                    'left': '0px',
                    'top': '0px',
                    'position': 'fixed',
                    'width': '100%',
                    'height': '100%',
                    'background-color': '#000',
                    'opacity': 0.45,
                    'overflow': 'hidden'
                },
                floatLayer: {
                    'border-radius': '10px',
                    'background': '#FFF',
                    'padding': '10px 20px',
                    'box-shadow': '1px 2px 5px #000',
                    'z-index': 999,
                    'height': 'auto',
                    'margin-left': 'auto',
                    'margin-right': 'auto',
                    'position': 'fixed',
                    'color': '#000'
                }

            },
            maskLayer: function() {
                var self = this;
                $('body').append('<div id="dialog"><div id="maskLayer"></div><div id="floatLayer"></div></div>');
                $(self.id).css(self.css.dialog).css({
                    'height': $(document).height()
                });
                $('#maskLayer').css(self.css.maskLayer);
                $('#floatLayer').css(self.css.floatLayer);

                return self;
            },
            close: function() {
                $(this.id).hide();
                return this;
            },
            closeBtn: function() {
                var self = this;
                $(document).on('click', '.close', function() {
                    self.close();
                })
                return self;
            },
            show: function(h, obj) {
                var cssObj = obj ? obj : {};

                document.getElementById("floatLayer").innerHTML = h;
                $(this.id).show();


                // 该死的IE
                if (jQuery.browser.msie && jQuery.browser.version === "6.0") {


                    $("#floatLayer").css({
                        width: $("#floatLayer .box").outerWidth(),
                        top: $(window).scrollTop() + 150,
                        position: 'relative'
                    }).css(cssObj);


                    $('#maskLayer').css({
                        position: 'absolute'
                    })


                } else {

                    $("#floatLayer").css(cssObj);

                    this.center();

                }

                return this;
            },

            center: function() {

                var windowHeight = $(window).outerHeight();
                var windowouterWidth = $('body').outerWidth();
                var floatLayerHeight = $("#floatLayer").outerHeight() + 100;
                var floatLayerouterWidth = $("#floatLayer").outerWidth();
                var topPx = windowHeight < floatLayerHeight ? 0 : (windowHeight - floatLayerHeight) / 2;
                var leftPx = windowouterWidth < floatLayerouterWidth ? 0 : (windowouterWidth - floatLayerouterWidth) / 2;

                $("#floatLayer").css({
                    top: topPx,
                    left: leftPx
                });

                $('#maskLayer').css({
                    position: 'fixed'
                })
            },

            loading: function(t, obj) {
                var cssObj = obj ? obj : {
                    width: 220
                };
                this.show('<span class="loading" style="width:auto; padding-left:22px;background: url(/static/images/loading_s.gif) no-repeat;">' + t + '</span>', cssObj)

                return this;
            },

            msg: function(msg, t, obj) {
                var self = this;
                var cssObj = obj ? obj : {
                    width: 220
                };
                var time = !t ? 1000 : t;


                this.show('<span class="message" style="text-align:center; width:220px">' + msg + '</span>', cssObj);

                setTimeout(function(){
                    self.close();
                }, time);

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


    });

    $.fn.extend({
        ajaxGET: function(url, func) {
            $.dialog.loading('努力加载中，请稍候');
            $.ajax({
                type: "GET",
                url: url,
                dataType: 'json',
                success: function(data) {
                    if (data.typ == 'error') {
                        $.dialog.msg(data.msg);

                    } else {
                        $.dialog.close();

                        !! func && func(data)

                    }
                },
                error: function() {
                    $.dialog.msg('加载出错，请稍候再试');
                }
            });
        }

    });

})(jQuery);

$(document).ready(function() {
    $.dialog.maskLayer().closeBtn();
    $.ajaxSetup({
        cache: false //close AJAX cache
    });
});