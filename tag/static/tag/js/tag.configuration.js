t = {
    like: function() {
        $(document).on('click', '.btnLike', function() {
            $.dialog.ajax($(this).attr('href'), function(data) {
                $.dialog.msg($('<p></p>').text('识货！'));
                $('.count_like_' + data.data.id).text(data.data.like);
            });
            return false;
        });
        return this;
    },
    buy: function() {
        $(document).on('click', '.btnBuy', function() {
            $.dialog.ajax($(this).attr('href'), function(data) {
                $.dialog.popup(data, function(data) {
                    var table = $('<table>', {
                        'width': '100%',
                        'class': 'tdpd5'
                    }).append($('<th>').text('规格'), $('<th>').text('原价'), $('<th>').text('会员价'));
                    $.each(data.data, function(i, v) {
                        table.append($('<tr>').append($('<td>').text(v.spec), $('<td>').text(v.fee), $('<td>').text(v.nfee), $('<td>').append($('<a>', {
                            'href': '/cart/buy/' + v.id + '/',
                            'class': 'btn btnbr'
                        }).text('购买'))));
                    });
                    return table;
                });
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