// 置顶工具条
$(document).ready(function() {
    b.nav().odd('odd').odds().plugin();
})

b = {
    // 表格鼠标移入移出特效
    odd: function(c) {
        $("table tr").live('mouseover',

        function() {
            $(this).addClass(c);
        }).live('mouseout',

        function() {
            $(this).removeClass(c);
        });

        return this;
    },

    odds: function() {

        $('.oddbox').live('click',

        function(event) {
            event.stopPropagation();
        });

        $("table tr").live('click',

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
    act: function(func){
        $('.oprt a:not(.logisticslogcsEdit, .ordercopyOrd, .ordereditOrd)').live('click', function(){
            var self = $(this);
            self.ajaxGET(self.attr('href'), function(data){
                var s = '';
                for(var i in data.data._act){
                    s += '.' + data.data._act[i][2] 
                    if (i < data.data._act.length - 1)
                    {
                        s += ', ';
                    }

                }

                var act = '';
                for(var i in data.data.act){
                    act += '<a href="'+ data.data.act[i][3]  +'" class="button '+ data.data.act[i][2] +'">'+ data.data.act[i][1] +'</a>'

                }

                self.siblings(s).remove();
                self.parent().prepend(act);
                self.remove();

                return func(data);

            });

            return false
        });

        return this;
    }
}