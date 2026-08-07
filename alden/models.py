from fastapi import (
    FastAPI,
    HTTPException
)
from pydantic import BaseModel


class Todo(BaseModel):
    user_id: int
    title: str
    is_completed: bool
    
