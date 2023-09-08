from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

# variables para el nombre de usuario y la contraseña
username = os.environ.get("USER")
password = os.environ.get("PASS")

if "USER" and "PASS" in os.environ:
    url = f"mongodb+srv://{username}:{password}@cluster0.lwjhtor.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(url, server_api=ServerApi('1'))
else: 
    client= MongoClient("mongodb://localhost:27017/")

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db_client = client['users']

