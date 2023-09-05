from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 #Duracion del JWT
SECRET = "1191cc7466fd6fec3941a9c7e70cd5f94ed7c77c6a36f04c76a40699ff364ad2"

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

class UserDB(User):
    password: str


# en las pruebas usar como contraseña <nombre_persona>123
users_db = {
     "john_doe": 
    {
      "username": "john_doe",
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "disable": False,
      "password": "$2a$12$9rlOB1K/lT7v0tqVHtLfOeE4xu05iKiPNpeHi.t/QHyQXiUH3ZpyS"
    },
    "jane_smith": {
      "username": "jane_smith",
      "full_name": "Jane Smith",
      "email": "jane.smith@example.com",
      "disable": False,
      "password": "$2a$12$ogpLTBU0XSmIaka3a/n3...S10bcKX8vItiW9bU0tQw7RBWGqjPuO"
    },
    "mike_Johnson":{
      "username": "mike_johnson",
      "full_name": "Mike Johnson",
      "email": "mike.johnson@example.com",
      "disable": True,
      "password": "$2a$12$6qiWwukLy.mBNmz5wvJyt.itD1ExbmjF/Jw4wXU76FC6cCQRdNOk6"
    },
    "emma_wilson":{
      "username": "emma_wilson",
      "full_name": "Emma Wilson",
      "email": "emma.wilson@example.com",
      "disable": False,
      "password": "$2a$12$xq0cWpOaMQnBJhuc4XgWbeMtRluFH1QtSC7QByicBJx6fw/VIccaO"
    },
    "alex_parker":{
      "username": "alex_parker",
      "full_name": "Alex Parker",
      "email": "alex.parker@example.com",
      "disable": True,
      "password": "$2a$12$I/rw21C5CWQn0m3l9UbHOevixB9vNaY.JyHzSJViqlO50u5Wde8ES"
    }
}

def search_user(username:str):
    if username in users_db:
        return UserDB(**users_db[username])
    
def search_user_np(username:str):
    if username in users_db:
        return User(**users_db[username])
    
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autetificación invalidos",
            headers={"WWW-Authenticate":"Bearer"}
            )

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError: 
        raise exception

    return search_user_np(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario inactivo"
            )

    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):

    user_db = users_db.get(form.username)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto XC"
        )
    
    user = search_user(form.username)

    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta XC"
        )
    
    access_token = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
        }
    
    return {"access_token": jwt.encode(access_token,SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user