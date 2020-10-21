let use_id;
let follow_code;
$(document).ready(function(){
  $('.follow-button').click(function() {
    use_id = document.getElementById("myuser_id").textContent;
    follow_code = $(this).attr('alt');
      $.ajax({
      type: 'POST',
      url: '/flw/' + follow_code,
      success: function ( response ) {
        $('#hi'+follow_code).show();
        $('#'+follow_code).hide();
        }
      });
  });
  $('.follwed').click(function() {
    a = document.getElementById("myuser_id").textContent;
    follow_code = $(this).attr('alt');
    $.ajax({
      type: 'DELETE',
      url: '/flw/' + follow_code,
      success: function ( response ) {
        $('#'+follow_code).show();
        $('#hi'+follow_code).hide();
        }
      });
      });
    });
