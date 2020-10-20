let use_id;
let follow_code;
 
  $(document).on('click', '.follow-button', function() {
    use_id = document.getElementById("myuser_id").textContent;
    follow_code = $(this).attr('alt');
      $.ajax({
      type: 'POST',
      url: '/flw/' + follow_code,
      success: function ( response ) {
        $('#'+follow_code).remove();
        $('#hi'+follow_code).show();
        }
      });
  });