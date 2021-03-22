from typing import Dict
from motor.motor_asyncio import AsyncIOMotorClient
from collections import OrderedDict
import os
from schemas import cuisine_schema, recipe_schema


# Singleton for instantiating mongodb client
class MongoClient(object):
    _instance = None
    _connection = None
    _user = os.getenv("MONGO_USER")
    _password = os.getenv("MONGO_PASSWORD")
    _port = os.getenv("HOST_PORT")
        
    def __new__(cls):
        if cls._instance is None:
            print("Creating MongoDB Client...")
            cls._instance = super(MongoClient, cls).__new__(cls)
        else:
            raise Exception("An instance of the MongoDB Client already exists!")
        return cls._instance

    def __init__(self) -> None:
        self._connection = AsyncIOMotorClient(f"mongodb://{self._user}:{self._password}@localhost:{self._port}")
        
    async def get_connection(self, database: str, config: Dict) -> None:
        # self._connection = self._connection[database]
        connection = self._connection[database]
        
        # create collection if it does not exist
        collection_list = await connection.list_collection_names()
        
        if not config["recipes_collection"] in collection_list:
            await connection.create_collection(config["recipes_collection"])
        
        if not config["cuisines_collection"] in collection_list:
            await connection.create_collection(config["cuisines_collection"])
            
        
        cmd1 = OrderedDict([ 
        ('collMod', config["cuisines_collection"]),
        ("validator", config["cuisine_schema"]),
        ("validationLevel", "moderate")
        ])
        
        cmd2 = OrderedDict([ 
        ('collMod', config["recipes_collection"]),
        ("validator", config["recipe_schema"]),
        ("validationLevel", "moderate")
        ])
        
        # apply collection schemas    
        await connection.command(cmd1, cmd2)
        
        return connection
