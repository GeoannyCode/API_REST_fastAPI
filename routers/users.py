from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"])

#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [User(id=1,name="Diego" , surname="Bracero", url="geoannycode.com", age=26),
              User(id=2,name="Pablo" , surname="Bracero", url="Pablocode.com", age=29),
              User(id=3,name="Juan" , surname="Bracero", url="Juancacode.com", age=40)]

@router.get("/users")
async def users():
    return users_list

#path
@router.get("/user/{id}")
async def user(id:int):
    return search_user(id)
    
#query
@router.get("/user/")
async def user(id:int):
    return search_user(id)

@router.post("/user/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
       raise HTTPException(status_code=204, detail="El usuario ya existe!")
    
    users_list.append(user)
    return user
    
@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
    if not found:
        return {"error": "No se ha actualizado el usuario"}
    else:
        return user

@router.delete("/user/{id}")
async def user(id:int):
    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return {"Dato Eliminado"}
        if not found:
            return {"error", "no se ha eliminado el usaurio"}
   
def search_user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except:
        return {"error" : "Usuario no encontrado"}

