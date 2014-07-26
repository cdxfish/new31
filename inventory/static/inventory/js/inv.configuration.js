$(document).ready(function() {
    i.act();
});

i = {
    act: function() {
        $('.act').click(function() {
            var $this = $(this);
            var val = parseInt($this.parent().prev().find('input').val());

            $.dialog.ajax($this.attr('href').replace(/(\d+)\/$/, val < 0 ? 0 : val + '/'), function(data){
                $('.s' + data.data.id).text(data.data.num);
                $('.c' + data.data.id).text(data.data.count);

                $.dialog.close();

            });


            return false;
        });
        return this;
    }
}