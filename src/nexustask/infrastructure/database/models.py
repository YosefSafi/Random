from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    title = Column(String(255), nullable=False)
    project_id = Column(String(36), nullable=False)
    status = Column(String(50), nullable=False)
    version = Column(Integer, nullable=False, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class EventStoreModel(Base):
    __tablename__ = "event_store"

    sequence_id = Column(Integer, primary_key=True, autoincrement=True)
    aggregate_id = Column(String(36), index=True)
    event_type = Column(String(255))
    payload = Column(JSON)
    occurred_on = Column(DateTime)
