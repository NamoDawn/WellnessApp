const $ = window.$;
$(document).ready(function () {
    /* JQuery Section
     * Sign up button clicked will retrieve the input fields and call function signup*/
    $('#signup_button').on('click', function () {
	const email = $('#email').val()
	const password = $('#password').val()
	const f_name = $('#f_name').val()
	const l_name = $('#l_name').val()
	signup(email, password, f_name, l_name);
    });


    /*Sign in button clicked will retrieve the input fields and call function signin*/
    $('#signin_button').on('click', function () {
	const email = $('#si_email').val()
	const password = $('#si_password').val()
	signin(email, password);
    });

    /*Tabs Toggle functionality*/
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
    /*Behavior for background image moving*/
    $('.container .bg').mousemove(function(e){
	var amountMovedX = (e.pageX * -1 / 30);
	var amountMovedY = (e.pageY * -1 / 9);
	$(this).css('background-position', amountMovedX + 'px ' + amountMovedY + 'px');
    });
    /* Load experience page with ajax
     * endpoint: http://54.193.75.123:5000/experience
     * http method: GET
     * onSuccess: redirects user to /experience*/
    function load_experience_page() {
	$.ajax({
	        url: 'http://54.193.75.123:5000/experience',
	        type: 'GET',
	        contentType: 'text',
	        success: function (res) {
		    $( location ).attr("href", 'http://54.193.75.123:5000/experience');
		        },
	        error: function (res) {
		    console.error('Failed to call endpoint "experience"')
		        }
	    });
    }
    /* Sign User in
     * method: signin
     * parameter(s): email, password
     * additional info:
     * endpoint: http://54.193.75.123:5000/signin
     * http method: POST
     * onSuccess: redirects user to /experience*/
    function signin(email, password) {
	creds = [{'email':email, 'password':password}];
	$.ajax({
	    url: 'http://54.193.75.123:5000/signin',
	    type: 'POST',
	    dataType: 'json',
	    contentType: 'application/json',
	    data: JSON.stringify(creds),
	    success: function (res) {
		if (res[1] === true) {
		    saveData({'user_id': res[0]});
		    
		    $( location ).attr("href", 'http://54.193.75.123:5000/experience');
		    } else {
			return false;
			}
		},
	    error: function (res) {
		console.error('error with signin:' + res);
		}
	    });
    }

    function saveData(data = {}) {
	data = btoa(JSON.stringify(data));
	localStorage.setItem('data', data);
	}
    /* Sign User up
     * method: signup
     * parameter(s): email, password, f_name, l_name
     * additional info:
     * endpoint: http://54.193.75.123:5000/signup
     * http method: POST*/
    function signup(email, password, f_name, l_name) {
	const creds = [{'email': email, 'password': password, 'f_name': f_name, 'l_name': l_name}];
	$.ajax ({
	    url: 'http://54.193.75.123:5000/signup',
	    type: 'POST',
	    dataType: 'json',
	    contentType: 'application/json',
	    data: JSON.stringify(creds),
	    success: function (res) {

		},
	    error: function (res) {
		console.error('error with signup:' + res);
		}
	    });
    }
});
