from fastapi import HTTPException, Depends, FastAPI
from typing import Annotated, List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database import SessionLocal, engine, Base
from models import TodoList, CompletedList
from fastapi.middleware.cors import CORSMiddleware





app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins = ['https://todolist-application-wheat.vercel.app'],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# create pydantic models


class TodoBase(BaseModel):
    newItem: str


class TodoModel(TodoBase):
    id: int

    class Config:
        orm_mode = True

# database dependencies


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables in the database
Base.metadata.create_all(bind=engine)

# endpoints


@app.post("/TodoList/", response_model=TodoModel)
async def create_todos(todo: TodoBase,  db: Session = Depends(get_db)):
    db_todo = TodoList(newItem=todo.newItem)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/TodoList/", response_model=List[TodoModel])
async def get_todos(db: Session = Depends(get_db)):
    return db.query(TodoList).all()


@app.delete("/TodoList/{todo_id}/", response_model=TodoModel)
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = db.query(TodoList).filter(TodoList.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(db_todo)
    db.commit()
    return db_todo


@app.put("/TodoList/{todo_id}/", response_model=TodoModel)
async def update_todo(todo_id: int, todo: TodoBase, db: Session = Depends(get_db)):
    db_todo = db.query(TodoList).filter(TodoList.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db_todo.newItem = todo.newItem
    db.commit()
    db.refresh(db_todo)
    return db_todo


# Clear All Todolist
@app.delete("/TodoList/", response_model=None)
async def clear_todo_list(db: Session = Depends(get_db)):
    try:
        db.query(TodoList).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# completed list
class CompletedBase(BaseModel):
    completedItem: str


class CompletedModel(CompletedBase):
    id: int

    class Config:
        orm_mode = True


@app.post("/CompletedList/", response_model=CompletedModel)
async def create_completed(completed: CompletedBase,  db: Session = Depends(get_db)):
    db_completed = CompletedList(completedItem=completed.completedItem)
    db.add(db_completed)
    db.commit()
    db.refresh(db_completed)
    return db_completed


@app.get("/CompletedList/", response_model=List[CompletedModel])
async def get_completed(db: Session = Depends(get_db)):
    return db.query(CompletedList).all()


# clear all the completed tasks
@app.delete("/CompletedList/", response_model=None)
async def clear_completed_list(db: Session = Depends(get_db)):
    try:
        db.query(CompletedList).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
