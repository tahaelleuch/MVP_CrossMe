function login()
{
    let email=document.getElementById("email").value;
    if (email === "") {
      alert("no email");
      return;
    }
    let pass=document.getElementById("password").value;
    if (pass === "") {
      alert("no password");
      return;
    }
    if ($('.submit').text() === "Login"){
        alert(email + pass);
    } else {
        let name=document.getElementById("full_name").value;
        if (name === "") {
          alert("no name");
          return;
        }
        var ajax=$.ajax({
            crossDomain: true,
            type: 'POST',
            data: JSON.stringify({email:email,password:pass,full_name:document.getElementById("full_name").value}),
            contentType: 'application/json',
            dataType: "json",
            url: "http://0.0.0.0:5009/authoapi/new_user/"}).done(function(data, status){
              console.log(status);
              if (status === 'success') {
                $('.mybody').empty();
                $('.mybody').append(
                '<div class="steptwo">' +
                '<p>One More Step...</p>' +
                '</div>'
                )
              }
            });
        ajax.fail(function(data){


            alert(data);
        });


            }
};