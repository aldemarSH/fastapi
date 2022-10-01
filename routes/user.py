
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from auth.auth import AuthHandler
from db.models import UserInput, User, UserLogin
from sqlmodel import Session, select
from db.database import engine, session


router = APIRouter(
    prefix='/user',
    tags=['user']
)
auth_handler = AuthHandler()


@router.post('/registration', status_code=status.HTTP_201_CREATED,
                  description='Register new user')
def register(user: UserInput):

    statement = select(User)
    users = session.exec(statement).all()

    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    user = User(username=user.username, password=hashed_pwd, email=user.email,
             is_creator=user.is_creator)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post('/login')
def login(user: UserLogin):
    statement = select(User).where(User.username == user.username)
    user_found = session.exec(statement).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user_found.username)
    return {'token': token}


@router.get('/me')
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user