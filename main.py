from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import User, Task, Role
from schemas import UserCreate, TaskCreate, Task, User, LoginRequest, TaskBases
from auth import authenticate_user, create_access_token, get_password_hash
from typing import List
from database import SessionLocal, engine
from typing import Annotated, List
import models
from fastapi.middleware.cors import CORSMiddleware


from typing import List, Optional
from fastapi import Query


app = FastAPI()

origins = {
    "http://localhost:3000",

}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

db_dependency = Annotated[Session, Depends(get_db)]
models.Base.metadata.create_all(bind= engine)


@app.post("/register", response_model=User)
def register_user(user: UserCreate, db: db_dependency):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, password=hashed_password, confirmpassword=hashed_password, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    print("Received login request:", request)
    
    # Authenticate the user
    user = authenticate_user(db, request.username, request.password)
    
    if not user:
        # If authentication fails, raise an exception
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    # If authentication is successful, create an access token
    access_token = create_access_token(data={"sub": user.username})
    
    # Return the token and userId as part of the response
    return {"access_token": access_token, "token_type": "bearer", "userId": user.t_id}


@app.post("/tasks", response_model=Task)
def create_task(task: TaskCreate, db: db_dependency):
    print(task)
    db_task = models.Task(
        title=task.title, description=task.description, status=task.status,
        assigned_to=task.assigned_to, created_by=task.created_by
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@app.get("/tasks", response_model=List[TaskBases])
async def get_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    created_by: Optional[int] = Query(None)  # Optional query parameter
):
    # Base query for tasks
    query = db.query(models.Task)

    # Filter by userId if provided
    if created_by is not None:
        query = query.filter(models.Task.created_by == created_by)

    # Fetch tasks with pagination
    tasks = query.offset(skip).limit(limit).all()

    # Replace 'created_by' and 'assigned_to' user IDs with usernames
    for task in tasks:
        user = db.query(models.User).filter(models.User.t_id == task.created_by).first()
        assign = db.query(models.User).filter(models.User.t_id == task.assigned_to).first()

        if user:
            task.created_by = user.username
        if assign:
            task.assigned_to = assign.username

    return tasks



