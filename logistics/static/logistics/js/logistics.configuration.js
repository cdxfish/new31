$(document).ready(function() {
    logcs.ad().dman();

    b.act(function(data){

    })

});

var logcs = {
    ad: function() {
        $('.ad').change(function() {
            var self = $(this);

            $.dialog.ajax('/logistics/cadv/' + self.attr('id') + '/' + self.val() + '/');
        });

        return this
    },
    dman: function() {
        $('.dman').change(function() {
            var self = $(this);

            $.dialog.ajax('/logistics/cdman/' + self.attr('id') + '/' + self.val() + '/');
        });

        return this
    }

}