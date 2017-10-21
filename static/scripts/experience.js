const $ = window.$;

let stagedExp = [];
let stagedObj = [];

$(document).ready(function(){
    /* Add positive button clicked
     * Positive Experience Button Clicked adds to build expObj*/
    $("#positive-add").on('click', function () {
		const name = $('#positive').val()
		let scale = $('#positive_scale').val()

		queueExp(name, scale, 'positive');
		$('#positive').val('');
		$('#positive_scale').val('');
	});

	$('#stow_button').on('click', function () {
		save_experiences(stagedObj);
		$("#experienceAdded").empty();
		stagedExp = []
		stagedObj = []
	});

    /* Add negative button clicked
     * Negative Experience Button Clicked adds to build expObj*/
    $("#negative-add").click(function(){
        let name = $('#negative').val();
        let scale = $('#negative_scale').val();

		queueExp(name, scale, 'negative')
		$('#negative').val('');
		$('#negative_scale').val('');
    });

    /* 'Remove' icon clicked
     * Deletes expObj that was clicked*/
    $('body').on('click', '.remove-icon', function() {
	/*Delete the element*/
	$(this).parent().fadeOut(300);
	let index = expName.indexOf($(this).children().attr("name"));
	expName.splice(index, 1);
	/*update the expObj*/
	for (let i = 0; i < expObj.length; i++) {
	    if(expObj[i].name === $(this).children().attr("name")) {
		expObj.splice(i,1);
	    }
	}
    });
});

function queueExp(name, scale, type) {
	if (scale == '') {
		scale = 5;
	}
	/*checks if the experience was already added in the current session already*/
	if (!stagedExp.includes(name) && name != "") {
        const experienceadded = $('#experienceAdded');
        let grid = $('<div/>', {class: 'col-xs-3'}).appendTo(experienceadded);
        const icon = $('<span/>', {class: 'glyphicon glyphicon-remove-circle remove-icon'}).appendTo(grid);
        const text = $('<span/>', {class: 'symdisplay', id:name+scale, name: name, text:name + '(' + scale + ')'}).appendTo(icon);
		stagedExp.push(name);
		stagedObj.push({'symp_name': name, 'scale':scale, 'type': type})
	}
}

function save_experiences(stagedObj) {
	for (let i = 0; i < stagedObj.length; i++) {
		const obj = stagedObj[i]
		$.ajax({
			url: 'http://localhost:5001/save_exp',
			type: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify(obj),
			success: function (res) {
				console.log(res)
			},
			error: function (res) {
				console.error('Error: ' + res);
			}
		});
	}
}
