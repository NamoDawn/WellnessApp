const $ = window.$;
$(document).ready(function () {
  /* Signup event listener */
  $('#signup_button').on('click', function () {
    const email = $('#email').val();
    const password = $('#password').val();
    const fName = $('#fName').val();
    const lName = $('#lName').val();
    signup(email, password, fName, lName);
    modal.style.display = "block";
  });

  /*Modal Script*/

    // Get the modal
    var modal = document.getElementById('signupModal');
    // Get the button that opens the modal
    var btn = document.getElementById("signup_button");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // When the user clicks the button, open the modal
    //btn.onclick = function() {
    //modal.style.display = "block";
    //}

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
	modal.style.display = "none";
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
	if (event.target == modal) {
            modal.style.display = "none";
	}
    }

  /* Signin event listener */
  $('#signin_button').on('click', function () {
    const email = $('#si_email').val();
    const password = $('#si_password').val();
    signin(email, password);
  });
  /* Tab toggle functionality */
  $('.tabs .tab').click(function () {
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
//      url: '/bless_those_gals_naomi_and_lisa',
      url: '/experience',
      type: 'GET',
      contentType: 'text',
      success: function (res) {
//        $(location).attr('href', '/bless_those_gals_naomi_and_lisa');
        $(location).attr('href', '/experience');
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
          setTimeout(function () {
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
	  $("#signup_notification").html("Sign Up Successful!");
          $("#f_name").val("");
          $("#l_name").val("");
          $("#email").val("");
          $("#password").val("");
	  return true;
      },
      error: function (res) {
        console.error('error with signup:' + res);
        $("#signup_notification").html("Failed! Sign Up Was Not Successful!");

        return false;
      }
    });
  }
});
