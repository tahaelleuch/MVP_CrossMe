let user_id;
let page_num = 0;

document.addEventListener('DOMContentLoaded', function () {

  //function to post a new post
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

  //function to get more posts from api
  $(document).on('click', '.loadmore button', function() {
    user_id = document.getElementById("myuser_id").textContent;
    page_num = page_num + 1;
    let n = page_num.toString();
    $.ajax({
      type: 'GET',
      url: 'https://0.0.0.0:5002/api/v1/friendposts/' + user_id + '/' + n,
      success: function ( response ) {
        $( '.loadmore button' ).remove()
        let pst_src;
        let img_src;
        for (const i in response.data) {

          if (response.data[i].post_source === "FACEBOOK") {
            pst_src = '<div class="postsource" id="fromfb">' +
            '<img src="/static/images/fb.png" alt="fb" class="smico">' +
            '</div>'
          } else if (response.data[i].post_source === "Instagram") {
            pst_src = '<div class="postsource" id="fromig">' +
            '<img src="/static/images/ig.png" alt="ig" class="smico">' +
            '</div>'
          } else {
            pst_src = '<div class="postsource" id="fromcm"></div>'
          }

          console.log(response.data[i].media_url)

          if ( response.data[i].media_url != "nomedia") {
            img_src = '<img src="' + response.data[i].media_url +
            '" alt="postimage" class="postimage">'
          } else {
            img_src = " "
          }

          $( '.mybody' ).append(
            '<div class="mypost" id="' + response.data[i].id + '">' + pst_src +
            '<div class="creatorinfo">' +
            '<img src="' + response.data[i].user_avatar + '" alt="profilepic" class="postimage">' +
            '<section class="name"><h2>' + response.data[i].full_name + '</h2>' +
            '<h4>' + response.data[i].creation_date + '</h4></section>' +
            '</div>' +
            '<div class="postinfo"><div class="message"><p>' + response.data[i].post_text + '</p>' +
            img_src +
            '</div></div></div>'
          )
        }
        if (response.data.length === 10) {
          $( '.mybody' ).append(
            '<div class="loadmore">' +
            '<button type="button">Load More ...</button>' +
            '</div>'
          )
        }
      }
    });
  });
});

