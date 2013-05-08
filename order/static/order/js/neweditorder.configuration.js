$(document).ready(function() {
    aeo.cu();
    aeog.a().search();
});


aeo = {
    cu: function() {
        $('#checkout #user').change(
        aeo.u

        );
        return this;
    },
    u: function() {

        var user = $(this).val();

        if (user.length > 0 || !/^1[3|4|5|8][0-9]\d{8}$/.test(user)) {

            $.dialog.message('用户名无效!');

        }
    }
}


aeog = {

    a: function() {
        //添加商品
        $("#addNewGoods").live("click",

        function() {
            var data = {
                data: {},
                error: false,
                message: ''
            };
            $.dialog.dialogMsg(data, aeog.sgBtn, {
                'width': 400
            });
        });

        return this;
    },

    sgBtn: function(data) {
        var html = '';
        html += '   <h3 style="padding: 0 0 10px;"><input type="text" name="keyword" id="keyword" /><input type="button" name="search" value=" 搜索 " id="goodsSearch" class="button" /></h3>  \r\n';

        return html;
    },

    search: function() {
        // 搜索商品
        $("#goodsSearch").live('click',

        function() {

            var keyword = $('#keyword').val();

            $(this).ajaxDialog(function(a) {

                $.getJSON('/ajax/item/', {
                    k: keyword
                },

                function(data) {
                    $.dialog.dialogMsg(data, aeog.sg, {
                        'position': 'absolute',
                        'width': 400
                    });

                });

            });

        });

        return this
    },

    sg: function(data) {
        var html = '';
        html += aeog.sgBtn();

        html += '        <form action="/order/additemtoorder/" method="POST">  \r\n';
        html += '        <table width="100%" cellpadding="3" cellspacing="1" id="searchGoodslist" class="sortTable">  \r\n';
        html += '        <tr>  \r\n';
        html += '          <th width="20px"></th>  \r\n';
        html += '          <th>商品名称</th>  \r\n';
        html += '          <th width="90px" >货号</th>  \r\n';
        html += '        </tr>  \r\n';

        $.each(data.data, function(i, v) {
            html += '    <tr>  \r\n';
            html += '      <td align="center"><input type="checkbox" name="i" value="' + i + '" class="oddbox"></td>  \r\n';
            html += '      <td>' + v.name + '</td>  \r\n';
            html += '      <td align="center">' + v.sn + '</td>  \r\n';
            html += '    </tr>  \r\n';
        });

        html += '        </table>  \r\n';
        html += '      <center>  \r\n';
        html += csrf;
        html += '        <input type="submit" value="加入订单" class="button" />  \r\n';
        html += '      </center>  \r\n';
        html += '      </form>  \r\n';

        return html;
    }

}