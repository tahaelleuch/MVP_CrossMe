let user_id;
let num_like;
let current_user_id;

document.addEventListener('DOMContentLoaded', function () {

  //make a like
  $(document).on('click', '.heart', function() {
      var post_id_like = $(this).attr('id');
      var post_id = $( this ).attr('alt');
      var targ_id = $( this ).attr('title');

      num_like = document.getElementById(post_id + 'okok').textContent;

      var numok = $('#numok').text()
      user_id = document.getElementById("myuser_id").textContent;

      current_user_id = document.getElementById("current_user_id").textContent;

      $.ajax({
        type: 'POST',
        contentType: 'application/json',
        url: 'https://0.0.0.0:5002/api/v1/like/' + post_id,
        data: JSON.stringify({'source_user_id':current_user_id,'target_user_id':targ_id,'post_id':post_id}),
        success: function (data) {
          $( '#' + post_id_like).toggleClass('likedheart').removeClass('heart');
          let my_num = parseInt(num_like)
          //check if no likes bofore
          //if ($('.likenum').is(':empty')){
          if (my_num === 0) {
            $( '#' + post_id + 'num' ).append(
                '<div class="liked"><h1>1</h1></div>'
            )
          } else {
            $( '#' + post_id + 'num' ).empty();
            $( '#' + post_id + 'num' ).append(
                '<div class="liked"><h1>' + num_like + '</h1></div>'
            );
            num_like = (parseInt(num_like) + 1).toString();
            location.reload(true);
          }
        }
      });
  });



  // make a dislike (delete like)
  $(document).on('click', '.likedheart', function() {
      var post_id_like = $(this).attr('id');
      var post_id = $( this ).attr('alt');

      num_like = document.getElementById(post_id + 'okok').textContent;

      current_user_id = document.getElementById("current_user_id").textContent;

      var numok = $('#numok').text()
      user_id = document.getElementById("myuser_id").textContent;

      $.ajax({
        url: 'https://0.0.0.0:5002/api/v1/react/' + post_id + '/' + current_user_id,
        type: 'DELETE',
        success: function (data) {
            $( '#' + post_id_like).toggleClass('heart').removeClass('likedheart');

            //check if just you liked
            if (parseInt(num_like) === 0) {
              $( '#' + post_id + 'num' ).empty();
            } else {
              num_like = (parseInt(num_like) - 1).toString();
              $( '#' + post_id + 'num' ).empty();
              $( '#' + post_id + 'num' ).append(
                '<div class="liked"><h1>' + num_like + '</h1></div>'
              );
            }
            location.reload(true);
        }
      });
  });


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
