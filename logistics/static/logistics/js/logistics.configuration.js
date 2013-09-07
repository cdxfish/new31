$(document).ready(function() {
    logcs.ad().dman().act();

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
    },
    act: function(){
        $('.logisticslogcsUnsent').click(function(){
            var self = $(this);
            self.ajaxGET(self.attr('href'), function(data){
                
            });

            return false
        });

        return this
    }

}