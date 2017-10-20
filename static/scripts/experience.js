const $ = window.$;

$(document).ready(function(){

    let expName = [];
    let expObj = [];


    $("#positive-add").click(function(){
	let posVal = $('#positive').val();
	let posScale = $('#positivescale').val();

	if (posScale == "") {
	    posScale = 5;
	}

	if (!expName.includes(posVal) && posVal != "") {
            let experienceadded = $('#experienceAdded');
            let grid = $('<div/>', {class: 'col-xs-3'}).appendTo(experienceadded);
            let icon = $('<span/>', {class: 'glyphicon glyphicon-remove-circle remove-icon'}).appendTo(grid);
            let text = $('<span/>', {class: 'symdisplay', id:posVal+posScale, name: posVal, text:posVal + '(' + posScale + ')'}).appendTo(icon);
	    expName.push(posVal);
            $('#positive').val('');
	    $('#positivescale').val('');
	    expObj[posVal] = {'scale': posScale, 'type': 'pos'};
	}
    });

    $("#negative-add").click(function(){
        let negVal = $('#negative').val();
        let negScale = $('#negativescale').val();

        if (negScale == "") {
            negScale = 5;
        }

        if (!expName.includes(negVal) && negVal != "") {
            let experienceadded = $('#experienceAdded');
            let grid = $('<div/>', {class: 'col-xs-3'}).appendTo(experienceadded);
            let icon = $('<span/>', {class: 'glyphicon glyphicon-remove-circle remove-icon'}).appendTo(grid);
            let text = $('<span/>', {class: 'symdisplay', id:negVal + negScale, name: negVal, text:negVal + '(' + negScale + ')'}).appendTo(icon);
            expName.push(negVal);
            $('#negative').val('');
            $('#negativescale').val('');
            expObj[negVal] = {'scale': negScale, 'type': 'neg'};
        }
    });


    $('body').on('click', '.remove-icon', function() {
	$(this).parent().fadeOut(300);
	let index = expName.indexOf($(this).children().attr("name"));
	expName.splice(index, 1);
    });
});
