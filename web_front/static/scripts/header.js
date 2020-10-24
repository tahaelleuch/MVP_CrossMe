function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

document.addEventListener('DOMContentLoaded', function () {
  $('.mysearchin').keyup(function(event) {
    if (event.which === 13) {
      event.preventDefault();
      document.getElementById("mysearch").click();
      console.log("aa")
    }
  });
  $( '#mysearch' ).click(function(){
    var str = $('.mysearchin').val();
    window.location.replace("/search/" + str);
  });
});