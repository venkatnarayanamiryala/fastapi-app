from pydantic import BaseModel
from typing import Optional

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    role_id: int

class UserCreate(UserBase):
    password: str
    confirmpassword: str


class User(UserBase):
    t_id: int

    class Config:
        orm_mode = True
        

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "created"
    assigned_to: Optional[int]
    created_by: int

class TaskBases(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    assigned_to: str
    created_by: str
 

class TaskCreate(TaskBase):
    assigned_to: Optional[int]
    created_by: int

class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    username: str
    password: str
