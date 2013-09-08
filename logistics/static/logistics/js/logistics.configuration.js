$(document).ready(function() {
    logcs.ad().dman();

    b.act(function(data){
        $('#l'+ data.data.sn).text(data.data.sStr).removeClass().addClass('status_' + data.data.s);

    })

});

var logcs = {
    ad: function() {
        $('.ad').change(function() {
            var self = $(this);

            self.ajaxGET('/logistics/cadv/?sn=' + self.attr('id') + '&value=' + self.val());
        });

        return this
    },
    dman: function() {
        $('.dman').change(function() {
            var self = $(this);

            self.ajaxGET('/logistics/cdman/?sn=' + self.attr('id') + '&value=' + self.val());
        });

        return this
    }

}