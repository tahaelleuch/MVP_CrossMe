#!/usr/bin/python3
"""scrap api"""

from flask import Flask, make_response, jsonify, redirect
from flask import request as rq
from flask_cors import CORS
from models.post import Post
from models.user import User
from models import storage
import requests
import uuid
from datetime import datetime
import urllib
import io
import PIL.Image as Image
from werkzeug.utils import secure_filename
import os

scrap_app = Flask(__name__)
cors = CORS(scrap_app)
scrap_app.config["IMAGE_UPLOADS"] = "./web_front/static/images/"
scrap_app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]


@scrap_app.route('/image_test/<user_id>', methods=['POST'])
def import_image(user_id):
    """import image"""
    if 'image' not in rq.files:
        print('No file part')
    if rq.method == "POST":
        if rq.files:

            image = rq.files["image"]
            if "." in image.filename:
                ext = image.filename.split(".")[-1]
                if ext.upper() not in scrap_app.config["ALLOWED_IMAGE_EXTENSIONS"]:
                    redirect('https://0.0.0.0:5000/error_photo')
            else:
                redirect('https://0.0.0.0:5000/error_photo')
            new_filename = 'cm_' + user_id + '.' + ext

            final_filename = secure_filename(new_filename)
            image.save(os.path.join(scrap_app.config["IMAGE_UPLOADS"], final_filename))
            final_path = '/static/images/' + final_filename

            my_user = storage.get(User, user_id)
            my_user.update_attr("user_avatar", final_path)


            return redirect('https://0.0.0.0:5000/login')
    return redirect('https://0.0.0.0:5000/login')

@scrap_app.route('/profile_pic/<user_id>/<access_token>', methods=['GET'])
def save_user_photo(user_id, access_token):
    """get my user photo and save it to db"""
    MYURL = 'https://graph.facebook.com/me/picture?redirect=false&height=500&access_token=' + access_token
    r = requests.get(MYURL).json()
    if r["data"]:
        image_url = r["data"]["url"]
        forsave = urllib.request.urlopen(image_url)
        data = forsave.read()
        image = Image.open(io.BytesIO(data))
        path = './web_front/static/images/fb_' + user_id + '.png'
        image.save(path)
        succ_dict = {}
        succ_dict["mycode"] = "ok"

        my_user = storage.get(User, user_id)
        db_path = '/static/images/fb_' + user_id + '.png'
        my_user.update_attr("user_avatar", db_path)

        return redirect('https://0.0.0.0:5000/login')
    err_dict = {}
    err_dict["mycode"] = "notok"
    return make_response(jsonify(err_dict), 200)






@scrap_app.route('/fb_post/<user_id>/<access_token>', methods=['GET'])
def get_data_fb(user_id, access_token):
    """scrap data from facebook"""

    my_user = storage.get(User, user_id)
    my_user.update_attr("fb_access_token", access_token)

    r = requests.get('https://graph.facebook.com/me/feed?access_token=' + access_token)
    result = r.json()
    post_dict = {}
    post_list = []
    index = 0
    for posts in result["data"]:
        if index == 10:
            break
        new_post = {}

        new_post["CrossMe_user_id"] = user_id
        new_post["Post_id_CrossMe"] = str(uuid.uuid4())

        if "message" in posts.keys():
            new_post["message"] = posts["message"]
        else:
            new_post["message"] = "NULL"

        new_post["created_time"] = datetime.strptime(posts["created_time"], '%Y-%m-%dT%H:%M:%S+%f')

        new_post["source"] = "FACEBOOK"

        new_post["fb_post_id"] = posts["id"]


        URLPOST = 'https://graph.facebook.com/' + posts["id"] + '?fields=object_id&access_token=' + access_token
        post_data = requests.get(URLPOST).json()
        if "object_id" in post_data.keys():
            URLIMAGE = 'https://graph.facebook.com/' + post_data["object_id"] + '?fields=images&access_token=' + access_token
            image_data = requests.get(URLIMAGE).json()
            if "images" not in image_data.keys():
                continue
            all_images = image_data["images"]
            new_post["image_url"] = all_images[1]["source"]
            posts["media_type"] = "IMAGE"
        else:
            continue
            posts["media_type"] = "STATUS"
            new_post["image_url"] = "NULL"

        post_list.append(new_post)
        index = index + 1

        my_post = Post()

        my_post.user_id = new_post["CrossMe_user_id"]
        my_post.creation_date = new_post["created_time"]
        my_post.post_source = new_post["source"]
        my_post.post_type = posts["media_type"]
        my_post.post_text = new_post["message"]
        my_post.media_url = new_post["image_url"]
        my_post.save()


    post_dict["fb_last_post"] = post_list

    return make_response(jsonify(post_dict), 200)

@scrap_app.route('/ig_post/<user_id>/<ig_code>', methods=['GET'])
def get_acess_token(user_id, ig_code):
    """generate acess token from ig code"""

    files = {
        'client_id': (None, '425368628431983'),
        'client_secret': (None, '9c18abaf114db46610e7855a642dd6c9'),
        'grant_type': (None, 'authorization_code'),
        'redirect_uri': (None, 'https://0.0.0.0:5000/register'),
        'code': (None, ig_code),
    }

    r = requests.post('https://api.instagram.com/oauth/access_token', files=files).json()

    short_access_token = r["access_token"]

    res = requests.get(
        "https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=9c18abaf114db46610e7855a642dd6c9&access_token=" +
        short_access_token).json()

    long_access_token = res["access_token"]

    my_user = storage.get(User, user_id)
    my_user.update_attr("ig_access_token", long_access_token)

    URL = "https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,timestamp&access_token=" + long_access_token

    r_media = requests.get(URL)
    medias = r_media.json()

    post_dict = {}
    post_list = []
    index = 0
    for posts in medias["data"]:
        if index == 10:
            break

        new_post = {}

        new_post["ig_post_id"] = posts["id"]

        new_post["Post_id_CrossMe"] = str(uuid.uuid4())

        if "caption" in posts.keys():
            new_post["message"] = posts["caption"]
        else:
            new_post["message"] = "NULL"

        new_post["created_time"] = datetime.strptime(posts["timestamp"], '%Y-%m-%dT%H:%M:%S+%f')

        new_post["type"] = posts["media_type"]

        if posts["media_type"] != "CAROUSEL_ALBUM":
            new_post["image_url"] = posts["media_url"]
        else:
            continue
            new_post["image_url"] = []
            URLCASS = "https://graph.instagram.com/" + new_post["ig_post_id"] + "?fields=children&access_token=" + long_access_token
            r_cass = requests.get(URLCASS)
            cass = r_cass.json()
            data_cass = cass["children"]["data"]
            for inside_data in data_cass:
                inside_id = inside_data["id"]
                URLINSIDE = "https://graph.instagram.com/" + inside_id + "?fields=media_url&access_token=" + long_access_token
                r_inside = requests.get(URLINSIDE)
                inside = r_inside.json()
                new_post["image_url"].append(inside["media_url"])

        new_post["CrossMe_user_id"] = user_id
        new_post["source"] = "Instagram"
        post_list.append(new_post)
        index = index + 1

        my_post = Post()

        my_post.user_id = new_post["CrossMe_user_id"]
        my_post.creation_date = new_post["created_time"]
        my_post.post_source = new_post["source"]
        my_post.post_type = posts["media_type"]
        my_post.post_text = new_post["message"]
        my_post.media_url = new_post["image_url"]
        my_post.save()




    post_dict["fb_last_post"] = post_list

    return make_response(jsonify(post_dict), 200)

if __name__ == "__main__":
    """ Main Function """
    scrap_app.run(host='0.0.0.0', port=5001, ssl_context=('./ssl/server.crt', './ssl/server.key'))
