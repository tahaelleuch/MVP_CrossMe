#!/usr/bin/python3
"""
Creat table reaction in db
"""

import models
from models.base_model import BaseModel, Base, DateTime
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from datetime import datetime
from sqlalchemy.orm import relationship



class Reaction(BaseModel, Base):
    """Representation of reaction"""
    __tablename__ = 'reaction'
    __table_args__ = {'extend_existing': True}
    source_user_id = Column(String(60),ForeignKey('user.id'),nullable=False )

    target_user_id = Column(String(60),ForeignKey('posts.user_id'), nullable=False)
    post_id = Column(String(60), ForeignKey('posts.id'), nullable=False)
    creation_date = Column(DateTime, nullable=True, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)