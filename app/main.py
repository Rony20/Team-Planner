from fastapi import FastAPI
from .db.mongodb_utils import DatabaseConnector, Collections

db_connector = DatabaseConnector()

app = FastAPI()

app.add_event_handler("startup", db_connector.create_database_connection)
app.add_event_handler("shutdown", db_connector.close_database_connection)


@app.get("/")
def demo():
    doc = db_connector.collection(
        Collections.PROJECTS).insert_one({"name": "hello"})
    return doc.acknowledged
    # return { 'status': 'success'}
