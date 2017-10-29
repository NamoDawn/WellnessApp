server: 54.193.75.123
Description: /signin route testing
Serving on http://0.0.0.0:5001

Scenario 1
 - ajax uses url: "/signin" (no port)
 - tesing w.o gunicorn

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


- AJAX finishes in error function, not success function
- /experience never called bc post never made
- UI calls / route for some reason and reloads login.html

Chrome:
network:
Name	Method	Status	Type	Initiator		Size	Time
signin	OPTIONS	200	xhr	jquery-3.2.1.min.js:4	364 B	4 ms
signin	POST	(canceled)	xhr			0 B	30 ms

console:
VM37 wellness.js?95cd947e-dc05-4928-b05a-144d3843a8a9:84 error with signin:[object Object]
----- > error @ VM37 wellness.js?95cd947e-dc05-4928-b05a-144d3843a8a9:84
i @ VM35 jquery-3.2.1.min.js:2
fireWith @ VM35 jquery-3.2.1.min.js:2
A @ VM35 jquery-3.2.1.min.js:4
(anonymous) @ VM35 jquery-3.2.1.min.js:4
XMLHttpRequest.send (async)
send @ VM35 jquery-3.2.1.min.js:4
ajax @ VM35 jquery-3.2.1.min.js:4
signin @ VM37 wellness.js?95cd947e-dc05-4928-b05a-144d3843a8a9:68
(anonymous) @ VM37 wellness.js?95cd947e-dc05-4928-b05a-144d3843a8a9:18
dispatch @ VM35 jquery-3.2.1.min.js:3
q.handle @ VM35 jquery-3.2.1.min.js:3
Navigated to http://54.193.75.123/?email=myemail%40gmail.com&password=my_pwd


Chrome:
// - async: false must be used
// - /experince route must be called within it's own AJAX call after /signin route is succesful

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
