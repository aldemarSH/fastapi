from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from db.models import User, UserInput, UserLogin
from db.database import session
from sqlmodel import select
from auth.auth import AuthHandler


router = APIRouter(
    prefix='/user',
    tags=['user']
)

auth_handler = AuthHandler()

@router.post('/registration', status_code= status.HTTP_201_CREATED, description='register new user')
def register(user: UserInput):

    statement = select(User)
    users = session.exec(statement).all()

    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username is already taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    user = User(username=user.username, password=hashed_pwd,password2=hashed_pwd , email= user.email, is_creator=user.is_creator )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post('/login')
def login(user: UserLogin):
    statement = select(User).where(User.username == user.username)
    user_found = session.exec(statement).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='invalid')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='invalid')
    token  = auth_handler.encode_token(user_found.username)
    return {'token': token}