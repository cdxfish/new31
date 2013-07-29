$(document).ready(function() {
    logcs.ad().dman();

});

var logcs = {
    ad: function() {
        $('.ad').change(function() {
            var self = $(this);

            self.ajaxGET('/ajax/cadv/?sn=' + self.attr('id') + '&value=' + self.val());
        });

        return this
    },
    dman: function() {
        $('.dman').change(function() {
            var self = $(this);

            self.ajaxGET('/ajax/cdman/?sn=' + self.attr('id') + '&value=' + self.val());
        });

        return this
    }

}