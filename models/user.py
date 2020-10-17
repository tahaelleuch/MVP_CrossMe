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

class User(BaseModel, Base):
    """Representation of user"""
    __tablename__ = 'user'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    full_name = Column(String(128), nullable=False)
    user_avatar = Column(String(500), nullable=False)
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
