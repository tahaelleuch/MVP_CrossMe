let user_id;

document.addEventListener('DOMContentLoaded', function () {

  // update profile pic
  $('#file-upload').change(function() {
    console.log("done");
    user_id = document.getElementById("myuser_id").textContent;
    var fd = new FormData();
    var files = $('#file-upload')[0].files;
    if ( files.length > 0 ){
      fd.append('image',files[0]);
    }
    $.ajax({
      type: 'POST',
      data: fd,
      enctype: 'multipart/form-data',
      processData: false,
      contentType: false,
      url: 'https://0.0.0.0:5001/image_test/' + user_id,
      success: function ( response ) {
        location.reload(true);
      }
    });
  });

  //delete post
  $(document).on('click', '.delpost', function() {
    var post_id = $(this).attr('alt');
    $.ajax({
      url: 'https://0.0.0.0:5002/api/v1/post/' + post_id,
      type: 'DELETE',
      success: function(response) {
        $('#' + post_id).remove();
        location.reload(true);
      }
    });
  });
  //create a new post
  $(document).on('click', '.subbtn', function() {
    user_id = document.getElementById("myuser_id").textContent;
    var status = $("#mystatus").val();
    var fd = new FormData();
    var files = $('#selectedFile')[0].files;
    if ( files.length > 0 ){
      fd.append('file',files[0]);
    }
    if ( status ) {
      fd.append('data', status)
    }
    $.ajax({
      type: 'POST',
      data: fd,
      enctype: 'multipart/form-data',
      processData: false,
      contentType: false,
      url: 'https://0.0.0.0:5002/api/v1/post/' + user_id + '/new',
      success: function ( response ) {
        $('#mystatus').val('');
        $('#selectedFile').val('');
        location.reload(true);
        if ( response.media_url != "nomedia") {
            $( '#newpost' ).after(
            '<div class="mypost" id="' + response.id + '">' +
            '<div class="postsource" id="fromcm"></div>' +
            '<div class="creatorinfo">' +
            '<img src="' + response.user_avatar + '" alt="profilepic" class="postimage">' +
            '<section class="name"><h2>' + response.user_full_name + '</h2>' +
            '<h4>' + response.creation_date + '</h4></section>' +
            '<button class="delpost" alt="' + response.id + '">X</button>' +
            '</div>' +
            '<div class="postinfo"><div class="message"><p>' + response.post_text + '</p>' +
            '<img src="' + response.media_url + '" alt="postimage" class="postimage">' +
            '</div></div></div>'
            )
        } else {
            $( '#newpost' ).after(
            '<div class="mypost" id="' + response.id + '">' +
            '<div class="postsource" id="fromcm"></div>' +
            '<div class="creatorinfo">' +
            '<img src="' + response.user_avatar + '" alt="profilepic" class="postimage">' +
            '<section class="name"><h2>' + response.user_full_name + '</h2>' +
            '<h4>' + response.creation_date + '</h4></section>' +
            '<button class="delpost" alt="' + response.id + '">X</button>' +
            '</div>' +
            '<div class="postinfo"><div class="message"><p>' + response.post_text + '</p>' +
            '</div></div></div>'
            )
        }
      }
    });
  });
});
