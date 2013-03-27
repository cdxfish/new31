$(document).ready(function() {
    itemNum();
});

itemNum = function() {
    $('.iNum').change(function() {
        alert($(this).attr('name'));
    })
}