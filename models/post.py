#!/usr/bin/python3
"""
Creat table Post in db
"""

import models
from models.base_model import BaseModel, Base, DateTime
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from datetime import datetime

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

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
