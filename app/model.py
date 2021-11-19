from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql.expression import true
from .database import Base

class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, index=True)
    username=Column(String,unique=true)
    firstname=Column(String)
    othernames=Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    last_login=Column(String,nullable=true,default='')
    token=Column(String,nullable=true,default='')