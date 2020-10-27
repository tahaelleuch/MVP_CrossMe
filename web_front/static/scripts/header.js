function myFunction() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

let aser_id;
document.addEventListener('DOMContentLoaded', function () {

  let notiftxt;

  aser_id = document.getElementById("myuser_id").textContent;
  $('.notifpopup').hide();
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
  $('#notif').click(function(){
    var cur = document.getElementById("notif");
    if (cur.className === "closed") {
      $('.notifpopup').show();
      $('#notif').toggleClass('open').removeClass('closed');
      $.ajax({
        type: 'GET',
        url: 'https://0.0.0.0:5002/api/v1/notif/' + aser_id,
        success: function ( response ) {
          for (const j in response.data) {
            if (response.data[j].type === "like") {
              notiftxt = '<p>Liked your post</p>'
            } else {
              notiftxt = '<p>started following you</p>'
            }
            $(".notifpopup").append(
            '<div class="onenotif" alt="' + response.data[j].maker_user_id +
            '"><div class="notiffriend">' +
            '<img src="' + response.data[j].maker_avatar + '"></div>' +
            '<div class="notiftext"><div class="acbn">' +
            '<h1>' + response.data[j].maker_full_name + '</h1>' +
            notiftxt + '<h3>' + response.data[j].creation_date + '<h3>' +
            '</div></div>' +
            '<div class="delnotif" alt="' + response.data[j].id + '">X</div></div>'
            );
          }
          $(".notifpopup").append(
            '<div class="morenotif">See all notifications</div>'
          );
        }
      });
    } else {
      $('#notif').toggleClass('closed').removeClass('open');
      $('.notifpopup').hide();
      $(".notifpopup").empty();
    }
  });

  $(document).on('click', '.onenotif', function() {
    var maker_id = $( this ).attr('alt');
    console.log(maker_id);
    window.location.replace("/profile/" + maker_id);
  });

  $(document).on('click', '.delnotif', function() {
    var notf_id = $( this ).attr('alt');
    $.ajax({
      url: 'https://0.0.0.0:5002/api/v1/notif/' + notf_id,
      type: 'DELETE',
      success: function (data) {
        $('.notifpopup').hide();
        $('.notifpopup').show();
      }
    });
  });

});