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

class User(BaseModel, Base):
    """Representation of user"""
    __tablename__ = 'user'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    full_name = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
