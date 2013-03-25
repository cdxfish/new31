$(document).ready(function() {
    weiboShare();
    btnReplay();
    btnLike();
});



// 微博分享

weiboShare = function() {
    var weiboShare = $('<div class=\"weiboShare\"><a href=\"javascript:void(0);\" onclick=\"SharePhotos();\">微博分享</a></div>').appendTo($("body"))
        .click(function() {
        dialog("l", [{
            val: "l",
            title: "正在为你生成分享的图片，请稍候...",
            className: "l",
            fadeOut: -1,
            width: 220
        }]);
        setTimeout(

        function() {
            ShareHtml('/m/DSC_3500.jpg');
        },
        1000);



    });

}

btnReplay = function() {

    $('.btnReplay').live('click',

    function() {
        var getURL = $(this).attr('href');
        dialog("l", [{
            val: "l",
            title: "正在为您获取规格，请稍候...",
            className: "l",
            fadeOut: -1,
            width: 220
        }]);

        getAttr(getURL);

        return false;
    });
}

btnLike = function() {

    $('.btnLike').live('click',

    function() {
        timeClosePopup('衷心感谢您的喜欢！', 1000);

        return false;
    });

}


ShareHtml = function(uploadShareImage, linkText, pageUrl, sinaUrl, qqUrl, sohuUrl) {

    var share = '   <p><a class=\"btn_close\" href=\"javascript:void(0);\" onclick=\"closePopupNow();\">关闭</a></p>';
    share += '   <div class=\"shareSelectBox\">  \r\n';
    share += '      <div class=\"shareYourPhotosL\"><img width=\"300px\" src=\"' + uploadShareImage + '\" alt=\"\"/></div>  \r\n';
    share += '      <div class=\"shareYourPhotosR\"><h3>分享到</h3>  \r\n';
    share += '          <ul>  \r\n';
    share += '            <li><a target=\"_blank\" href=\"" + sinaUrl + "\"><img src=\"' + '/images/t.sina.png' + '\" height=\"50\" width=\"120\" alt=\"\"/></a></li>  \r\n';
    share += '            <li><a target=\"_blank\" href=\"" + qqUrl + "\"><img src=\"' + '/images/t.qq.png' + '\" height=\"50\" width=\"120\" alt=\"\"/></a></li>  \r\n';
    share += '          </ul>  \r\n';
    share += '          <h3>分享地址<span>(适用于论坛博客)</span></h3>  \r\n';
    share += '          <textarea><a href=\"" + pageUrl + "\" target=\"_blank\">" + linkText + "</a></textarea>  \r\n';
    share += '      </div>  \r\n';
    share += '   </div>  \r\n';

    dialog("share", [{
        val: "share",
        text: share,
        isPanel: true,
        fadeOut: -1,
        width: 760
    }]);

    $("#floatingLayer").addClass("popup800");

}

getAttr = function(link) {

    $.getJSON(link,

    function(data) {
        ajax(data, buyBtn);

    });
}



buyBtn = function(data) {
    var html = '   <p><a class=\"btn_close\" href=\"javascript:void(0);\" onclick=\"closePopupNow();\">关闭</a></p>';
    html += '   <div class=\"shareSelectBox\">  \r\n';
    html += '      <div class=\"buySpc\"><h3>请选择规格</h3>  \r\n';
    html += '        <table width="100%">  \r\n';

    $.each(data.item, function(i, v) {
        html += '          <tr>  \r\n';
        html += '             <td>' + v.attr + '</td>  \r\n';
        html += '             <td>￥' + v.amount + ' 元</td>  \r\n';
        html += '             <td><a href="/ajax/buy/' + v.id + '/" class="btnB sBtn">购买</a></td>  \r\n';
        html += '          </tr>  \r\n';
    });

    html += '        </table>  \r\n';
    html += '      </div>  \r\n';
    html += '   </div>  \r\n';

    return html;
}