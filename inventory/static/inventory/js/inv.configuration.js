$(document).ready(function() {
    i.act().count().default();
});

i = {
    act: function() {
        var self = this;
        $('.act').click(function() {
            var $this = $(this);
            var val = parseInt($this.parent().prev().find('input').val());

            $.dialog.ajax($this.attr('href').replace(/(\d+)\/$/, val < 0 ? 0 : val + '/'), function(data) {
                $('.a' + data.data.id).text(data.data.adv);
                $('.s' + data.data.id).text(data.data.num);
                $('.c' + data.data.id).text(data.data.count);

                $this.parents('.spec').attr('data-adv', data.data.adv).attr('data-num', data.data.num).attr('data-count', data.data.count);

                self.count();

                $.dialog.close();

            });


            return false;
        });
        return this;
    },
    count: function() {
        var self = this;
        $('.item').each(function(i, v) {
            self.setnum($(this));
        });

        return this;
    },
    setnum: function(ele) {
        var adv = 0;
        var count = 0;
        var num = 0;
        ele.nextAll('.spec[data-id=' + ele.attr('data-id') + ']').each(function(ii, vv) {
            $this = $(this);
            adv += parseInt($this.attr('data-adv'));
            count += parseInt($this.attr('data-count'));
            num += parseInt($this.attr('data-num'));
        });

        ele.find('.item-adv').text(adv);
        ele.find('.item-count').text(count);
        ele.find('.item-num').text(num);

    },
    default: function() {
        $('#default').click(function() {
            var date = $('#id_s').val();
            $.dialog.ajax('/inventory/sbuild/', function(data) {
                $.dialog.popup(data, function(data) {
                    var table = $('<table>', {
                        'width': '100%',
                        'cellpadding': 3,
                        'cellpadding': 1
                    });

                    $.each(data.data, function(i, v) {
                        table.append(
                            $('<tr>').append(
                                $('<td>', {
                                    'align': 'center'
                                }).append(
                                    $('<a>', {
                                        'href': '/inventory/default/' + date + '/?b=' + v.id,
                                        'class': 'button'
                                    }).text(v.name)
                                )
                            )
                        );
                    });
                 return table;

                });
            });
            return false;
        });

        return this;
    }
}
