from jose import JWTError, jwt
from datetime import  datetime, timedelta
from . import schemas, database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models
from . config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({ "exp" : expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token : str, credentials_exception):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM])
        id = payload.get("user_id")
        if id is None: 
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token : str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate" : "Bearer"})
    
    user_token = verify_access_token(token, credentials_exception)
    print(f"USER_TOKEN = {user_token}")
    user = db.query(models.ItemDatabaseUser).filter(models.ItemDatabaseUser.id == user_token.id).first()
    return user
                     