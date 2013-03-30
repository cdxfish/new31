$(document).ready(function() {
    weiboShare();
    btnReplay();
    like();
});



// 微博分享
weiboShare = function() {
    var weiboShare = $('<div class="weiboShare"><a href="javascript:void(0);" >微博分享</a></div>').appendTo($("body"))
        .click(function() {

        $.dialog.loading('正在为你生成分享的图片，请稍候...').show(shareBtn());

    });

}

shareBtn = function() {
    var h = '';
    h += '   <a class="close" href="javascript:void(0);">关闭</a>';
    h += '   <div class="box">  \r\n';
    h += '      <div class="boxL"><img width="300px" src="/m/images/3133001p475a.jpg" alt=""/></div>  \r\n';
    h += '      <div class="boxR"><h3>分享到</h3>  \r\n';
    h += '          <ul>  \r\n';
    h += '            <li><a target="_blank" href="sinaUrl"><img src="/images/t.sina.png" height="50px" width="120px" alt=""/></a></li>  \r\n';
    h += '            <li><a target="_blank" href="qqUrl"><img src="/images/t.qq.png" height="50px" width="120px" alt=""/></a></li>  \r\n';
    h += '          </ul>  \r\n';
    h += '          <h3>分享地址<span>(适用于论坛博客)</span></h3>  \r\n';
    h += '          <textarea><a href="pageUrl" target="_blank">linkText</a></textarea>  \r\n';
    h += '      </div>  \r\n';
    h += '   </div>  \r\n';
    return h;

}


like = function() {

    $('.btnLike').live('click',

    function() {

        $.dialog.message('衷心感谢您的喜欢！...');

        return false;
    });

}



btnReplay = function() {

    $('.btnReplay').live('click',

    function() {

        $.dialog.loading('正在为您获取规格，请稍候');

        $.getJSON($(this).attr('href'),

        function(data) {
            $.dialog.dialogMsg(data, buyBtn);

        });

        return false;
    });
}

buyBtn = function(data) {
    var html = '';
    html += '   <h3>请选择规格</h3>  \r\n';
    html += '        <table width="100%">  \r\n';

    $.each(data.data, function(i, v) {
        html += '          <tr>  \r\n';
        html += '             <td>' + v.attr + '</td>  \r\n';
        html += '             <td>￥' + v.amount + ' 元</td>  \r\n';
        html += '             <td><a href="/cart/buy/' + v.t + v.id + '/" class="btnB sBtn">购买</a></td>  \r\n';
        html += '          </tr>  \r\n';
    });

    html += '        </table>  \r\n';

    return html;
}