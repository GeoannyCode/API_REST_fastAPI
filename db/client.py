from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# variables para el nombre de usuario y la contraseña
username = "tu_usuario"
password = "tu_contraseña"

# url = "mongodb+srv://{username}:{password}@cluster0.lwjhtor.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(url, server_api=ServerApi('1'))

client= MongoClient("mongodb://localhost:27017/")
db_client = client['users']

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)