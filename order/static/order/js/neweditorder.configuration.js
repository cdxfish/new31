$(document).ready(function() {
    aeog.a().search().cItem();
});

aeog = {

    a: function() {
        var self = this;
        //添加商品
        $("#addNewGoods").live("click",

        function() {

            $.dialog.bnMsg({
                data: {},
                err: false,
                msg: ''
            }, self.sgBtn, {
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
        var self = this;

        // 搜索商品
        $("#goodsSearch").live('click',

        function() {

            var keyword = $('#keyword').val();

            $.dialog.ajaxGET('/ajax/item/', self.sg, {
                'position': 'absolute',
                'width': 400
            });


        });

        return this;
    },

    sg: function(data) {
        var html = '';
        html += aeog.sgBtn();

        html += '        <form action="/order/additem/" method="POST">  \r\n';
        html += '        <table width="100%" cellpadding="3" cellspacing="1" id="searchGoodslist" class="sortTable">  \r\n';
        html += '        <tr>  \r\n';
        html += '          <th width="20px"></th>  \r\n';
        html += '          <th>商品名称</th>  \r\n';
        html += '          <th width="90px" >货号</th>  \r\n';
        html += '        </tr>  \r\n';

        $.each(data.data, function(i, v) {
            html += '    <tr>  \r\n';
            html += '      <td align="center"><input type="checkbox" name="i" value="' + v.id + '" class="oddbox"></td>  \r\n';
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
    },

    cItem: function() {

        $('.spec, .dis, .num').change(

        function() {
            var self = $(this);
            $(this).ajaxGET('/ajax/citem/?name=' + self.attr('name') + '&mark=' + self.attr('id') + '&value=' + self.val(), function(data) {
                $('#nfee' + data.data.mark).text(data.data.nfee);
                $('#st' + data.data.mark).text(data.data.st);
                $('#total').text(data.data.total);
            });

        });
        return this;
    }
}