$(document).ready(function() {
    i.act();
});

i = {
    act: function() {
        $('.act').click(function() {
            var self = $(this);
            self.attr('href', self.attr('href').replace(/(\d+)\/$/, self.parent().prev().find('input').val() + '/'));
        });
        return this;
    }
}