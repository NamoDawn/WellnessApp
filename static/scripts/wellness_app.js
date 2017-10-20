window.onload = function () {
    console.log('Window loaded!');

    $('#signup_button').on('click', function () {
	const username = $('#username_input').val()
	const password = $('#password_input').val()
	const f_name = $('#f_name_input').val()
	const l_name = $('#l_name_input').val()
	const email = $('#email_input').val()
	signup(username, password, f_name, l_name, email);

    });

    function signup(username, password, f_name, l_name, email) {
	creds = [{'username': username, 'password': password, 'f_name': f_name, 'l_name': l_name, 'email': email}]
	$.ajax ({
	        url: 'http://54.159.152.54:6002/signup',
	        type: 'POST',
	        dataType: 'json',
	        contentType: 'application/json',
	        data: json.dumps(creds),
	        success: function (res) {
		    console.log(res);
		 },
	        error: function (res) {
		    console.log('ERROR!');
		}
	    });
    }
}
