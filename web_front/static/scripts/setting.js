$(document).ready(() => {
    $('#security').on('click', () => {
        $('.securitysetting').css('display', 'block');
        $('.Generalsetting').hide();
        $('.message').empty();
        $('#security').addClass("active"); 
        $('#general').removeClass("active"); 


    })
    $('#general').on('click', () => {
        $('.securitysetting').hide();
        $('.Generalsetting').show();
        $('#general').addClass("active"); 
        $('#security').removeClass("active"); 
        $('.message').empty();
        
    })
});
$(document).ready(() => {
    let myid= $("#myuser_id").text();
    let token= $("#token").text();
    $(".generalsettingsave").click(function(e) {
        
        let name = $("#name").val();
        let email = $("#email").val();
        if (name == '' || email == '') {
            $('.message').text("Please fill all fields...!")
        }
        else{
            $.ajax({

                "url": "https://0.0.0.0:5002/api/v1/changedata",
                "method": "POST",
                "timeout": 0,
                "headers": {
                  "Content-Type": "application/json"
                },
                "data": JSON.stringify({"user_id":myid,"securecode":token,"email":email,"name":name}),
                error: function (xhr) {
                    var err = JSON.parse(xhr.responseText);
                    $('.message').text(err.error);
                },
                    success: function () {
                        $('.message').text("Done !");
                        window.location.replace('/logout')
                    }
                    
              });

        }
    });

    $(".pwdsettingsave").click(function(e) {
        let old = $("#oldpwd").val();
        let newpwd = $("#pwd").val();
        let confirm = $("#confirmation").val();
        if (old == '' || newpwd == '' || confirm == '' ) {
            $('.message').text("Please fill all fields...!")
        }
            
        else if (!(newpwd).match(confirm)) {
            $('.message').text("Your passwords don't match. Try again?")
                } 
        else {
            $.ajax({

                "url": "https://0.0.0.0:5002/api/v1/changerequest",
                "method": "POST",
                "timeout": 0,
                "headers": {
                  "Content-Type": "application/json"
                },
                "data": JSON.stringify({"user_id":myid,"securecode":token,"password":old,"newpwd":newpwd}),
                error: function (xhr) {
                    var err = JSON.parse(xhr.responseText);
                    $('.message').text(err.error)
                },
                    success: function () {
                        $('.message').text("Done !")
                    }
              });
        }
    });
  }); 
