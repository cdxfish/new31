$(document).ready(function() {
    b.chng($('#ord input, #ord select'), '/order/cord/').act(function(data){
        $('#o'+ data.data.sn).text(data.data.sStr).removeClass().addClass('status_' + data.data.s);

    })
});