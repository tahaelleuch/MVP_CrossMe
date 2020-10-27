#!/usr/bin/python3
"""
Create table notification in db
"""

import models
from models.base_model import BaseModel, Base, DateTime
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class Notification(BaseModel, Base):
    """representation of notification"""
    __tablename__ = 'notification'
    reciver_user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    maker_user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    creation_date = Column(DateTime, nullable=True, default=datetime.utcnow())
    type = Column(String(50), nullable=False)
    reaction_id = Column(String(60), ForeignKey('reaction.id'), nullable=True)
    follow_id = Column(String(60), ForeignKey('follow.id'), nullable=True)

    @hybrid_property
    def object_id(self):
        return self.reaction_id or self.follow_id
