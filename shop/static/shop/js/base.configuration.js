var b = {

    chng: function(obj, url) {
        obj.change(function() {
            var self = $(this);
            $.dialog.ajax(url + '?' + self.attr('name') + '=' + encodeURI(self.val()));


        });
        return this;
    }

}