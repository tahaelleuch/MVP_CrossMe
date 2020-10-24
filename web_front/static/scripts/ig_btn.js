let accessToken;
let user_id;

if (accessToken != null) {
  $('.myfacebook').show();
}

function checkLoginState() {
  FB.getLoginStatus(function(response) {
    if (response.status === "connected") {
      accessToken = response.authResponse.accessToken;
      ScrapData();
      $('.myfacebook').hide();
      $('.nextbtn').hide();
      $(" .waiting ").show();
    }
  });
}

function ScrapData() {
  $(function () {
    $.get('https://0.0.0.0:5001/fb_post/'+ user_id + '/' + accessToken, function (response) {
      if (response) {
        console.log(response);
        $('.nextbtn').show();
        $(" .waiting ").hide();
      }
    });
  });
};

document.addEventListener('DOMContentLoaded', function () {

  $(" .waiting ").hide();
  user_id = document.getElementById("myuser_id").textContent
  if (window.location.href.indexOf('?code=') < 0) {
    $( '.insta button' ).click(function() {
      window.location.href = 'https://www.instagram.com/oauth/authorize?client_id=425368628431983&redirect_uri=https://0.0.0.0:5000/register&scope=user_profile,user_media&response_type=code';
    });
  } else {
    $( '.insta' ).empty();
    $(function () {
      var url = window.location.search;
      var new_url = url.substring(6);
      $.get('https://0.0.0.0:5001/ig_post/' + user_id + '/' + new_url, function (response) {
      });
    });
  }
  $( '.nextbtn button' ).click(function() {
    $('.steptwo').empty();
    $('.steptwo').append(
      '<p>Select image<p>' +
      '<form action="https://0.0.0.0:5001/image_test/' + user_id +
      '" method="POST" enctype="multipart/form-data"><div class="form-group">' +
      '<label></label>' +
      '<div class="custom-file">' +
      '<input type="file" class="custom-file-input" name="image" id="image">' +
      '<label class="custom-file-label" for="image"></label>' +
      '</div></div>' +
      '<button type="submit" class="myimport">Upload and select</button></form>' +
      '<p>Or simply use Facebook Profile Picture</p>'
    )
    if (accessToken == null) {
      $('.myfacebook').show();
      $('.steptwo').append(
      '<h1>You must login on Facebook first<h2>' +
      '<div id="fb-root"></div>' +
      '<div class="fb-login-button" data-size="large" data-button-type="continue_with" data-layout="default" data-auto-logout-link="false" data-use-continue-as="true" data-width="" onlogin="checkLoginState();" scope="email,user_birthday,user_posts"></div>'
      )
    } else {
      $('.steptwo').append('<div class="getMyImage"><button type="button">Click here to get your Facebook Photo</button></div>')
    }
    $('.steptwo').append('<div class="finbtn"><button type="button" onclick="location.href=\'/\'">Finish</button></div>');
    $('.getMyImage button').click(function() {
        $.get('https://0.0.0.0:5001/profile_pic/' + user_id + '/' + accessToken, function (response) {
            if (response.mycode == "ok") {
              $('.getMyImage button').empty();
              $('.getMyImage button').append('<p>done</p>' +
              '<img src="/static/images/fb_' + user_id + '.png"' +
               'alt="profilepic" width="500" height="500">'
              );
            }
        });
    });
  });
});
