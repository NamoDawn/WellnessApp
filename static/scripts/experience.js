const $ = window.$;

$(document).ready(function(){
    $("#positive-add").click(function(){
	let posVal = $('#positive').val();
	let posScale = $('#positivescale').val();
        let experienceadded = $('#experienceAdded');
        let grid = $('<div/>', {class: 'col-xs-3'}).appendTo(experienceadded);
        let icon = $('<span/>', {class: 'glyphicon glyphicon-remove-circle remove-icon'}).appendTo(grid);
        let text = $('<span/>', {text:posVal + '(' + posScale + ')'}).appendTo(icon);


        $('#positive').val('');
        $('#positivescale').val('');
    });


    $('body').on('click', '.remove-icon', function() {
	$(this).parent().fadeOut(300);
    });
});
