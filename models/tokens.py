#!/usr/bin/python3
"""
Creat table follow in db
"""

import models
from models.base_model import BaseModel, Base, DateTime
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from datetime import datetime , timedelta



class Token(BaseModel, Base):
    """Representation of token security"""
    __tablename__ = 'token'
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False, primary_key=True)
    securecode = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @classmethod
    def delete_expired(cls):
        models.storage.reload()
        limit = datetime.now() - timedelta(hours=1)
        a = models.storage.all(cls)
        for i in a.values():
            if i.created_at <= limit:
                i.delete()
            else:
                continue
        models.storage.save()