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

        try:
            self._client = MongoClient(MONGODB_URI)
        except errors.InvalidURI as uri_exception:
            print(uri_exception)
        except errors.ConfigurationError as configuration_exception:
            print(configuration_exception)
        except errors.ConnectionFailure as connection_error:
            print(connection_error)

    @property
    def database(self) -> Database:
        "This function will strickly return database object"

        return self._client.rp

    def collection(self, name: Collections) -> Collection:
        "This function will strickly return collection object"

        return self.database[name]

