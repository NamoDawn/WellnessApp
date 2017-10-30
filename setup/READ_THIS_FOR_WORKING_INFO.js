/* server: 54.193.75.123
Description: /signin route testing
Serving on http://0.0.0.0:5001
Works in Chrome (server and local.  FF doesn't work

Firefox: 
- flask is never called. FF console shows:

GET http://54.193.75.123/ [HTTP/1.1 200 OK 20ms]
----> error with signin:[object Object]  wellness.js:84:3
GET http://54.193.75.123/static/scripts/wellness.js [HTTP/1.1 200 OK 18ms]
GET http://54.193.75.123/static/styles/login.css [HTTP/1.1 200 OK 37ms]
GET https://code.jquery.com/jquery-3.2.1.min.js [HTTP/2.0 200 OK 31ms]
GET https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.11.2/jquery-ui.min.js [HTTP/2.0 200 OK 34ms]
GET https://fonts.googleapis.com/css [HTTP/2.0 200 OK 51ms]
GET https://fonts.gstatic.com/s/lato/v14/v0SdcGFAl2aezM9Vq_aFTQ.ttf [HTTP/2.0 200 OK 31ms]
GET https://fonts.gstatic.com/s/lato/v14/DvlFBScY1r-FMtZSYIYoYw.ttf [HTTP/2.0 200 OK 31ms]
GET https://s7.postimg.org/boj7tcxhn/image.jpg [HTTP/2.0 200 OK 68ms]
GET http://54.193.75.123/static/styles/login.css [HTTP/1.1 200 OK 17ms]



<Chrome:
// - async: false must be used
// - /experince route must be called within it's own AJAX call after /signin route is succesful
*/

  function loadExperiencePage () {
    $.ajax({
      url: '/experience',
      type: 'GET',
      contentType: 'text',
      success: function (res) {
        $(location).attr('href', '/experience');
      },
      error: function (res) {
        console.error('Failed to call endpoint \'experience\'');
      }
    });
  }


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
          loadExperiencePage();
          return true;
        }
        return false;
      },
      error: function (res) {
        console.error('error with signin:' + res);
      }
    });
  }

$(location).attr("href", "/experience") must be called within its own nested AJAX call
