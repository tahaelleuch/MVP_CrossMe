#!/usr/bin/python3
"""
Creat table User in db
"""

from datetime import datetime
import models
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from models.follow import Follow
from models.post import Post
from models.notification import Notification

class User(BaseModel, Base):
    """Representation of user"""
    __tablename__ = 'user'
    email = Column(String(128), primary_key=True)
    password = Column(String(128), nullable=False)
    full_name = Column(String(128), nullable=False)
    user_avatar = Column(String(500), nullable=False)
    fb_access_token = Column(String(500), nullable=True)
    ig_access_token = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def hashpwd(self, pwd):
        return generate_password_hash(pwd)


    def verify_password(self, pwd, hash):
        return check_password_hash(hash, pwd)

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_dict_nopwd(self):
        a={c.name: getattr(self, c.name) for c in self.__table__.columns}
        a.pop('password', None)
        return a

    def follower_list(self):
        """get follower list of a user"""
        follow_list_obj = models.storage.get_by_followed_id(Follow, self.id)
        follow_list = []
        for obj in follow_list_obj:
            follow_list.append(obj.follower_id)
        return follow_list

    def follow_list(self):
        """get list of user follow"""
        follow_list_obj = models.storage.get_by_follower_id(Follow, self.id)
        follow_list = []
        for obj in follow_list_obj:
            follow_list.append(obj.user_id)
        return follow_list

    def post_list(self):
        """get post list of a user"""
        post_list_obj = models.storage.getlist_by_attr(Post, self.id)
        post_list = []
        for obj in post_list:
            post_list.append(obj)

    def notification_list(self):
        """get all notifications of a user"""
        user_notifs = models.storage.get_all_user_notif(Notification ,self.id)
        return user_notifs
