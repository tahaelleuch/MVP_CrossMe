#!/usr/bin/python3
"""
Creat table Post in db
"""

import models
from models.base_model import BaseModel, Base, DateTime
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from datetime import datetime
from sqlalchemy.orm import relationship
from models.reaction import Reaction

class Post(BaseModel, Base):
    """Representation of post"""
    __tablename__ = 'posts'
    __table_args__ = {'extend_existing': True}
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    creation_date = Column(DateTime, nullable=True)
    post_source = Column(String(20), nullable=True)
    post_type = Column(String(20), nullable=True)
    post_text = Column(String(2000), nullable=True)
    media_url = Column(String(2000), nullable=True)
    reactions = relationship("Reaction",
                             backref="post",
                             cascade="all, delete, delete-orphan")

    def reactionlist(self):
        """
            reacts list
        """
        lt = []
        for i in models.storage.all(Reaction).values():
            if i.post_id == self.id:
                lt.append(i)
        return lt

    def reaction_list_source_user_id(self):
        """
            user who reacted this post
        """
        rect_list = self.reactionlist()
        source_list = []
        for react in rect_list:
            source_list.append(react.source_user_id)
        return source_list

    def number_of_reaction(self):
        """get the number of reaction of a post"""
        react_list = self.reactionlist()
        num_of_react = len(react_list)
        return (str(num_of_react))

    def check_if_user_reacted(self, follower_id):
        """
        check if a user is already react on a post
        """
        reactor_list = self.reaction_list_source_user_id()
        for id in reactor_list:
            if id == follower_id:
                return True
        return False


    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
