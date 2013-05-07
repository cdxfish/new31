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
                width: 700
            });
        });

        return this;
    },

    sgBtn: function(data) {
        var html = '';
        html += '   <h4><input type="text" name="keyword" /><input type="button" name="search" value=" 搜索 " id="goodsSearch" class="button" /></h4>  \r\n';

        return html;
    },

    search: function() {
        // 搜索商品
        $("#goodsSearch").live('click',

        function() {

            $(this).ajaxDialog(function(a) {

                var keyword = $('#keyword').val();

                $.getJSON('/ajax/item/', {
                    k: keyword
                },

                function(data) {
                    $.dialog.dialogMsg(data, aeog.sg)

                });

            });

        });

        return this
    },

    sg: function(data) {
        var html = '';
        html += aeog.sgBtn();

        html += '        <table width="100%" cellpadding="3" cellspacing="1" id="searchGoodslist">  \r\n';
        html += '        <tr>  \r\n';
        html += '          <th width="20px"></th>  \r\n';
        html += '          <th>商品名称</th>  \r\n';
        html += '          <th width="90px" >货号</th>  \r\n';
        html += '        </tr>  \r\n';

        $.each(data.data, function(i, v) {
            html += '    <tr>  \r\n';
            html += '      <td align="center"><input type="checkbox" value="'+n.goods_id+'"></td>  \r\n';
            html += '      <td>'+n.goods_name+'</td>  \r\n';
            html += '      <td align="center">'+n.goods_sn+'</td>  \r\n';
            html += '    </tr>  \r\n';
        });

        html += '        </table>  \r\n';
        html += '      <center>';
        html += '        <input type="button" value="加入订单" class="button" id="addToOrder" />';
        html += '      </center>';

        return html;
    }


}