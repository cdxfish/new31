$(document).ready(function() {
    cart.itemNum();
});


var cart = {
    itemNum: function() {
        $('.iNum').change(function() {
            var that = $(this);
            var thisValue = that.val();
            if (parseInt(thisValue) == thisValue) {
                $.getJSON(
                    '/ajax/itemnum/' + thisValue + '/' + that.attr('name') + '/',

                function(data) {
                    $.dialog.dialogMsgAndReload(data,

                    function(data) {
                        $('.st' + data.data.i).text(data.data.itemSubtotal);
                        $('.total').text(data.data.subtotal);
                    })
                })
            } else {
                that.val(1);
            }

        })

        return this
    }

}