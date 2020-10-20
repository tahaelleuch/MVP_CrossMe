let use_id;
let follow_code;

document.addEventListener('DOMContentLoaded', function () {
  $(document).on('click', '.followbtn', function() {
    use_id = document.getElementById("myuser_id").textContent;
    follow_code = $(this).attr('alt');
    if (follow_code !== "1" && follow_code !== "3") {
      $.ajax({
      type: 'POST',
      url: '/flw/' + use_id,
      success: function ( response ) {
          location.reload(true);
        }
      });
    } else if (follow_code === "1") {
      $.ajax({
      type: 'DELETE',
      url: '/flw/' + use_id,
      success: function ( response ) {
          location.reload(true);
        }
      });
    }
  });
});