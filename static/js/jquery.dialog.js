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
            maskLayer: function() {
                $('body').append('<div id="floatingLayer"></div><div id="maskLayer"></div>');
                return this;
            },
            close: function() {
                $("#maskLayer").hide();
                $("#floatingLayer").hide();
                return this;
            },
            closeBtn: function() {
                $('.close').live('click',

                function() {
                    $.dialog.close();
                });
                return this;
            },
            show: function(h) {
                $("#maskLayer").show();
                $("#floatingLayer").html(h).fadeIn('fast').css({
                    "top": (window.innerHeight - $("#floatingLayer").outerHeight() - 100) / 2,
                    "left": (window.innerWidth - $("#floatingLayer").outerWidth()) / 2
                });
                return this;
            },
            delayClose: function(msg, t) {
                var time = !t ? 1000 : t;
                $("#floatingLayer").fadeOut(time);
                $("#maskLayer").fadeOut(time);
                return this;
            },
            dialogMsgAndReload: function(data, f, t) {
                var time = !t ? 1500 : t;
                if (data.error) {
                    timeClose(data.message, time);
                    setTimeout('window.location.reload()', time);
                } else {
                    if (f) {
                        f(data);
                    }
                }
                return this;
            },
            loading: function(t) {
                $.dialog.show('<span class="loading">' + t + '</span>')

                return this;
            },
            message: function(msg, t) {
                var time = !t ? 1500 : t;
                $.dialog.show('<span>' + msg + '</span>');

                setTimeout('$.dialog.delayClose()', time);

                return this;
            },

            dialogMsg: function(data, f) {
                if (data.error) {
                    $.dialog.message(data.message);

                } else {
                    var h = '';
                    h += '   <a class="close" href="javascript:void(0);">关闭</a>';
                    h += '   <div class="box">  \r\n';
                    h += f(data);
                    h += '      </div>  \r\n';
                    h += '   </div>  \r\n';
                    $.dialog.show(h);
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
            }

        }


    });

})(jQuery);

$(document).ready(function() {
    $.dialog.maskLayer().closeBtn();
});