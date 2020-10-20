#!/usr/bin/python3
"""
Creat table follow in db
"""

import models
from models.base_model import BaseModel, Base, DateTime
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from datetime import datetime



class Follow(BaseModel, Base):
    """Representation of post"""
    __tablename__ = 'follow'
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    follower_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    creation_date = Column(DateTime, nullable=True, default=datetime.utcnow())
    follow_code = Column(Integer, nullable=False, default=0)

    def get_status_code(self, follower, followed):
        """get status code of user"""
        obj = models.storage.get_by_two(self, follower, followed)
        return obj.follow_code

    def follower_list(self, followed):
        """get follower list of a user"""
        if followed is not None:
            follow_list_obj = models.storage.get_by_followed_id(self, followed)
            follow_list = []
            for obj in follow_list_obj:
                follow_list.append(obj.follower_id)
            return follow_list
        return None
"""
    def check_follow_back(self):
        #check if follower is following back
        obj = models.storage.get_by_two(self, self.user_id, self.follower_id):
        if obj.follow_code == 1:
            obj.follow_code = 2
            obj.save()
            if self.follow_code == 1:
                self.follow_code = 2
"""