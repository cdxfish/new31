$(document).ready(function() {
    p.post()
});

p = {
    post: function() {
        $('#print').submit(function(){
            $(this).find("input:checked").each(function(i, v){
                window.open('/print/print/' + $(v).attr('name') + '/');
            })

            return false;
        })
    }
}