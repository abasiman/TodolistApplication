from database import Base
from sqlalchemy import Column, String, Integer


class TodoList(Base):
    __tablename__ = 'TodoList'
    id = Column(Integer, primary_key=True, index=True)
    newItem = Column(String(length=500))


class CompletedList(Base):
    __tablename__ = 'CompletedList'
    id = Column(Integer, primary_key=True, index=True)
    completedItem = Column(String(length=500))
