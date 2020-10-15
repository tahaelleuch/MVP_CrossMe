document.addEventListener('DOMContentLoaded', function () {
  $('.signin').click(function () {
    $('.myform').empty();
    $('.submit').empty();
    $('.myform').attr('action', "/login");
    $('.myform').append(
    '<div class="mywhite"></div>' +
    '<input type="email" name="email" id="email" placeholder="Email"><br>' +
    '<input type="password" name="password" id="password" placeholder="Password"><br>'
    )
    $('.submit').append(`Login`);
  });
  $('.signup').click(function () {
    $('.myform').empty();
    $('.submit').empty();
    $('.myform').attr('action', "/register");
    $('.myform').append(
    '<input type="text" name="full_name"  id="full_name" placeholder="Your Full Name"><br>' +
    '<input type="email" name="email" id="email" placeholder="Email"><br>' +
    '<input type="password" name="password" id="password" placeholder="PassWord"><br>'
    )
    $('.submit').append(`Sign Up`);
  });
});