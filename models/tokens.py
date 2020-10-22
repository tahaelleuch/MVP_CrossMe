#!/usr/bin/python3
"""
Creat table follow in db
"""

import models
from models.base_model import BaseModel, Base, DateTime
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from datetime import datetime



class Token(BaseModel, Base):
    """Representation of token security"""
    __tablename__ = 'token'
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False, primary_key=True)
    securecode = Column(String(200), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)