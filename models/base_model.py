#!/usr/bin/python3
"""base model class"""


import models
import sqlalchemy
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime

Base = declarative_base()

class BaseModel:
    """The BaseModel class from which will be used as base"""
    id = Column(String(60), primary_key=True)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        self.id = uuid.uuid4()

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
