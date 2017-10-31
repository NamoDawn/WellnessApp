const $ = window.$;
$(document).ready(function () {
/******************* START TEST ***************************/
    function testFunction() {
	$.ajax({
	    url: '/laughter',
	    type: 'GET',
	    contentType: 'text',
	    success: function (res) {
		console.log('yes');
//		window.location = '/stinky/';
		$(location).attr('href', '/laughter');
	    },
	    error: function (res, error, xhr) {
		console.log('no');
	    }
	});
    }

    $('#test').on('click', function () {
	testFunction();
    });
  // REMOVE WHEN DONE TESTING
  $('#si_email').val('myemail@gmail.com');
  $('#si_password').val('my_pwd');

/******************** END TEST *********************************/



  /* Signup event listener */
  $('#signup_button').on('click', function () {
    const email = $('#email').val();
    const password = $('#password').val();
    const fName = $('#fName').val();
    const lName = $('#lName').val();
    signup(email, password, fName, lName);
  });
  /* Signin event listener */
  $('#signin_button').on('click', function () {
    const email = $('#si_email').val();
    const password = $('#si_password').val()
    signin(email, password);
  });
  /* Tab toggle functionality */
  $('.tabs .tab').click(function (){
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
  /* Behavior for background image moving */
  $('.container .bg').mousemove(function (e) {
    let amountMovedX = (e.pageX * -1 / 30);
    let amountMovedY = (e.pageY * -1 / 9);
    $(this).css('background-position', amountMovedX + 'px ' + amountMovedY + 'px');
  });
  /* Flask call to  render experience.html */
  function loadExperiencePage () {
    $.ajax({
      url: '/bless_those_gals_naomi_and_lisa',
//      url: '/experience',
      type: 'GET',
      contentType: 'text',
      success: function (res) {
        $(location).attr('href', '/bless_those_gals_naomi_and_lisa');
      },
      error: function (res) {
        console.error('Failed to call endpoint \'experience\'');
      }
    });
  }
  /* Sign User in
   * params: email, password
   * endpoint: /signin
   * method: POST
   * on success: redirects user to /experience */
  function signin (email, password) {
    const creds = [{'email': email, 'password': password}];
    $.ajax({
      async: false,
      url: '/signin',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(creds),
      success: function (res) {
        if (res[1] === true) {
          saveData({'user_id': res[0]});
          setTimeout(loadExperiencePage(), 3000);
	  setTimeout(function() {
	      return true;
	  }, 10000);
        }
        return false;
      },
      error: function (res) {
        console.error('error with signin:' + res);
      }
    });
  }
  /* Save user id locally
   * params: dict of info to be stored */
  function saveData (data = {}) {
    data = btoa(JSON.stringify(data));
    localStorage.setItem('data', data);
  }
  /* Sign User up
   * params: email, password, fName, lName
   * endpoint: /signup
   * method: POST
   * on success: writes user data to db */
  function signup (email, password, fName, lName) {
    const creds = [{'email': email, 'password': password, 'fName': fName, 'lName': lName}];
    $.ajax({
      url: '/signup',
      type: 'POST',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify(creds),
      success: function (res) {
        return true;
      },
      error: function (res) {
        console.error('error with signup:' + res);
        return false;
      }
    });
  }
});
