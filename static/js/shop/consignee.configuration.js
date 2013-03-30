$(document).ready(function() {
    c.noteObj($('.note')).note().submit().cCon();
    $('.date').Zebra_DatePicker({
        direction: true
    }); //日期选择控件
});


c = {
    noteObj: function(obj) {
        c.noteObj = obj;
        return this;
    },

    noteText: '您可以在此填写您是否需要生日牌、祝福语（20字以内）以及关于订单的任何疑问、要求等。\n' + '如：我不希望你们和收货人联系，我要给收货人一个惊喜。具体的联系我的电话：158xxxxxxxx。',

    note: function() {
        if (c.noteObj.val() == 0) {
            c.noteObj.css({
                "color": "#CCCCCC"
            }).val(c.noteText);
        }

        c.noteObj.focus(

        function() {
            if (c.noteObj.val() == c.noteText) {
                c.noteObj.css({
                    "color": "#000000"
                }).val("");
            }
        }).focusout(

        function() {
            if (c.noteObj.val() == 0) {
                c.noteObj.css({
                    "color": "#CCCCCC"
                }).val(c.noteText);
            }
        });

        return this;
    },

    submit: function() {
        $('#checkout').submit(

        function() {

            var message = "";

            if ($('.pay').val() == 0) {
                message += '请选择支付方式!<br />';
            }
            if ($('.ship').val() == 0) {
                message += '请选择配送方式!<br />';
            }
            if ($('.consignee').val() == 0) {
                message += '请填写收货人姓名!<br />';
            }

            if ($('.city').val() == 0) {
                message += '请选择城市!<br />';
            }

            if ($('.block').val() == 0) {
                message += '请选择区域!<br />';
            }

            if ($('.address').val() == 0) {
                message += '请填写详细地址!<br />';
            }

            if ($('.tel').val() == 0) {
                message += '请填写联系电话!<br />';
            }

            if ($('.date').val() == 0) {
                message += '请填写最佳送货日期!<br />';
            }

            if ($('.time').val() == 0) {
                message += '请填写最佳送货时间!<br />';
            }

            if (message != 0) {
                timeClosePopup(message, 3000);

                return false;
            } else {
                if (c.noteObj.val() == c.noteText) {
                    c.noteObj.val('');
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

        })
        return this;
    }
}