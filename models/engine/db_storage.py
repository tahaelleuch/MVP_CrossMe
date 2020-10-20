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
from models.follow import Follow
import models

classes = {"User": User, "Post": Post, "Follow": Follow}

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

        return None

    def get_by_followed_id(self, cls, user_id):
        """
        get a list of cls id with followed
        """
        if cls not in classes.values():
            return None
        all_cls = models.storage.all(cls)
        obj_list = []
        for value in all_cls.values():
            if value.user_id == user_id:
                obj_list.append(value)
        return obj_list

    def get_by_follower_id(self, cls, follower_id):
        """
        get a list of user follow
        """
        if cls not in classes.values():
            return None
        all_cls = models.storage.all(cls)
        obj_list = []
        for value in all_cls.values():
            if value.follower_id == follower_id:
                obj_list.append(value)
        return obj_list

    def get_by_two(self, cls, follower, followed):
        """get follow instance with the two ids"""
        if cls not in classes.values():
            return None

        if follower is not None and followed is not None:
            follow_list = models.storage.get_by_followed_id(cls, followed)
            print (follow_list)
            for obj in follow_list:
                if obj.follower_id == follower:
                    return obj
        return None

    def follower_number(self, cls, user_id):
        """count a user followers"""
        if cls not in classes.values():
            return None

        if user_id is not None:
            follow_list = models.storage.get_by_followed_id(cls, user_id)
            number_of_follow = len(follow_list)
            return (str(number_of_follow))



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

    def getlist_by_attr(self, cls, user_id):
        """
        get all posts of a user by user_id
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        list_val = []
        for value in all_cls.values():
            if value.user_id == user_id:
                list_val.append(value.to_dict())

        if cls == Post:
            models.storage.sort_posts(list_val)

        return list_val


    def sort_posts(self, post_lists):
        """sort a list of post by creation date"""
        my_new_list = post_lists
        my_new_list.sort(key=lambda date: date["creation_date"])
        my_new_list.reverse()
        return my_new_list

