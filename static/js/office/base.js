// 置顶工具条
$(document).ready(function() {
    var navMenuRight = 0;
    var navMenu = $('#navMenu');
    $("#showNav").toggle(function() {
        navMenuRight = navMenu.css('right');
        navMenu.stop().animate({
            'right': '0px'
        }, 150)
        $(this).css({
            'background': 'url(/images/ico_showmorel.png) no-repeat'
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
            'background': 'url(/images/ico_showmorer.png) no-repeat'
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

    $("#myTable").tablesorter();

    // 表格鼠标移入移出特效
    $(".odd").live("mouseover",

    function() {
        $(this).children().css({
            background: "#CFC"
        });
        return false;
    }).live("mouseout",

    function() {
        $(this).children().css({
            background: "#FFF"
        });
        return false;
    });

})