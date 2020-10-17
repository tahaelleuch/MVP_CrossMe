#!/usr/bin/python3
"""
class DBStorage
"""

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import BaseModel, Base
from models.user import User
from models.post import Post
import models

classes = {"User": User, "Post": Post}

class DBStorage():
    """DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Inisialisation of class DBStorage"""
        CM_MYSQL_USER = "cm_dev"
        CM_MYSQL_PWD = "test"
        CM_MYSQL_HOST = "localhost"
        CM_MYSQL_DB = "crossmedb"
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(CM_MYSQL_USER,
                                             CM_MYSQL_PWD,
                                             CM_MYSQL_HOST,
                                             CM_MYSQL_DB,
                                             pool_pre_ping=True))

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def check(self, cls=None, email="str"):
        """check"""
        val_list = self.__session.query(cls).all()
        for user in val_list:
            if email == user.email:
                return 1
        else:
            return 0

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """reload data from db"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """close methode"""
        self.__session.close()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def getbyemail(self, cls, email):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.email == email):
                return value

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
