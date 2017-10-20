window.onload = function () {
    console.log('Window loaded!');

    $('#signup_button').on('click', function () {
		const email = $('#email').val()
		const password = $('#password').val()
		const f_name = $('#f_name').val()
		const l_name = $('#l_name').val()
		signup(email, password, f_name, l_name);
//		signup('108@holbertonschool.com', 'test_pw', 'stuey', 'gk'); // <--- use hardcode for testing
    });


    $('#signin_button').on('click', function () {
		const email = $('#si_email').val()
		const password = $('#si_password').val()
		signin(email, password);
//		signin('108@holbertonschool.com', 'test_pw'); // <--- use hardcode for testing
    });

$('.tabs .tab').click(function(){
	if ($(this).hasClass('signin')) {
            $('.tabs .tab').removeClass('active');
            $(this).addClass('active');
            $('.cont').hide();
            $('.signin-cont').show();
		}
	if ($(this).hasClass('signup')) {
            $('.tabs .tab').removeClass('active');
            $(this).addClass('active');
            $('.cont').hide();
            $('.signup-cont').show();
		}
    });
    $('.container .bg').mousemove(function(e){
		var amountMovedX = (e.pageX * -1 / 30);
		var amountMovedY = (e.pageY * -1 / 9);
		$(this).css('background-position', amountMovedX + 'px ' + amountMovedY + 'px');
    });


	function signin(email, password) {
		creds = [{'email':email, 'password':password}];
		$.ajax({
			url: 'http://localhost:5001/signin',
			type: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: JSON.stringify(creds),
			success: function (res) {
				if (res == true) {
					console.log('Logged In!')
					// LISA: redirect to member page
				} else {
					console.log('Login failed')
					// LISA: 'You have entered an invalid email/password combination. Please try again or click "Sign Up" to create a new account'
				}
			},
			error: function (res) {
				console.log('ERROR!!');
			}
		});

	}
    function signup(email, password, f_name, l_name) {
		const creds = [{'email': email, 'password': password, 'f_name': f_name, 'l_name': l_name}];
		$.ajax ({
			url: 'http://localhost:5001/signup',
//			url: 'http://54.193.75.123:5001/signup',
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
