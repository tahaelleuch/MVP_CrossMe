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
    #reactions = relationship("Reaction", foreign_keys='id',uselist=False,back_populates="reaction",cascade="all, delete")

    @property
    def reactionlist(self):
        """
            reacts list
        """
        lt = []
        for i in models.storage.all(Reaction).values():
            if i.post_id == self.id:
                lt.append(i)
        return lt

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
