$(document).ready(function() {
    c.strFocusText($('#id_note'), c.noteText).strFocusText($('#id_tel'), c.telText).cCon().submit();
});


c = {
    noteText: '您可以在此填写您是否需要生日牌、祝福语（20字以内）以及关于订单的任何疑问、要求等。\n' + '如：我不希望你们和收货人联系，我要给收货人一个惊喜。具体的联系我的电话：158xxxxxxxx。',
    telText: '请填写多个号码，并用空格隔开。如：134XXXXXXXX 0771XXXXXXX。',

    strFocusText: function(obj, str) {
        if (obj.val() == 0) {
            obj.css({
                "color": "#CCCCCC"
            }).val(str);
        }

        obj.focus(

        function() {
            if (obj.val() == str) {
                obj.css({
                    "color": "#000000"
                }).val("");
            }
        }).focusout(

        function() {
            if (obj.val() == 0) {
                obj.css({
                    "color": "#CCCCCC"
                }).val(str);
            }
        });

        return this;
    },

    submit: function() {
        $('#checkout').submit(

        function() {

            var message = "";

            if ($('#id_pay').val() == 0) {
                message += '请选择支付方式!<br />';
            }

            // if ($('#ship').val() == 0) {
            //     message += '请选择配送方式!<br />';
            // }

            if ($('#id_consignee').val() == 0) {
                message += '请填写收货人姓名!<br />';
            }

            if ($('#id_area').val() == 0) {
                message += '请选择区域!<br />';
            }

            if ($('#id_address').val() == 0) {
                message += '请填写详细地址!<br />';
            }

            if ($('#id_tel').val() == c.telText || $('#id_tel').val() == 0) {
                message += '请填写联系电话!<br />';
            }


            if ($('#id_date').val() == 0) {
                message += '请填写最佳送货日期!<br />';
            }

            if ($('#id_time').val() == 0) {
                message += '请填写最佳送货时间!<br />';
            }

            if (message != 0) {
                $.dialog.message(message);

                return false;
            } else {
                if ($('#id_note').val() == c.noteText) {
                    $('#id_note').val('');
                }


            }

        })

        return this;

    },
    cCon: function() {
        $('#checkout input, #checkout select, #checkout textarea').change(

        function() {
            var name = $(this).attr('name');
            var value = $(this).val();

            $.getJSON(
                '/ajax/ccon/?' + name + '=' + value,

            function(data) {
                $.dialog.dialogMsgAndReload(data);
            })

        });
        return this;
    }
}