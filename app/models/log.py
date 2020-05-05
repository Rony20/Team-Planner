"""Provides logging related models."""

from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Schema


class LogType(str, Enum):
    """Log type enumerations."""

    INFO = "info"
    ERROR = "error"
    WARNING = "warning"


class Log(BaseModel):
    """The outgoing log model."""

    message: str
    type: LogType = Schema(LogType.INFO)
    createdAt: datetime = Schema(datetime.now())
