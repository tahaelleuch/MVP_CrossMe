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
