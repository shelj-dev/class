from fastapi import (
    FastAPI,
    Depends
)
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Todo
import schemas

app = FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message":"ok"}

@app.post("/todos/db")
def add_todo_db(todo: Todo, db: Session = Depends(get_db)):
    
    new_todo = schemas.Product(
        id=todo.user_id,
        title=todo.title,
        is_completed=todo.is_completed
    )
    
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    return {
        "message":"Todo added successfully",
        "data": new_todo
    }