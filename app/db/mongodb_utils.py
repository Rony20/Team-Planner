import logging
from enum import Enum

from pymongo import MongoClient, errors
from pymongo.collection import Collection
from pymongo.database import Database

from ..core.config import MONGODB_URI

class Collections(str, Enum):
    "This is a ENUM class for Mongo Collectios"

    PROJECTS = "projects"
    EMPLOYEES = "employees"

class DatabaseConnector():
    "This is database connection class"
    
    def __init__(self):
        "Intialize Database"

        self._client = None
    
    def create_database_connection(self) -> None:
        "This function will create database connection when application startsup"

        self._client = MongoClient(MONGODB_URI)

    def close_database_connection(self) -> None:
        "This function will close database conection when application shutdowns"

        self._client.close()

    @property
    def database(self) -> Database:
        "This function will strickly return database object"

        return self._client.rp

    def collection(self, name: Collections) -> Collection:
        "This function will strickly return collection object"

        return self.database[name]

