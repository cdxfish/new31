// 置顶工具条
$(document).ready(function() {
    ob.nav().odd('#CFC');
    $(".sortTable").tablesorter();

    $('.date').Zebra_DatePicker(); //日期选择控件
})

ob = {
    // 表格鼠标移入移出特效
    odd: function(c) {
        $("table tr").bind('mouseover',

        function() {
             $(this).addClass('odd');
        }).bind('mouseout',

        function() {
             $(this).removeClass('odd');
        });

        return this;
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
    }
}