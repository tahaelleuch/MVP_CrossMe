import models
from models.base_model import BaseModel, Base, DateTime
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Integer
from datetime import datetime , timedelta



class Emailsecurity(BaseModel, Base):
    """Representation of token security"""
    __tablename__ = 'emailtoken'
    email = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    @classmethod
    def delete_expired(cls):
        models.storage.reload()
        limit = datetime.now() - timedelta(days=1)
        a = models.storage.all(cls)
        for i in a.values():
            if i.created_at <= limit:
                print(i.id +"deleted")
                i.delete()
            else:
                continue
        models.storage.save()
