# Users DB API
from fastapi import APIRouter, HTTPException
from db.models.user import User
from db.schemas.user import user_schema, users_scheme
from db.client import db
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={404: {"message": "No encontrado"}})


@router.get("/", response_model=list[User], status_code=201)
async def users():
    return users_scheme(db.users.find())


@router.get("/{id}")
async def user(id:str):
     return search_user("_id", ObjectId(id))
    
@router.post("/", response_model=User, status_code=201)
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe!")

    user_dict = dict(user)
    del user_dict["id"]
    
    id = db.users.insert_one(user_dict).inserted_id

    new_user = user_schema(db.users.find_one({"_id":id}))
    return User(**new_user)
    
@router.put("/", response_model=User)
async def user(user: User):

    user_dict = dict(user)
    del user_dict["id"]

    try:

        db.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No se ha actualizado el usuario"}
    
    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}",  status_code=204)
async def user(id:str):
    found = db.users.find_one_and_delete({"_id":  ObjectId(id)})

    if not found:
        return {"error", "no se ha eliminado el usaurio"}
        

def search_user (field:str, key):
    try:
        user =  db.users.find_one({field: key})
        return User(**user_schema(user))
    except:
        return {"error" : "Usuario no encontrado"}

