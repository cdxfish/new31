$(document).ready(function() {
    weiboShare();
    btnReplay();
    like();
});


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

        $(this).ajaxDialog(function(a) {

            $.getJSON(a.attr('href'),

            function(data) {
                $.dialog.dialogMsg(data, buyBtn, {
                    width: 460
                });

            });

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
        html += '             <td>' + v.spec + '</td>  \r\n';
        html += '             <td>￥' + v.amount + ' 元</td>  \r\n';
        html += '             <td><a href="/cart/buy/' + v.t + v.id + '/" class="btnB sBtn">购买</a></td>  \r\n';
        html += '          </tr>  \r\n';
    });

    html += '        </table>  \r\n';

    return html;
}


// 微博分享
weiboShare = function() {
    var weiboShare = $('<div class="weiboShare"><a href="/weibo/" >微博分享</a></div>').appendTo($("body"))
        .click(function() {

        $(this).ajaxDialog(function(a) {

            // $.getJSON(a.attr('href'),

            // function(data) {
                $.dialog.dialogMsg({
                    error: false,
                    data: {},
                    message: ''
                }, shareBtn);

            // });

        });

        return false;

    });

}

shareBtn = function(data) {
    var h = '';
    h += '      <div class="weibo">';
    h += '          <div class="weiboL"><img width="300px" src="/m/images/3133001p475a.jpg" alt=""/></div>  \r\n';
    h += '          <div class="weiboR"><h3>分享到</h3>  \r\n';
    h += '              <ul>  \r\n';
    h += '                  <li><a target="_blank" href="sinaUrl"><img src="/static/images/t.sina.png" height="50px" width="120px" alt=""/></a></li>  \r\n';
    h += '                  <li><a target="_blank" href="qqUrl"><img src="/static/images/t.qq.png" height="50px" width="120px" alt=""/></a></li>  \r\n';
    h += '              </ul>  \r\n';
    h += '              <h3>分享地址<span>(适用于论坛博客)</span></h3>  \r\n';
    h += '              <textarea><a href="pageUrl" target="_blank">linkText</a></textarea>  \r\n';
    h += '          </div>  \r\n';
    h += '      </div>  \r\n';
    return h;

}