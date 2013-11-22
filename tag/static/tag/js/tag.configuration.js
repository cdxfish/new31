$(document).ready(function() {
    t.btnReplay().like();
});

t = {
    like: function() {

        $(document).on('click', '.btnLike',

        function() {
            $(this).ajaxGET($(this).attr('href'), function(data) {
                $.dialog.msg('衷心感谢您的喜欢！...');
                $('.count_like_' + data.data.id).text(data.data.like);

            });


            return false;
        });

        return this;
    },

    btnReplay: function() {
        $(document).on('click', '.btnReplay', function() {
            $.dialog.ajaxGET($(this).attr('href'), function(data) {
                var html = '';
                html += '   <h3>请选择规格</h3>  \r\n';
                html += '        <table width="100%">  \r\n';

                $.each(data.data, function(i, v) {
                    html += '          <tr>  \r\n';
                    html += '             <td>' + v.spec + '</td>  \r\n';
                    html += '             <td>原价：' + v.fee + '</td>  \r\n';
                    html += '             <td>现价：' + v.nfee + '</td>  \r\n';
                    html += '             <td><a href="/cart/buy/' + v.id + '/" class="btnB sBtn">购买</a></td>  \r\n';
                    html += '          </tr>  \r\n';
                });

                html += '        </table>  \r\n';

                return html;
            });

            return false;
        });
        return this;
    },

    // 微博分享
    weiboShare: function() {
        $('<div class="weiboShare"><a href="/weibo/" >微博分享</a></div>').appendTo($("body")).click(function() {

            $.dialog.bnMsg({
                error: false,
                data: {},
                message: ''
            }, function(data) {
                var h = '';
                h += '      <div class="weibo">';
                h += '          <div class="weiboL"><img width="300px" src="/media/images/3133001p475a.jpg" alt=""/></div>  \r\n';
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
            }, {
                width: 750
            });

            return false;

        });
        return this;
    }
}