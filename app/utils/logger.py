"""Contains logging related classes."""

from datetime import datetime
from enum import Enum

from .singleton import Singleton
from ..db.mongodb_utils import DatabaseConnector, Collections
from ..models.log import Log

db_connector = DatabaseConnector()

class LogType(str, Enum):
    """Log type enumerations."""

    INFO = "info"
    ERROR = "error"
    WARNING = "warning"


class Logger(metaclass=Singleton):
    """Class used to log messages."""

    def __init__(self):
        """Initialize a new logger."""
        self._connector = db_connector
        # TODO: use capped collection here
        # self._connector.db.create_collection(Collections.LOGS, {
        #     "capped": True,
        #     "max": 1000
        # })

    def update_level(self):
        """Refresh logLevel from the database."""
        settings = db_connector.collection(Collections.SETTINGS).find_one(
            {}
        )
        try:
            self._level = LogType(settings["logLevel"])
        except TypeError:
            self._level = LogType.INFO

    def info(self, message: str):
        """Log an information message.

        Args:
            message (str): Message to be logged.
        """
        if self._level not in [LogType.INFO]:
            return
        log = Log(message=message, type=LogType.INFO, createdAt=datetime.now())
        self._connector.collection(Collections.LOGS).insert_one(log.dict())

    def warn(self, message: str):
        """Log a warning message.

        Args:
            message (str): Message to be logged.
        """
        if self._level not in [LogType.WARNING, LogType.INFO]:
            return
        log = Log(
            message=message, type=LogType.WARNING, createdAt=datetime.now()
        )
        self._connector.collection(Collections.LOGS).insert_one(log.dict())

    def error(self, message: str):
        """Log an error message.

        Args:
            message (str): Message to be logged.
        """
        if self._level not in [LogType.ERROR, LogType.WARNING, LogType.INFO]:
            return
        log = Log(
            message=message, type=LogType.ERROR, createdAt=datetime.now()
        )
        self._connector.collection(Collections.LOGS).insert_one(log.dict())
