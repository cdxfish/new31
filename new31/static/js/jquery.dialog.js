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
                $('body').append('<div id="dialog"><div id="maskLayer"></div><div id="floatLayer"></div></div>');
                $('#dialog').css($.dialog.css.dialog).css({
                    'height': $(document).height()
                });
                $('#maskLayer').css($.dialog.css.maskLayer);
                $('#floatLayer').css($.dialog.css.floatLayer);

                return this;
            },
            close: function() {
                $("#dialog").hide();
                return this;
            },
            closeBtn: function() {
                $('.close').live('click',

                function() {
                    $.dialog.close();
                });
                return this;
            },
            showDialog: function(h, obj) {
                var cssObj = obj ? obj : {};

                document.getElementById("floatLayer").innerHTML = h;
                $('#dialog').show();


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

                    $.dialog.dialogCenter();

                }

                return this;
            },

            dialogCenter: function() {

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

            delayClose: function(msg, t) {
                var time = !t ? 1000 : t;
                $("#dialog").fadeOut(time);
                return this;
            },
            loading: function(t, obj) {
                var cssObj = obj ? obj : {
                    width: 220
                };
                $.dialog.showDialog('<span class="loading" style="width:auto; padding-left:22px;background: url(/static/images/loading_s.gif) no-repeat;">' + t + '</span>', cssObj)

                return this;
            },
            message: function(msg, t, obj) {
                var cssObj = obj ? obj : {
                    width: 220
                };
                var time = !t ? 1500 : t;


                $.dialog.showDialog('<span class="message" style="text-align:center; width:220px">' + msg + '</span>', cssObj);

                setTimeout('$.dialog.delayClose()', time);

                return this;
            },

            dialogMsg: function(data, f, obj) {
                var cssObj = obj ? obj : {};
                if (data.error) {
                    $.dialog.message(data.message);

                } else {
                    var h = '';
                    h += '   <div class="topBox" style="width:100%;height:22px;line-height:22px;padding-bottom: 5px;float:right;"><a class="close" href="javascript:void(0);" style="background:url(/static/images/btn_close.gif) no-repeat; display:block;height: 22px; width:22px;text-indent:-9999em;float:right;">关闭</a></div>';
                    h += '   <div class="box" style="overflow:hidden; _zoom:1; background:#f0f0f0; border:2px dashed #d6d6d6; padding:15px;margin-bottom: 10px; clear:both;">  \r\n';
                    h += f(data);
                    h += '      </div>  \r\n';
                    h += '   </div>  \r\n';

                    $.dialog.showDialog(h, cssObj);
                }
            },

            dialogMsgAndReload: function(data, f, t) {
                var time = !t ? 1500 : t;
                if (data.error) {
                    $.dialog.message(data.message, time);
                    setTimeout('window.location.reload()', time);
                } else {
                    if (f) {
                        f(data);
                    }
                }
            },

            ajaxDialog: function(h, f, l) {
                var f = f ? f : function() {};
                var l = l ? l : '努力加载中请稍候，请稍候';

                $.dialog.loading(l);

                f(h);

            },

            allPrpos: function(obj) {
                this.dialogMsg({
                    error: false,
                    data: obj,
                    message: ''
                }, function(obj) {
                    var props = '<p>';

                    for (var p in obj.data) {
                        props += p + ": " + obj[p] + "  <br />";

                    }
                    props += '</p>';
                    return props;

                });
            }

        }


    });

    $.fn.extend({
        ajaxDialog: function(f, l) {
            var f = f ? f : function() {};
            var l = l ? l : '努力加载中请稍候，请稍候';

            $.dialog.loading(l);

            f(this);

        }
    })

})(jQuery);

$(document).ready(function() {
    $.dialog.maskLayer().closeBtn();
});