// 置顶工具条
$(document).ready(function() {
    ob.nav().odd('#CFC').odds().plugin();
})

ob = {
    // 表格鼠标移入移出特效
    odd: function(c) {
        $("table tr").live('mouseover',

        function() {
            $(this).addClass('odd');
        }).live('mouseout',

        function() {
            $(this).removeClass('odd');
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
        $(".sortTable").tablesorter();

        $('.dateNoDir').Zebra_DatePicker(); //日期选择控件
        $('.date').Zebra_DatePicker({
            direction: true
        });
        $('select').jgdDropdown({
            clsLIExpand: false
            // selected: 'RS'
        });

        return this;
    }
}