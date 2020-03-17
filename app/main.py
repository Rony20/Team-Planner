from fastapi import FastAPI

from .db.mongodb_utils import DatabaseConnector, Collections
from app.api.api import router

db_connector = DatabaseConnector()

app = FastAPI(title="Resource Planner")

app.add_event_handler("startup", db_connector.create_database_connection)
app.add_event_handler("shutdown", db_connector.close_database_connection)
app.include_router(router)
