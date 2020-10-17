#!/usr/bin/python3
"""base model class"""


import models
import sqlalchemy
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
from datetime import datetime

time = "%Y-%m-%dT%H:%M:%S.%f"
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

    def to_dict(self, save_fs=None):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if save_fs is None:
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict

    def update_attr(self, attr=None, new_value=None):
        """update an attribute by it new value"""
        if attr is not None and new_value is not None:
            self.updated_at = datetime.utcnow()
            setattr(self, attr, new_value)
            models.storage.save()
            models.storage.reload()
