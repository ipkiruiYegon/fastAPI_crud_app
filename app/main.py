from datetime import datetime
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud,schemas,model
from .database import SessionLocal, engine
from .functions.users import authenticate_user,create_access_token

model.Base.metadata.create_all(bind=engine)

origins = [
'http://127.0.0.1:8008',
'http://localhost:8008',
'http://127.0.0.1:8000',
'http://localhost:8008'
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

@app.get("/")
def root():
    return {"App": "Welcome to my Simple Authentication app"} 

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email (db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/login/")
def login(username:str,password: str, db: Session = Depends(get_db)):
    # check if user with supplied credentials are valid.
    user = authenticate_user(db, username,password)
    if not user:
        raise HTTPException(status_code=403, detail="Either Username or Password is incorrect 1")
    
    # issue token to user.
    token = create_access_token({"userid":user.id,"email":user.email,"status":user.is_active})
    if not token:
        raise HTTPException(status_code=500, detail="Error occured generating your user token")

    # update last login
    user.token = token
    user.last_login = datetime.now()
    db.commit()
    
    return {"Message":"Login Success", "token":token}

