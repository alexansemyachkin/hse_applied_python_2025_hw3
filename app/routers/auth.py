from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from ..database import get_db
from .. import crud, schemas


router = APIRouter(prefix="/auth")


@router.post("/register")
def register(data: schemas.UserCreate, db: Session = Depends(get_db)):

    user = crud.get_user_by_email(db, data.email)

    if user:
        raise HTTPException(status_code=400, detail="user exists")

    password_hash = bcrypt.hash(data.password)

    user = crud.create_user(
        db,
        data.email,
        password_hash
    )

    return {"user_id": user.id}


@router.post("/login")
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):

    user = crud.get_user_by_email(db, data.email)

    if not user:
        raise HTTPException(status_code=404)

    if not bcrypt.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401)

    return {"user_id": user.id}
