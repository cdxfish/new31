$(document).ready(function() {
    cart.itemNum();
});


var cart = {
    itemNum: function() {
        $(document).on('change', '.num',

            function() {
                var self = $(this);
                var val = self.val();
                if (parseInt(val) == val) {
                    $.dialog.ajax('/cart/cnum/' + self.attr('name') + '/' + val + '/',

                        function(data) {

                            var stotal = $('#am' + self.attr('name')).text() * val + '.00';

                            $('#st' + self.attr('name')).text(stotal);

                            $('.total').text(data.data);

                            $.dialog.close();

                        });


                } else {
                    self.val(1);
                }

            })

        return this
    }

}
