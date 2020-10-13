document.addEventListener('DOMContentLoaded', function () {
  $('.signin').click(function () {
    $('.myform').empty();
    $('.submit').empty();
    $('.myform').append(
    '<div class="mywhite"></div>' +
    '<input type="email" id="email" placeholder="Email"><br>' +
    '<input type="password" id="password" placeholder="PassWord"><br>'
    )
    $('.submit').append(`Login`);
  });
  $('.signup').click(function () {
    $('.myform').empty();
    $('.submit').empty();
    $('.myform').append(
    '<input type="text" id="full_name" placeholder="Your Full Name"><br>' +
    '<input type="email" id="email" placeholder="Email"><br>' +
    '<input type="password" id="password" placeholder="PassWord"><br>'
    )
    $('.submit').append(`Sign Up`);
  });
});