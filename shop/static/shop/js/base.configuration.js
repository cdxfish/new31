$(document).ready(function() {
    $('.date').Zebra_DatePicker({
        direction: true
    }); //日期选择控件
    $('select').jgdDropdown({
        clsLIExpand: false
        // selected: 'RS'
    });
    $("img").scrollLoading(); //异步加载图片
});

var b = {

    // 返回顶部按钮
    backToTopEle: function() {
        var backToTopEle = $('<a href="javascript:void(0);" class="backToTop" title=\"返回顶部\"></a>').appendTo($("body")).click(function() {
            $("html, body").animate({
                scrollTop: 0
            }, 300, "linear", function() {
                backToTopEle.hide();
            });
        });
        $(window).scroll(function() {
            var st = $(document).scrollTop();
            var winh = $(window).height();
            (st > 0) ? backToTopEle.show() : backToTopEle.hide();
            //IE6下的定位
            if (!window.XMLHttpRequest) {
                backToTopEle.css("top", st + winh - 80);
            }
        });

        return this
    },

    chng: function(obj, url) {
        obj.change(function() {
            var self = $(this);
            $.dialog.ajax(url + '?' + self.attr('name') + '=' + encodeURI(self.val()));


        });
        return this;
    }

}