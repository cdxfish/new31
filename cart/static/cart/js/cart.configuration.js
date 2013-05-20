$(document).ready(function() {
    cart.itemNum();
});


var cart = {
    itemNum: function() {
        $('.iNum').live('change',

        function() {
            var that = $(this);
            var thisValue = that.val();
            if (parseInt(thisValue) == thisValue) {
                $.getJSON(
                    '/ajax/itemnum/' + that.attr('name') + '/' + thisValue + '/',

                function(data) {
                    $.dialog.dialogMsgAndReload(data,

                    function(data) {
                        var stotal = $('#am' + that.attr('name')).text() * thisValue + '.00';

                        $('#st' + that.attr('name')).text(stotal);

                        $('.total').text(data.data);
                    })
                })
            } else {
                that.val(1);
            }

        })

        return this
    }

}