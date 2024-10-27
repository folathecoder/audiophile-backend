from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from app.core.config import settings

uri = settings.MONGODB_URI
client = MongoClient(uri, server_api=ServerApi("1"))
db = client.audiophile
