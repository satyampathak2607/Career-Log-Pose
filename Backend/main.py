from Backend.utils.schemas import UserLogin, UserRegister
from Backend.utils.hash import hash_password, verify_password
from Backend.utils.database import SessionLocal, engine, Base
from Backend.utils.models.user import User

from fastapi import Depends
from sqlalchemy.orm import Session

from dotenv import load_dotenv
from fastapi import FastAPI
import os

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print("Connected to DB:", DATABASE_URL)



app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.post("/register")


def register_user(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        return {"error": "User with this email already exists."}
    
    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.refresh(new_user)
    return {
        "message": f"User {user.username} registered successfully!",
        "user_id": new_user.id
    }

@app.post("/login")
def login_user(user: UserLogin,db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user or not verify_password(user.password, existing_user.password):

        return {"error": "Invalid email or password!."}
    
    return {
        "message": f"Welcome back, {existing_user.username}!",
        "user_id": existing_user.id
    }

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Career Log Pose is sailing! ⛵"}

