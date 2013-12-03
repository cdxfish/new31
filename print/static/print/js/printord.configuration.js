$(document).ready(function() {
    p.post().all()
});

p = {
    post: function() {
        $('#print').submit(function(){
            $(this).find("input:checked:not(#all)").each(function(i, v){
                window.open('/print/print/' + $(v).attr('name') + '/');
            })

            return false;
        });
        return this;
    },
    all: function(){
    	$('#all').click(function(){
    		var input = $('#print input:not(#all)')
    		if ($(this).attr('checked') == 'checked'){
    			input.attr('checked', true);
    		}
    		else{
    			input.attr('checked', false);

    		}
    	});

    	return this;
    }
}