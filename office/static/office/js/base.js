// 置顶工具条
$(document).ready(function() {
    b.nav().odd('odd').plugin().loadMsg();
    // $(window).on('focus', b.loadMsg);
})

b = {
    // 表格鼠标移入移出特效
    odd: function(c) {
        $(document).on('click', '.oddbox', function(event) {
            event.stopPropagation();
        }).on('mouseover', 'table tr',

        function() {
            $(this).addClass(c);
        }).on('mouseout', 'table tr',

        function() {
            $(this).removeClass(c);
        }).on('click', 'table tr',

        function() {
            var oddbox = $(this).find('.oddbox');

            if (oddbox.length) {
                if (oddbox.attr('checked') == 'checked') {

                    oddbox.attr("checked", false);
                } else {

                    oddbox.attr("checked", true);
                }
            }

            // return false
        });
        return this
    },

    nav: function() {

        var navMenuRight = 0;
        var navMenu = $('#navMenu');
        $("#showNav").toggle(function() {
            navMenuRight = navMenu.css('right');
            navMenu.stop().animate({
                'right': '0px'
            }, 150)
            $(this).css({
                'background': 'url(/static/images/ico_showmorel.png) no-repeat'
            });
            return false;
        },

        function() {
            $('.nav').removeClass('on');
            $('.messagePop').slideUp('fast');

            navMenu.stop().animate({
                'right': navMenuRight
            }, 150);
            $(this).css({
                'background': 'url(/static/images/ico_showmorer.png) no-repeat'
            });
            return false;
        })


        $("#navMenu .nav").click(function() {
            if (!$(this).is(".on")) {
                $('.nav').removeClass('on');
                $('.messagePop').slideUp('fast');
            }

            $(this).toggleClass('on').next(".messagePop").slideToggle('fast');

            return false;
        });

        return this;
    },
    plugin: function() {
        $(".sort").tablesorter();

        $('.dateNoDir').Zebra_DatePicker(); //日期选择控件
        $('.date').Zebra_DatePicker({
            direction: true
        });
        $('select').jgdDropdown({
            clsLIExpand: false
            // selected: 'RS'
        });

        return this;
    },
    chng: function(obj, url) {
        obj.change(

        function() {
            var self = $(this);

            self.ajaxGET(url + '?' + self.attr('name') + '=' + encodeURI(self.val()));
        });
        return this;
    },
    act: function(func) {
        $('.oprt').on('click', 'a:not(.logisticslogcsEdit, .ordercopyOrd, .ordereditOrd)', function() {
            var self = $(this);
            self.ajaxGET(self.attr('href'), function(data) {
                var s = '';
                for (var i in data.data._act) {
                    s += '.' + data.data._act[i][2]
                    if (i < data.data._act.length - 1) {
                        s += ', ';
                    }

                }

                var act = '';
                for (var i in data.data.act) {
                    act += '<a href="' + data.data.act[i][3] + '" class="button ' + data.data.act[i][2] + '">' + data.data.act[i][1] + '</a>';

                }

                self.siblings(s).remove();
                self.parent().prepend(act);
                self.remove();
                $('#' + data.data.obj + data.data.sn).text(data.data.sStr).removeClass().addClass('status_' + data.data.s);

                return func(data);

            });

            return false
        });

        return this;
    },
    loadMsg: function() {
        var load = function() {
                $.getJSON('/message/get/', function(data) {
                    if (data.typ == 'error') {
                        $.debug.error(data.msg);
                    } else {
                        var read = [];
                        $.each(data.data, function(i, v) {
                            var str = ''; !! v.data.from && (str += v.data.from + ' '); !! v.time && (str += v.time + '：'); !! v.msg && (str += v.msg + ' '); !! v.data.sn && (str += v.data.sn + ' ');

                            $.debug[v.typ](str);

                            read.push(v.id);
                        });

                        if (read.length) {
                            $.getJSON('/message/read/', {
                                id: read
                            }, function(data) {
                                if (data.typ == 'error') {
                                    $.debug.error(data.msg);
                                }
                            });

                        }
                    }
                });

            }
        var stime;
        $(window).on('focus', function() {
            load();
            stime = setInterval(load, 10000);
        }).on('blur', function() {
            clearInterval(stime);
        });

        return this;
    }
}