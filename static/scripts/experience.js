const $ = window.$;

$(document).ready(function(){
    /* Add positive button clicked
     * Positive Experience Button Clicked adds to build expObj*/
    $("#positive-add").on('click', function () {
		const symp_name = $('#positive').val();
		const scale = $('#positive_scale').val();
//		const date = new Date().toLocaleString();
		const type = 'positive';
		const obj = [{'symp_name': symp_name,
					'scale':scale,
					'type': type}]

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

	});

/*    $("#positive-add").click(function(){
		let posVal = $('#positive').val();
		let posScale = $('#positivescale').val();

		if (posScale == "") {
			posScale = 5;
		}
		/*checks if the experience was already added in the current session already*/
/*		if (!expName.includes(posVal) && posVal != "") {
			/*Dynamically building the DOM*/
    /*        let experienceAdded = $('#experienceAdded');
            let grid = $('<div/>', {class: 'col-xs-3'}).appendTo(experienceAdded);
            let icon = $('<span/>', {class: 'glyphicon glyphicon-remove-circle remove-icon'}).appendTo(grid);
            let text = $('<span/>', {class: 'symdisplay', id:posVal+posScale, name: posVal, text:posVal + '(' + posScale + ')'}).appendTo(icon);
			/*adding the experience to expObj*/
	/*		expName.push(posVal);
            $('#positive').val('');
			$('#positivescale').val('');
			newPos = {'name': posVal,'scale': posScale, 'type': 'pos'};
			expObj.push(newPos);;
		}
    }); */
    /* Add negative button clicked
     * Negative Experience Button Clicked adds to build expObj*/
    $("#negative-add").click(function(){
        let negVal = $('#negative').val();
        let negScale = $('#negativescale').val();

        if (negScale == "") {
            negScale = 5;
        }
	/*checks if the experience was already added in the current session already*/
        if (!expName.includes(negVal) && negVal != "") {
	    /*Dynamically building the DOM*/
            let experienceAdded = $('#experienceAdded');
            let grid = $('<div/>', {class: 'col-xs-3'}).appendTo(experienceAdded);
            let icon = $('<span/>', {class: 'glyphicon glyphicon-remove-circle remove-icon'}).appendTo(grid);
            let text = $('<span/>', {class: 'symdisplay', id:negVal + negScale, name: negVal, text:negVal + '(' + negScale + ')'}).appendTo(icon);
	    /*adding the experience to expObj*/
            expName.push(negVal);
            $('#negative').val('');
            $('#negativescale').val('');
            expObj[negVal] = {'scale': negScale, 'type': 'neg'};
        }
    });

    /* Remove icon clicked
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
