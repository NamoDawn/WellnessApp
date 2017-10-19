window.onload = function () {
    console.log('Window loaded!');

    $('#signup_button').on('click', function () {
	const email = $('#email_input').val()
	const password = $('#password_input').val()
	const f_name = $('#f_name_input').val()
	const l_name = $('#l_name_input').val()
//	signup(username, password, f_name, l_name, email); // <--- undo after connected to real html
	signup('108@holbertonschool.com', 'test_pw', 'stuey', 'gk');
    });

    function signup(email, password, f_name, l_name) {
	const creds = [{'email': email, 'password': password, 'f_name': f_name, 'l_name': l_name}];
	$.ajax ({
	    url: 'http://54.193.75.123:5001/sign_up',
	    type: 'POST',
	    dataType: 'json',
	    contentType: 'application/json',
	    data: JSON.stringify(creds),
	    success: function (res) {
		console.log(res);
	    },
	    error: function (res) {
		console.log('ERROR!');
	    }
	});
    }
}
