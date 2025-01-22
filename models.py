from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

class User(Base):
    __tablename__ = "users"

    t_id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing primary key
    username = Column(String, unique=True, index=True)
    password = Column(String)
    confirmpassword = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))

    role = relationship("Role")




class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="pending")
    assigned_to = Column(Integer, ForeignKey("users.t_id"))
    created_by = Column(Integer, ForeignKey("users.t_id"))
