"""This class will return MongoClient to make connection with MongoDB"""

from pymongo import MongoClient


class DataBase:
    """This class creates one attribute of type MongoClient"""

    client: MongoClient


db = DataBase()


async def get_database() -> MongoClient:
    """This collection will return object of type MongoClient"""

    return db.client
