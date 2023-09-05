from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

#* (Clase que se encarga de autentufucacion)/(forma en la que se va a enviar la informacion y se va a capturar)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# ***__Entidad usuario__***
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

# ***__Heredero de usuario agregando contraseña__***
class UserDB(User):
    password: str

users_db = {
     "john_doe": 
    {
      "username": "john_doe",
      "full_name": "John Doe",
      "email": "john.doe@example.com",
      "disable": False,
      "password": "john123"
    },
    "jane_smith": {
      "username": "jane_smith",
      "full_name": "Jane Smith",
      "email": "jane.smith@example.com",
      "disable": False,
      "password": "jane123"
    },
    "mike_Johnson":{
      "username": "mike_johnson",
      "full_name": "Mike Johnson",
      "email": "mike.johnson@example.com",
      "disable": True,
      "password": "mike123"
    },
    "emma_wilson":{
      "username": "emma_wilson",
      "full_name": "Emma Wilson",
      "email": "emma.wilson@example.com",
      "disable": False,
      "password": "emma123"
    },
    "alex_parker":{
      "username": "alex_parker",
      "full_name": "Alex Parker",
      "email": "alex.parker@example.com",
      "disable": True,
      "password": "alex123"
    }
}



def search_user(username:str):
    if username in users_db:
        return UserDB(**users_db[username]) #** el (**) quiere decir que pueden ir varios parametros
    
def search_user_np(username:str):
    if username in users_db:
        return User(**users_db[username])
    
#** Criterio de dependencia
async def current_user(token:str = Depends(oauth2)):
    user = search_user_np(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales de autetificación invalidos",
            headers={"WWW-Authenticate":"Bearer"}
            )
    if user.disable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Usuario inactivo"
            )

    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()): #** Recibe datos pero no depende de nadie
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=404, detail="El usuario no es correcto")
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=404, detail="La contraseña no es correcta")
    
    return {"access_token": user.username,"token_type":"bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user