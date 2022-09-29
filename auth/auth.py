from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from db.models import User
from db.database import session
from sqlmodel import select
import jwt
import datetime

class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'])
    secret = 'supersecret' # cualquier script


    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)

    def encode_token(self, user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id

        }
        return jwt.encode(payload, self.secret, algorithm='HS256')


    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'] )
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Expired token')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

    
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    
    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security)):
        credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= 'not validate credentials')
        username = self.decode_token(auth.credentials)
        if username is None:
            raise credentials_exception

        statement = select(User).where(User.username == username)
        user_found = session.exec(statement).first()

        if user_found is None:
            raise credentials_exception
        return user_found