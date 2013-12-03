$(document).ready(function() {
    aeog.a().u().search().cItem();
});

aeog = {

    a: function() {
        var self = this;
        //添加商品
        $(document).on("click", '#addNewGoods', function() {
            $.dialog.popup({
                data: {},
                err: false,
                msg: ''
            }, function(data) {
                return $('<h3>').append($('<input>', {
                    type: 'text',
                    name: 'keyword',
                    id: 'keyword'
                }), $('<input>', {
                    type: 'button',
                    name: 'search',
                    id: 'goodsSearch',
                    class: 'button',
                    value: '搜索'
                }));
            });
        });

        return this;
    },

    search: function() {
        var self = this;
        // 搜索商品
        $(document).on('click', '#goodsSearch', function() {
            $.dialog.ajax('/order/item/?k=' + $('#keyword').val(), function(data) {
                $.dialog.popup(data, function(data) {
                    var table = $('<table>', {
                        width: '100%',
                        cellpadding: 3,
                        cellpadding: 1,
                        id: 'searchGoodslist'
                    }).append(
                    $('<tr>').append($('<th>', {
                        width: '20px'
                    }).text(''), $('<th>').text('商品名称'), $('<th>', {
                        width: '90px'
                    }).text('货号')));

                    $.each(data.data, function(i, v) {
                        table.append(
                        $('<tr>').append(
                        $('<td>', {
                            align: 'center'
                        }).append(
                        $('<input>', {
                            type: 'checkbox',
                            name: 'i',
                            value: v.id,
                            class: 'oddbox'
                        })), $('<td>').text(v.name), $('<td>', {
                            align: 'center'
                        }).text(v.sn)));
                    });

                    var center = $('<center>').append($('<input>', {
                        type: 'submit',
                        class: 'button',
                        value: '加入订单'
                    }), csrf);

                    return $('<form>', {
                        action: '/order/additem/',
                        method: 'POST'
                    }).append(table, center);
                })
            });
        });

        return this;
    },

    cItem: function() {
        $('.spec, .dis, .num').change(

        function() {
            var self = $(this);
            $.dialog.ajax('/order/citem/?name=' + self.attr('name') + '&mark=' + self.attr('id') + '&value=' + self.val(), function(data) {
                $('#nfee' + data.data.mark).text(data.data.nfee);
                $('#st' + data.data.mark).text(data.data.st);
                $('#total').text(data.data.total);
            });

        });
        return this;
    },
    u: function() {
        $('#checkUser').click(function() {
            $.dialog.ajax('/order/user/?u=' + $(this).prev().val(), function(data) {
                $.dialog.popup(data, function(data) {
                    var table = $('<table>', {
                        width: '100%',
                        cellpadding: 3,
                        cellpadding: 1
                    });
                    $.each(data.data, function(i, v) {
                        table.append($('<tr>').append($('<td>').text(i), $('<td>').text(v)));
                    });
                    return table;
                });
            });
        });
        return this;
    }
}