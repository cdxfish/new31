$(document).ready(function() {
    $(this).on("click", '.note', function() {
        var $this = $(this);

        $.dialog.popup({
            data: {},
            err: false,
            msg: ''
        }, function(data) {
            return $('<form>', {
                'method': 'POST',
                'action': '/tasting/note/' + $this.attr('data-id') + '/'
            }).append($('<textarea>', {
                'cols': 80,
                'name': 'note',
                'rows': 4,
                'id': 'textarea'
            }), $('<input>', {
                'type': 'submit',
                'id': 'submit',
                'class': 'button',
                'value': '提交'
            }), csrf);
        });

        return false;
    });
});
