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
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    creation_date = Column(DateTime, nullable=False)
    post_source = Column(String(20), nullable=False)
    post_type = Column(String(20), nullable=False)
    post_text = Column(String(500), nullable=True)
    media_url = Column(String(500), nullable=False)
