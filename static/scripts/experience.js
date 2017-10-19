const $ = window.$;

$(document).ready(function () {

    $(".remove-icon").click(function(){
	$(this).parent().fadeOut(300);
    });

    $("#positive-add").click(function(){
	console.log("this");
    });
});
