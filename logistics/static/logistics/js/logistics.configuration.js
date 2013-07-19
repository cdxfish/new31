$(document).ready(function() {
    logcs.ad().dman();

});

var logcs = {
    ad: function() {
        $('.ad').change(function() {
            var self = $(this);
            var sn = self.attr('id');
            var value = self.val();
            self.ajaxDialog(function() {
                $.getJSON('/ajax/cadvance/?sn=' + sn + '&value=' + value,

                function(data) {
                    $.dialog.msg(data);
                });

            });
        });

        return this
    },
    dman: function() {
        $('.dman').change(function() {
            var self = $(this);
            var sn = self.attr('id');
            var value = self.val();
            self.ajaxDialog(function() {
                $.getJSON('/ajax/cdman/?sn=' + sn + '&value=' + value,

                function(data) {
                    $.dialog.msg(data);
                });

            });
        });

        return this
    }

}