$(document).ready(function() {
    c.strFocusText($('#id_note'), c.noteText).strFocusText($('#id_tel'), c.telText).submit();
    b.chng($('#logcs input, #logcs select, #logcs textarea'), '/logistics/clogcs/');
});


c = {
    noteText: '您可以在此填写您是否需要生日牌、祝福语（20字以内）以及关于订单的任何疑问、要求等。\n' + '如：我不希望你们和收货人联系，我要给收货人一个惊喜。具体的联系我的电话：158xxxxxxxx。',
    telText: '请填写多个号码，并用空格隔开。如：134XXXXXXXX 0771XXXXXXX。',

    strFocusText: function(obj, str) {
        var color = obj.css('color');

        var func = function() {
                if (!obj.val() || obj.val() == str) {
                    obj.css({
                        color: "#CCCCCC"
                    }).val(str);
                }
            }

        func();


        obj.focus(

        function() {
            if (obj.val() == str) {
                obj.css({
                    color: color
                }).val('');
            }
        }).focusout(func);

        return this;
    },

    submit: function() {
        $('#checkout').submit(

        function() {

            var message = [];

            if ($('#id_dlvr').val() == 0) {
                message.push($('<p></p>').text('请选择配送方式!'));
            }
            if (!$('#id_consignee').val()) {
                message.push($('<p></p>').text('请填写收货人姓名!'));
            }

            if (!$('#id_area').val()) {
                message.push($('<p></p>').text('请选择区域!'));
            }

            if (!$('#id_address').val()) {
                message.push($('<p></p>').text('请填写详细地址!'));
            }

            if ($('#id_tel').val() == c.telText || !$('#id_tel').val()) {
                message.push($('<p></p>').text('请填写联系电话!'));
            }


            if (!$('#id_date').val()) {
                message.push($('<p></p>').text('请填写最佳送货日期!'));
            }

            if (!$('#id_time').val()) {
                message.push($('<p></p>').text('请填写最佳送货时间!'));
            }

            if (message.length) {
                $.dialog.msg(message);

                return false;
            } else {
                if ($('#id_note').val() == c.noteText) {
                    $('#id_note').val('');
                }


            }

        })

        return this;

    }
}